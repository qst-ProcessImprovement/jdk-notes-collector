"""Temurin JDKリリースノートからIssue ID一覧を抽出するユーティリティ。"""
from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Sequence, Tuple
from xml.etree import ElementTree

import re
_BASE_DIR = Path(__file__).parent
_TEMURIN_DIR = _BASE_DIR / "temurin"
_OUTPUT_DIR = _BASE_DIR / "issue_ids_output"
_PER_FILE_DIR = _OUTPUT_DIR / "per_file"
_JDK_ISSUES_DIR = Path("/Users/irieryuuhei/Documents/qst-ProcessImprovement/jdk-notes-collector/Phage1/run/jdk_issues")
_TMP_DIR = _BASE_DIR / "tmp"
_AGGREGATED_FILENAME = "all_issue_ids.txt"
_ISSUE_ID_PATTERN = re.compile(r"^JDK-\d+$")


@dataclass(slots=True, frozen=True)
class ReleaseNoteEntry:
    priority: str
    issue_type: str
    issue_id: str
    summary: str
    component: str | None


def _iter_release_notes(text_path: Path) -> Iterable[ReleaseNoteEntry]:
    """temurinテキストに含まれるリリースノート項目を順に返す。"""
    if not text_path.is_file():
        raise FileNotFoundError(f"入力テキストが見つかりません: {text_path}")

    raw_lines = text_path.read_text(encoding="utf-8").splitlines()
    lines = [line.strip() for line in raw_lines if line.strip()]
    index = 0
    line_count = len(lines)

    while index < line_count:
        priority = lines[index]
        index += 1
        if not priority.startswith("P"):
            raise ValueError(f"優先度行の形式が不正です: {text_path} -> '{priority}'")

        if index >= line_count:
            raise ValueError(f"タイプ行が欠落しています: {text_path}")
        issue_type = lines[index]
        index += 1

        if index >= line_count:
            raise ValueError(f"Issue ID行が欠落しています: {text_path}")
        candidate = lines[index]
        index += 1

        if _ISSUE_ID_PATTERN.fullmatch(candidate):
            component: str | None = None
            issue_id = _require_jdk_issue_id(candidate, source_path=text_path, field_name="id")
        else:
            component = candidate
            if index >= line_count:
                raise ValueError(f"Issue ID行が欠落しています: {text_path}")
            issue_id = _require_jdk_issue_id(lines[index], source_path=text_path, field_name="id")
            index += 1

        if index >= line_count:
            raise ValueError(f"概要行が欠落しています: {text_path}:{issue_id}")
        summary = lines[index]
        index += 1

        yield ReleaseNoteEntry(
            priority=priority,
            issue_type=issue_type,
            issue_id=issue_id,
            summary=summary,
            component=component,
        )


def collect_issue_ids(
    release_path: Path,
    entries: Iterable[ReleaseNoteEntry],
    reference_backports: dict[str, str],
    missing_backport_origins: set[str],
) -> Tuple[List[str], dict[str, set[str]]]:
    """Backportの元Issue IDを含むIssue ID一覧とBackport対応表を抽出して返す。"""
    issue_ids: List[str] = []
    backport_map: dict[str, set[str]] = {}

    for entry in entries:
        if entry.issue_type == "Backport":
            try:
                backport_origin = _resolve_backport_origin(
                    entry.issue_id,
                    reference_backports,
                    release_path=release_path,
                )
            except (FileNotFoundError, ValueError):
                missing_backport_origins.add(entry.issue_id)
                continue
            backport_of = _require_jdk_issue_id(
                backport_origin,
                source_path=release_path,
                field_name="backportOf",
            )
            backport_map.setdefault(backport_of, set()).add(entry.issue_id)
            issue_ids.append(backport_of)
            continue

        backport_map.setdefault(entry.issue_id, set())
        issue_ids.append(entry.issue_id)

    return issue_ids, backport_map


def _load_reference_backports() -> dict[str, str]:
    """issue_ids_output配下からBackport -> 元Issue IDのマップを構築する。"""
    mapping: dict[str, str] = {}

    aggregate_path = _OUTPUT_DIR / _AGGREGATED_FILENAME
    if aggregate_path.is_file():
        _update_reference_mapping_from_file(mapping, aggregate_path)

    if _PER_FILE_DIR.is_dir():
        for per_file_path in sorted(_PER_FILE_DIR.glob("*.txt")):
            _update_reference_mapping_from_file(mapping, per_file_path)

    return mapping


