# SOW: ログ原因調査

## 目的
`[INFO] {fix_version} {build_number}: 対応する課題が見つかりません (保存をスキップ)` が出力される条件を特定し、利用者に説明する。

## スコープ
- `Phage2/run/fetch/fetch_openjdk_resolved_builds.py`
  - `extract_issue_total` (L1262-L1283): JIRA 検索結果 XML の `<issue total="...">` 属性値を整数に変換して返却する。
  - `fetch_build_xml` (L1295-L1319): XML を取得して課題総数を検査し、0 件時に当該 INFO ログを出力する。

## 調査結果（確証済み）
1. `fetch_build_xml` は JIRA から取得した XML を `extract_issue_total` で解析し、課題総数 (`issue_total`) が 0 の場合に INFO ログを出力して `FetchOutcome.NOT_FOUND` を返すことを確認済み。
   - 参照: `Phage2/run/fetch/fetch_openjdk_resolved_builds.py:1295`
2. `extract_issue_total` は `<channel><issue total="N">` の `total` 属性を整数化して返し、XML に課題が 0 件のとき `issue_total == 0` を返す。
   - 参照: `Phage2/run/fetch/fetch_openjdk_resolved_builds.py:1262`

## アウトオブスコープ
- 他バージョンのログ整合性検証
- XML 取得元の JIRA 側設定変更
- 追加の機能開発や例外処理変更

## 次アクション
- 調査結果をユーザーへ報告（本回答）。
