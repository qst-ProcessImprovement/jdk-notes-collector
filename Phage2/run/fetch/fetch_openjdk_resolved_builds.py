"""JDK 21 の "Resolved In Build" ごとの JIRA XML を収集し、個別ファイルと統合 XML を生成するスクリプト。"""

from __future__ import annotations

import datetime as _dt
import re
import sys
import time
import shutil
from collections import Counter
from dataclasses import dataclass
from enum import Enum
from functools import lru_cache
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any, Callable, Dict, Iterable, List, NamedTuple, Optional, Sequence
from xml.etree import ElementTree as ET

# 取得対象のバージョンと "Resolved in Build" の正準定義。
import json
OPENJDK_RESOLVED_BUILD_TARGETS: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("21", tuple(f"b{index:02d}" for index in range(1, 36))),
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
ORACLEJDK_RESOLVED_BUILD_TARGETS: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("21.0.3-oracle", tuple(f"b{index:02d}" for index in range(1, 7))),
    ("21.0.4-oracle", tuple(f"b{index:02d}" for index in range(1, 9))),
    ("21.0.4.0.1-oracle", ("b01",)),
    ("21.0.5-oracle", tuple(f"b{index:02d}" for index in range(1, 10))),
    ("21.0.6-oracle", tuple(f"b{index:02d}" for index in range(1, 9))),
    ("21.0.7-oracle", tuple(f"b{index:02d}" for index in range(1, 8))),
    ("21.0.7.0.1-oracle", ("b01",)),
    ("21.0.8-oracle", tuple(f"b{index:02d}" for index in range(1, 12))),
    ("21.0.8.0.1-oracle", ("b01",)),
    ("21.0.8.0.2-oracle", ("b01",)),
)
ORACLEJDK_FIX_VERSIONS: tuple[str, ...] = tuple(version for version, _ in ORACLEJDK_RESOLVED_BUILD_TARGETS)


class DistributionTarget(NamedTuple):
    label: str
    output_subdirectory: Path
    targets: tuple[tuple[str, tuple[str, ...]], ...]
    fix_versions: tuple[str, ...]
    aggregate_filename: str
    issue_ids_aggregate_filename: str


class IssueIdGenerationResult(NamedTuple):
    aggregated_path: Path
    aggregated_issue_map: dict[str, set[str]]


DISTRIBUTION_TARGETS: tuple[DistributionTarget, ...] = (
    DistributionTarget(
        "OpenJDK",
        Path("OpenJDK"),
        OPENJDK_RESOLVED_BUILD_TARGETS,
        OPENJDK_FIX_VERSIONS,
        "all_builds_openjdk.xml",
        "all_issue_ids_openjdk.txt",
    ),
    DistributionTarget(
        "OracleJDK",
        Path("OracleJDK"),
        ORACLEJDK_RESOLVED_BUILD_TARGETS,
        ORACLEJDK_FIX_VERSIONS,
        "all_builds_oraclejdk.xml",
        "all_issue_ids_oraclejdk.txt",
    ),
)


# JIRA 検索結果 XML のリクエスト URL テンプレート。
# https://bugs.openjdk.org/sr/jira.issueviews:searchrequest-xml/temp/SearchRequest.xml?jqlQuery=project+%3D+JDK+AND+fixVersion+%3D+{fix_version}+AND+resolution+%3D+Fixed+AND+%22resolved+in+build%22+%3D+{build_number}
ISSUE_KEY_PATTERN = re.compile(r"^([A-Z]+)-(\d+)$")
XML_OUTPUT_ROOT = Path("builds") / "xml"
ISSUE_IDS_OUTPUT_ROOT = Path("builds") / "issue_ids"

TEMURIN_INPUT_ROOT = Path("INPUT") / "temurin"
TEMURIN_PER_FILE_SUBDIRECTORY = Path("temurin") / "per_file"
TEMURIN_TMP_SUBDIRECTORY = Path("temurin") / "tmp"
TEMURIN_AGGREGATED_FILENAME = "all_issue_ids_temurin.txt"
TEMURIN_TMP_FILENAME = "temurin_jdk_ids.txt"
TEMURIN_BACKOUT_TMP_FILENAME = "temurin_backout_excluded_ids.txt"
TEMURIN_BACKOUT_MARKER_PATTERN = re.compile(r"\[BACKOUT\]", re.IGNORECASE)
TEMURIN_BACKOUT_JDK_ID_PATTERN = re.compile(r"JDK-(\d+)", re.IGNORECASE)
TEMURIN_BACKOUT_NUMERIC_ID_PATTERN = re.compile(r"\b(\d{6,})\b")
TEMURIN_REDO_MARKER_PATTERN = re.compile(r"\[REDO\]", re.IGNORECASE)
TEMURIN_ISSUE_ID_PATTERN = re.compile(r"^JDK-\d+$")

JDK_ISSUE_ID_PATTERN = TEMURIN_ISSUE_ID_PATTERN
TEMURIN_JDK_ISSUES_DIR = Path(
    "/Users/irieryuuhei/Documents/qst-ProcessImprovement/jdk-notes-collector/Phage1/run/jdk_issues"
)



class JDKDiffProductSpec(NamedTuple):
    name: str
    backport_prefix: str
    aggregate_filename: str


JDK_DIFF_OUTPUT_FILENAME = "jdk_diff_report.md"
JDK_DIFF_PRODUCT_SPECS: tuple[JDKDiffProductSpec, ...] = (
    JDKDiffProductSpec("OpenJDK", "openjdk", "all_issue_ids_openjdk.txt"),
    JDKDiffProductSpec("OracleJDK", "oraclejdk", "all_issue_ids_oraclejdk.txt"),
    JDKDiffProductSpec("Temurin", "temurin", TEMURIN_AGGREGATED_FILENAME),
)


class JDKDiffError(Exception):
    """JDK 差分レポート生成時の例外。"""

