"""JDK課題の分類結果を集計し、リリースノート差分調査の資料作成を補助するモジュール。

``filter_jdk_issues`` の判定ルールを再利用して、詳細一覧とリリース別・領域別の件数
サマリを出力する。判定ロジックは以下のとおりで、いずれの除外条件にも該当しなかった
課題が「要確認 (`needs_review`)」として残る。

1. `doc_or_test`: summary/description/comment にドキュメント・テスト専用のキーワードや
   `noreg-*` ラベルが一定数含まれる。
2. `new_feature`: Backport 元が Enhancement/New Feature で、Add/Introduce/Support/Implement
   を含む要約かつ将来リリース向けの fixVersion 等から新機能の追加と判断できる。
3. `non_windows11_platform`: summary/description/customfield[OS] が Windows 11 以外の OS
   のみを指しており、Win11 の記載が存在しない。
4. `gc_related`: component/subcomponent が hotspot/gc、または GC/ Garbage/Shenandoah/ZGC/G1
   等のキーワード・ラベルが付いている。

これらのどれにも当てはまらない課題が互換性確認の対象「要確認」となる。

出力する CSV は次の3種類。

- `jdk_issues_summary_detail.csv`: 個票一覧。Issue ID、対象リリース、影響判定、機能領域、
  適用ルールやラベルを横持ちでまとめ、要確認 Issue の深掘りに使う。
- `jdk_issues_summary_release.csv`: リリース別 × 影響判定の件数サマリ。21.0.6〜21.0.8 の
  要確認件数を俯瞰する。
- `jdk_issues_summary_area.csv`: リリース別 × 機能領域 × 影響判定の件数サマリ。どの
  機能領域に調査リソースを割るか判断するための材料を提供する。
"""
from __future__ import annotations

import argparse
import csv
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence
import re

# 同一リポジトリ内の step5.非互換抽出/filter_jdk_issues.py を利用するため、パスを追加
import sys

SCRIPT_DIR = Path(__file__).resolve().parent
FILTER_MODULE_DIR = SCRIPT_DIR.parent / "step5.非互換抽出"
if FILTER_MODULE_DIR.exists():
    sys.path.append(str(FILTER_MODULE_DIR))

from filter_jdk_issues import (
    IssueClassification,
    IssueClassifier,
    IssueData,
    IssueRepository,
)

TARGET_RELEASES = {"21.0.6", "21.0.7", "21.0.8"}


SECURITY_KEYWORDS = re.compile(
    r"\b(cve|security|tls|ssl|keystore|certificate|crypto|pkcs|jce|kerberos)\b",
    re.IGNORECASE,
)
PERFORMANCE_KEYWORDS = re.compile(
    r"\b(perf(?:ormance)?|throughput|latency|slow(?:er)?|regression)\b",
    re.IGNORECASE,
)
SPEC_KEYWORDS = re.compile(r"\b(spec|csr|compatibility|behavior change)\b", re.IGNORECASE)
INTEROP_KEYWORDS = re.compile(
    r"\b(jni|foreign|panama|ffm|interop|socket|nio|net|locale|charset)\b",
    re.IGNORECASE,
)
TEST_INFRA_KEYWORDS = re.compile(r"\bjtreg|test harness|test infra\b", re.IGNORECASE)


COMPILER_SUBCOMPONENTS = {
    "javac",
    "javadoc",
    "jshell",
    "tools",
}
INTEROP_SUBCOMPONENTS = {
    "java.lang.foreign",
    "java.net",
    "java.nio",
    "java.util:i18n",
    "org.ietf.jgss",
    "javax.naming",
}
SECURITY_SUBCOMPONENTS = {
    "java.security",
    "java.util.jar",
    "org.ietf.jgss",
}
PERF_LABELS = {"noreg-performance", "perf"}


@dataclass(slots=True)
class AggregatedRow:
    issue_id: str
    release: str
    impact_status: str
    feature_area: str
    highlight_tags: str
    action_required: str
    impact_notes: str
    applied_rules: str
    summary: str
    components: str
    subcomponents: str
    labels: str
    fix_versions: str


def determine_release(issue: IssueData) -> str:
    for fix_version in issue.fix_versions:
        if fix_version in TARGET_RELEASES:
            return fix_version
    for label in issue.labels:
        if label.startswith("jdk21u-") and "-fix" in label:
            return "21.0.x"
    return "unknown"


def select_feature_area(issue: IssueData) -> str:
    lowered_components = {component.lower() for component in issue.components}
    lowered_subcomponents = {sub.lower() for sub in issue.subcomponents}
    text = f"{issue.summary}\n{issue.description}" if issue.description else issue.summary

    if any("security" in comp for comp in lowered_components) or (
        lowered_subcomponents & {sub.lower() for sub in SECURITY_SUBCOMPONENTS}
    ) or SECURITY_KEYWORDS.search(text):
        return "security"

    if "hotspot" in lowered_components:
        if "gc" in lowered_subcomponents:
            return "gc"  # should already be excluded upstream, keep visible if not
        return "runtime_core"

    if "core-svc" in lowered_components:
        return "runtime_core"

    if "infrastructure" in lowered_components:
        return "test_infra"

    if "tools" in lowered_components:
        if lowered_subcomponents & {sub.lower() for sub in COMPILER_SUBCOMPONENTS}:
            return "compiler_tools"
        if TEST_INFRA_KEYWORDS.search(text):
            return "test_infra"
        return "compiler_tools"

    if "client-libs" in lowered_components:
        return "classlib"

    if "core-libs" in lowered_components:
        if lowered_subcomponents & {sub.lower() for sub in INTEROP_SUBCOMPONENTS}:
            return "interop"
        if INTEROP_KEYWORDS.search(text):
            return "interop"
        return "classlib"

    if INTEROP_KEYWORDS.search(text):
        return "interop"

    return "other"


