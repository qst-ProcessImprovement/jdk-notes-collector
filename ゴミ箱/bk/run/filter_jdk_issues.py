"""JDK課題を除外ルールに基づいて分類するユーティリティ。

指定ディレクトリ配下の課題XMLを解析し、
- 文書/テストのみの変更
- JDK21.0.5以降に追加された新機能のバックポート
- Windows 11 以外のプラットフォーム専用の変更
- GC関連の変更
に該当するものを自動的に除外ディレクトリへ振り分ける。
"""
from __future__ import annotations

import argparse
import csv
import re
import shutil
import sys
from dataclasses import dataclass
from html import unescape
from pathlib import Path
from typing import Iterable, Iterator
import xml.etree.ElementTree as ET

# -----------------------------
# データモデル
# -----------------------------


@dataclass(slots=True)
class IssueData:
    """JDK課題のメタ情報とテキストを保持する。"""

    key: str
    summary: str
    description: str
    comments: list[str]
    labels: list[str]
    issue_type: str
    components: list[str]
    subcomponents: list[str]
    fix_versions: list[str]
    os_values: list[str]
    backport_sources: list[str]
    source_dir: Path
    source_file: Path


@dataclass(slots=True)
class RuleMatch:
    """適用された除外ルールを表す。"""

    name: str
    details: str


@dataclass(slots=True)
class IssueClassification:
    """課題の分類結果。"""

    issue: IssueData
    category: str  # excluded or review
    matches: list[RuleMatch]


# -----------------------------
# 解析ユーティリティ
# -----------------------------


HTML_BREAK_PATTERN = re.compile(r"(?i)<br\s*/?>")
HTML_TAG_PATTERN = re.compile(r"<[^>]+>")
MULTI_WHITESPACE_PATTERN = re.compile(r"[ \t]+")
MULTI_NEWLINE_PATTERN = re.compile(r"\n{3,}")


def normalize_text(raw: str | None) -> str:
    """HTMLを含むテキストを簡易整形しプレーンテキストへ変換する。"""
    if not raw:
        return ""
    text = unescape(raw)
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = HTML_BREAK_PATTERN.sub("\n", text)
    text = re.sub(r"(?i)</p>", "\n\n", text)
    text = re.sub(r"(?i)<p>", "", text)
    text = HTML_TAG_PATTERN.sub(" ", text)
    text = MULTI_WHITESPACE_PATTERN.sub(" ", text)
    text = MULTI_NEWLINE_PATTERN.sub("\n\n", text)
    lines = [line.strip() for line in text.split("\n")]
    return "\n".join(line for line in lines if line).strip()


def normalize_inline(raw: str | None) -> str:
    """インラインテキスト用の簡易整形。"""
    return unescape(raw or "").strip()


def parse_issue(xml_path: Path) -> IssueData:
    """XMLファイルから IssueData を生成する。"""
    try:
        root = ET.parse(xml_path).getroot()
    except ET.ParseError as exc:  # noqa: B904
        raise ValueError(f"XML解析に失敗しました: {xml_path}") from exc

    item = root.find(".//item")
    if item is None:
        raise ValueError(f"item要素が見つかりません: {xml_path}")

    key = normalize_inline(item.findtext("key"))
    summary = normalize_inline(item.findtext("summary"))
    description = normalize_text(item.findtext("description"))

    comments = [
        normalize_text(comment.text)
        for comment in item.findall("comments/comment")
        if comment.text
    ]

    labels = [
        normalize_inline(label.text)
        for label in item.findall("labels/label")
        if label.text
    ]

    issue_type = normalize_inline(item.findtext("type"))
    components = [
        normalize_inline(component.text)
        for component in item.findall("component")
        if component.text
    ]
    fix_versions = [
        normalize_inline(fv.text)
        for fv in item.findall("fixVersion")
        if fv.text
    ]

    os_values: list[str] = []
    subcomponents: list[str] = []
    for customfield in item.findall("customfields/customfield"):
        name = normalize_inline(customfield.findtext("customfieldname"))
        values = [
            normalize_inline(value.text)
            for value in customfield.findall("customfieldvalues/customfieldvalue")
            if value.text
        ]
        if not values:
            continue
        lowered_name = name.lower()
        if lowered_name == "os":
            os_values.extend(values)
        elif lowered_name == "subcomponent":
            subcomponents.extend(values)

    backport_sources = [
        normalize_inline(link.findtext("issuekey"))
        for link in item.findall(
            "issuelinks/issuelinktype[@name='Backport']/inwardlinks/issuelink"
        )
        if link.findtext("issuekey")
    ]

    return IssueData(
        key=key,
        summary=summary,
        description=description,
        comments=comments,
        labels=labels,
        issue_type=issue_type,
        components=components,
        subcomponents=subcomponents,
        fix_versions=fix_versions,
        os_values=os_values,
        backport_sources=backport_sources,
        source_dir=xml_path.parent,
        source_file=xml_path,
    )


