#!/usr/bin/env python3
"""JDK差分テーブル生成モジュール."""
from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Callable, Dict, Iterable, List, Sequence, Tuple
import xml.etree.ElementTree as ET

SCRIPT_DIR = Path(__file__).resolve().parent
OUTPUT_FILENAME = "jdk_diff_report.txt"

PRODUCT_DEFINITIONS: Tuple[Tuple[str, Tuple[str, ...]], ...] = (
    ("OpenJDK", ("openjdk", "issue_ids.txt")),
    ("OracleJDK", ("oraclejdk", "issue_ids.txt")),
    ("Temurin", ("temurin", "issue_ids.txt")),
)


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


def load_issue_ids(path: Path) -> set[str]:
    if not path.is_file():
        raise JDKDiffError(f"JDK番号リストが見つかりません: {path}")

    issue_ids: set[str] = set()
    with path.open(encoding="utf-8") as handle:
        for lineno, raw_line in enumerate(handle, start=1):
            entry = raw_line.strip()
            if not entry:
                continue
            if not entry.startswith("JDK-") or not entry[4:].isdigit():
                raise JDKDiffError(
                    f"正準表現に反する行を検出しました: {path}:{lineno} -> '{entry}'"
                )
            issue_ids.add(entry)
    return issue_ids


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
    matrix = [list(headers), *[list(row) for row in rows]]
    columns = list(zip(*matrix))
    widths = [max(len(str(cell)) for cell in column) for column in columns]

    def render_line(cells: Sequence[str]) -> str:
        padded_cells = []
        for index, (cell, width) in enumerate(zip(cells, widths)):
            cell_str = str(cell)
            if index == len(widths) - 1:
                padded_cells.append(cell_str)
            else:
                padded_cells.append(cell_str.ljust(width))
        return " | ".join(padded_cells).rstrip()

    lines = [render_line(headers)]
    lines.append("-+-".join("-" * width for width in widths))
    for row in rows:
        lines.append(render_line(row))
    return "\n".join(lines)


def build_diff_table(
    data: Dict[str, set[str]], fix_version_loader: Callable[[str], Tuple[str, ...]]
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
            fix_versions = ["N/A"]
            counted = False
        if counted:
            non_21_count += 1
        formatted_fix_versions = ", ".join(fix_versions)
        rows.append([issue_id, *presence, formatted_fix_versions])

    return rows, len(diff_ids), len(common_ids), non_21_count


def build_report() -> tuple[str, int, int, int]:
    product_specs, base_dir = resolve_product_specs()
    fix_version_loader = make_fix_version_loader(base_dir)

    product_data: Dict[str, set[str]] = {}
    for product, path in product_specs:
        product_data[product] = load_issue_ids(path)

    rows, diff_count, matched_count, non_21_count = build_diff_table(product_data, fix_version_loader)
    headers = ["JDK", *product_data.keys(), "Fix Version/s"]
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
        f"プロダクト差分JDK件数: {diff_count}",
        f"全てのプロダクトで一致したJDK件数: {matched_count}",
        f"Fix Version/sが21以外のJDK件数: {non_21_count}",
        "",
    ]
    output_path.write_text("\n".join(output_lines), encoding="utf-8")

    print(f"プロダクト差分JDK件数: {diff_count}")
    print(f"出力ファイル: {output_path}")


if __name__ == "__main__":
    main()
