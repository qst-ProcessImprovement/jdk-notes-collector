"""JDK 21 の "Resolved In Build" ごとの JIRA XML を収集し、個別ファイルと統合 XML を生成するスクリプト。"""

from __future__ import annotations

import datetime as _dt
import sys
from enum import Enum
import urllib.error
import urllib.request
from pathlib import Path
from typing import Iterable, Sequence, NamedTuple
from xml.etree import ElementTree as ET

# 取得対象のバージョンと "Resolved in Build" の正準定義。
OPENJDK_RESOLVED_BUILD_TARGETS: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("21.0.1", tuple(f"b{index:02d}" for index in range(1, 11))),
    ("21.0.2", tuple(f"b{index:02d}" for index in range(1, 14))),
    ("21.0.3", tuple(f"b{index:02d}" for index in range(1, 10))),
    ("21.0.4", tuple(f"b{index:02d}" for index in range(1, 8))),
    ("21.0.5", tuple(f"b{index:02d}" for index in range(1, 12))),
    ("21.0.6", tuple(f"b{index:02d}" for index in range(1, 8))),
    ("21.0.7", tuple(f"b{index:02d}" for index in range(1, 7))),
    ("21.0.8", tuple(f"b{index:02d}" for index in range(1, 10))),
)
OPENJDK_FIX_VERSIONS: tuple[str, ...] = tuple(version for version, _ in OPENJDK_RESOLVED_BUILD_TARGETS)
ORACLEJDK_RESOLVED_BUILD_TARGETS: tuple[tuple[str, tuple[str, ...]], ...] = tuple(
    (f"{version}-oracle", build_numbers) for version, build_numbers in OPENJDK_RESOLVED_BUILD_TARGETS
)
ORACLEJDK_FIX_VERSIONS: tuple[str, ...] = tuple(version for version, _ in ORACLEJDK_RESOLVED_BUILD_TARGETS)


class DistributionTarget(NamedTuple):
    label: str
    output_subdirectory: Path
    targets: tuple[tuple[str, tuple[str, ...]], ...]
    fix_versions: tuple[str, ...]
    aggregate_filename: str


DISTRIBUTION_TARGETS: tuple[DistributionTarget, ...] = (
    DistributionTarget(
        "OpenJDK",
        Path("OpenJDK"),
        OPENJDK_RESOLVED_BUILD_TARGETS,
        OPENJDK_FIX_VERSIONS,
        "all_builds_openjdk.xml",
    ),
    DistributionTarget(
        "OracleJDK",
        Path("OracleJDK"),
        ORACLEJDK_RESOLVED_BUILD_TARGETS,
        ORACLEJDK_FIX_VERSIONS,
        "all_builds_oraclejdk.xml",
    ),
)
# JIRA 検索結果 XML のリクエスト URL テンプレート。
# https://bugs.openjdk.org/sr/jira.issueviews:searchrequest-xml/temp/SearchRequest.xml?jqlQuery=project+%3D+JDK+AND+fixVersion+%3D+{fix_version}+AND+resolution+%3D+Fixed+AND+%22resolved+in+build%22+%3D+{build_number}
JIRA_SEARCH_URL_TEMPLATE = (
    "https://bugs.openjdk.org/sr/jira.issueviews:searchrequest-xml/temp/SearchRequest.xml"
    "?jqlQuery=project+%3D+JDK+AND+fixVersion+%3D+{fix_version}+AND+resolution+%3D+Fixed+"
    "AND+%22resolved+in+build%22+%3D+{build_number}"
)

# 出力先は実行時カレントディレクトリ配下。
OUTPUT_DIRECTORY = Path("builds")

REQUEST_TIMEOUT_SECONDS = 60
USER_AGENT = "jdk-notes-collector/1.0"


class XmlIssueCountError(RuntimeError):
    """XML 内から課題総数を特定できない場合の例外。"""


def build_request_url(fix_version: str, build_number: str) -> str:
    return JIRA_SEARCH_URL_TEMPLATE.format(fix_version=fix_version, build_number=build_number)


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


def fetch_build_xml(fix_version: str, build_number: str) -> tuple[FetchOutcome, bytes | None]:
    url = build_request_url(fix_version, build_number)
    try:
        xml_content = fetch_xml(url)
    except urllib.error.URLError as error:
        if isinstance(error, urllib.error.HTTPError) and error.code == 400:
            print(
                f"[INFO] {fix_version} {build_number}: JIRA に該当するビルドが存在しません (HTTP 400)"
            )
            return FetchOutcome.NOT_FOUND, None
        print(f"[ERROR] {fix_version} {build_number}: {error}", file=sys.stderr)
        return FetchOutcome.ERROR, None

    try:
        issue_total = extract_issue_total(xml_content)
    except XmlIssueCountError as error:
        print(f"[ERROR] {fix_version} {build_number}: {error}", file=sys.stderr)
        return FetchOutcome.ERROR, None

    if issue_total == 0:
        print(f"[INFO] {fix_version} {build_number}: 対応する課題が見つかりません (保存をスキップ)")
        return FetchOutcome.NOT_FOUND, None

    return FetchOutcome.SUCCESS, xml_content




