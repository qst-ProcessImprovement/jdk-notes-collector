"""JDK issueファイルを結合するモジュール。

`jdk_issues/`配下に存在する全てのファイルを再帰的に列挙し、
ファイル境界が分かるよう区切り線を挿入しながら一つの出力ファイルへ結合する。
"""
from __future__ import annotations

import argparse
import sys
from html import unescape
import re
from pathlib import Path
from typing import Iterable, Literal, Sequence
import xml.etree.ElementTree as ET

# 区切り線および出力先は正準値として固定する
BOUNDARY_LINE = "=" * 80
BOUNDARY_HEADER_PREFIX = "# SOURCE: "
DEFAULT_OUTPUT_FILENAME = "jdk_issues_combined.txt"
TARGET_SUFFIX = ".xml"
ContentMode = Literal["full", "summary"]


def list_issue_files(source_dir: Path) -> list[Path]:
    """結合対象となるファイル一覧を相対パス昇順で返す。"""
    if not source_dir.exists():
        raise FileNotFoundError(f"ディレクトリが存在しません: {source_dir}")
    if not source_dir.is_dir():
        raise NotADirectoryError(f"ディレクトリではありません: {source_dir}")

    files = [
        path
        for path in source_dir.rglob("*")
        if path.is_file() and path.suffix.lower() == TARGET_SUFFIX
    ]
    files.sort(key=lambda p: p.relative_to(source_dir).as_posix())
    if not files:
        raise FileNotFoundError(f"ファイルが見つかりません: {source_dir}")
    return files


def format_boundary(relative_path: Path) -> str:
    """出力に挿入する区切り線を生成する。"""
    rel_display = relative_path.as_posix()
    return (
        f"{BOUNDARY_LINE}\n"
        f"{BOUNDARY_HEADER_PREFIX}{rel_display}\n"
        f"{BOUNDARY_LINE}\n"
    )


def extract_summary(path: Path, *, encoding: str) -> tuple[str, str]:
    """XMLを解析してタイトルと説明の要約を返す。"""
    xml_text = path.read_text(encoding=encoding)
    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError as exc:
        raise ValueError(f"XML解析に失敗しました: {path}") from exc

    item = root.find(".//item")
    if item is None:
        raise ValueError(f"item要素が見つかりません: {path}")

    raw_title = item.findtext("title", default="")
    raw_description = item.findtext("description", default="")
    title = normalize_inline_text(raw_title)
    description = normalize_description(raw_description)
    return title, description


def normalize_inline_text(raw_value: str) -> str:
    """HTMLエンティティを展開し、前後空白を除去する。"""
    return unescape(raw_value).strip()


def normalize_description(raw_value: str) -> str:
    """説明文のHTMLエンティティを展開し簡易整形する。"""
    text = unescape(raw_value or "")
    if not text:
        return ""

    replacements = (
        (r"(?i)<br\s*/?>", "\n"),
        (r"(?i)</p>", "\n\n"),
        (r"(?i)<p>", ""),
        (r"(?i)</li>", "\n"),
        (r"(?i)<li>", "- "),
        (r"(?i)</tr>", "\n"),
        (r"(?i)</td>", "\t"),
        (r"(?i)<(td|th)>", ""),
        (r"(?i)</(div|span|tbody|table|ul|ol|body|html|head)>", "\n"),
        (r"(?i)<(div|span|tbody|table|ul|ol|body|html|head)>", ""),
    )
    for pattern, repl in replacements:
        text = re.sub(pattern, repl, text)

    text = re.sub(r"<[^>]+>", "", text)
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"\n{3,}", "\n\n", text)
    lines = [line.rstrip() for line in text.splitlines()]
    return "\n".join(lines).strip()


def write_combined_file(
    source_dir: Path,
    output_path: Path,
    *,
    encoding: str,
    mode: ContentMode,
    file_paths: Iterable[Path] | None = None,
) -> None:
    """ファイル内容を結合して出力する。"""
    paths = list_issue_files(source_dir) if file_paths is None else list(file_paths)
    if not paths:
        raise FileNotFoundError(f"ファイルが見つかりません: {source_dir}")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", encoding=encoding, newline="\n") as out_f:
        for index, path in enumerate(paths):
            relative_path = path.relative_to(source_dir)
            boundary = format_boundary(relative_path)
            if index > 0:
                out_f.write("\n")
            out_f.write(boundary)

            if mode == "full":
                text = path.read_text(encoding=encoding)
                out_f.write(text)
                if not text.endswith("\n"):
                    out_f.write("\n")
                continue

            title, description = extract_summary(path, encoding=encoding)
            out_f.write(f"Title: {title}\n")
            out_f.write("Description:\n")
            if description:
                out_f.write(description)
                if not description.endswith("\n"):
                    out_f.write("\n")
            else:
                out_f.write("(no description)\n")


def combine_jdk_issues(
    source_dir: Path,
    *,
    encoding: str = "utf-8",
    mode: ContentMode = "full",
) -> Path:
    """公開インターフェース: カレントディレクトリに結合ファイルを生成する。"""
    output_path = Path.cwd() / DEFAULT_OUTPUT_FILENAME
    write_combined_file(source_dir, output_path, encoding=encoding, mode=mode)
    return output_path


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="jdk_issues配下のファイルを結合するユーティリティ",
    )
    parser.add_argument(
        "--source-dir",
        type=Path,
        default=Path("jdk_issues"),
        help="結合対象のディレクトリ (既定: jdk_issues)",
    )
    parser.add_argument(
        "--encoding",
        type=str,
        default="utf-8",
        help="入出力で使用する文字エンコーディング (既定: utf-8)",
    )
    parser.add_argument(
        "--content-mode",
        choices=("full", "summary"),
        default="full",
        help="出力形式を選択 (full: 元ファイルを全て結合, summary: タイトルと説明のみ)",
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    try:
        output_path = combine_jdk_issues(
            args.source_dir,
            encoding=args.encoding,
            mode=args.content_mode,
        )
        print(f"出力ファイル: {output_path}")
    except (FileNotFoundError, NotADirectoryError, ValueError) as exc:
        print(f"エラー: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