@dataclass(slots=True, frozen=True)
class TemurinReleaseNoteEntry:
    issue_id: str
    issue_type: str | None
    priority: str | None
    title: str
    component: str | None
    backport_of: str | None
    backout_targets: tuple[str, ...]
    redo_targets: tuple[str, ...]




def iter_temurin_release_notes(
    release: dict[str, object],
    *,
    aggregated_path: Path,
    release_name: str,
) -> Iterable[TemurinReleaseNoteEntry]:
    """Temurin の単一JSON内のリリース定義から項目を抽出する。"""
    source_label = f"{aggregated_path}:{release_name}"

    release_notes = release.get("release_notes")
    if not isinstance(release_notes, list):
        raise ValueError(f"release_notes が配列ではありません: {source_label}")

    for index, raw_entry in enumerate(release_notes, start=1):
        if not isinstance(raw_entry, dict):
            raise ValueError(
                f"release_notes[{index}] がオブジェクトではありません: {source_label}"
            )

        issue_id = require_temurin_jdk_issue_id(
            raw_entry.get("id"),
            source_path=source_label,
            field_name=f"release_notes[{index}].id",
        )

        issue_type_raw = raw_entry.get("type")
        if issue_type_raw is None:
            issue_type: str | None = None
        elif isinstance(issue_type_raw, str):
            normalized_type = issue_type_raw.strip()
            issue_type = normalized_type or None
        else:
            raise ValueError(
                f"type が文字列ではありません: {source_label}:release_notes[{index}].type"
            )

        priority_raw = raw_entry.get("priority")
        if priority_raw is None:
            priority: str | None = None
        elif isinstance(priority_raw, str):
            normalized_priority = priority_raw.strip()
            priority = normalized_priority or None
        else:
            raise ValueError(
                f"priority が文字列ではありません: {source_label}:release_notes[{index}].priority"
            )

        title_raw = raw_entry.get("title")
        if not isinstance(title_raw, str):
            raise ValueError(
                f"title が文字列ではありません: {source_label}:release_notes[{index}].title"
            )
        title = title_raw.strip()
        if not title:
            raise ValueError(
                f"title が空文字です: {source_label}:release_notes[{index}].title"
            )

        component_raw = raw_entry.get("component")
        if component_raw is None:
            component: str | None = None
        elif isinstance(component_raw, str):
            normalized_component = component_raw.strip()
            component = normalized_component or None
        else:
            raise ValueError(
                f"component が文字列ではありません: {source_label}:release_notes[{index}].component"
            )

        backport_of_raw = raw_entry.get("backportOf")
        if backport_of_raw is None:
            backport_of: str | None = None
        else:
            backport_of = require_temurin_jdk_issue_id(
                backport_of_raw,
                source_path=source_label,
                field_name=f"release_notes[{index}].backportOf",
            )

        backout_targets = extract_temurin_backout_targets(title)
        redo_targets = extract_temurin_redo_targets(title)

        yield TemurinReleaseNoteEntry(
            issue_id=issue_id,
            issue_type=issue_type,
            priority=priority,
            title=title,
            component=component,
            backport_of=backport_of,
            backout_targets=backout_targets,
            redo_targets=redo_targets,
        )


def require_temurin_jdk_issue_id(
    value: object, *, source_path: Path | str, field_name: str
) -> str:
    """JDK Issue ID の正準表現を検証し、正当な値を返す。"""
    if not isinstance(value, str):
        raise ValueError(f"{source_path}:{field_name} が文字列ではありません: {value!r}")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{source_path}:{field_name} が空文字です")
    if not TEMURIN_ISSUE_ID_PATTERN.fullmatch(normalized):
        raise ValueError(
            f"正準表現に合致しないIssue IDを検出しました: {source_path}:{field_name} -> '{normalized}'"
        )
    return normalized

def extract_temurin_backout_targets(title: str) -> tuple[str, ...]:
    """BACKOUT タイトルから除外対象の JDK 番号を抽出する。"""
    match = TEMURIN_BACKOUT_MARKER_PATTERN.search(title)
    if match is None:
        return ()

    tail = title[match.end() :]
    targets: set[str] = set()

    for jdk_match in TEMURIN_BACKOUT_JDK_ID_PATTERN.finditer(tail):
        targets.add(f"JDK-{jdk_match.group(1)}")

    if not targets:
        for numeric_match in TEMURIN_BACKOUT_NUMERIC_ID_PATTERN.finditer(tail):
            targets.add(f"JDK-{numeric_match.group(1)}")

    if not targets:
        return ()

    return tuple(sorted(targets, key=lambda item: int(item.split("-", maxsplit=1)[1])))


def extract_temurin_redo_targets(title: str) -> tuple[str, ...]:
    """[REDO] タイトルから再適用対象の JDK 番号を抽出する。"""
    match = TEMURIN_REDO_MARKER_PATTERN.search(title)
    if match is None:
        return ()

    tail = title[match.end() :]
    targets: set[str] = set()

    for jdk_match in TEMURIN_BACKOUT_JDK_ID_PATTERN.finditer(tail):
        targets.add(f"JDK-{jdk_match.group(1)}")

    if not targets:
        for numeric_match in TEMURIN_BACKOUT_NUMERIC_ID_PATTERN.finditer(tail):
            targets.add(f"JDK-{numeric_match.group(1)}")

    if not targets:
        return ()

    return tuple(sorted(targets, key=lambda item: int(item.split("-", maxsplit=1)[1])))


def lookup_temurin_backport_origin_in_issue_xml(
    backport_issue_id: str, jdk_issues_dir: Path
) -> str | None:
    """jdk_issues ディレクトリ内の XML を解析して Backport 元を取得する。"""
    issue_dir = jdk_issues_dir / backport_issue_id
    xml_path = issue_dir / f"{backport_issue_id.lower()}.xml"
    if not xml_path.is_file():
        raise FileNotFoundError(f"Backport Issue XMLが存在しません: {xml_path}")

    try:
        tree = ET.parse(xml_path)
    except ET.ParseError as exc:
        raise ValueError(f"Backport Issue XMLの解析に失敗しました: {xml_path}") from exc

    root = tree.getroot()
    for link_type in root.findall(".//issuelinktype"):
        if link_type.findtext("name") != "Backport":
            continue
        for inwardlinks in link_type.findall("inwardlinks"):
            if inwardlinks.get("description") != "backport of":
                continue
            issue_key = inwardlinks.findtext("issuelink/issuekey")
            if issue_key and TEMURIN_ISSUE_ID_PATTERN.fullmatch(issue_key):
                return issue_key
    return None