def resolve_output_path(
    fix_version: str,
    build_number: str,
    output_dir: Path,
    output_subdirectory: Path,
) -> Path:
    filename = f"jdk-{fix_version}_{build_number}.xml"
    return output_dir / output_subdirectory / filename

def save_individual_xml(
    fix_version: str,
    build_number: str,
    xml_content: bytes,
    output_dir: Path,
    output_subdirectory: Path,
) -> Path:
    output_path = resolve_output_path(
        fix_version, build_number, output_dir, output_subdirectory
    )
    write_xml(xml_content, output_path)
    print(
        f"[INFO] {fix_version} {build_number}: {output_path.relative_to(Path.cwd())} に保存しました"
    )
    return output_path


def build_aggregate_xml(
    entries: Sequence[tuple[str, str, bytes]],
    target_fix_versions: Sequence[str],
) -> bytes:
    root = ET.Element(
        "resolvedInBuildCollection",
        attrib={
            "generatedAt": _dt.datetime.now(tz=_dt.timezone.utc).isoformat(),
            "targetFixVersions": ",".join(target_fix_versions),
        },
    )

    fix_versions_in_order = tuple(dict.fromkeys(fix_version for fix_version, _, _ in entries))
    if fix_versions_in_order:
        root.set("fixVersions", ",".join(fix_versions_in_order))

    for fix_version, build_number, xml_content in entries:
        container = ET.SubElement(
            root, "searchResult", attrib={"fixVersion": fix_version, "build": build_number}
        )
        rss_root = ET.fromstring(xml_content)
        container.append(rss_root)

    return ET.tostring(root, encoding="utf-8", xml_declaration=True)


def write_aggregate_xml(
    entries: Sequence[tuple[str, str, bytes]],
    output_dir: Path,
    aggregate_filename: str,
    target_fix_versions: Sequence[str],
) -> Path:
    aggregate_path = output_dir / aggregate_filename
    aggregate_content = build_aggregate_xml(entries, target_fix_versions)
    write_xml(aggregate_content, aggregate_path)
    print(f"[INFO] 統合 XML: {aggregate_path.relative_to(Path.cwd())} に保存しました")
    return aggregate_path


def collect_resolved_in_build_xml(
    targets: Iterable[tuple[str, Iterable[str]]],
    output_dir: Path,
    output_subdirectory: Path,
) -> tuple[list[tuple[str, str, bytes]], int]:
    collected: list[tuple[str, str, bytes]] = []
    failures = 0
    for fix_version, build_numbers in targets:
        for build_number in build_numbers:
            output_path = resolve_output_path(
                fix_version, build_number, output_dir, output_subdirectory
            )
            if output_path.exists():
                try:
                    xml_content = output_path.read_bytes()
                except OSError as error:
                    print(
                        f"[WARN] {fix_version} {build_number}: 既存 XML の読み込みに失敗しました ({error})",
                        file=sys.stderr,
                    )
                else:
                    print(f"[INFO] {fix_version} {build_number}: 既存 XML を再利用します")
                    collected.append((fix_version, build_number, xml_content))
                    continue

            outcome, xml_content = fetch_build_xml(fix_version, build_number)
            if outcome is FetchOutcome.ERROR:
                failures += 1
                continue
            if outcome is FetchOutcome.NOT_FOUND:
                continue
            assert xml_content is not None
            collected.append((fix_version, build_number, xml_content))
    return collected, failures


def main() -> None:
    output_dir = Path.cwd() / OUTPUT_DIRECTORY
    total_failures = 0
    any_collected = False

    for distribution in DISTRIBUTION_TARGETS:
        collected_entries, failures = collect_resolved_in_build_xml(
            distribution.targets, output_dir, distribution.output_subdirectory
        )
        total_failures += failures

        if not collected_entries:
            print(
                f"[WARN] {distribution.label}: 保存対象となる XML がありませんでした",
                file=sys.stderr,
            )
            continue

        any_collected = True
        for fix_version, build_number, xml_content in collected_entries:
            save_individual_xml(
                fix_version,
                build_number,
                xml_content,
                output_dir,
                distribution.output_subdirectory,
            )

        write_aggregate_xml(
            collected_entries,
            output_dir,
            distribution.aggregate_filename,
            distribution.fix_versions,
        )

    if not any_collected:
        print("[WARN] 保存対象となる XML がありませんでした", file=sys.stderr)
        sys.exit(1)

    if total_failures:
        print(f"[WARN] 取得に失敗したビルドが {total_failures} 件あります", file=sys.stderr)
        sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    main()