def _update_reference_mapping_from_file(mapping: dict[str, str], source_path: Path) -> None:
    """issue_ids_outputの1ファイルからBackport情報を抽出してマップへ追記する。"""
    for raw_line in source_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line:
            continue
        parts = [part.strip() for part in line.split(",") if part.strip()]
        if not parts:
            continue
        original = _require_jdk_issue_id(parts[0], source_path=source_path, field_name="original")
        for suffix in parts[1:]:
            if not suffix.startswith("temurin_"):
                continue
            backport_id = suffix[len("temurin_") :]
            backport_issue_id = _require_jdk_issue_id(
                backport_id, source_path=source_path, field_name="backport"
            )
            existing = mapping.get(backport_issue_id)
            if existing is not None and existing != original:
                raise ValueError(
                    f"Backportの対応関係が衝突しています: {source_path}:{backport_issue_id}"
                )
            mapping[backport_issue_id] = original


def _resolve_backport_origin(
    backport_issue_id: str,
    reference_backports: dict[str, str],
    *,
    release_path: Path,
) -> str:
    """Backport Issue IDの元Issue IDを既存マップまたはjdk_issuesから取得する。"""
    origin = reference_backports.get(backport_issue_id)
    if origin is not None:
        return origin

    origin = _lookup_backport_origin_in_issue_xml(backport_issue_id)
    if origin is None:
        raise ValueError(
            f"Backport元のIssue IDをjdk_issuesから解決できません: {release_path}:{backport_issue_id}"
        )
    reference_backports[backport_issue_id] = origin
    return origin


def _lookup_backport_origin_in_issue_xml(backport_issue_id: str) -> str | None:
    """jdk_issuesディレクトリ内のXMLを解析してBackport元を取得する。"""
    issue_dir = _JDK_ISSUES_DIR / backport_issue_id
    xml_path = issue_dir / f"{backport_issue_id.lower()}.xml"
    if not xml_path.is_file():
        raise FileNotFoundError(f"Backport Issue XMLが存在しません: {xml_path}")

    try:
        tree = ElementTree.parse(xml_path)
    except ElementTree.ParseError as exc:
        raise ValueError(f"Backport Issue XMLの解析に失敗しました: {xml_path}") from exc

    root = tree.getroot()
    for link_type in root.findall(".//issuelinktype"):
        if link_type.findtext("name") != "Backport":
            continue
        for inwardlinks in link_type.findall("inwardlinks"):
            if inwardlinks.get("description") != "backport of":
                continue
            issue_key = inwardlinks.findtext("issuelink/issuekey")
            if issue_key and _ISSUE_ID_PATTERN.fullmatch(issue_key):
                return issue_key
    return None


def _sorted_unique(values: Sequence[str]) -> List[str]:
    """重複を排除しつつ辞書順ソートしたリストを返す。"""
    return sorted(set(values))


def _sorted_duplicates(values: Sequence[str]) -> List[str]:
    """複数回出現した値のみを辞書順で返す。"""
    counter = Counter(values)
    return sorted([value for value, count in counter.items() if count > 1])


def _require_jdk_issue_id(value: object, *, source_path: Path, field_name: str) -> str:
    """JDK Issue IDが正準表現か検証し、正当な値を返す。"""
    if not isinstance(value, str):
        raise ValueError(f"{source_path}:{field_name} が文字列ではありません: {value!r}")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{source_path}:{field_name} が空文字です")
    if not _ISSUE_ID_PATTERN.fullmatch(normalized):
        raise ValueError(
            f"正準表現に合致しないIssue IDを検出しました: {source_path}:{field_name} -> '{normalized}'"
        )
    return normalized


def _format_issue_line(issue_id: str, backport_ids: Iterable[str]) -> str:
    """元Issue IDにtemurin Backport IDを付与した行を生成する。"""
    suffixes = [f"temurin_{backport}" for backport in _sorted_unique(list(backport_ids))]
    if not suffixes:
        return issue_id
    return ",".join([issue_id, *suffixes])

