# Statement of Work: OpenJDK Issue ID 抽出モジュール作成

## 背景と目的
- `Phage2/run/fetch/OpenJDK/*.xml` に格納された OpenJDK JIRA 検索結果から、JDK バージョンアップ対応 issue ID の一覧を抽出し、再利用可能な形でファイル出力したい。
- Backport issue は真の元 issue ID のみを残す必要があり、正準表現原則に従った ID 集約の仕組みを新設する。

## スコープ
- Python 標準ライブラリのみで XML を解析し、issue ID を収集・整形するモジュールを `Phage2/run/fetch` 配下に新規作成する。
- Backport 判定ロジックを実装し、元 issue の ID へ正規化する。
- 収集した ID を重複排除し、安定した順序（辞書順）でファイルに書き出す CLI エントリポイントを提供する。

## 非スコープ
- XML の取得ロジック（`fetch_openjdk_fix_versions.py`）の変更。
- JIRA への追加アクセスや XML スキーマ変更対応。

## 作業項目 (Atomic Tasks)
1. XML サンプル構造の確認と Backport リンク表現の調査。
2. 新規モジュール骨子作成（入出力仕様、CLI インタフェースの定義）。
3. XML 解析・Backport 正規化・ID 集約処理の実装。
4. ファイル出力・エラーハンドリング実装と静的検証（self review）。

## 影響範囲 (LSP 調査結果)
- `Phage2/run/fetch/fetch_openjdk_fix_versions.py`: 定義済みシンボル {`FIX_VERSIONS`, `JIRA_SEARCH_URL_TEMPLATE`, `OUTPUT_DIRECTORY_NAME`, `REQUEST_TIMEOUT_SECONDS`, `USER_AGENT`, `build_request_url`, `fetch_xml`, `write_xml`, `download_fix_version_xml`, `download_all_fix_versions`, `main`}（既存・参照のみ、変更予定なし）。
- 新規ファイル（仮称）`Phage2/run/fetch/collect_openjdk_issue_ids.py` を追加予定。既存呼び出し元は存在しないため、導入後に利用箇所を別途検討可能。

## 元 issue ID 取得方法
- `<item>` 配下の `<issuelinks>` に `Backport` タイプが存在する場合、`<issuelinktype><name>Backport</name>` 配下の `<issuelink><issuekey>` 要素に元 issue の ID が記載されている。
- Backport issue 判定により `<key>` と `<issuelinks>` 内の issue ID が一致しない場合は、後者を正とみなし ID を正規化する。
- Backport 情報が複数存在する場合は、最初の `backport of` リンクを採用し、複数リンクが矛盾するケースはエラーとして検出する。
- Backport 情報が欠落しているにもかかわらず issue タイプが Backport の場合は、入力データ不整合として警告を出力し、該当 issue をスキップする（正準表現原則の維持）。

## 成果物
- `Phage2/run/fetch/collect_openjdk_issue_ids.py`: issue ID 抽出・ファイル出力モジュール。
- `OpenJDK/issues.txt`（想定）: 最新抽出結果（必要に応じて生成）。

## 検証方針
- モジュール単体を CLI で実行し、全 XML を入力に issue ID リストを生成する。
- 出力のサンプル確認（Backport のみを含む issue が元 ID に正規化されていることを spot check）。

## リスク・懸念
- XML 構造が将来的に変わった場合の保守コスト。
- Backport 情報が欠落している項目が存在する場合の取り扱い（エラーメッセージで通知予定）。