def resolve_temurin_backport_origin(
    backport_issue_id: str,
    reference_backports: dict[str, str],
    *,
    release_label: str,
    jdk_issues_dir: Path,
) -> str:
    """Backport Issue ID の元 Issue ID を既存マップまたは jdk_issues から取得する。"""
    origin = reference_backports.get(backport_issue_id)
    if origin is not None:
        return origin

    origin = lookup_temurin_backport_origin_in_issue_xml(backport_issue_id, jdk_issues_dir)
    if origin is None:
        raise ValueError(
            f"Backport元のIssue IDをjdk_issuesから解決できません: {release_label}:{backport_issue_id}"
        )
    reference_backports[backport_issue_id] = origin
    return origin


def update_temurin_reference_mapping_from_file(
    mapping: dict[str, str], source_path: Path
) -> None:
    """既存の Issue ID 出力ファイルから Backport 情報を読み込む。"""
    for raw_line in source_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line:
            continue
        parts = [part.strip() for part in line.split(",") if part.strip()]
        if not parts:
            continue
        original = require_temurin_jdk_issue_id(
            parts[0], source_path=source_path, field_name="original"
        )
        for suffix in parts[1:]:
            if not suffix.startswith("temurin_"):
                continue
            backport_id = suffix[len("temurin_") :]
            backport_issue_id = require_temurin_jdk_issue_id(
                backport_id, source_path=source_path, field_name="backport"
            )
            existing = mapping.get(backport_issue_id)
            if existing is not None and existing != original:
                raise ValueError(
                    f"Backportの対応関係が衝突しています: {source_path}:{backport_issue_id}"
                )
            mapping[backport_issue_id] = original


def load_temurin_reference_backports(issue_output_root: Path) -> dict[str, str]:
    """過去の Temurin 出力から Backport -> 元 Issue ID マップを組み立てる。"""
    mapping: dict[str, str] = {}
    aggregate_path = issue_output_root / TEMURIN_AGGREGATED_FILENAME
    if aggregate_path.is_file():
        update_temurin_reference_mapping_from_file(mapping, aggregate_path)

    per_file_dir = issue_output_root / TEMURIN_PER_FILE_SUBDIRECTORY
    if per_file_dir.is_dir():
        for per_file_path in sorted(per_file_dir.glob("*.txt")):
            update_temurin_reference_mapping_from_file(mapping, per_file_path)

    return mapping


def collect_temurin_issue_ids(
    release_label: str,
    entries: Iterable[TemurinReleaseNoteEntry],
    reference_backports: dict[str, str],
    missing_backport_origins: set[str],
    jdk_issues_dir: Path,
) -> tuple[list[str], dict[str, set[str]], set[str]]:
    """Backport の元 Issue ID を含む Issue ID 一覧と Backport 対応表、BACKOUT 指定による除外一覧を返す。"""
    issue_ids: list[str] = []
    backport_map: dict[str, set[str]] = {}
    excluded_issue_ids: set[str] = set()

    for entry in entries:
        if entry.redo_targets:
            excluded_issue_ids.difference_update(entry.redo_targets)

        if entry.backout_targets:
            excluded_issue_ids.update(entry.backout_targets)
            continue

        if entry.issue_type == "Backport":
            if entry.redo_targets:
                for target in entry.redo_targets:
                    excluded_issue_ids.discard(target)
                    backport_map.setdefault(target, set()).add(entry.issue_id)
                    issue_ids.append(target)
                    reference_backports.setdefault(entry.issue_id, target)
                continue

            backport_origin: str | None
            if entry.backport_of is not None:
                backport_origin = entry.backport_of
            else:
                try:
                    backport_origin = resolve_temurin_backport_origin(
                        entry.issue_id,
                        reference_backports,
                        release_label=release_label,
                        jdk_issues_dir=jdk_issues_dir,
                    )
                except (FileNotFoundError, ValueError):
                    missing_backport_origins.add(entry.issue_id)
                    continue

            excluded_issue_ids.discard(backport_origin)
            backport_map.setdefault(backport_origin, set()).add(entry.issue_id)
            issue_ids.append(backport_origin)
            reference_backports.setdefault(entry.issue_id, backport_origin)
            continue

        excluded_issue_ids.discard(entry.issue_id)
        backport_map.setdefault(entry.issue_id, set())
        issue_ids.append(entry.issue_id)

    if excluded_issue_ids:
        issue_ids = [issue_id for issue_id in issue_ids if issue_id not in excluded_issue_ids]
        for issue_id in excluded_issue_ids:
            backport_map.pop(issue_id, None)

    return issue_ids, backport_map, excluded_issue_ids


def temurin_sorted_unique(values: Iterable[str]) -> list[str]:
    """重複を排除しつつ辞書順ソートしたリストを返す。"""
    return sorted(set(values))


def temurin_sorted_duplicates(values: Iterable[str]) -> list[str]:
    """複数回出現した値のみを辞書順で返す。"""
    counter = Counter(values)
    return sorted([value for value, count in counter.items() if count > 1])


def format_temurin_issue_line(issue_id: str, backport_ids: Iterable[str]) -> str:
    """元 Issue ID に temurin Backport ID を付与した行を生成する。"""
    suffixes = [f"temurin_{backport}" for backport in temurin_sorted_unique(backport_ids)]
    if not suffixes:
        return issue_id
    return ",".join([issue_id, *suffixes])


