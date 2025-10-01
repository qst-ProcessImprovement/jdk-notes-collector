#!/usr/bin/env python3
"""JDK差分テーブル生成モジュール."""
from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Callable, Dict, Iterable, List, Sequence, Tuple
import xml.etree.ElementTree as ET

SCRIPT_DIR = Path(__file__).resolve().parent
OUTPUT_FILENAME = "jdk_diff_report.md"

PRODUCT_DEFINITIONS: Tuple[Tuple[str, Tuple[str, ...]], ...] = (
    ("OpenJDK", ("openjdk", "issue_ids.txt")),
    ("OracleJDK", ("oraclejdk", "issue_ids.txt")),
    ("Temurin", ("temurin", "issue_ids.txt")),
)
BACKPORT_PREFIX_TO_PRODUCT: Dict[str, str] = {
    path_parts[0]: product for product, path_parts in PRODUCT_DEFINITIONS
}


class JDKDiffError(Exception):
    """モジュール内で発生する例外."""


def resolve_product_specs() -> Tuple[List[Tuple[str, Path]], Path]:
    """実行ディレクトリとモジュール配置ディレクトリの順にデータルートを探索する."""
    candidates = (Path.cwd(), SCRIPT_DIR)
    for base_dir in candidates:
        specs = [(product, base_dir.joinpath(*path_parts)) for product, path_parts in PRODUCT_DEFINITIONS]
        if all(path.is_file() for _, path in specs):
            return specs, base_dir
    expected = ", ".join("/".join(path_parts) for _, path_parts in PRODUCT_DEFINITIONS)
    raise JDKDiffError(
        "JDK番号リストが見つかりません: "
        f"期待パス [{expected}] が実行ディレクトリ ({Path.cwd()}) とモジュール配置ディレクトリ ({SCRIPT_DIR}) のいずれにも存在しません"
    )


def load_issue_ids(path: Path) -> Tuple[set[str], Dict[str, Dict[str, List[str]]]]:
    if not path.is_file():
        raise JDKDiffError(f"JDK番号リストが見つかりません: {path}")

    issue_ids: set[str] = set()
    backport_entries: Dict[str, Dict[str, List[str]]] = {}
    with path.open(encoding="utf-8") as handle:
        for lineno, raw_line in enumerate(handle, start=1):
            entry = raw_line.strip()
            if not entry:
                continue

            segments = [segment.strip() for segment in entry.split(",")]
            base_issue = segments[0]
            if not base_issue.startswith("JDK-") or not base_issue[4:].isdigit():
                raise JDKDiffError(
                    f"正準表現に反する行を検出しました: {path}:{lineno} -> '{entry}'"
                )
            if base_issue in issue_ids:
                raise JDKDiffError(
                    f"同一JDK番号が重複しています: {path}:{lineno} -> '{base_issue}'"
                )

            issue_ids.add(base_issue)

            for raw_backport in segments[1:]:
                if not raw_backport:
                    raise JDKDiffError(
                        f"正準表現に反するbackport指定を検出しました: {path}:{lineno}"
                    )
                if "_" not in raw_backport:
                    raise JDKDiffError(
                        f"backport指定の形式が不正です: {path}:{lineno} -> '{raw_backport}'"
                    )

                prefix, backport_issue = raw_backport.split("_", 1)
                product_name = BACKPORT_PREFIX_TO_PRODUCT.get(prefix)
                if product_name is None:
                    raise JDKDiffError(
                        f"未知のbackport接頭辞を検出しました: {path}:{lineno} -> '{prefix}'"
                    )
                if not backport_issue.startswith("JDK-") or not backport_issue[4:].isdigit():
                    raise JDKDiffError(
                        f"backport指定のJDK番号が正準表現に反します: {path}:{lineno} -> '{backport_issue}'"
                    )

                per_issue = backport_entries.setdefault(base_issue, {})
                backport_list = per_issue.setdefault(product_name, [])
                if backport_issue not in backport_list:
                    backport_list.append(backport_issue)

    return issue_ids, backport_entries


def make_fix_version_loader(base_dir: Path) -> Callable[[str], Tuple[str, ...]]:
    """Fix Version/s をロードする関数を生成する."""
    issues_root = base_dir / "jdk_issues"
    if not issues_root.is_dir():
        raise JDKDiffError(f"Fix Version情報ディレクトリが見つかりません: {issues_root}")

    @lru_cache(maxsize=None)
    def load(issue_id: str) -> Tuple[str, ...]:
        issue_dir = issues_root / issue_id
        if not issue_dir.is_dir():
            raise JDKDiffError(f"Fix Version情報ディレクトリが見つかりません: {issue_dir}")
        xml_path = issue_dir / f"{issue_id.lower()}"
        xml_path = xml_path.with_suffix(".xml")
        if not xml_path.is_file():
            raise JDKDiffError(f"Fix Version情報が見つかりません: {xml_path}")
        try:
            tree = ET.parse(xml_path)
        except ET.ParseError as error:
            raise JDKDiffError(f"Fix Version XMLの解析に失敗しました: {xml_path}") from error

        seen: set[str] = set()
        versions: List[str] = []
        for element in tree.iterfind(".//fixVersion"):
            value = (element.text or "").strip()
            if not value:
                continue
            if value not in seen:
                seen.add(value)
                versions.append(value)

        if not versions:
            raise JDKDiffError(f"Fix Version/s が取得できません: {xml_path}")

        return tuple(versions)

    return load


