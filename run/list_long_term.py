"""list_underscored.txt の長期運用を支援するユーティリティモジュール."""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Tuple
import xml.etree.ElementTree as ET

try:
    from update_list_underscored import ISSUE_ID_PATTERN, read_list_lines
except ImportError:
    current_dir = Path(__file__).resolve().parent
    if str(current_dir) not in sys.path:
        sys.path.append(str(current_dir))
    try:
        from update_list_underscored import ISSUE_ID_PATTERN, read_list_lines
    except ImportError as exc:  # pragma: no cover - 想定外の ImportError を明示化
        raise RuntimeError("update_list_underscored.py を読み込めませんでした") from exc


ISSUE_TITLE_PATTERN = re.compile(r"^Title: \[(JDK-\d+)\]")


class ListParseError(ValueError):
    """list_underscored.txt のレコード解析時に発生する例外."""


def _get_text(element: ET.Element, tag: str) -> str | None:
    """子要素のテキストを取得し、空文字の場合は None を返す."""

    child = element.find(tag)
    if child is None or not child.text:
        return None
    return child.text.strip()


@dataclass(slots=True)
class ListRecord:
    """list_underscored.txt 1 行分の情報."""

    priority: str
    workstream: str
    subsystem: str | None
    issue_id: str
    summary: str

    @property
    def category(self) -> str:
        """優先度・系統・サブシステムを結合したカテゴリ名."""

        if self.subsystem:
            return f"{self.priority}_{self.workstream}_{self.subsystem}"
        return f"{self.priority}_{self.workstream}"


def parse_record(line: str, *, line_number: int) -> ListRecord:
    """単一行を構造化データへ変換する."""

    parts = line.strip().split("_")
    if len(parts) < 4:
        raise ListParseError(f"line {line_number}: 不正なフィールド数です ({line!r})")

    priority = parts[0]
    workstream = parts[1]

    subsystem: str | None = None
    issue_index = 2
    if issue_index < len(parts) and not parts[issue_index].startswith("JDK-"):
        subsystem = parts[issue_index]
        issue_index += 1

    if issue_index >= len(parts):
        raise ListParseError(f"line {line_number}: Issue ID が見つかりません ({line!r})")

    issue_id = parts[issue_index]
    if not ISSUE_ID_PATTERN.fullmatch(issue_id):
        raise ListParseError(f"line {line_number}: Issue ID が不正です ({issue_id!r})")

    summary = "_".join(parts[issue_index + 1 :]).strip()

    return ListRecord(
        priority=priority,
        workstream=workstream,
        subsystem=subsystem,
        issue_id=issue_id,
        summary=summary,
    )


def load_records(list_path: Path, *, encoding: str = "utf-8") -> List[ListRecord]:
    """list_underscored.txt から ListRecord を読み込む."""

    lines, _ = read_list_lines(list_path, encoding)
    records: List[ListRecord] = []

    for index, line in enumerate(lines, start=1):
        stripped = line.strip()
        if not stripped or "JDK-" not in stripped:
            continue
        records.append(parse_record(stripped, line_number=index))

    return records


def filter_records(
    records: Sequence[ListRecord],
    *,
    priority: str | None = None,
    workstream: str | None = None,
    subsystem: str | None = None,
    category: str | None = None,
) -> List[ListRecord]:
    """フィルタ条件に合致するレコードを抽出する."""

    target_priority = priority
    target_workstream = workstream
    target_subsystem = subsystem

    if category is not None:
        segments = category.split("_")
        if len(segments) == 2:
            target_priority, target_workstream = segments
            target_subsystem = None
        elif len(segments) == 3:
            target_priority, target_workstream, target_subsystem = segments
        else:
            raise ValueError("category は priority_workstream[_subsystem] 形式で指定してください")

    filtered: List[ListRecord] = []
    for record in records:
        if target_priority is not None and record.priority != target_priority:
            continue
        if target_workstream is not None and record.workstream != target_workstream:
            continue
        if target_subsystem is not None and record.subsystem != target_subsystem:
            continue
        filtered.append(record)

    return filtered


def build_issue_category_map(records: Sequence[ListRecord]) -> Dict[str, str]:
    """Issue ID -> カテゴリ名 の写像を生成する."""

    return {record.issue_id: record.category for record in records}


class CategoryResolver:
    """Issue ID からカテゴリを導出するためのヘルパー."""

    def __init__(self, base_map: Dict[str, str], issues_root: Path) -> None:
        self._base_map = base_map
        self._issues_root = issues_root
        self._cache: Dict[str, str | None] = {}

    def resolve(self, issue_id: str) -> str | None:
        category = self._base_map.get(issue_id)
        if category is not None:
            return category
        if issue_id in self._cache:
            return self._cache[issue_id]
        derived = self._derive_from_xml(issue_id)
        self._cache[issue_id] = derived
        return derived

    def _derive_from_xml(self, issue_id: str) -> str | None:
        xml_dir = self._issues_root / issue_id
        xml_path = xml_dir / f"{issue_id.lower()}.xml"
        if not xml_path.exists():
            return None
        try:
            item = ET.parse(xml_path).find("./channel/item")
        except ET.ParseError:
            return None
        if item is None:
            return None
        priority = _get_text(item, "priority")
        workstream = _get_text(item, "type")
        subsystem = _get_text(item, "component")
        if priority is None or workstream is None:
            return None
        workstream = workstream.replace(" ", "-")
        if subsystem:
            subsystem = subsystem.replace(" ", "-")
            return f"{priority}_{workstream}_{subsystem}"
        return f"{priority}_{workstream}"


