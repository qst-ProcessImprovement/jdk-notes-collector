"""Temurin JDKリリースノートからIssue ID一覧を抽出するユーティリティ。"""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Iterable, List, Sequence

_BASE_DIR = Path(__file__).parent
_TEMURIN_DIR = _BASE_DIR / "temurin"
_OUTPUT_DIR = _BASE_DIR / "issue_ids"


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


def collect_issue_ids(json_path: Path) -> List[str]:
    """Backportの元Issue IDを含むIssue ID一覧を抽出して返す。"""
    issue_ids: List[str] = []
    for entry in _iter_release_notes(json_path):
        issue_type = entry.get("type")
        if issue_type == "Backport":
            backport_of = entry.get("backportOf")
            if not isinstance(backport_of, str) or not backport_of:
                raise ValueError(f"Backport項目に backportOf がありません: {json_path}")
            issue_ids.append(backport_of)
            continue

        issue_id = entry.get("id")
        if not isinstance(issue_id, str) or not issue_id:
            raise ValueError(f"Issue項目に id がありません: {json_path}")
        issue_ids.append(issue_id)
    return issue_ids


def _sorted_unique(values: Sequence[str]) -> List[str]:
    """重複を排除しつつ辞書順ソートしたリストを返す。"""
    return sorted(set(values))


def _sorted_duplicates(values: Sequence[str]) -> List[str]:
    """複数回出現した値のみを辞書順で返す。"""
    counter = Counter(values)
    return sorted([value for value, count in counter.items() if count > 1])


def _write_unique_ids(json_path: Path, issue_ids: Sequence[str]) -> Path:
    """ユニークなIssue IDをファイルへ書き出し、出力パスを返す。"""
    _OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_path = _OUTPUT_DIR / json_path.with_suffix(".txt").name
    unique_ids = _sorted_unique(issue_ids)
    output_path.write_text("\n".join(unique_ids) + "\n", encoding="utf-8")
    return output_path


def main() -> None:
    """temurin配下のJSONを処理し、重複IDのみを標準出力する。"""
    if not _TEMURIN_DIR.is_dir():
        raise FileNotFoundError(f"temurinディレクトリが存在しません: {_TEMURIN_DIR}")

    json_files = sorted(_TEMURIN_DIR.glob("*.json"))
    if not json_files:
        raise FileNotFoundError(f"JSONファイルが見つかりません: {_TEMURIN_DIR}")

    for json_path in json_files:
        issue_ids = collect_issue_ids(json_path)
        _write_unique_ids(json_path, issue_ids)
        duplicate_ids = _sorted_duplicates(issue_ids)
        if not duplicate_ids:
            continue

        print(json_path.name)
        for issue_id in duplicate_ids:
            print(issue_id)
        print()


if __name__ == "__main__":
    main()
