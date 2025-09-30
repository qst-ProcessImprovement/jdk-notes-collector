# Statement of Work: OpenJDK Fix Version XML Fetcher

## 目的
- OpenJDK JIRA の検索結果 XML を JDK 21.0.x 系列の fixVersion ごとに取得し、モジュール実行時のカレントディレクトリ直下にある `OpenJDK` フォルダへ保存する。
- スクリプトは `Phage2/run/fetch` 配下に配置し、モジュール名は `fetch_openjdk_fix_versions.py` とする。

## スコープ
- 対象 fixVersion: 21.0.1〜21.0.8（先頭付近でリストとして定義し、容易に変更可能とする）。
- JIRA 検索 URL: `https://bugs.openjdk.org/sr/jira.issueviews:searchrequest-xml/temp/SearchRequest.xml?jqlQuery=project+%3D+JDK+AND+status+in+%28Closed%2C+Resolved%29+AND+fixVersion+%3D+<FIX_VERSION>` をバージョンごとに発行し XML を取得。
- 出力: 実行時カレントディレクトリ配下の `OpenJDK/<FIX_VERSION>.xml`（存在しない場合は `OpenJDK` ディレクトリを生成）。

## 影響調査 (LSP)
- 新規ファイル追加のみ。既存シンボルへの直接影響なし。

## タスク分解 (AT)
1. `Phage2/run/fetch` 内の既存構造確認。
2. `fix_versions` 定数と JIRA ベース URL を備えたダウンロードスクリプトを実装。
3. ネットワークエラー・HTTP 異常終了時のハンドリングとメッセージ出力を実装。
4. 保存処理（ディレクトリ生成・XML 保存）を実装。
5. 実行方法・既知の制約（ネットワーク制限下では動作確認不可）を README コメント等で共有。

## 成果物
- `Phage2/run/fetch/fetch_openjdk_fix_versions.py`。
- 既存コードへの影響なし。

## テスト方針
- ネットワーク制限のため実際のダウンロードテストは不可。構文確認および dry-run ログで確認予定。
- 実運用時は `python fetch_openjdk_fix_versions.py` を実行し XML が出力されることを確認してもらう。

## リスク・前提条件
- オフライン環境では HTTP 取得不可。
- URL 形式が変更された場合は修正が必要。

## 承認依頼事項
- 上記スコープとタスクで実装を進めてもよいか確認をお願いします。
