"""list_underscored.txt を Jira XML の description で更新するユーティリティ."""

from __future__ import annotations

import argparse
import html
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Tuple
import re
import xml.etree.ElementTree as ET

DESCRIPTION_PLACEHOLDER = "(no description)"
ISSUE_ID_PATTERN = re.compile(r"\b(JDK-\d+)\b")
BR_TAG_PATTERN = re.compile(r"<br\s*/?>", re.IGNORECASE)
TAG_PATTERN = re.compile(r"<[^>]+>")


class ListUpdateError(Exception):
    """更新処理でのリカバリ不可能なエラー."""


@dataclass(slots=True)
class UpdateSummary:
    """処理結果のサマリ."""

    updated_lines: int
    missing_descriptions: Sequence[str]
    missing_issue_files: Sequence[str]


@dataclass(slots=True)
class IssueDescriptions:
    """Issue ID ごとの説明文と欠落情報."""

    descriptions: Dict[str, str]
    missing_issue_files: List[str]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="list_underscored.txt の description フィールドを XML から補完する"
    )
    parser.add_argument(
        "--list-path",
        required=True,
        help="更新対象の list_underscored.txt のパス",
    )
    parser.add_argument(
        "--issues-root",
        required=True,
        help="JDK Issue の XML が格納されたルートディレクトリ",
    )
    parser.add_argument(
        "--encoding",
        default="utf-8",
        help="入出力で使用する文字エンコーディング (既定: utf-8)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="ファイルを書き換えずに更新差分の概要だけを表示する",
    )
    return parser.parse_args()


def normalize_description(raw: str) -> str:
    """XML 内の description テキストを 1 行の説明文に整形する."""

    text = html.unescape(raw)
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = BR_TAG_PATTERN.sub("\n", text)
    text = TAG_PATTERN.sub(" ", text)
    normalized = " ".join(text.split())
    return normalized


def parse_issue_description(xml_path: Path) -> str | None:
    """Issue XML ファイルから description 要素を抽出する."""

    try:
        tree = ET.parse(xml_path)
    except ET.ParseError as exc:
        print(f"警告: XML パースに失敗しました: {xml_path} ({exc}).", file=sys.stderr)
        return None

    item = tree.find("./channel/item")
    if item is None:
        return None

    description_element = item.find("description")
    if description_element is None or description_element.text is None:
        return None

    normalized = normalize_description(description_element.text)
    if not normalized:
        return None
    return normalized


def collect_issue_descriptions(issues_root: Path) -> IssueDescriptions:
    """issues_root 配下の XML から description を集約する."""

    descriptions: Dict[str, str] = {}
    missing_issue_files: List[str] = []

    for xml_path in sorted(issues_root.glob("JDK-*/jdk-*.xml")):
        issue_id = xml_path.parent.name
        description = parse_issue_description(xml_path)
        if description is None:
            missing_issue_files.append(str(xml_path))
            continue
        descriptions[issue_id] = description

    return IssueDescriptions(descriptions=descriptions, missing_issue_files=missing_issue_files)


def read_list_lines(list_path: Path, encoding: str) -> Tuple[List[str], bool]:
    """list_underscored.txt を読み込んで行と末尾の改行有無を返す."""

    raw_text = list_path.read_text(encoding=encoding)
    had_trailing_newline = raw_text.endswith("\n")
    lines = raw_text.splitlines()
    return lines, had_trailing_newline


def apply_descriptions(
    lines: Iterable[str],
    descriptions: Dict[str, str],
) -> Tuple[List[str], UpdateSummary]:
    """行リストに description を適用し、更新結果を返却する."""

    updated_lines: List[str] = []
    updated_count = 0
    missing_descriptions: List[str] = []

    for line in lines:
        issue_match = ISSUE_ID_PATTERN.search(line)
        if issue_match is None:
            updated_lines.append(line)
            continue

        issue_id = issue_match.group(1)
        description = descriptions.get(issue_id)
        if description is None:
            missing_descriptions.append(issue_id)
            updated_lines.append(line)
            continue

        head, sep, tail = line.rpartition("_")
        if not head:
            updated_lines.append(line)
            continue

        new_line = f"{head}{sep}{description}"
        if new_line != line:
            updated_count += 1
        updated_lines.append(new_line)

    summary = UpdateSummary(
        updated_lines=updated_count,
        missing_descriptions=sorted(set(missing_descriptions)),
        missing_issue_files=[],
    )
    return updated_lines, summary


def write_lines(list_path: Path, lines: Sequence[str], encoding: str, append_newline: bool) -> None:
    """更新済み行をファイルへ書き出す."""

    text = "\n".join(lines)
    if append_newline:
        text += "\n"
    list_path.write_text(text, encoding=encoding)


def update_list(
    list_path: Path,
    issues_root: Path,
    encoding: str,
    dry_run: bool,
) -> UpdateSummary:
    if not list_path.exists():
        raise ListUpdateError(f"list ファイルが見つかりません: {list_path}")

    if not issues_root.exists() or not issues_root.is_dir():
        raise ListUpdateError(f"issues ルートが不正です: {issues_root}")

    issue_descriptions = collect_issue_descriptions(issues_root)
    lines, had_trailing_newline = read_list_lines(list_path, encoding)
    updated_lines, summary = apply_descriptions(lines, issue_descriptions.descriptions)
    summary = UpdateSummary(
        updated_lines=summary.updated_lines,
        missing_descriptions=summary.missing_descriptions,
        missing_issue_files=issue_descriptions.missing_issue_files,
    )

    if dry_run:
        report_summary(summary, dry_run=True)
        return summary

    write_lines(list_path, updated_lines, encoding, had_trailing_newline)
    report_summary(summary, dry_run=False)
    return summary


def report_summary(summary: UpdateSummary, dry_run: bool) -> None:
    mode = "DRY-RUN" if dry_run else "UPDATED"
    print(f"[{mode}] {summary.updated_lines} 行を更新対象として検出しました。")

    if summary.missing_descriptions:
        joined = ", ".join(summary.missing_descriptions)
        print(f"説明が見つからなかった Issue: {joined}", file=sys.stderr)

    if summary.missing_issue_files:
        joined = ", ".join(summary.missing_issue_files)
        print(f"description が欠落していた XML: {joined}", file=sys.stderr)


def main() -> None:
    args = parse_args()

    list_path = Path(args.list_path).resolve()
    issues_root = Path(args.issues_root).resolve()

    try:
        update_list(
            list_path=list_path,
            issues_root=issues_root,
            encoding=args.encoding,
            dry_run=args.dry_run,
        )
    except ListUpdateError as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