def temurin_canonical_output_filename(source_identifier: str | Path) -> str:
    """入力識別子からビルド番号サフィックスを除いた出力ファイル名を得る。"""
    if isinstance(source_identifier, Path):
        stem = source_identifier.stem
    else:
        stem = source_identifier
    stem = stem.split("/")[-1]
    if stem.endswith(".json"):
        stem = stem[:-5]
    canonical_stem = re.sub(r"\+\d+$", "", stem)
    return f"{canonical_stem}.txt"


def write_temurin_unique_ids(
    per_file_dir: Path,
    release_name: str,
    issue_ids: Iterable[str],
    backport_map: dict[str, set[str]],
) -> list[str]:
    """ユニークな Issue ID を Temurin 用ディレクトリへ書き出し、書き出した ID を返す。"""
    per_file_dir.mkdir(parents=True, exist_ok=True)
    output_filename = temurin_canonical_output_filename(release_name)
    output_path = per_file_dir / output_filename
    unique_ids = temurin_sorted_unique(issue_ids)
    lines = [
        format_temurin_issue_line(issue_id, backport_map.get(issue_id, ())) for issue_id in unique_ids
    ]
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return unique_ids


def generate_temurin_issue_outputs(
    input_root: Path,
    issue_output_root: Path,
    jdk_issues_dir: Path,
) -> Path:
    """Temurin リリースノート集約ファイルから Issue ID 集約ファイルを生成する。"""
    if not jdk_issues_dir.is_dir():
        raise FileNotFoundError(f"jdk_issuesディレクトリが存在しません: {jdk_issues_dir}")

    aggregated_path: Path | None = None
    if input_root.is_file():
        aggregated_path = input_root
    elif input_root.is_dir():
        candidate = input_root / "temurin_releases.json"
        if candidate.is_file():
            aggregated_path = candidate
        else:
            nested = input_root / "json" / "temurin_releases.json"
            if nested.is_file():
                aggregated_path = nested
    if aggregated_path is None:
        raise FileNotFoundError(
            f"temurinリリースノート集約ファイルが見つかりません: {input_root}"
        )

    try:
        aggregated_data = json.loads(aggregated_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"Temurin集約JSONの解析に失敗しました: {aggregated_path}") from exc

    releases = aggregated_data.get("releases")
    if not isinstance(releases, list) or not releases:
        raise ValueError(f"releases が空、または配列ではありません: {aggregated_path}")

    reference_backports = load_temurin_reference_backports(issue_output_root)
    temurin_per_file_dir = issue_output_root / TEMURIN_PER_FILE_SUBDIRECTORY
    temurin_tmp_dir = issue_output_root / TEMURIN_TMP_SUBDIRECTORY
    aggregate_ids: set[str] = set()
    aggregate_backports: dict[str, set[str]] = {}
    collected_text_issue_ids: set[str] = set()
    missing_backport_origins: set[str] = set()
    excluded_backout_issue_ids: set[str] = set()

    for release in releases:
        if not isinstance(release, dict):
            raise ValueError(f"不正なリリース定義を検出しました: {aggregated_path}")
        release_name = release.get("release_name")
        if not isinstance(release_name, str) or not release_name.strip():
            raise ValueError(
                f"release_name が不正です: {aggregated_path} -> {release.get('release_name')!r}"
            )
        release_name = release_name.strip()
        release_label = f"{aggregated_path}:{release_name}"

        entries = list(
            iter_temurin_release_notes(
                release,
                aggregated_path=aggregated_path,
                release_name=release_name,
            )
        )
        if not entries:
            continue

        collected_text_issue_ids.update(entry.issue_id for entry in entries)
        issue_ids, backport_map, excluded_ids = collect_temurin_issue_ids(
            release_label,
            entries,
            reference_backports,
            missing_backport_origins,
            jdk_issues_dir,
        )
        excluded_backout_issue_ids.update(excluded_ids)

        for original, backports in backport_map.items():
            for backport in backports:
                reference_backports.setdefault(backport, original)

        unique_ids = write_temurin_unique_ids(
            temurin_per_file_dir,
            release_name,
            issue_ids,
            backport_map,
        )
        aggregate_ids.update(unique_ids)
        for issue_id in unique_ids:
            aggregate_backports.setdefault(issue_id, set())
        for issue_id, backports in backport_map.items():
            aggregate_backports.setdefault(issue_id, set()).update(backports)

        duplicate_ids = temurin_sorted_duplicates(issue_ids)
        if duplicate_ids:
            print(f"[INFO] Temurin duplicate ids: {release_name}")
            for issue_id in duplicate_ids:
                print(f"  {issue_id}")

    temurin_tmp_dir.mkdir(parents=True, exist_ok=True)
    tmp_issue_path = temurin_tmp_dir / TEMURIN_TMP_FILENAME
    tmp_ids = temurin_sorted_unique(collected_text_issue_ids)
    tmp_issue_path.write_text(
        "\n".join(tmp_ids) + ("\n" if tmp_ids else ""), encoding="utf-8"
    )

    effective_excluded = {
        issue_id for issue_id in excluded_backout_issue_ids if issue_id not in aggregate_ids
    }
    backout_issue_path = temurin_tmp_dir / TEMURIN_BACKOUT_TMP_FILENAME
    sorted_backout_ids = (
        sorted(effective_excluded, key=issue_sort_key) if effective_excluded else []
    )
    backout_issue_path.write_text(
        "\n".join(sorted_backout_ids) + ("\n" if sorted_backout_ids else ""),
        encoding="utf-8",
    )

    if effective_excluded:
        aggregate_ids.difference_update(effective_excluded)
        for issue_id in effective_excluded:
            aggregate_backports.pop(issue_id, None)

    issue_output_root.mkdir(parents=True, exist_ok=True)
    aggregate_output_path = issue_output_root / TEMURIN_AGGREGATED_FILENAME
    aggregate_output = temurin_sorted_unique(aggregate_ids)
    aggregate_lines = [
        format_temurin_issue_line(
            issue_id,
            aggregate_backports.get(issue_id, ()),
        )
        for issue_id in aggregate_output
    ]
    aggregate_output_path.write_text(
        "\n".join(aggregate_lines) + ("\n" if aggregate_lines else ""),
        encoding="utf-8",
    )

    def resolve_display_path(path: Path) -> Path:
        return path if not path.is_absolute() else path.relative_to(Path.cwd())

    tmp_issue_display = resolve_display_path(tmp_issue_path)
    backout_issue_display = resolve_display_path(backout_issue_path)
    aggregate_output_display = resolve_display_path(aggregate_output_path)
    per_file_display = resolve_display_path(temurin_per_file_dir)

    print(f"[INFO] Temurin tmp issue ids -> {tmp_issue_display}")
    print(f"[INFO] Temurin BACKOUT excluded ids -> {backout_issue_display}")
    print(f"[INFO] Temurin aggregate issue ids -> {aggregate_output_display}")
    print(f"[INFO] Temurin per-file issue ids -> {per_file_display}")

    if missing_backport_origins:
        unresolved = temurin_sorted_unique(missing_backport_origins)
        print("[INFO] Temurin missing backport origins:")
        for issue_id in unresolved:
            print(f"  {issue_id}")
        raise ValueError(
            "Backport元のIssue IDを解決できません。jdk_issuesの取得状況を確認してください: "
            + ", ".join(unresolved)
        )

    return aggregate_output_path

