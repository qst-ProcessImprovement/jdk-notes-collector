"""JDK 21 の "Resolved In Build" ごとの JIRA XML を収集し、個別ファイルと統合 XML を生成するスクリプト。"""

from __future__ import annotations

import datetime as _dt
import sys
from enum import Enum
import urllib.error
import urllib.request
from pathlib import Path
from typing import Iterable, Sequence
from xml.etree import ElementTree as ET

# 取得対象のビルド番号（正準表現として b1〜b35 を列挙）。
BUILD_NUMBERS: tuple[str, ...] = tuple(f"b{index:02d}" for index in range(1, 36))
FIX_VERSION = "21"

# JIRA 検索結果 XML のリクエスト URL テンプレート。
# https://bugs.openjdk.org/sr/jira.issueviews:searchrequest-xml/temp/SearchRequest.xml?jqlQuery=project+%3D+JDK+AND+fixVersion+%3D+{fix_version}+AND+resolution+%3D+Fixed+AND+%22resolved+in+build%22+%3D+{build_number}
JIRA_SEARCH_URL_TEMPLATE = (
    "https://bugs.openjdk.org/sr/jira.issueviews:searchrequest-xml/temp/SearchRequest.xml"
    "?jqlQuery=project+%3D+JDK+AND+fixVersion+%3D+{fix_version}+AND+resolution+%3D+Fixed+"
    "AND+%22resolved+in+build%22+%3D+{build_number}"
)

# 出力先は実行時カレントディレクトリ配下。
OUTPUT_DIRECTORY = Path(".")
BUILD_SUBDIRECTORY = Path("builds")
AGGREGATE_FILENAME = "all_builds.xml"

REQUEST_TIMEOUT_SECONDS = 60
USER_AGENT = "jdk-notes-collector/1.0"


class XmlIssueCountError(RuntimeError):
    """XML 内から課題総数を特定できない場合の例外。"""


def build_request_url(build_number: str) -> str:
    return JIRA_SEARCH_URL_TEMPLATE.format(fix_version=FIX_VERSION, build_number=build_number)


def fetch_xml(url: str) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=REQUEST_TIMEOUT_SECONDS) as response:
        if response.status != 200:
            raise urllib.error.HTTPError(
                url=url,
                code=response.status,
                msg=f"Unexpected HTTP status: {response.status}",
                hdrs=response.headers,
                fp=None,
            )
        return response.read()


def extract_issue_total(xml_content: bytes) -> int:
    try:
        root = ET.fromstring(xml_content)
    except ET.ParseError as error:
        raise XmlIssueCountError(f"Failed to parse XML: {error}") from error

    channel = root.find("channel")
    if channel is None:
        raise XmlIssueCountError("Missing <channel> element")

    issue = channel.find("issue")
    if issue is None:
        raise XmlIssueCountError("Missing <issue> element")

    total_attr = issue.attrib.get("total")
    if total_attr is None:
        raise XmlIssueCountError("Missing 'total' attribute on <issue> element")

    try:
        return int(total_attr)
    except ValueError as error:
        raise XmlIssueCountError("Invalid issue total value") from error


def write_xml(content: bytes, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(content)


class FetchOutcome(Enum):
    SUCCESS = "success"
    NOT_FOUND = "not_found"
    ERROR = "error"


def fetch_build_xml(build_number: str) -> tuple[FetchOutcome, bytes | None]:
    url = build_request_url(build_number)
    try:
        xml_content = fetch_xml(url)
    except urllib.error.URLError as error:
        if isinstance(error, urllib.error.HTTPError) and error.code == 400:
            print(f"[INFO] {build_number}: JIRA に該当するビルドが存在しません (HTTP 400)")
            return FetchOutcome.NOT_FOUND, None
        print(f"[ERROR] {build_number}: {error}", file=sys.stderr)
        return FetchOutcome.ERROR, None

    try:
        issue_total = extract_issue_total(xml_content)
    except XmlIssueCountError as error:
        print(f"[ERROR] {build_number}: {error}", file=sys.stderr)
        return FetchOutcome.ERROR, None

    if issue_total == 0:
        print(f"[INFO] {build_number}: 対応する課題が見つかりません (保存をスキップ)")
        return FetchOutcome.NOT_FOUND, None

    return FetchOutcome.SUCCESS, xml_content


def save_individual_xml(build_number: str, xml_content: bytes, output_dir: Path) -> Path:
    output_path = output_dir / BUILD_SUBDIRECTORY / f"{build_number}.xml"
    write_xml(xml_content, output_path)
    print(f"[INFO] {build_number}: {output_path.relative_to(Path.cwd())} に保存しました")
    return output_path


def build_aggregate_xml(entries: Sequence[tuple[str, bytes]]) -> bytes:
    root = ET.Element(
        "resolvedInBuildCollection",
        attrib={
            "fixVersion": FIX_VERSION,
            "generatedAt": _dt.datetime.now(tz=_dt.timezone.utc).isoformat(),
        },
    )

    for build_number, xml_content in entries:
        container = ET.SubElement(root, "searchResult", attrib={"build": build_number})
        rss_root = ET.fromstring(xml_content)
        container.append(rss_root)

    return ET.tostring(root, encoding="utf-8", xml_declaration=True)


def write_aggregate_xml(entries: Sequence[tuple[str, bytes]], output_dir: Path) -> Path:
    aggregate_path = output_dir / AGGREGATE_FILENAME
    aggregate_content = build_aggregate_xml(entries)
    write_xml(aggregate_content, aggregate_path)
    print(f"[INFO] 統合 XML: {aggregate_path.relative_to(Path.cwd())} に保存しました")
    return aggregate_path


def collect_resolved_in_build_xml(build_numbers: Iterable[str]) -> tuple[list[tuple[str, bytes]], int]:
    collected: list[tuple[str, bytes]] = []
    failures = 0
    for build_number in build_numbers:
        outcome, xml_content = fetch_build_xml(build_number)
        if outcome is FetchOutcome.ERROR:
            failures += 1
            continue
        if outcome is FetchOutcome.NOT_FOUND:
            continue
        assert xml_content is not None
        collected.append((build_number, xml_content))
    return collected, failures


def main() -> None:
    output_dir = Path.cwd() / OUTPUT_DIRECTORY
    collected_entries, failures = collect_resolved_in_build_xml(BUILD_NUMBERS)

    if not collected_entries:
        print("[WARN] 保存対象となる XML がありませんでした", file=sys.stderr)
        sys.exit(1)

    for build_number, xml_content in collected_entries:
        save_individual_xml(build_number, xml_content, output_dir)

    write_aggregate_xml(collected_entries, output_dir)
    if failures:
        print(f"[WARN] 取得に失敗したビルドが {failures} 件あります", file=sys.stderr)
        sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    main()
