"""OpenJDK issue ID extraction module.

対象ディレクトリ配下の XML ファイルから Issue ID を抽出し、Backport 課題は元 Issue ID のみを記録する。
個別ファイルと集約ファイルを専用ディレクトリに出力し、各ファイル内で重複排除と JDK 番号順ソートを行う。
"""
from __future__ import annotations

import re
import sys
from pathlib import Path
import xml.etree.ElementTree as ET
from typing import Iterable, Iterator, List, Sequence, Tuple

XML_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = XML_DIR / "issue_ids_output"
OUTPUT_FILENAME = "issue_ids.txt"
ISSUE_KEY_PATTERN = re.compile(r"^([A-Z]+)-(\d+)$")


def iter_xml_files(root: Path) -> Iterator[Path]:
    """対象ディレクトリ配下の XML ファイルをソート済みで列挙する。"""
    return (path for path in sorted(root.rglob("*.xml")) if path.is_file())


def extract_issue_ids_from_item(item: ET.Element, source: Path) -> List[str]:
    """単一 item 要素から出力すべき Issue ID を抽出する。"""
    issue_key_elem = item.find("key")
    if issue_key_elem is None or not (issue_key_elem.text or "").strip():
        print(f"[WARN] Issue key が存在しない item を検出: file={source}", file=sys.stdout)
        return []

    issue_key = (issue_key_elem.text or "").strip()
    issue_type_text = (item.findtext("type") or "").strip()

    if issue_type_text != "Backport":
        return [issue_key]

    collected: List[str] = []
    backport_links = item.findall("issuelinks/issuelinktype")

    for link in backport_links:
        name_text = (link.findtext("name") or "").strip()
        if name_text != "Backport":
            continue
        for inward in link.findall("inwardlinks"):
            description = (inward.get("description") or "").strip()
            if description != "backport of":
                continue
            for issue in inward.findall("issuelink/issuekey"):
                original = (issue.text or "").strip()
                if original and original not in collected:
                    collected.append(original)

    if not collected:
        print(
            f"[WARN] Backport 課題なのに元 Issue ID が見つかりません: file={source} issue={issue_key}",
            file=sys.stdout,
        )

    return collected


def extract_issue_ids(xml_path: Path) -> List[str]:
    """単一 XML ファイルから Issue ID を抽出する。"""
    try:
        tree = ET.parse(xml_path)
    except ET.ParseError as exc:
        print(f"[WARN] XML の解析に失敗しました: file={xml_path} error={exc}", file=sys.stdout)
        return []

    root = tree.getroot()
    channel = root.find("channel")
    if channel is None:
        print(f"[WARN] channel 要素が存在しません: file={xml_path}", file=sys.stdout)
        return []

    issue_ids: List[str] = []
    for item in channel.findall("item"):
        issue_ids.extend(extract_issue_ids_from_item(item, xml_path))

    return issue_ids


def issue_sort_key(issue_id: str) -> Tuple[str, int]:
    """JDK 番号順でソートするためのキーを生成する。"""
    match = ISSUE_KEY_PATTERN.match(issue_id)
    if not match:
        return (issue_id, 0)
    prefix, number = match.groups()
    return (prefix, int(number))


def normalize_issue_ids(issue_ids: Iterable[str]) -> List[str]:
    """重複排除後、JDK 番号順にソートした Issue ID を返す。"""
    unique_ids = {issue_id for issue_id in issue_ids if issue_id}
    return sorted(unique_ids, key=issue_sort_key)


def collect_issue_ids(root: Path) -> Tuple[List[Tuple[Path, List[str]]], List[str]]:
    """ディレクトリ配下の全 XML を処理し、個別結果と集約結果を得る。"""
    per_file: List[Tuple[Path, List[str]]] = []
    aggregated_set = set()
    for xml_file in iter_xml_files(root):
        issue_ids = normalize_issue_ids(extract_issue_ids(xml_file))
        per_file.append((xml_file, issue_ids))
        aggregated_set.update(issue_ids)
    aggregated = sorted(aggregated_set, key=issue_sort_key)
    return per_file, aggregated


def ensure_parent_directory(path: Path) -> None:
    """出力ファイルの親ディレクトリを作成する。"""
    path.parent.mkdir(parents=True, exist_ok=True)


def write_issue_ids(issue_ids: Sequence[str], output_path: Path) -> None:
    """抽出した Issue ID をテキストファイルに保存する。"""
    ensure_parent_directory(output_path)
    output_path.write_text("\n".join(issue_ids), encoding="utf-8")


def write_individual_outputs(results: Sequence[Tuple[Path, Sequence[str]]]) -> None:
    """専用出力ディレクトリ配下へ個別出力ファイルを作成する。"""
    for xml_path, issue_ids in results:
        relative = xml_path.relative_to(XML_DIR)
        output_path = (OUTPUT_DIR / relative).with_suffix(".txt")
        write_issue_ids(issue_ids, output_path)


def write_aggregated_output(issue_ids: Sequence[str]) -> Path:
    """集約ファイルを書き出し、パスを返す。"""
    output_path = OUTPUT_DIR / OUTPUT_FILENAME
    write_issue_ids(issue_ids, output_path)
    return output_path


def main() -> int:
    per_file_results, aggregated_issue_ids = collect_issue_ids(XML_DIR)
    write_individual_outputs(per_file_results)
    aggregated_path = write_aggregated_output(aggregated_issue_ids)
    print(f"集約ファイル出力完了: {aggregated_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