class IssueRepository:
    """課題XMLをキャッシュするリポジトリ。"""

    def __init__(self, roots: Iterable[Path]):
        self._store: dict[str, IssueData] = {}
        for root in roots:
            root = root.resolve()
            if not root.exists():
                continue
            for xml_path in root.rglob("jdk-*.xml"):
                issue = parse_issue(xml_path)
                # 既に同一IDが登録済みの場合は最初のものを優先
                self._store.setdefault(issue.key, issue)

    def get(self, key: str) -> IssueData | None:
        return self._store.get(key)

    def issues_in_dir(self, directory: Path) -> Iterator[IssueData]:
        resolved = directory.resolve()
        for issue in self._store.values():
            if issue.source_dir.parent.resolve() == resolved:
                yield issue


# -----------------------------
# 除外ルール
# -----------------------------


DOCUMENT_KEYWORD_PATTERNS: dict[str, re.Pattern[str]] = {
    "open source": re.compile(r"\bopen\s+source\b", re.IGNORECASE),
    "problemlist": re.compile(r"\bproblemlist\b", re.IGNORECASE),
    "jtreg": re.compile(r"\bjtreg\b", re.IGNORECASE),
    "test": re.compile(r"\btest(?:s|ing)?\b", re.IGNORECASE),
    "manual test": re.compile(r"\bmanual\s+test(?:s|ing)?\b", re.IGNORECASE),
    "doc": re.compile(r"\bdoc(?:s|umentation)?\b", re.IGNORECASE),
    "spec update": re.compile(r"\bspec(?:ification)?\s+update\b", re.IGNORECASE),
    "copyright": re.compile(r"\bcopyright\b", re.IGNORECASE),
}
DOCUMENT_ALERT_PATTERN = re.compile(
    r"\b(crash(?:es|ed)?|exception(?:s)?|regression(?:s)?)\b",
    re.IGNORECASE,
)
NOREG_LABEL_PATTERN = re.compile(r"^noreg-", re.IGNORECASE)
HGUPDATE_LABEL = "hgupdate-sync"

FEATURE_KEYWORD_PATTERN = re.compile(
    r"\b(add|introduce|support|implement)(?:s|ed|ing)?\b",
    re.IGNORECASE,
)
FEATURE_EXCLUDE_PATTERN = re.compile(r"\b(doc|docs|documentation|test|tests|testing)\b", re.IGNORECASE)
FUTURE_FIXVERSION_PATTERN = re.compile(r"^(2[2-9]|[3-9]\d)(\.|$)")
FEATURE_LABEL_PATTERN = re.compile(r"^(\d{2}|\d{2}u)-na$", re.IGNORECASE)

OS_KEYWORD_PATTERNS: dict[str, re.Pattern[str]] = {
    "linux": re.compile(r"\blinux\b", re.IGNORECASE),
    "macos": re.compile(r"\bmac\s*os\b|\bmacos\b", re.IGNORECASE),
    "aix": re.compile(r"\baix\b", re.IGNORECASE),
    "solaris": re.compile(r"\bsolaris\b", re.IGNORECASE),
    "alpine": re.compile(r"\balpine\b", re.IGNORECASE),
    "windows xp": re.compile(r"\bwindows\s+xp\b", re.IGNORECASE),
    "windows 7": re.compile(r"\bwindows\s+7\b", re.IGNORECASE),
    "windows 8": re.compile(r"\bwindows\s+8(\.1)?\b", re.IGNORECASE),
    "windows 10": re.compile(r"\bwindows\s+10\b", re.IGNORECASE),
    "windows server": re.compile(r"\bwindows\s+server\b", re.IGNORECASE),
}
WINDOWS11_PATTERNS = (
    re.compile(r"\bwindows\s*11\b", re.IGNORECASE),
    re.compile(r"\bwin\s*11\b", re.IGNORECASE),
)

