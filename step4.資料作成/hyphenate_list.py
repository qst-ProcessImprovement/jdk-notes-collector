"""list.txt のレコードをハイフン連結で書き出すユーティリティ."""

from __future__ import annotations

from argparse import ArgumentParser, Namespace
from pathlib import Path
from typing import Iterable, List


def is_record_marker(field: str) -> bool:
    """優先度行 (P?, P1, ...) 判定を行う."""
    if not field:
        return False
    if field[0] not in {"P", "p"}:
        return False
    if len(field) == 1:
        return True
    lead = field[1]
    return lead.isdigit() or lead == "?"


def hyphenate_records(lines: Iterable[str]) -> List[str]:
    """p/P で始まる優先度行を区切りとしてレコードをハイフン結合する."""

    records: List[str] = []
    current_fields: List[str] = []

    for raw_line in lines:
        field = raw_line.strip()
        if not field:
            continue

        if is_record_marker(field) and current_fields:
            records.append("-".join(current_fields))
            current_fields = []

        current_fields.append(field)

    if current_fields:
        records.append("-".join(current_fields))

    return records


def hyphenate_file(input_path: Path, output_path: Path) -> Path:
    """入力ファイルをハイフン連結して出力ファイルに書き出す."""

    lines = input_path.read_text(encoding="utf-8").splitlines()
    records = hyphenate_records(lines)

    if records:
        output_text = "\n".join(records) + "\n"
    else:
        output_text = ""

    output_path.write_text(output_text, encoding="utf-8")
    return output_path


def parse_args() -> Namespace:
    parser = ArgumentParser(description="list.txt をハイフン区切りに変換する")
    parser.add_argument(
        "--input",
        default="list.txt",
        help="変換対象のファイル名（カレントディレクトリ想定）",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="出力ファイル名（省略時は list-hyphenated.txt）",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    input_path = (Path.cwd() / args.input).resolve()
    if not input_path.exists():
        raise SystemExit(f"入力ファイルが見つかりません: {input_path}")

    default_output = input_path.with_name("list-hyphenated.txt")

    if args.output is None:
        output_path = default_output
    else:
        output_path = (Path.cwd() / args.output).resolve()

    if output_path == input_path:
        raise SystemExit("出力ファイルは list.txt とは別名にしてください。")

    if output_path.parent != input_path.parent:
        raise SystemExit("出力ファイルは入力ファイルと同じディレクトリに配置してください。")

    hyphenate_file(input_path, output_path)


if __name__ == "__main__":
    main()