def iter_issue_xml_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for path in sorted(root.rglob("*.xml")):
        if path.is_file():
            files.append(path)
    return files


def extract_issue_pairs_from_item(item: ET.Element, source: Path) -> list[tuple[str, Optional[str]]]:
    issue_key_elem = item.find("key")
    if issue_key_elem is None or not (issue_key_elem.text or "").strip():
        print(f"[WARN] Issue key が存在しない item を検出: file={source}", file=sys.stdout)
        return []

    issue_key = (issue_key_elem.text or "").strip()
    issue_type_text = (item.findtext("type") or "").strip()

    if issue_type_text != "Backport":
        return [(issue_key, None)]

    collected: list[str] = []
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

    return [(original, issue_key) for original in collected]


def extract_issue_pairs_from_xml_content(
    xml_content: bytes, source: Path
) -> list[tuple[str, Optional[str]]]:
    try:
        root = ET.fromstring(xml_content)
    except ET.ParseError as error:
        print(f"[WARN] XML の解析に失敗しました: file={source} error={error}", file=sys.stdout)
        return []

    channel = root.find("channel")
    if channel is None:
        print(f"[WARN] channel 要素が存在しません: file={source}", file=sys.stdout)
        return []

    issue_pairs: list[tuple[str, Optional[str]]] = []
    for item in channel.findall("item"):
        issue_pairs.extend(extract_issue_pairs_from_item(item, source))

    return issue_pairs


def extract_issue_pairs_from_xml_file(xml_path: Path) -> list[tuple[str, Optional[str]]]:
    try:
        xml_content = xml_path.read_bytes()
    except OSError as error:
        print(f"[WARN] XML の読み込みに失敗しました: file={xml_path} error={error}", file=sys.stdout)
        return []
    return extract_issue_pairs_from_xml_content(xml_content, xml_path)


def build_issue_backport_map(
    issue_pairs: Iterable[tuple[str, Optional[str]]]
) -> dict[str, set[str]]:
    issue_map: dict[str, set[str]] = {}
    for original_issue, backport_issue in issue_pairs:
        backports = issue_map.setdefault(original_issue, set())
        if backport_issue:
            backports.add(backport_issue)
    return issue_map


def issue_sort_key(issue_id: str) -> tuple[str, int]:
    match = ISSUE_KEY_PATTERN.match(issue_id)
    if not match:
        return (issue_id, 0)
    prefix, number = match.groups()
    return (prefix, int(number))


def collect_issue_ids_from_directory(
    root: Path,
) -> tuple[list[tuple[Path, dict[str, set[str]]]], dict[str, set[str]]]:
    per_file: list[tuple[Path, dict[str, set[str]]]] = []
    aggregated: dict[str, set[str]] = {}
    for xml_file in iter_issue_xml_files(root):
        issue_map = build_issue_backport_map(extract_issue_pairs_from_xml_file(xml_file))
        per_file.append((xml_file, issue_map))
        for original_issue, backports in issue_map.items():
            aggregated.setdefault(original_issue, set()).update(backports)
    return per_file, aggregated


def format_issue_lines(issue_map: dict[str, set[str]]) -> list[str]:
    formatted: list[str] = []
    for issue_id in sorted(issue_map, key=issue_sort_key):
        backports = issue_map[issue_id]
        if backports:
            decorated = [bp for bp in sorted(backports, key=issue_sort_key)]
            formatted.append(",".join([issue_id, *decorated]))
        else:
            formatted.append(issue_id)
    return formatted


def write_issue_lines(lines: Sequence[str], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines), encoding="utf-8")


def generate_issue_id_outputs(
    xml_root: Path,
    issue_output_root: Path,
    aggregate_filename: str,
    distribution_subdirectory: Path,
    supplemental_issue_maps: Optional[Sequence[dict[str, set[str]]]] = None,
) -> IssueIdGenerationResult:
    per_file_results, aggregated_issue_map = collect_issue_ids_from_directory(xml_root)
    distribution_issue_root = issue_output_root / distribution_subdirectory

    for xml_path, issue_map in per_file_results:
        relative = xml_path.relative_to(xml_root)
        output_path = (distribution_issue_root / relative).with_suffix(".txt")
        write_issue_lines(format_issue_lines(issue_map), output_path)

    merged_aggregated_map: dict[str, set[str]] = {
        issue_id: set(backports) for issue_id, backports in aggregated_issue_map.items()
    }
    if supplemental_issue_maps:
        counts = [len(supplemental) for supplemental in supplemental_issue_maps]
        print(
            f"[DEBUG] generate_issue_id_outputs: base_count={len(aggregated_issue_map)} supplemental_counts={counts}"
        )
        for supplemental in supplemental_issue_maps:
            for issue_id, backports in supplemental.items():
                merged_aggregated_map.setdefault(issue_id, set()).update(backports)

    aggregated_path = issue_output_root / aggregate_filename
    write_issue_lines(format_issue_lines(merged_aggregated_map), aggregated_path)
    return IssueIdGenerationResult(aggregated_path=aggregated_path, aggregated_issue_map=merged_aggregated_map)


