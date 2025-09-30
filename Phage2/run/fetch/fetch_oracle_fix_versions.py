"""Oracle JDK 用の特定 Fix Version 向け JIRA XML を取得するユーティリティ。"""

from __future__ import annotations

import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Iterable

# Fix Version 名は REST API (https://bugs.openjdk.org/rest/api/2/project/JDK/versions)
# で公開されている Oracle JDK 21 系の正式値のみを列挙する。
# 21.0.0〜21.0.2 の Oracle 版名称は公開されておらず、21-pool-oracle はリリース未確定の
# バックポート待機用バージョンのため対象外とする。
FIX_VERSIONS: tuple[str, ...] = (
    "21.0.3-oracle",
    "21.0.4-oracle",
    "21.0.4.0.1-oracle",
    "21.0.4.0.2-oracle",
    "21.0.5-oracle",
    "21.0.6-oracle",
    "21.0.7-oracle",
    "21.0.7.0.0.1-oracle",
    "21.0.7.0.1-oracle",
    "21.0.8-oracle",
    "21.0.8.0.1-oracle",
    "21.0.8.0.2-oracle",
)

JIRA_SEARCH_URL_TEMPLATE = (
    "https://bugs.openjdk.org/sr/jira.issueviews:searchrequest-xml/temp/"
    "SearchRequest.xml?jqlQuery=project+%3D+JDK+AND+status+in+%28Closed%2C+Resolved%29+"
    "AND+fixVersion+%3D+{fix_version}"
)

OUTPUT_DIRECTORY_NAME = "output"

REQUEST_TIMEOUT_SECONDS = 60
USER_AGENT = "jdk-notes-collector/1.0"


def build_request_url(fix_version: str) -> str:
    return JIRA_SEARCH_URL_TEMPLATE.format(fix_version=fix_version)


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


def write_xml(content: bytes, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(content)


def download_fix_version_xml(fix_version: str, output_dir: Path) -> bool:
    url = build_request_url(fix_version)
    try:
        xml_content = fetch_xml(url)
    except urllib.error.URLError as error:
        print(f"[ERROR] {fix_version}: {error}", file=sys.stderr)
        return False

    output_path = output_dir / f"{fix_version}.xml"
    write_xml(xml_content, output_path)
    print(f"[INFO] Saved {output_path.relative_to(Path.cwd())}")
    return True


def download_all_fix_versions(fix_versions: Iterable[str]) -> bool:
    output_dir = Path.cwd() / OUTPUT_DIRECTORY_NAME
    failures = 0
    for fix_version in fix_versions:
        if not download_fix_version_xml(fix_version, output_dir):
            failures += 1
    if failures:
        print(f"[WARN] Completed with {failures} failure(s)", file=sys.stderr)
    return failures == 0


def main() -> None:
    success = download_all_fix_versions(FIX_VERSIONS)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
