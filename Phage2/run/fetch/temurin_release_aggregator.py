"""Temurin リリースノート JSON を単一ファイルへ集約するユーティリティ。"""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path
from typing import Any, Iterable

DEFAULT_INPUT_DIR = Path("Phage2/run/fetch/INPUT/temurin/json")
DEFAULT_OUTPUT_PATH = DEFAULT_INPUT_DIR / "temurin_releases.json"


class AggregationError(Exception):
    """テンプリン集約処理中の例外。"""


def parse_args(argv: Iterable[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input-dir",
        type=Path,
        default=DEFAULT_INPUT_DIR,
        help="TemurinリリースノートJSONが配置されているディレクトリ",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT_PATH,
        help="集約したJSONを書き出すパス",
    )
    return parser.parse_args(argv)


def load_release_json(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise AggregationError(f"入力ファイルが見つかりません: {path}")

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise AggregationError(f"JSONの解析に失敗しました: {path}") from exc

    required_top_level = {"release_name", "release_notes"}
    missing = required_top_level - data.keys()
    if missing:
        raise AggregationError(f"必須キーが不足しています: {path} -> {sorted(missing)}")

    if not isinstance(data["release_name"], str) or not data["release_name"].strip():
        raise AggregationError(f"release_nameが不正です: {path}")

    if not isinstance(data["release_notes"], list):
        raise AggregationError(f"release_notesが配列ではありません: {path}")

    return data


def aggregate_releases(input_dir: Path) -> dict[str, Any]:
    if not input_dir.is_dir():
        raise AggregationError(f"入力ディレクトリが存在しません: {input_dir}")

    release_files = sorted(input_dir.glob("*.json"))
    if not release_files:
        raise AggregationError(f"JSONファイルが見つかりません: {input_dir}")

    releases: list[dict[str, Any]] = []
    seen_release_names: set[str] = set()
    duplicates: dict[str, list[Path]] = defaultdict(list)

    for file_path in release_files:
        release = load_release_json(file_path)
        release_name = release["release_name"].strip()
        if release_name in seen_release_names:
            duplicates[release_name].append(file_path)
            continue
        seen_release_names.add(release_name)
        releases.append(release)

    if duplicates:
        entries = [f"{name}: {paths}" for name, paths in duplicates.items()]
        raise AggregationError(
            "同一release_nameのファイルが複数存在します: " + "; ".join(entries)
        )

    releases.sort(key=lambda item: item["release_name"])
    return {"releases": releases}


def write_aggregate(data: dict[str, Any], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2, sort_keys=False) + "\n",
        encoding="utf-8",
    )


def main(argv: Iterable[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        aggregate = aggregate_releases(args.input_dir)
    except AggregationError as exc:
        print(f"[ERROR] {exc}")
        return 1

    write_aggregate(aggregate, args.output)
    print(f"[INFO] 集約結果を {args.output} に書き出しました")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
