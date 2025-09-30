from __future__ import annotations

import pathlib
import re
from typing import Iterable, List, Tuple

BASE_DIR = pathlib.Path(__file__).resolve().parent
INPUT_DIR = BASE_DIR / "OpenJDK"

_JDK_ID_PATTERN = re.compile(r"JDK-\d+")


def extract_jdk_issue_ids(markdown_text: str) -> List[str]:
    """Return all JDK issue identifiers in their appearance order."""
    return _JDK_ID_PATTERN.findall(markdown_text)


def write_issue_ids(issue_ids: Iterable[str], output_path: pathlib.Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(issue_ids) + ("\n" if issue_ids else ""), encoding="utf-8")


def iter_input_files(directory: pathlib.Path) -> List[pathlib.Path]:
    if not directory.is_dir():
        raise FileNotFoundError(f"Input directory does not exist: {directory}")
    return sorted(path for path in directory.iterdir() if path.is_file())


def deduplicate_issue_ids(issue_ids: Iterable[str]) -> Tuple[List[str], List[str]]:
    seen = set()
    unique: List[str] = []
    duplicates: List[str] = []
    for issue_id in issue_ids:
        if issue_id in seen:
            duplicates.append(issue_id)
        else:
            seen.add(issue_id)
            unique.append(issue_id)
    return unique, duplicates


def sort_issue_ids(issue_ids: Iterable[str]) -> List[str]:
    return sorted(issue_ids, key=lambda issue_id: int(issue_id.split("-", 1)[1]))


def format_duplicates(duplicates: Iterable[str]) -> str:
    sorted_unique = sort_issue_ids({*duplicates})
    return "\n".join(f"    {issue_id}" for issue_id in sorted_unique)


def main() -> None:
    output_dir = pathlib.Path.cwd() / "output_openjdk"

    input_files = iter_input_files(INPUT_DIR)
    if not input_files:
        return

    output_dir.mkdir(parents=True, exist_ok=True)
    for markdown_path in input_files:
        markdown_text = markdown_path.read_text(encoding="utf-8")
        issue_ids = extract_jdk_issue_ids(markdown_text)

        unique_issue_ids, duplicates = deduplicate_issue_ids(issue_ids)
        if duplicates:
            duplicate_summary = format_duplicates(duplicates)
            print(
                f"[WARN] Duplicated IDs ({len(duplicates)}) in {markdown_path.name}:\n{duplicate_summary}"
            )

        sorted_issue_ids = sort_issue_ids(unique_issue_ids)
        output_filename = f"jdk-{markdown_path.stem}.txt"
        output_path = output_dir / output_filename
        write_issue_ids(sorted_issue_ids, output_path)


if __name__ == "__main__":
    main()