def inject_category_lines(
    lines: Sequence[str],
    resolver: CategoryResolver,
) -> Tuple[List[str], bool, int]:
    """Issue テキストに Category 行を挿入または正規化する."""

    updated: List[str] = []
    changed = False
    applied_count = 0
    index = 0

    while index < len(lines):
        line = lines[index]
        match = ISSUE_TITLE_PATTERN.match(line)
        if match:
            updated.append(line)
            issue_id = match.group(1)
            category_value = resolver.resolve(issue_id)
            if category_value is None:
                index += 1
                continue

            desired = f"Category: {category_value}"
            next_index = index + 1
            if next_index < len(lines) and lines[next_index].startswith("Category:"):
                existing = lines[next_index]
                if existing != desired:
                    updated.append(desired)
                    changed = True
                    applied_count += 1
                else:
                    updated.append(existing)
                index += 2
                continue

            updated.append(desired)
            changed = True
            applied_count += 1
            index += 1
            continue

        updated.append(line)
        index += 1

    return updated, changed, applied_count


def apply_category_to_issue_dir(
    issue_dir: Path,
    resolver: CategoryResolver,
    *,
    encoding: str,
    dry_run: bool,
) -> List[Tuple[Path, int]]:
    """Issue ディレクトリ配下のファイルへカテゴリを適用する."""

    results: List[Tuple[Path, int]] = []

    for issue_path in sorted(issue_dir.glob("issue_jdk-*.txt")):
        if not issue_path.is_file():
            continue
        original_text = issue_path.read_text(encoding=encoding)
        lines = original_text.splitlines()
        updated_lines, changed, applied_count = inject_category_lines(lines, resolver)
        if not changed:
            continue
        results.append((issue_path, applied_count))
        if dry_run:
            continue
        new_text = "\n".join(updated_lines)
        if original_text.endswith("\n"):
            new_text += "\n"
        issue_path.write_text(new_text, encoding=encoding)

    return results


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="list_underscored.txt からカテゴリ単位で Issue ID を抽出する"
    )
    parser.add_argument(
        "--list-path",
        type=Path,
        default=Path(__file__).with_name("list_underscored.txt"),
        help="読み込む list_underscored.txt のパス",
    )
    parser.add_argument(
        "--encoding",
        default="utf-8",
        help="入出力に用いる文字エンコーディング (既定: utf-8)",
    )
    parser.add_argument(
        "--category",
        help="priority_workstream[_subsystem] 形式のカテゴリ名 (例: P2_Backport_hotspot)",
    )
    parser.add_argument(
        "--priority",
        help="優先度 (例: P2)",
    )
    parser.add_argument(
        "--workstream",
        help="系統 (例: Backport)",
    )
    parser.add_argument(
        "--subsystem",
        help="サブシステム (例: hotspot)",
    )
    parser.add_argument(
        "--with-summary",
        action="store_true",
        help="Issue ID に加えて概要も出力する",
    )
    parser.add_argument(
        "--issue-dir",
        type=Path,
        help="カテゴリを適用する Issue 一覧ディレクトリ",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Issue ファイルへカテゴリを書き戻す",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="書き込みを行わず適用予定のファイルを表示する",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if args.apply and args.dry_run:
        raise SystemExit("--apply と --dry-run は同時に指定できません")

    list_path = args.list_path.resolve()
    records = load_records(list_path, encoding=args.encoding)

    filtered = filter_records(
        records,
        priority=args.priority,
        workstream=args.workstream,
        subsystem=args.subsystem,
        category=args.category,
    )

    output_lines: Iterable[str]
    if args.with_summary:
        output_lines = (f"{record.issue_id}\t{record.summary}" for record in filtered)
    else:
        output_lines = (record.issue_id for record in filtered)

    for line in output_lines:
        print(line)

    if args.issue_dir is None:
        return

    if not filtered:
        print("指定条件に該当する Issue が存在しません。", file=sys.stderr)
        return

    category_map = build_issue_category_map(filtered)
    issue_dir = args.issue_dir.resolve()
    issues_root = Path(__file__).resolve().parent / "jdk_issues"
    resolver = CategoryResolver(category_map, issues_root)
    dry_run = args.dry_run or not args.apply

    results = apply_category_to_issue_dir(
        issue_dir,
        resolver,
        encoding=args.encoding,
        dry_run=dry_run,
    )

    if not results:
        print("カテゴリの更新対象となる Issue は見つかりませんでした。")
        return

    mode = "DRY-RUN" if dry_run else "APPLIED"
    total = sum(count for _, count in results)
    print(f"[{mode}] {len(results)} 件のファイルで {total} 個の Category 行を更新対象として検出しました。")
    for path, count in results:
        print(f"  {path} ({count} 件)")


if __name__ == "__main__":
    main()