def _canonical_output_filename(source_path: Path) -> str:
    """入力ファイル名からビルド番号サフィックスを除いた出力ファイル名を得る。"""
    stem = source_path.stem
    canonical_stem = re.sub(r"\+\d+$", "", stem)
    return f"{canonical_stem}.txt"

def _write_unique_ids(
    source_path: Path, issue_ids: Sequence[str], backport_map: dict[str, set[str]]
) -> List[str]:
    """ユニークなIssue IDをファイル別ディレクトリへ書き出し、書き出したIDを返す。"""
    _PER_FILE_DIR.mkdir(parents=True, exist_ok=True)
    output_filename = _canonical_output_filename(source_path)
    output_path = _PER_FILE_DIR / output_filename
    unique_ids = _sorted_unique(issue_ids)
    lines = [_format_issue_line(issue_id, backport_map.get(issue_id, ())) for issue_id in unique_ids]
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return unique_ids


def main() -> None:
    """temurin配下のテキストを処理し、重複IDのみを標準出力する。"""
    if not _TEMURIN_DIR.is_dir():
        raise FileNotFoundError(f"temurinディレクトリが存在しません: {_TEMURIN_DIR}")
    if not _JDK_ISSUES_DIR.is_dir():
        raise FileNotFoundError(f"jdk_issuesディレクトリが存在しません: {_JDK_ISSUES_DIR}")

    release_files = sorted(_TEMURIN_DIR.glob("*.txt"))
    if not release_files:
        raise FileNotFoundError(f"テキストファイルが見つかりません: {_TEMURIN_DIR}")

    reference_backports = _load_reference_backports()
    aggregate_ids: set[str] = set()
    aggregate_backports: dict[str, set[str]] = {}
    collected_text_issue_ids: set[str] = set()
    missing_backport_origins: set[str] = set()

    for release_path in release_files:
        entries = list(_iter_release_notes(release_path))
        if not entries:
            continue

        collected_text_issue_ids.update(entry.issue_id for entry in entries)
        issue_ids, backport_map = collect_issue_ids(
            release_path,
            entries,
            reference_backports,
            missing_backport_origins,
        )
        for original, backports in backport_map.items():
            for backport in backports:
                reference_backports.setdefault(backport, original)

        unique_ids = _write_unique_ids(release_path, issue_ids, backport_map)
        aggregate_ids.update(unique_ids)
        for issue_id in unique_ids:
            aggregate_backports.setdefault(issue_id, set())
        for issue_id, backports in backport_map.items():
            aggregate_backports.setdefault(issue_id, set()).update(backports)

        duplicate_ids = _sorted_duplicates(issue_ids)
        if duplicate_ids:
            print("duplicate ids: " + release_path.name)
            for issue_id in duplicate_ids:
                print(issue_id)
            print()

    _TMP_DIR.mkdir(parents=True, exist_ok=True)
    tmp_issue_path = _TMP_DIR / "temurin_jdk_ids.txt"
    tmp_ids = _sorted_unique(list(collected_text_issue_ids))
    tmp_issue_path.write_text("\n".join(tmp_ids) + ("\n" if tmp_ids else ""), encoding="utf-8")

    _OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    aggregate_output_path = _OUTPUT_DIR / _AGGREGATED_FILENAME
    aggregate_output = _sorted_unique(list(aggregate_ids))
    aggregate_lines = [
        _format_issue_line(issue_id, aggregate_backports.get(issue_id, ())) for issue_id in aggregate_output
    ]
    aggregate_output_path.write_text("\n".join(aggregate_lines) + "\n", encoding="utf-8")

    print(f"tmp issue ids -> {tmp_issue_path}")
    print(f"aggregate issue ids -> {aggregate_output_path}")
    print(f"per-file issue ids -> {_PER_FILE_DIR}")

    if missing_backport_origins:
        unresolved = _sorted_unique(list(missing_backport_origins))
        print("missing backport origins:")
        for issue_id in unresolved:
            print(issue_id)
        print()
        raise ValueError(
            "Backport元のIssue IDを解決できません。jdk_issuesの取得状況を確認してください: "
            + ", ".join(unresolved)
        )


if __name__ == "__main__":
    main()
