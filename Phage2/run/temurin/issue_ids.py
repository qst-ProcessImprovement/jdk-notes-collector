"""Temurin JDKリリースノートからIssue ID一覧を抽出するユーティリティ。"""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Iterable, List, Sequence, Tuple

import re
_BASE_DIR = Path(__file__).parent
_TEMURIN_DIR = _BASE_DIR / "temurin"
_OUTPUT_DIR = _BASE_DIR / "issue_ids_output"
_PER_FILE_DIR = _OUTPUT_DIR / "per_file"
_AGGREGATED_FILENAME = "all_issue_ids.txt"
_ISSUE_ID_PATTERN = re.compile(r"^JDK-\d+$")


def _iter_release_notes(json_path: Path) -> Iterable[dict]:
    """JSONに含まれるリリースノート項目を順に返す。"""
    try:
        with json_path.open("r", encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError as exc:
        raise FileNotFoundError(f"入力JSONが見つかりません: {json_path}") from exc

    notes = data.get("release_notes")
    if not isinstance(notes, list):
        raise ValueError("release_notes が配列ではありません")
    for entry in notes:
        if not isinstance(entry, dict):
            raise ValueError("release_notes 内の要素がオブジェクトではありません")
        yield entry


def collect_issue_ids(json_path: Path) -> Tuple[List[str], dict[str, set[str]]]:
    """Backportの元Issue IDを含むIssue ID一覧とBackport対応表を抽出して返す。"""
    issue_ids: List[str] = []
    backport_map: dict[str, set[str]] = {}
    for entry in _iter_release_notes(json_path):
        issue_type = entry.get("type")
        if issue_type == "Backport":
            backport_of = _require_jdk_issue_id(entry.get("backportOf"), json_path=json_path, field_name="backportOf")
            backport_issue_id = _require_jdk_issue_id(entry.get("id"), json_path=json_path, field_name="id")
            issue_ids.append(backport_of)
            backport_map.setdefault(backport_of, set()).add(backport_issue_id)
            continue

        issue_id = _require_jdk_issue_id(entry.get("id"), json_path=json_path, field_name="id")
        issue_ids.append(issue_id)
        backport_map.setdefault(issue_id, set())
    return issue_ids, backport_map


def _sorted_unique(values: Sequence[str]) -> List[str]:
    """重複を排除しつつ辞書順ソートしたリストを返す。"""
    return sorted(set(values))


def _sorted_duplicates(values: Sequence[str]) -> List[str]:
    """複数回出現した値のみを辞書順で返す。"""
    counter = Counter(values)
    return sorted([value for value, count in counter.items() if count > 1])


def _require_jdk_issue_id(value: object, *, json_path: Path, field_name: str) -> str:
    """JDK Issue IDが正準表現か検証し、正当な値を返す。"""
    if not isinstance(value, str):
        raise ValueError(f"{json_path}:{field_name} が文字列ではありません: {value!r}")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{json_path}:{field_name} が空文字です")
    if not _ISSUE_ID_PATTERN.fullmatch(normalized):
        raise ValueError(
            f"正準表現に合致しないIssue IDを検出しました: {json_path}:{field_name} -> '{normalized}'"
        )
    return normalized


def _format_issue_line(issue_id: str, backport_ids: Iterable[str]) -> str:
    """元Issue IDにtemurin Backport IDを付与した行を生成する。"""
    suffixes = [f"temurin_{backport}" for backport in _sorted_unique(list(backport_ids))]
    if not suffixes:
        return issue_id
    return ",".join([issue_id, *suffixes])

def _canonical_output_filename(json_path: Path) -> str:
    """JSONファイル名からビルド番号サフィックスを除いた出力ファイル名を得る。"""
    stem = json_path.stem
    canonical_stem = re.sub(r"\+\d+$", "", stem)
    return f"{canonical_stem}.txt"

def _write_unique_ids(
    json_path: Path, issue_ids: Sequence[str], backport_map: dict[str, set[str]]
) -> List[str]:
    """ユニークなIssue IDをファイル別ディレクトリへ書き出し、書き出したIDを返す。"""
    _PER_FILE_DIR.mkdir(parents=True, exist_ok=True)
    output_filename = _canonical_output_filename(json_path)
    output_path = _PER_FILE_DIR / output_filename
    unique_ids = _sorted_unique(issue_ids)
    lines = [_format_issue_line(issue_id, backport_map.get(issue_id, ())) for issue_id in unique_ids]
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return unique_ids


def main() -> None:
    """temurin配下のJSONを処理し、重複IDのみを標準出力する。"""
    if not _TEMURIN_DIR.is_dir():
        raise FileNotFoundError(f"temurinディレクトリが存在しません: {_TEMURIN_DIR}")

    json_files = sorted(_TEMURIN_DIR.glob("*.json"))
    if not json_files:
        raise FileNotFoundError(f"JSONファイルが見つかりません: {_TEMURIN_DIR}")

    aggregate_ids: set[str] = set()
    aggregate_backports: dict[str, set[str]] = {}

    for json_path in json_files:
        issue_ids, backport_map = collect_issue_ids(json_path)
        unique_ids = _write_unique_ids(json_path, issue_ids, backport_map)
        aggregate_ids.update(unique_ids)
        for issue_id in unique_ids:
            aggregate_backports.setdefault(issue_id, set())
        for issue_id, backports in backport_map.items():
            aggregate_backports.setdefault(issue_id, set()).update(backports)
        duplicate_ids = _sorted_duplicates(issue_ids)
        if not duplicate_ids:
            continue

        print("duplicate ids: " + json_path.name)
        for issue_id in duplicate_ids:
            print(issue_id)
        print()

    _OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    aggregate_output_path = _OUTPUT_DIR / _AGGREGATED_FILENAME
    aggregate_output = _sorted_unique(list(aggregate_ids))
    aggregate_lines = [
        _format_issue_line(issue_id, aggregate_backports.get(issue_id, ())) for issue_id in aggregate_output
    ]
    aggregate_output_path.write_text("\n".join(aggregate_lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
