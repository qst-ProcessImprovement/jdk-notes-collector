"""JDK課題リストに基づいて結合ファイルから対象セクションを抽出するユーティリティ。

使用例:
    python jdk_issue_extractor.py jdklist_jdk-21.0.7+6.txt

デフォルトでは `jdk_issues_combined.txt` を入力として利用する。"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Iterable, Mapping

KEY_PATTERN = re.compile(r"^JDK-\d+$")
SECTION_HEADER_PATTERN = re.compile(
    r"^===\n# SOURCE:\s+(JDK-\d+)/[^\n]*\n===\n",
    flags=re.MULTILINE,
)

HEADER_BLOCK_PATTERN = re.compile(
    r"^===\n# SOURCE:[^\n]*\n===\n",
    flags=re.MULTILINE,
)


def load_issue_keys(list_path: Path) -> list[str]:
    """JDKキー一覧ファイルを読み込み正準表現で検証して返す。"""
    if not list_path.is_file():
        raise FileNotFoundError(f"リストファイルが見つかりません: {list_path}")

    raw_lines = list_path.read_text(encoding="utf-8").splitlines()
    keys: list[str] = []
    seen: set[str] = set()

    for line_no, raw in enumerate(raw_lines, start=1):
        key = raw.strip()
        if not key:
            continue
        if not KEY_PATTERN.fullmatch(key):
            raise ValueError(f"{list_path}:{line_no} 正準表現(JDK-数値)ではありません: {key!r}")
        if key in seen:
            raise ValueError(f"{list_path}:{line_no} キーが重複しています: {key}")
        seen.add(key)
        keys.append(key)

    if not keys:
        raise ValueError(f"{list_path} に有効なJDKキーがありません")

    return keys


def build_section_index(text: str, source_path: Path) -> dict[str, str]:
    """結合済みテキストから `JDK-xxxxxxx` ごとのセクションを抽出する。"""
    matches = list(SECTION_HEADER_PATTERN.finditer(text))
    if not matches:
        raise ValueError(f"{source_path} から課題セクションを検出できませんでした")

    sections: dict[str, str] = {}
    for idx, match in enumerate(matches):
        key = match.group(1)
        start = match.start()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(text)
        section = text[start:end]
        if key in sections:
            raise ValueError(f"{source_path} 内でキーが重複しています: {key}")
        sections[key] = section

    return sections


def format_section(section: str) -> str:
    """セクション先頭のSOURCEヘッダを-----へ置換する。"""
    return HEADER_BLOCK_PATTERN.sub("-----\n", section, count=1)


def extract_sections(
    keys: Iterable[str], section_index: Mapping[str, str]
) -> tuple[list[str], list[str]]:
    """指定されたキー順にセクションを集め、見つからなかったキーを返す。"""
    found_sections: list[str] = []
    missing_keys: list[str] = []

    for key in keys:
        section = section_index.get(key)
        if section is None:
            missing_keys.append(key)
            continue
        found_sections.append(section)

    return found_sections, missing_keys


def run_cli(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "list_path",
        type=Path,
        help="JDKキーを1行ずつ列挙したテキストファイル",
    )
    parser.add_argument(
        "--combined-path",
        type=Path,
        default=Path("jdk_issues_combined.txt"),
        help="課題結合ファイルのパス（省略時は jdk_issues_combined.txt）",
    )

    args = parser.parse_args(argv)

    keys = load_issue_keys(args.list_path)
    combined_text = args.combined_path.read_text(encoding="utf-8")
    section_index = build_section_index(combined_text, args.combined_path)

    found_sections, missing_keys = extract_sections(keys, section_index)

    if found_sections:
        formatted_sections = [format_section(section) for section in found_sections]
        sys.stdout.write("".join(formatted_sections))
        if not formatted_sections[-1].endswith("\n"):
            sys.stdout.write("\n")

    if missing_keys:
        missing_list = ", ".join(missing_keys)
        print(
            f"警告: 指定されたキーが結合ファイル内で見つかりません: {missing_list}",
            file=sys.stderr,
        )

    return 0


if __name__ == "__main__":
    sys.exit(run_cli())
