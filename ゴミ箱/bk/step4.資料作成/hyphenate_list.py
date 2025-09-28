"""list.txt のレコードをアンダーバー連結し説明文を付加するユーティリティ."""

from __future__ import annotations

from argparse import ArgumentParser, Namespace
from pathlib import Path
from typing import Dict, Iterable, List, Mapping, Optional, Set
import sys

NO_DESCRIPTION_PLACEHOLDER = "(no description)"


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


def extract_issue_id(fields: Iterable[str]) -> Optional[str]:
    for field in fields:
        if field.startswith("JDK-"):
            return field
    return None


def load_issue_descriptions(combined_path: Path) -> Dict[str, str]:
    """JDK 番号ごとの説明文を読み込む."""

    if not combined_path.exists():
        raise SystemExit(f"説明ファイルが見つかりません: {combined_path}")

    lines = combined_path.read_text(encoding="utf-8").splitlines()
    descriptions: Dict[str, str] = {}
    current_id: Optional[str] = None
    current_desc_lines: Optional[List[str]] = None

    def finalize() -> None:
        nonlocal current_desc_lines
        if current_id is None:
            return
        if current_desc_lines is None:
            descriptions[current_id] = NO_DESCRIPTION_PLACEHOLDER
            return
        description = " ".join(line.strip() for line in current_desc_lines).strip()
        if not description:
            description = NO_DESCRIPTION_PLACEHOLDER
        descriptions[current_id] = description
        current_desc_lines = None

    for line in lines:
        stripped = line.strip()
        if line.startswith("Title: [JDK-"):
            finalize()
            start = line.find("[")
            end = line.find("]", start + 1)
            if start == -1 or end == -1:
                current_id = None
                current_desc_lines = None
                continue
            current_id = line[start + 1 : end]
            current_desc_lines = None
        elif line.startswith("Description:"):
            current_desc_lines = []
        elif current_desc_lines is not None:
            if stripped == "":
                finalize()
            else:
                current_desc_lines.append(stripped)

    finalize()
    return descriptions


def hyphenate_records(
    lines: Iterable[str], descriptions: Mapping[str, str], missing_ids: Optional[Set[str]] = None
) -> List[str]:
    """p/P の優先度行を区切りとし各項目をアンダーバー連結する."""

    records: List[str] = []
    current_fields: List[str] = []

    for raw_line in lines:
        field = raw_line.strip()
        if not field:
            continue

        if is_record_marker(field) and current_fields:
            records.append(_combine_fields(current_fields, descriptions, missing_ids))
            current_fields = []

        current_fields.append(field)

    if current_fields:
        records.append(_combine_fields(current_fields, descriptions, missing_ids))

    return records


def _combine_fields(
    fields: List[str], descriptions: Mapping[str, str], missing_ids: Optional[Set[str]] = None
) -> str:
    issue_id = extract_issue_id(fields)
    combined_fields = list(fields)

    if issue_id is not None:
        description = descriptions.get(issue_id)
        if description is None:
            if missing_ids is not None:
                missing_ids.add(issue_id)
            description = NO_DESCRIPTION_PLACEHOLDER
        combined_fields.append(description)

    return "_".join(combined_fields)


def hyphenate_file(
    input_path: Path, output_path: Path, descriptions: Mapping[str, str]
) -> Path:
    """入力ファイルをアンダーバー連結して出力ファイルに書き出す."""

    lines = input_path.read_text(encoding="utf-8").splitlines()
    missing_ids: Set[str] = set()
    records = hyphenate_records(lines, descriptions, missing_ids)

    if records:
        output_text = "\n".join(records) + "\n"
    else:
        output_text = ""

    output_path.write_text(output_text, encoding="utf-8")

    if missing_ids:
        joined = ", ".join(sorted(missing_ids))
        print(
            f"警告: 説明が見つからない課題があります ({joined})。",
            file=sys.stderr,
        )

    return output_path


def parse_args() -> Namespace:
    parser = ArgumentParser(description="list.txt をアンダーバー区切りに変換する")
    parser.add_argument(
        "--input",
        default="list.txt",
        help="変換対象のファイル名（カレントディレクトリ想定）",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="出力ファイル名（省略時は list_underscored.txt）",
    )
    parser.add_argument(
        "--combined",
        default="jdk_issues_combined.txt",
        help="説明文を含むファイル名（入力ファイルと同じディレクトリ想定）",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    input_path = (Path.cwd() / args.input).resolve()
    if not input_path.exists():
        raise SystemExit(f"入力ファイルが見つかりません: {input_path}")

    default_output = input_path.with_name("list_underscored.txt")

    if args.output is None:
        output_path = default_output
    else:
        output_path = (Path.cwd() / args.output).resolve()

    if output_path == input_path:
        raise SystemExit("出力ファイルは list.txt とは別名にしてください。")

    if output_path.parent != input_path.parent:
        raise SystemExit("出力ファイルは入力ファイルと同じディレクトリに配置してください。")

    combined_path = (Path.cwd() / args.combined).resolve()
    if combined_path.parent != input_path.parent:
        raise SystemExit("説明ファイルは入力ファイルと同じディレクトリに配置してください。")

    descriptions = load_issue_descriptions(combined_path)

    hyphenate_file(input_path, output_path, descriptions)


if __name__ == "__main__":
    main()