def sort_jdk_ids(issue_ids: Iterable[str]) -> List[str]:
    def numeric_key(item: str) -> int:
        try:
            return int(item.split("-", maxsplit=1)[1])
        except (IndexError, ValueError) as error:
            raise JDKDiffError(f"JDK番号の解析に失敗しました: '{item}'") from error

    return sorted(issue_ids, key=numeric_key)


def render_table(headers: Sequence[str], rows: Sequence[Sequence[str]]) -> str:
    def format_row(cells: Sequence[str]) -> str:
        return "| " + " | ".join(str(cell) for cell in cells) + " |"

    header_line = format_row(headers)
    separator_line = "| " + " | ".join("---" for _ in headers) + " |"
    lines = [header_line, separator_line]
    for row in rows:
        lines.append(format_row(row))
    return "\n".join(lines)


def build_diff_table(
    data: Dict[str, set[str]],
    backport_lookup: Dict[str, Dict[str, List[str]]],
    fix_version_loader: Callable[[str], Tuple[str, ...]]
) -> Tuple[List[List[str]], int, int, int]:
    if not data:
        return [], 0, 0, 0

    product_order = list(data.keys())
    all_ids = set.union(*data.values())
    common_ids = set.intersection(*data.values())
    diff_ids = sort_jdk_ids(all_ids - common_ids)

    rows: List[List[str]] = []
    non_21_count = 0
    for issue_id in diff_ids:
        presence = ["Y" if issue_id in data[product] else "N" for product in product_order]
        try:
            fix_versions = list(fix_version_loader(issue_id))
            counted = any(value != "21" for value in fix_versions)
        except JDKDiffError:
            fix_versions = ["Issueページなし"]
            counted = False
        if counted:
            non_21_count += 1
        formatted_fix_versions = ", ".join(fix_versions)
        per_issue_backports = backport_lookup.get(issue_id, {})
        backport_values: List[str] = []
        for product in product_order:
            issues = per_issue_backports.get(product)
            backport_values.append(", ".join(issues) if issues else "")
        rows.append([issue_id, *presence, formatted_fix_versions, *backport_values])

    return rows, len(diff_ids), len(common_ids), non_21_count


def build_report() -> tuple[str, int, int, int]:
    product_specs, base_dir = resolve_product_specs()
    fix_version_loader = make_fix_version_loader(base_dir)

    product_data: Dict[str, set[str]] = {}
    backport_lookup: Dict[str, Dict[str, List[str]]] = {}
    for product, path in product_specs:
        issue_ids, backports = load_issue_ids(path)
        product_data[product] = issue_ids
        for base_issue, per_product_backports in backports.items():
            target = backport_lookup.setdefault(base_issue, {})
            for backport_product, issues in per_product_backports.items():
                target_list = target.setdefault(backport_product, [])
                for issue in issues:
                    if issue not in target_list:
                        target_list.append(issue)

    rows, diff_count, matched_count, non_21_count = build_diff_table(
        product_data, backport_lookup, fix_version_loader
    )
    backport_headers = [f"JDK - {product} backport" for product in product_data.keys()]
    headers = ["JDK", *product_data.keys(), "Fix Version/s", *backport_headers]
    table_text = render_table(headers, rows)
    return table_text, diff_count, matched_count, non_21_count


def main() -> None:
    table_text, diff_count, matched_count, non_21_count = build_report()

    output_path = Path.cwd() / OUTPUT_FILENAME
    description = (
        "このファイルは OpenJDK・OracleJDK・Temurin の issue_ids.txt を比較し、三製品で一致しない JDK 番号と各 Fix Version/s を一覧化したものです。"
    )
    output_lines = [
        description,
        "",
        table_text,
        "",
        f"全てのプロダクトで一致したJDK件数: {matched_count}  ",
        f"プロダクトごとに差分のあるJDK件数: {diff_count}  ",
        f"Fix Version/sが21以外のJDK件数: {non_21_count}  ",
        "",
    ]
    output_path.write_text("\n".join(output_lines), encoding="utf-8")

    print(f"プロダクト差分JDK件数: {diff_count}")
    print(f"出力ファイル: {output_path}")


if __name__ == "__main__":
    main()
