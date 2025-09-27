#!/usr/bin/env python3
"""JDK issue formatter script.

Reads a release note text file containing one JDK issue ID per line and renders a
summary file pulling structured data from the local `jdk_issues` directory.
"""
from __future__ import annotations

import argparse
import html
import re
import sys
from pathlib import Path
from typing import Iterable, List
import xml.etree.ElementTree as ET

ISSUES_DIR_NAME = "jdk_issues"


class IssueFormatterError(Exception):
    """Raised for domain-specific failures."""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Format JDK issues listed in a release note file.")
    parser.add_argument("input_file", type=Path, help="Release note file containing one JDK issue ID per line")
    return parser.parse_args()


def ensure_path_exists(path: Path, message: str) -> None:
    if not path.exists():
        raise IssueFormatterError(message)


def read_issue_ids(path: Path) -> List[str]:
    ensure_path_exists(path, f"Input file not found: {path}")
    content = path.read_text(encoding="utf-8")
    issue_ids: List[str] = []
    for line_number, raw_line in enumerate(content.splitlines(), start=1):
        issue_id = raw_line.strip()
        if not issue_id:
            continue
        if not issue_id.startswith("JDK-") or not issue_id[4:].isdigit():
            raise IssueFormatterError(f"Invalid JDK issue ID at {path}:{line_number}: {raw_line}")
        issue_ids.append(issue_id)
    if not issue_ids:
        raise IssueFormatterError(f"No JDK issue IDs found in input file: {path}")
    return issue_ids


def normalize_description(raw_description: str | None) -> str | None:
    if not raw_description:
        return None
    decoded = html.unescape(raw_description).replace("\r", "")
    decoded = re.sub(r"<br\s*/?>", "\n", decoded, flags=re.IGNORECASE)

    cleaned: List[str] = []
    in_tag = False
    for char in decoded:
        if char == "<":
            in_tag = True
            continue
        if char == ">":
            in_tag = False
            continue
        if not in_tag:
            cleaned.append(char)
    description = "".join(cleaned)

    normalized_lines: List[str] = []
    for line in description.splitlines():
        stripped_line = line.strip()
        if stripped_line:
            normalized_lines.append(stripped_line)

    return "\n".join(normalized_lines) or None


def extract_components(item: ET.Element) -> str:
    components = [normalize_text(element.text) for element in item.findall("component") if normalize_text(element.text)]
    return ", ".join(components)


def extract_os(item: ET.Element) -> str | None:
    customfields = item.find("customfields")
    if customfields is None:
        return None
    for customfield in customfields.findall("customfield"):
        name_elem = customfield.find("customfieldname")
        if normalize_text(name_elem.text) != "OS":
            continue
        values_elem = customfield.find("customfieldvalues")
        if values_elem is None:
            return None
        values: List[str] = []
        for value_elem in values_elem.findall("customfieldvalue"):
            value_text = normalize_text(value_elem.text)
            if value_text:
                values.append(value_text)
        if not values:
            return None
        return ", ".join(values)
    return None


def normalize_text(text: str | None) -> str | None:
    if text is None:
        return None
    stripped = text.strip()
    return stripped or None


def load_issue_data(base_dir: Path, issue_id: str) -> dict[str, str | None]:
    issue_dir = base_dir / issue_id
    ensure_path_exists(issue_dir, f"Issue directory not found: {issue_dir}")
    xml_name = f"jdk-{issue_id[4:].lower()}.xml"
    xml_path = issue_dir / xml_name
    ensure_path_exists(xml_path, f"Issue XML not found: {xml_path}")
    try:
        tree = ET.parse(xml_path)
    except ET.ParseError as exc:
        raise IssueFormatterError(f"Failed to parse XML {xml_path}: {exc}") from exc
    item = tree.find(".//item")
    if item is None:
        raise IssueFormatterError(f"Missing item element in XML: {xml_path}")

    title = normalize_text(item.findtext("title"))
    priority = normalize_text(item.findtext("priority"))
    issue_type = normalize_text(item.findtext("type"))
    component = extract_components(item)
    description = normalize_description(item.findtext("description"))
    os_value = extract_os(item)

    missing_fields = [name for name, value in {
        "Title": title,
        "Priority": priority,
        "Type": issue_type,
        "Component": component,
    }.items() if not value]
    if missing_fields:
        raise IssueFormatterError(
            f"Required fields missing ({', '.join(missing_fields)}) in {xml_path}"
        )

    return {
        "Title": title,
        "Priority": priority,
        "Type": issue_type,
        "Component": component,
        "Description": description,
        "OS": os_value,
    }


def build_block(issue_data: dict[str, str | None]) -> str:
    lines = [
        f"Title: {issue_data['Title']}",
        f"Priority: {issue_data['Priority']}",
        f"Type: {issue_data['Type']}",
        f"Component: {issue_data['Component']}",
    ]
    if issue_data.get("Description"):
        lines.append(f"Description: {issue_data['Description']}")
    if issue_data.get("OS"):
        lines.append(f"OS: {issue_data['OS']}")
    return "\n".join(lines)


def write_output(blocks: Iterable[str], output_path: Path) -> None:
    output_text = "\n\n-----\n".join(blocks)
    output_path.write_text(output_text + "\n", encoding="utf-8")


def write_skipped(skipped: Iterable[str], skipped_path: Path) -> None:
    """Write skipped issue IDs (one per line) to a companion file."""
    data = "\n".join(skipped)
    if data:
        skipped_path.write_text(data + "\n", encoding="utf-8")
    else:
        skipped_path.write_text("", encoding="utf-8")


def main() -> None:
    args = parse_args()
    base_dir = Path.cwd() / ISSUES_DIR_NAME
    ensure_path_exists(base_dir, f"{ISSUES_DIR_NAME} directory not found in current working directory: {base_dir}")

    issue_ids = read_issue_ids(args.input_file)

    blocks: List[str] = []
    skipped: List[str] = []
    for issue_id in issue_ids:
        issue_dir = base_dir / issue_id
        if not issue_dir.exists():
            skipped.append(issue_id)
            continue
        issue_data = load_issue_data(base_dir, issue_id)
        blocks.append(build_block(issue_data))

    output_path = Path(f"{args.input_file}_output.txt")
    write_output(blocks, output_path)

    skipped_path = Path(f"{args.input_file}_skipped.txt")
    write_skipped(skipped, skipped_path)


if __name__ == "__main__":
    try:
        main()
    except IssueFormatterError as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(1)
    except Exception as exc:  # Safety net
        print(f"Unexpected error: {exc}", file=sys.stderr)
        sys.exit(1)