def ensure_jdk_issue_id(value: str, *, source_path: Path, lineno: int) -> str:
    """JDK 課題 ID の正準表現 (JDK-<digits>) を検証する。"""
    normalized = value.strip()
    if not normalized:
        raise JDKDiffError(f"空の JDK 番号を検出しました: {source_path}:{lineno}")
    if not JDK_ISSUE_ID_PATTERN.fullmatch(normalized):
        raise JDKDiffError(
            f"正準表現に反する JDK 番号を検出しました: {source_path}:{lineno} -> '{normalized}'"
        )
    return normalized


def load_issue_ids(
    path: Path,
    *,
    product_name: str,
    backport_prefix: str,
) -> tuple[set[str], Dict[str, Dict[str, List[str]]]]:
    """集約 issue_ids ファイルを読み込み、JDK 番号と backport 情報を返す。"""
    if not path.is_file():
        raise JDKDiffError(f"JDK 番号リストが見つかりません: {path}")

    issue_ids: set[str] = set()
    backport_entries: Dict[str, Dict[str, List[str]]] = {}
    with path.open(encoding="utf-8") as handle:
        for lineno, raw_line in enumerate(handle, start=1):
            entry = raw_line.strip()
            if not entry:
                continue

            segments = [segment.strip() for segment in entry.split(",")]
            if not segments:
                continue

            base_issue = ensure_jdk_issue_id(segments[0], source_path=path, lineno=lineno)
            if base_issue in issue_ids:
                raise JDKDiffError(
                    f"同一 JDK 番号が重複しています: {path}:{lineno} -> '{base_issue}'"
                )
            issue_ids.add(base_issue)

            for raw_backport in segments[1:]:
                if not raw_backport:
                    raise JDKDiffError(
                        f"正準表現に反する backport 指定を検出しました: {path}:{lineno}"
                    )

                if raw_backport.startswith(f"{backport_prefix}_"):
                    backport_issue = raw_backport[len(backport_prefix) + 1 :]
                elif "_" in raw_backport:
                    prefix, suffix = raw_backport.split("_", 1)
                    if prefix != backport_prefix:
                        raise JDKDiffError(
                            f"未知の backport 接頭辞を検出しました: {path}:{lineno} -> '{prefix}'"
                        )
                    backport_issue = suffix
                else:
                    if product_name == "Temurin":
                        raise JDKDiffError(
                            f"Temurin backport には接頭辞 {backport_prefix}_ が必要です: {path}:{lineno}"
                        )
                    backport_issue = raw_backport

                backport_id = ensure_jdk_issue_id(
                    backport_issue, source_path=path, lineno=lineno
                )
                per_issue = backport_entries.setdefault(base_issue, {})
                backport_list = per_issue.setdefault(product_name, [])
                if backport_id not in backport_list:
                    backport_list.append(backport_id)

    return issue_ids, backport_entries


def make_fix_version_loader(jdk_issues_dir: Path) -> Callable[[str], tuple[str, ...]]:
    """Fix Version/s をロードする関数を生成する。"""
    if not jdk_issues_dir.is_dir():
        raise JDKDiffError(
            f"Fix Version 情報ディレクトリが見つかりません: {jdk_issues_dir}"
        )

    @lru_cache(maxsize=None)
    def load(issue_id: str) -> tuple[str, ...]:
        issue_dir = jdk_issues_dir / issue_id
        if not issue_dir.is_dir():
            raise JDKDiffError(
                f"Fix Version 情報ディレクトリが見つかりません: {issue_dir}"
            )
        xml_path = (issue_dir / issue_id.lower()).with_suffix(".xml")
        if not xml_path.is_file():
            raise JDKDiffError(f"Fix Version 情報が見つかりません: {xml_path}")
        try:
            tree = ET.parse(xml_path)
        except ET.ParseError as error:
            raise JDKDiffError(
                f"Fix Version XML の解析に失敗しました: {xml_path}"
            ) from error

        seen: set[str] = set()
        versions: List[str] = []
        for element in tree.iterfind(".//fixVersion"):
            value = (element.text or "").strip()
            if not value:
                continue
            if value not in seen:
                seen.add(value)
                versions.append(value)

        if not versions:
            raise JDKDiffError(f"Fix Version/s を取得できません: {xml_path}")

        return tuple(versions)

    return load


def sort_jdk_ids(issue_ids: Iterable[str]) -> List[str]:
    """JDK 番号を数値順にソートする。"""
    def numeric_key(item: str) -> int:
        try:
            return int(item.split("-", maxsplit=1)[1])
        except (IndexError, ValueError) as error:
            raise JDKDiffError(f"JDK 番号の解析に失敗しました: '{item}'") from error

    return sorted(issue_ids, key=numeric_key)


def render_table(headers: Sequence[str], rows: Sequence[Sequence[str]]) -> str:
    """Markdown テーブル文字列を生成する。"""
    if not rows:
        return "(なし)"

    numbered_headers = ["No.", *headers]
    numbered_rows: List[List[object]] = []
    for index, row in enumerate(rows, start=1):
        numbered_rows.append([index, *row])

    def format_row(cells: Sequence[str]) -> str:
        return "| " + " | ".join(str(cell) for cell in cells) + " |"

    header_line = format_row(numbered_headers)
    separator_line = "| " + " | ".join("---" for _ in numbered_headers) + " |"
    lines = [header_line, separator_line]
    for row in numbered_rows:
        lines.append(format_row(row))
    return "\n".join(lines)


