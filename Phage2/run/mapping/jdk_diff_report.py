#!/usr/bin/env python3
"""JDK差分テーブル生成モジュール."""
from __future__ import annotations

from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Tuple

SCRIPT_DIR = Path(__file__).resolve().parent
OUTPUT_FILENAME = "jdk_diff_report.txt"

PRODUCT_DEFINITIONS: Tuple[Tuple[str, Tuple[str, ...]], ...] = (
    ("OpenJDK", ("openjdk", "issue_ids.txt")),
    ("OracleJDK", ("oraclejdk", "issue_ids.txt")),
    ("Temurin", ("temurin", "issue_ids.txt")),
)


class JDKDiffError(Exception):
    """モジュール内で発生する例外."""


def resolve_product_specs() -> List[Tuple[str, Path]]:
    """実行ディレクトリとモジュール配置ディレクトリの順にデータルートを探索する."""
    candidates = (Path.cwd(), SCRIPT_DIR)
    for base_dir in candidates:
        specs = [(product, base_dir.joinpath(*path_parts)) for product, path_parts in PRODUCT_DEFINITIONS]
        if all(path.is_file() for _, path in specs):
            return specs
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
        return " | ".join(str(cell).ljust(width) for cell, width in zip(cells, widths))

    lines = [render_line(headers)]
    lines.append("-+-".join("-" * width for width in widths))
    for row in rows:
        lines.append(render_line(row))
    return "\n".join(lines)


def build_diff_table(data: Dict[str, set[str]]) -> List[List[str]]:
    if not data:
        return []

    product_order = list(data.keys())
    all_ids = set.union(*data.values())
    common_ids = set.intersection(*data.values())
    diff_ids = sort_jdk_ids(all_ids - common_ids)

    rows: List[List[str]] = []
    for issue_id in diff_ids:
        presence = ["Y" if issue_id in data[product] else "N" for product in product_order]
        rows.append([issue_id, *presence])
    return rows


def build_report() -> str:
    product_specs = resolve_product_specs()
    product_data: Dict[str, set[str]] = {}
    for product, path in product_specs:
        product_data[product] = load_issue_ids(path)

    diff_rows = build_diff_table(product_data)
    headers = ["JDK", *product_data.keys()]
    return render_table(headers, diff_rows)


def main() -> None:
    table_text = build_report()

    output_path = Path.cwd() / OUTPUT_FILENAME
    output_path.write_text(table_text + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