GC_KEYWORD_PATTERNS = (
    re.compile(r"\bgc\b", re.IGNORECASE),
    re.compile(r"\bgarbage\b", re.IGNORECASE),
    re.compile(r"\bshenandoah\b", re.IGNORECASE),
    re.compile(r"\bzgc\b", re.IGNORECASE),
    re.compile(r"\bg1\b", re.IGNORECASE),
)
GC_LABEL_PATTERN = re.compile(r"^gc-", re.IGNORECASE)


class IssueClassifier:
    """除外判定を行うクラス。"""

    def __init__(self, repository: IssueRepository):
        self._repo = repository

    def classify(self, issue: IssueData) -> IssueClassification:
        matches: list[RuleMatch] = []

        doc_match = self._match_doc_or_test(issue)
        if doc_match:
            matches.append(doc_match)

        feature_match = self._match_new_feature(issue)
        if feature_match:
            matches.append(feature_match)

        platform_match = self._match_non_windows11(issue)
        if platform_match:
            matches.append(platform_match)

        gc_match = self._match_gc(issue)
        if gc_match:
            matches.append(gc_match)

        category = "excluded" if matches else "review"
        return IssueClassification(issue=issue, category=category, matches=matches)

    def _collect_text(self, issue: IssueData) -> str:
        parts = [issue.summary, issue.description, *issue.comments]
        return "\n".join(part for part in parts if part)

    def _match_doc_or_test(self, issue: IssueData) -> RuleMatch | None:
        combined = self._collect_text(issue)
        if not combined:
            return None
        if DOCUMENT_ALERT_PATTERN.search(combined):
            return None

        matched_keywords = {
            name
            for name, pattern in DOCUMENT_KEYWORD_PATTERNS.items()
            if pattern.search(combined)
        }
        label_hits = {
            label
            for label in issue.labels
            if NOREG_LABEL_PATTERN.match(label) or label.lower() == HGUPDATE_LABEL
        }
        total_score = len(matched_keywords) + len(label_hits)
        if total_score >= 2:
            details = []
            if matched_keywords:
                details.append("keywords=" + ",".join(sorted(matched_keywords)))
            if label_hits:
                details.append("labels=" + ",".join(sorted(label_hits)))
            return RuleMatch("doc_or_test", "; ".join(details) if details else "keyword threshold")
        return None

    def _match_new_feature(self, issue: IssueData) -> RuleMatch | None:
        base_candidates: list[IssueData] = []
        if issue.issue_type.lower() == "backport" and issue.backport_sources:
            for key in issue.backport_sources:
                base_issue = self._repo.get(key)
                if base_issue is not None:
                    base_candidates.append(base_issue)
        if not base_candidates:
            base_candidates.append(issue)

        for base in base_candidates:
            if base.issue_type.lower() not in {"enhancement", "new feature"}:
                continue
            if not FEATURE_KEYWORD_PATTERN.search(base.summary):
                continue
            if FEATURE_EXCLUDE_PATTERN.search(base.summary):
                continue
            if base.fix_versions and not any(
                FUTURE_FIXVERSION_PATTERN.match(fv)
                for fv in base.fix_versions
                if fv
            ):
                continue
            label_matches = [
                lbl
                for lbl in base.labels + issue.labels
                if FEATURE_LABEL_PATTERN.match(lbl)
            ]
            details_parts = [f"base={base.key or issue.key}"]
            if base.fix_versions:
                details_parts.append("fixVersion=" + "/".join(base.fix_versions))
            if label_matches:
                details_parts.append("labels=" + ",".join(sorted(set(label_matches))))
            return RuleMatch("new_feature", "; ".join(details_parts))
        return None

    def _match_non_windows11(self, issue: IssueData) -> RuleMatch | None:
        target_text = f"{issue.summary}\n{issue.description}"
        matched_tokens = {
            name
            for name, pattern in OS_KEYWORD_PATTERNS.items()
            if pattern.search(target_text)
        }
        for value in issue.os_values:
            for name, pattern in OS_KEYWORD_PATTERNS.items():
                if pattern.search(value):
                    matched_tokens.add(name)
        if not matched_tokens:
            return None
        if any(pattern.search(target_text) for pattern in WINDOWS11_PATTERNS):
            return None
        if any(pattern.search(value) for value in issue.os_values for pattern in WINDOWS11_PATTERNS):
            return None
        details = "targets=" + ",".join(sorted(matched_tokens))
        if issue.os_values:
            details += f"; os_field={'/'.join(issue.os_values)}"
        return RuleMatch("non_windows11_platform", details)

    def _match_gc(self, issue: IssueData) -> RuleMatch | None:
        lower_components = {comp.lower() for comp in issue.components}
        lower_subcomponents = {sub.lower() for sub in issue.subcomponents}
        component_hit = "hotspot" in lower_components and "gc" in lower_subcomponents

        combined_text = f"{issue.summary}\n{issue.description}"
        keyword_hits = [
            pattern.pattern
            for pattern in GC_KEYWORD_PATTERNS
            if pattern.search(combined_text)
        ]
        label_hits = [label for label in issue.labels if GC_LABEL_PATTERN.match(label)]
        if component_hit or keyword_hits or label_hits:
            details = []
            if component_hit:
                details.append("component=hotspot/gc")
            if keyword_hits:
                details.append("keywords=" + ",".join(sorted(set(keyword_hits))))
            if label_hits:
                details.append("labels=" + ",".join(sorted(set(label_hits))))
            return RuleMatch("gc_related", "; ".join(details) if details else "gc indicator")
        return None


