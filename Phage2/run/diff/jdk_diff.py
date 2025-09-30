from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Mapping
import xml.etree.ElementTree as ET

DEFAULT_TEMURIN_PATH = Path("Phage2/run/temurin/output_temurin/jdk-21.0.8.txt")
DEFAULT_OPENJDK_PATH = Path("Phage2/run/openjdk/output_openjdk/jdk-21.0.8.txt")
DEFAULT_OUTPUT_DIR = Path("Phage2/run/diff/output")
DEFAULT_ISSUES_DIR = Path("Phage2/run/diff/jdk_issues")
TEMURIN_ONLY_FILENAME = "temurin_only.txt"
OPENJDK_ONLY_FILENAME = "openjdk_only.txt"


@dataclass(frozen=True)
class IssueDetail:
    identifier: str
    summary: str | None
    status: str | None
    resolution: str | None
    link: str | None
    note: str | None = None

    def format_block(self) -> str:
        lines: list[str] = [self.identifier]
        if self.note:
            lines.append(f"note: {self.note}")
        else:
            lines.append(f"summary: {self.summary or '未取得'}")
            lines.append(f"status: {self.status or '未取得'}")
            lines.append(f"resolution: {self.resolution or '未取得'}")
            lines.append(f"link: {self.link or '未取得'}")
        return "\n".join(lines)


def read_identifiers(file_path: Path) -> set[str]:
    """Return the set of non-empty identifiers from the given file."""
    if not file_path.is_file():
        raise FileNotFoundError(f"Input file not found: {file_path}")

    identifiers: set[str] = set()
    with file_path.open("r", encoding="utf-8") as reader:
        for raw_line in reader:
            identifier = raw_line.strip()
            if identifier:
                identifiers.add(identifier)
    return identifiers


def write_issue_details(
    identifiers: Iterable[str],
    issues_dir: Path,
    output_path: Path,
) -> None:
    """Write identifiers and their details to the given path."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    sorted_ids = sorted(set(identifiers))

    with output_path.open("w", encoding="utf-8") as writer:
        for index, identifier in enumerate(sorted_ids):
            detail = load_issue_detail(identifier, issues_dir)
            writer.write(f"{detail.format_block()}\n")
            if index < len(sorted_ids) - 1:
                writer.write("\n")


def compute_differences(
    temurin_identifiers: set[str],
    openjdk_identifiers: set[str],
) -> Mapping[str, set[str]]:
    """Compute directional set differences for the two inputs."""
    return {
        "temurin_only": temurin_identifiers - openjdk_identifiers,
        "openjdk_only": openjdk_identifiers - temurin_identifiers,
    }


def load_issue_detail(identifier: str, issues_dir: Path) -> IssueDetail:
    """Load issue details from the jdk_issues directory."""
    issue_dir = issues_dir / identifier
    xml_path = issue_dir / f"{identifier.lower()}.xml"

    if not issue_dir.is_dir():
        return IssueDetail(
            identifier=identifier,
            summary=None,
            status=None,
            resolution=None,
            link=None,
            note="issueディレクトリが存在しません",
        )

    if not xml_path.is_file():
        return IssueDetail(
            identifier=identifier,
            summary=None,
            status=None,
            resolution=None,
            link=None,
            note="詳細XMLが存在しません",
        )

    try:
        root = ET.parse(xml_path).getroot()
    except ET.ParseError as error:
        return IssueDetail(
            identifier=identifier,
            summary=None,
            status=None,
            resolution=None,
            link=None,
            note=f"XML解析に失敗しました: {error}",
        )

    item = root.find(".//item")
    if item is None:
        return IssueDetail(
            identifier=identifier,
            summary=None,
            status=None,
            resolution=None,
            link=None,
            note="XML内にitem要素が存在しません",
        )

    def extract_text(tag: str) -> str | None:
        element = item.find(tag)
        if element is None or element.text is None:
            return None
        return element.text.strip()

    return IssueDetail(
        identifier=identifier,
        summary=extract_text("summary"),
        status=extract_text("status"),
        resolution=extract_text("resolution"),
        link=extract_text("link"),
    )


def collect_jdk_diff(
    temurin_path: Path = DEFAULT_TEMURIN_PATH,
    openjdk_path: Path = DEFAULT_OPENJDK_PATH,
    output_dir: Path = DEFAULT_OUTPUT_DIR,
    issues_dir: Path = DEFAULT_ISSUES_DIR,
) -> Mapping[str, Path]:
    """Generate diff files including issue details and return their paths."""
    temurin_identifiers = read_identifiers(temurin_path)
    openjdk_identifiers = read_identifiers(openjdk_path)

    differences = compute_differences(temurin_identifiers, openjdk_identifiers)

    temurin_only_path = output_dir / TEMURIN_ONLY_FILENAME
    openjdk_only_path = output_dir / OPENJDK_ONLY_FILENAME

    write_issue_details(differences["temurin_only"], issues_dir, temurin_only_path)
    write_issue_details(differences["openjdk_only"], issues_dir, openjdk_only_path)

    return {
        "temurin_only": temurin_only_path,
        "openjdk_only": openjdk_only_path,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate diff files from Temurin and OpenJDK issue lists.",
    )
    parser.add_argument(
        "--temurin-path",
        type=Path,
        default=DEFAULT_TEMURIN_PATH,
        help="Path to the Temurin JDK issue list.",
    )
    parser.add_argument(
        "--openjdk-path",
        type=Path,
        default=DEFAULT_OPENJDK_PATH,
        help="Path to the OpenJDK JDK issue list.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help="Directory where diff files will be stored.",
    )
    parser.add_argument(
        "--issues-dir",
        type=Path,
        default=DEFAULT_ISSUES_DIR,
        help="Directory containing issue detail folders (jdk_issues).",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    outputs = collect_jdk_diff(
        temurin_path=args.temurin_path,
        openjdk_path=args.openjdk_path,
        output_dir=args.output_dir,
        issues_dir=args.issues_dir,
    )
    for label, path in outputs.items():
        print(f"{label}: {path}")


if __name__ == "__main__":
    main()