def detect_highlight_tags(issue: IssueData) -> list[str]:
    text = f"{issue.summary}\n{issue.description}" if issue.description else issue.summary
    lowered_labels = {label.lower() for label in issue.labels}

    tags: list[str] = []
    if PERFORMANCE_KEYWORDS.search(text) or lowered_labels & PERF_LABELS:
        tags.append("performance_regression")
    if SPEC_KEYWORDS.search(text):
        tags.append("spec_change")
    if TEST_INFRA_KEYWORDS.search(text):
        tags.append("test_infra")
    return tags


def build_row(issue: IssueData, classification: IssueClassification) -> AggregatedRow:
    release = determine_release(issue)
    feature_area = select_feature_area(issue)
    highlight_tags = detect_highlight_tags(issue)

    impact_status = "excluded" if classification.category == "excluded" else "needs_review"
    action_required = "対応不要" if impact_status == "excluded" else "要確認"

    impact_notes = ""
    applied_rules = ""
    if classification.matches:
        rule_names = [match.name for match in classification.matches]
        applied_rules = ",".join(rule_names)
        details = [match.details for match in classification.matches if match.details]
        if details:
            impact_notes = " | ".join(details)
        else:
            impact_notes = "rule applied"

    return AggregatedRow(
        issue_id=issue.key,
        release=release,
        impact_status=impact_status,
        feature_area=feature_area,
        highlight_tags=";".join(highlight_tags),
        action_required=action_required,
        impact_notes=impact_notes,
        applied_rules=applied_rules,
        summary=issue.summary,
        components="/".join(issue.components),
        subcomponents="/".join(issue.subcomponents),
        labels=",".join(issue.labels),
        fix_versions="/".join(issue.fix_versions),
    )


def write_detail_report(path: Path, rows: Sequence[AggregatedRow]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(
            [
                "issue_id",
                "release",
                "impact_status",
                "feature_area",
                "highlight_tags",
                "action_required",
                "impact_notes",
                "applied_rules",
                "summary",
                "components",
                "subcomponents",
                "labels",
                "fix_versions",
            ]
        )
        for row in rows:
            writer.writerow(
                [
                    row.issue_id,
                    row.release,
                    row.impact_status,
                    row.feature_area,
                    row.highlight_tags,
                    row.action_required,
                    row.impact_notes,
                    row.applied_rules,
                    row.summary,
                    row.components,
                    row.subcomponents,
                    row.labels,
                    row.fix_versions,
                ]
            )


def write_release_summary(path: Path, rows: Sequence[AggregatedRow]) -> None:
    counter: Counter[tuple[str, str]] = Counter()
    for row in rows:
        counter[(row.release, row.impact_status)] += 1
    records = sorted(counter.items(), key=lambda item: (item[0][0], item[0][1]))

    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["release", "impact_status", "count"])
        for (release, impact_status), count in records:
            writer.writerow([release, impact_status, count])


def write_area_summary(path: Path, rows: Sequence[AggregatedRow]) -> None:
    counter: Counter[tuple[str, str, str]] = Counter()
    for row in rows:
        counter[(row.release, row.feature_area, row.impact_status)] += 1
    records = sorted(counter.items(), key=lambda item: (item[0][0], item[0][1], item[0][2]))

    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["release", "feature_area", "impact_status", "count"])
        for (release, feature_area, impact_status), count in records:
            writer.writerow([release, feature_area, impact_status, count])


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Aggregate classified JDK issues")
    parser.add_argument(
        "--source-dir",
        type=Path,
        default=Path("step4.非互換抽出/jdk_issues"),
        help="Directory containing classified issue XML files",
    )
    parser.add_argument(
        "--extra-source",
        type=Path,
        action="append",
        default=[],
        help="Additional directories to resolve backport sources",
    )
    output_root = Path.cwd() / "csv"
    parser.add_argument(
        "--detail-report",
        type=Path,
        default=output_root / "jdk_issues_summary_detail.csv",
        help="Detail CSV output path",
    )
    parser.add_argument(
        "--release-summary",
        type=Path,
        default=output_root / "jdk_issues_summary_release.csv",
        help="Release summary CSV output path",
    )
    parser.add_argument(
        "--area-summary",
        type=Path,
        default=output_root / "jdk_issues_summary_area.csv",
        help="Feature area summary CSV output path",
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)

    repository = IssueRepository([args.source_dir, *args.extra_source])
    classifier = IssueClassifier(repository)

    issues = sorted(repository.issues_in_dir(args.source_dir), key=lambda issue: issue.key)
    rows = [build_row(issue, classifier.classify(issue)) for issue in issues]

    write_detail_report(args.detail_report, rows)
    write_release_summary(args.release_summary, rows)
    write_area_summary(args.area_summary, rows)

    print(f"Detail report: {args.detail_report}")
    print(f"Release summary: {args.release_summary}")
    print(f"Feature area summary: {args.area_summary}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
