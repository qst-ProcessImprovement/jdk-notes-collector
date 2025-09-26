# 除外ルールと「要確認」基準まとめ

このドキュメントは、JDK 21.0.5 → 21.0.8 の差分調査で使用している自動分類ロジックを
共有し、資料作成担当者が判定方針を把握しやすくするためのメモです。

## 判定フロー概要

`filter_jdk_issues.py` で Issue を解析し、以下の除外ルールのいずれかに
一致した場合は `excluded`、どれにも一致しなかった場合は `review`（= 要確認）として
分類されます。集計側 (`step4.Issueサマリ/aggregate_jdk_issues.py`) では
`impact_status` にこの結果を引き継いでいます。

### doc_or_test（ドキュメント・テスト専用変更）
- summary / description / comment に `open source`, `problemlist`, `jtreg`, `doc` などの
  キーワードが複数含まれる。
- ラベルに `noreg-*` や `hgupdate-sync` が付いている。
- ただし同じ文章内に `crash`, `exception`, `regression` があれば除外対象から外す。

### new_feature（新機能バックポート）
- Issue が Backport で、参照元 Issue の type が `Enhancement` または `New Feature`。
- summary に `Add / Introduce / Support / Implement` のいずれかを含み、`doc` や `test`
  を含まない。
- fixVersion が 22 / 23 / 24 など将来リリースで、Backport 側の summary と一致。
- ラベルに `22-na` など将来リリース向けの NA ラベルが付いている場合も同様に除外。

### non_windows11_platform（Windows 11 以外のプラットフォーム限定）
- summary / description / customfield[OS] に Linux, macOS, AIX, Solaris, Windows 7/10 など
  Win11 以外の OS が出現。
- 同じテキストに Windows 11 の記載がない。
- OS フィールドで Win11 が明示されていれば除外対象にはしない。

### gc_related（GC 関連の修正）
- component が `hotspot` かつ subcomponent が `gc`。
- summary / description に `GC`, `Garbage`, `Shenandoah`, `ZGC`, `G1` などを含む。
- ラベルが `gc-*` の場合も対象。

## 「要確認 (needs_review)」となるケース

上記いずれの除外ルールにも当てはまらない Issue は、互換性影響の可能性があるものと
して「要確認」に分類します。集計レポートでは以下の列で識別できます。

- `impact_status`: `needs_review` が要確認、`excluded` が除外済み。
- `action_required`: `要確認` または `対応不要`。
- `applied_rules` / `impact_notes`: 除外された場合の具体的なルール名と根拠。

## 参考ファイル

- `filter_jdk_issues.py` : 除外判定ロジックの実装。
- `step4.Issueサマリ/aggregate_jdk_issues.py` : 集計と説明用 CSV 出力の実装。
- `csv/jdk_issues_summary_detail.csv` : 個別 Issue の判定内容。

担当者は、`needs_review` の項目を重点的に確認し、必要に応じて影響評価や対応方針を
資料に落とし込んでください。
