from __future__ import annotations

import pathlib
import re
from typing import Iterable, List

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


def main() -> None:
    output_dir = pathlib.Path.cwd() / "issue_ids"
    print(f"[INFO] Input directory: {INPUT_DIR}")
    print(f"[INFO] Output directory: {output_dir}")

    try:
        input_files = iter_input_files(INPUT_DIR)
    except FileNotFoundError as exc:
        print(f"[ERROR] {exc}")
        raise

    if not input_files:
        print("[WARN] No files found in input directory.")
        return

    output_dir.mkdir(parents=True, exist_ok=True)
    for markdown_path in input_files:
        print(f"[INFO] Processing: {markdown_path}")
        markdown_text = markdown_path.read_text(encoding="utf-8")
        issue_ids = extract_jdk_issue_ids(markdown_text)
        print(f"[INFO] Found {len(issue_ids)} issue IDs")
        output_path = output_dir / markdown_path.name
        write_issue_ids(issue_ids, output_path)
        print(f"[INFO] Wrote: {output_path}")

    print("[INFO] Extraction completed.")


if __name__ == "__main__":
    main()
