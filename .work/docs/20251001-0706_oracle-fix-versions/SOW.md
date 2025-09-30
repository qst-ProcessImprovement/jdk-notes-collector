# Statement of Work: Oracle 版 JDK Fix Version 収集モジュール追加

## 背景
- 既存モジュール `Phage2/run/fetch/fetch_openjdk_fix_versions.py` は OpenJDK 向けの Fix Version 一覧に限定して JIRA XML を収集している。
- Oracle 版のみを対象とした独立モジュールを新設し、Oracle 専用の Fix Version を使用して同様の XML 収集を行いたい。

## 目的
- Oracle JDK 21 系専用の Fix Version 名称に基づき、Closed/Resolved チケットの検索結果を XML でダウンロードするスクリプトを追加する。
- 既存モジュールからの直接参照に依存しない独立実装とする。

## スコープ
- 新規ファイル `Phage2/run/fetch/fetch_oracle_fix_versions.py` の追加
- Oracle 版 Fix Version 名称の調査と正準リストの定義
- 既存 OpenJDK 版モジュールと同等の関数構成・振る舞いを Oracle 版で再実装

## 非対象
- 既存 OpenJDK 版モジュールの修正や統合
- 他モジュールからのインポート・共通化
- JDK 21 以外の Oracle 版 Fix Version 収集

## 調査結果・前提
- `https://bugs.openjdk.org/rest/api/2/project/JDK/versions` の REST API から Oracle 版 Fix Version 名の一覧取得を確認。
- `"21."` で始まり `"-oracle"` を含む Fix Version 名のうち、JavaFX (`jfx` プレフィックス) と `21-pool-oracle` を除外したリストを採用予定。
- 想定 Fix Version 候補:
  - 21.0.3-oracle
  - 21.0.4-oracle / 21.0.4.0.1-oracle / 21.0.4.0.2-oracle
  - 21.0.5-oracle
  - 21.0.6-oracle
  - 21.0.7-oracle / 21.0.7.0.0.1-oracle / 21.0.7.0.1-oracle
  - 21.0.8-oracle / 21.0.8.0.1-oracle / 21.0.8.0.2-oracle
  - 21.0.9-oracle
  - 21.0.10-oracle
  - 21.0.11-oracle
  - 21.0.12-oracle
  - 21.0.13-oracle
  - 21.0.14-oracle
  - 21.0.15-oracle
- 21.0.1-oracle / 21.0.2-oracle は REST 一覧上で確認できず、現行では公開されていないと判断。
- 追加確認事項: `21-pool-oracle` を対象に含める必要がある場合は指示を要請。

## 影響シンボル (LSP 調査)
- `Phage2/run/fetch/fetch_openjdk_fix_versions.py`
  - 定数: `FIX_VERSIONS`, `JIRA_SEARCH_URL_TEMPLATE`, `OUTPUT_DIRECTORY_NAME`, `REQUEST_TIMEOUT_SECONDS`, `USER_AGENT`
  - 関数: `build_request_url`, `fetch_xml`, `write_xml`, `download_fix_version_xml`, `download_all_fix_versions`, `main`

## タスク分解 (AT)
1. Oracle 版 Fix Version 名称リストの最終確定 (必要なら `21-pool-oracle` の取り扱い確認)。
2. `fetch_openjdk_fix_versions.py` を基に、Oracle 版 Fix Version リストを組み込んだ新規モジュールを `fetch_oracle_fix_versions.py` として作成。
3. 実装の静的検証 (Lint/型チェックが未導入のため `python -m compileall Phage2/run/fetch/fetch_oracle_fix_versions.py` で構文確認予定)。
4. ドキュメント (README 等) の更新は必要なしと想定、必要になれば別途協議。

## 成果物
- 新規 Python スクリプト `Phage2/run/fetch/fetch_oracle_fix_versions.py`
- (必要に応じて) 簡易動作確認ログ

## 検収観点
- Oracle 版 Fix Version に限定した XML 取得が行えること。
- ネットワーク障害時に OpenJDK 版と同等のエラーハンドリングを行うこと。