# -----------------------------
# 出力ユーティリティ
# -----------------------------


def clear_directory(path: Path) -> None:
    if path.exists():
        if not path.is_dir():
            raise ValueError(f"ディレクトリではありません: {path}")
        shutil.rmtree(path)
    path.mkdir(parents=True, exist_ok=True)


def copy_issue(issue: IssueData, destination_root: Path) -> None:
    target = destination_root / issue.source_dir.name
    shutil.copytree(issue.source_dir, target)


def write_report(report_path: Path, classifications: Iterable[IssueClassification]) -> None:
    report_path.parent.mkdir(parents=True, exist_ok=True)
    with report_path.open("w", encoding="utf-8", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["issue_id", "category", "rules", "details"])
        for classification in classifications:
            rules = ",".join(match.name for match in classification.matches)
            details = " | ".join(match.details for match in classification.matches)
            writer.writerow([classification.issue.key, classification.category, rules, details])


# -----------------------------
# CLI
# -----------------------------


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="JDK課題を除外ルールで分類するツール")
    parser.add_argument(
        "--source-dir",
        type=Path,
        default=Path("jdk_issues"),
        help="解析対象の課題ディレクトリ (既定: jdk_issues)",
    )
    parser.add_argument(
        "--extra-source",
        type=Path,
        action="append",
        default=[],
        help="追加で参照する課題ディレクトリ (Backport元など)",
    )
    parser.add_argument(
        "--output-review",
        type=Path,
        default=Path.cwd() / "jdk_issues_要確認",
        help="要確認課題のコピー先 (既定: ./jdk_issues_要確認)",
    )
    parser.add_argument(
        "--output-excluded",
        type=Path,
        default=Path.cwd() / "jdk_issues_非互換考慮不要",
        help="除外課題のコピー先 (既定: ./jdk_issues_非互換考慮不要)",
    )
    parser.add_argument(
        "--report",
        type=Path,
        default=Path.cwd() / "jdk_issues_classification.csv",
        help="分類結果レポートの出力先 (既定: ./jdk_issues_classification.csv)",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_arg_parser()
    args = parser.parse_args(argv)

    if not args.source_dir.exists():
        parser.error(f"source directory not found: {args.source_dir}")

    repository = IssueRepository([args.source_dir, *args.extra_source])
    classifier = IssueClassifier(repository)

    try:
        source_issues = list(repository.issues_in_dir(args.source_dir))
    except Exception as exc:  # noqa: BLE001
        parser.error(str(exc))
        return 2

    clear_directory(args.output_excluded)
    clear_directory(args.output_review)

    classifications: list[IssueClassification] = []
    for issue in sorted(source_issues, key=lambda item: item.key):
        classification = classifier.classify(issue)
        destination = (
            args.output_excluded if classification.category == "excluded" else args.output_review
        )
        copy_issue(issue, destination)
        classifications.append(classification)

    write_report(args.report, classifications)
    excluded_count = sum(1 for cls in classifications if cls.category == "excluded")
    review_count = len(classifications) - excluded_count
    print(f"除外: {excluded_count} 件 / 要確認: {review_count} 件")
    print(f"レポート: {args.report}")
    print(f"出力先: 除外 -> {args.output_excluded}, 要確認 -> {args.output_review}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