def build_diff_table(
    data: Dict[str, set[str]],
    backport_lookup: Dict[str, Dict[str, List[str]]],
    fix_version_loader: Callable[[str], tuple[str, ...]],
) -> tuple[List[List[str]], List[List[str]], int, int, int]:
    """差分テーブル行と統計値を生成する。"""
    if not data:
        return [], [], 0, 0, 0

    product_order = list(data.keys())
    all_ids = set.union(*data.values())
    common_ids = set.intersection(*data.values())
    diff_ids = sort_jdk_ids(all_ids - common_ids)

    rows: List[List[str]] = []
    missing_issue_rows: List[List[str]] = []
    temurin_index = product_order.index("Temurin") if "Temurin" in product_order else None
    non_21_count = 0
    for issue_id in diff_ids:
        presence = ["Y" if issue_id in data[product] else "N" for product in product_order]
        try:
            fix_versions = list(fix_version_loader(issue_id))
            has_non_21 = any(value != "21" for value in fix_versions)
        except JDKDiffError:
            fix_versions = ["Issueページなし"]
            has_non_21 = False
        if has_non_21:
            non_21_count += 1
        formatted_fix_versions = ", ".join(fix_versions)
        per_issue_backports = backport_lookup.get(issue_id, {})
        backport_values: List[str] = []
        for product in product_order:
            issues = per_issue_backports.get(product)
            backport_values.append(", ".join(issues) if issues else "")
        row = [issue_id, *presence, formatted_fix_versions, *backport_values]
        if (
            formatted_fix_versions == "Issueページなし"
            and temurin_index is not None
            and presence[temurin_index] == "Y"
        ):
            unknown_presence = [
                "不明" if product != "Temurin" else presence[temurin_index]
                for product in product_order
            ]
            missing_issue_rows.append(
                [issue_id, *unknown_presence, formatted_fix_versions, *backport_values]
            )
            continue
        rows.append(row)

    return rows, missing_issue_rows, len(diff_ids), len(common_ids), non_21_count


def generate_jdk_diff_report(
    issue_output_root: Path,
    output_dir: Path,
    jdk_issues_dir: Path,
) -> Path:
    """集約済み issue_ids を比較し、差分レポートを生成する。"""
    product_data: Dict[str, set[str]] = {}
    backport_lookup: Dict[str, Dict[str, List[str]]] = {}

    for spec in JDK_DIFF_PRODUCT_SPECS:
        source_path = issue_output_root / spec.aggregate_filename
        issue_ids, backports = load_issue_ids(
            source_path, product_name=spec.name, backport_prefix=spec.backport_prefix
        )
        product_data[spec.name] = issue_ids
        for base_issue, per_product_backports in backports.items():
            target = backport_lookup.setdefault(base_issue, {})
            for product, issues in per_product_backports.items():
                target_list = target.setdefault(product, [])
                for issue in issues:
                    if issue not in target_list:
                        target_list.append(issue)

    fix_version_loader = make_fix_version_loader(jdk_issues_dir)
    rows, missing_issue_rows, diff_count, matched_count, non_21_count = build_diff_table(
        product_data, backport_lookup, fix_version_loader
    )
    missing_issue_count = len(missing_issue_rows)
    diff_only_count = diff_count - missing_issue_count
    backport_headers = [f"JDK - {product} backport" for product in product_data.keys()]
    headers = ["JDK", *product_data.keys(), "Fix Version/s", *backport_headers]
    table_text = render_table(headers, rows)

    output_lines = [
        "このファイルは OpenJDK・OracleJDK・Temurin の issue_ids.txt を比較し、三製品で一致しない JDK 番号と各 Fix Version/s を一覧化したものです。",
        "",
        table_text,
        "",
    ]

    if missing_issue_rows:
        output_lines.extend(
            [
                "Temurin に含まれるが Fix Version/s を取得できなかった JDK の一覧 (Issueページなし)",
                "",
                render_table(headers, missing_issue_rows),
                "",
            ]
        )

    output_lines.extend(
        [
            f"全てのプロダクトで一致したJDK件数: {matched_count}  ",
            f"プロダクトごとに差分のあるJDK件数: {diff_only_count}  ",
            f"Fix Version/sが21以外のJDK件数: {non_21_count}  ",
            f"Issueページが存在しないJDK件数: {missing_issue_count}  ",
            "",
        ]
    )

    output_path = output_dir / JDK_DIFF_OUTPUT_FILENAME
    output_path.write_text("\n".join(output_lines), encoding="utf-8")
    return output_path
JIRA_SEARCH_URL_TEMPLATE = (
    "https://bugs.openjdk.org/sr/jira.issueviews:searchrequest-xml/temp/SearchRequest.xml"
    "?jqlQuery=project+%3D+JDK+AND+fixVersion+%3D+{fix_version}+AND+resolution+%3D+Fixed+"
    "AND+%22resolved+in+build%22+%3D+{build_number}"
)

# 出力先は実行時カレントディレクトリ配下。
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
    entries: Sequence[ResolvedBuildEntry],
    target_fix_versions: Sequence[str],
) -> bytes:
    root = ET.Element(
        "resolvedInBuildCollection",
        attrib={
            "generatedAt": _dt.datetime.now(tz=_dt.timezone.utc).isoformat(),
            "targetFixVersions": ",".join(target_fix_versions),
        },
    )

    fix_versions_in_order = tuple(dict.fromkeys(entry.fix_version for entry in entries))
    if fix_versions_in_order:
        root.set("fixVersions", ",".join(fix_versions_in_order))

    for entry in entries:
        container = ET.SubElement(
            root,
            "searchResult",
            attrib={
                "fixVersion": entry.fix_version,
                "build": entry.build_number,
            },
        )
        container.append(ET.fromstring(entry.xml_content))

    return ET.tostring(root, encoding="utf-8", xml_declaration=True)


def write_aggregate_xml(
    entries: Sequence[ResolvedBuildEntry],
    output_dir: Path,
    aggregate_filename: str,
    target_fix_versions: Sequence[str],
) -> Path:
    aggregate_path = output_dir / aggregate_filename
    aggregate_content = build_aggregate_xml(entries, target_fix_versions)
    write_xml(aggregate_content, aggregate_path)
    print(f"[INFO] 統合 XML: {aggregate_path.relative_to(Path.cwd())} に保存しました")
    return aggregate_path




class ResolvedBuildEntry(NamedTuple):
    """Resolved in Build の XML を収集した結果1件分。"""

    fix_version: str
    build_number: str
    xml_content: bytes
    fetched: bool

def collect_resolved_in_build_xml(
    targets: Iterable[tuple[str, Iterable[str]]],
    output_dir: Path,
    output_subdirectory: Path,
) -> tuple[list[ResolvedBuildEntry], int]:
    collected: list[ResolvedBuildEntry] = []
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
                    # print(f"[INFO] {fix_version} {build_number}: 既存 XML を再利用します")
                    collected.append(
                        ResolvedBuildEntry(
                            fix_version=fix_version,
                            build_number=build_number,
                            xml_content=xml_content,
                            fetched=False,
                        )
                    )
                    continue

            outcome, xml_content = fetch_build_xml(fix_version, build_number)
            if outcome is FetchOutcome.ERROR:
                failures += 1
                continue
            if outcome is FetchOutcome.NOT_FOUND:
                continue
            assert xml_content is not None
            collected.append(
                ResolvedBuildEntry(
                    fix_version=fix_version,
                    build_number=build_number,
                    xml_content=xml_content,
                    fetched=True,
                )
            )
    return collected, failures



def cleanup_generated_outputs(*, xml_root: Path, issue_root: Path, diff_report_path: Path) -> None:
    """実行前に主要生成物のみを削除し、再取得が不要なキャッシュは保持する。"""

    # 集約 XML ファイルのみ削除し、ビルド単位の XML キャッシュは残す。
    for aggregated_xml in (
        xml_root / "all_builds_openjdk.xml",
        xml_root / "all_builds_oraclejdk.xml",
    ):
        if aggregated_xml.exists():
            aggregated_xml.unlink()

    # issue_ids 配下は集約結果および per_file 出力が生成物なので初期化する。
    aggregated_issue_files = [
        issue_root / spec.aggregate_filename for spec in JDK_DIFF_PRODUCT_SPECS
    ]
    for issue_file in aggregated_issue_files:
        if issue_file.exists():
            issue_file.unlink()

    for directory in (
        issue_root / "OpenJDK",
        issue_root / "OracleJDK",
        issue_root / "temurin",
    ):
        if directory.is_dir():
            shutil.rmtree(directory)

    if diff_report_path.exists():
        diff_report_path.unlink()


def main() -> None:
    xml_output_root = Path.cwd() / XML_OUTPUT_ROOT
    issue_output_root = Path.cwd() / ISSUE_IDS_OUTPUT_ROOT
    temurin_input_root = Path.cwd() / TEMURIN_INPUT_ROOT
    diff_report_path = Path.cwd() / JDK_DIFF_OUTPUT_FILENAME

    cleanup_generated_outputs(
        xml_root=xml_output_root,
        issue_root=issue_output_root,
        diff_report_path=diff_report_path,
    )
    total_failures = 0
    any_collected = False
    issue_generation_results: dict[str, IssueIdGenerationResult] = {}

    for distribution in DISTRIBUTION_TARGETS:
        collected_entries, failures = collect_resolved_in_build_xml(
            distribution.targets, xml_output_root, distribution.output_subdirectory
        )
        total_failures += failures

        if not collected_entries:
            print(
                f"[WARN] {distribution.label}: 保存対象となる XML がありませんでした",
                file=sys.stderr,
            )
            continue

        any_collected = True
        for entry in collected_entries:
            if not entry.fetched:
                continue
            save_individual_xml(
                entry.fix_version,
                entry.build_number,
                entry.xml_content,
                xml_output_root,
                distribution.output_subdirectory,
            )

        write_aggregate_xml(
            collected_entries,
            xml_output_root,
            distribution.aggregate_filename,
            distribution.fix_versions,
        )
        supplemental_issue_maps: list[dict[str, set[str]]] = []
        if distribution.label == "OracleJDK":
            openjdk_result = issue_generation_results.get("OpenJDK")
            if openjdk_result is not None:
                supplemental_issue_maps.append(openjdk_result.aggregated_issue_map)
        issue_result = generate_issue_id_outputs(
            xml_output_root / distribution.output_subdirectory,
            issue_output_root,
            distribution.issue_ids_aggregate_filename,
            distribution.output_subdirectory,
            supplemental_issue_maps or None,
        )
        issue_generation_results[distribution.label] = issue_result
        print(
            f"[INFO] Issue ID 集約: {issue_result.aggregated_path.relative_to(Path.cwd())} に保存しました"
        )

    try:
        temurin_aggregate_path = generate_temurin_issue_outputs(
            temurin_input_root,
            issue_output_root,
            TEMURIN_JDK_ISSUES_DIR,
        )
    except (FileNotFoundError, ValueError) as error:
        print(f"[ERROR] Temurin: {error}", file=sys.stderr)
        sys.exit(1)
    else:
        print(
            f"[INFO] Temurin Issue ID 集約: {temurin_aggregate_path.relative_to(Path.cwd())} に保存しました"
        )

    try:
        diff_report_path = generate_jdk_diff_report(
            issue_output_root,
            Path.cwd(),
            TEMURIN_JDK_ISSUES_DIR,
        )
    except JDKDiffError as error:
        print(f"[ERROR] JDK Diff Report: {error}", file=sys.stderr)
        sys.exit(1)
    else:
        print(
            f"[INFO] JDK差分レポート: {diff_report_path.relative_to(Path.cwd())} に保存しました"
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
