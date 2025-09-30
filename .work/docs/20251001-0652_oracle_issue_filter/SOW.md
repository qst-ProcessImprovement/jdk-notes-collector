# Statement of Work: Oracle版Fix Version取得モジュール追加

## 背景 / 目的
- 現在 `Phage2/run/fetch/fetch_openjdk_fix_versions.py` は特定の Fix Version (21.0.x 系) の OpenJDK JIRA XML を取得している。
- Oracle 版に固有の Issue のみを取得する独立モジュールが存在せず、Oracle 向けの差分整理や分析を自動化できていない。
- 依頼は当該モジュールを複製し、Oracle 版 Issue だけを取得するよう改修した新しいモジュールを追加すること。

## 既存調査 (LSP 使用結果)
対象ファイル: `Phage2/run/fetch/fetch_openjdk_fix_versions.py`
- 定数: `FIX_VERSIONS`, `JIRA_SEARCH_URL_TEMPLATE`, `OUTPUT_DIRECTORY_NAME`, `REQUEST_TIMEOUT_SECONDS`, `USER_AGENT`
- 関数: `build_request_url`, `fetch_xml`, `write_xml`, `download_fix_version_xml`, `download_all_fix_versions`, `main`
  - いずれも新モジュール側で再定義する必要がある (独立運用のため)

## スコープ
- 同一ディレクトリに Oracle 版 Issue 専用モジュール (仮称: `fetch_oracle_fix_versions.py`) を新規作成。
- 既存モジュールや他モジュールへの依存を追加しない (完全独立)。
- 出力形式 (Fix Version ごとの XML 保存) は現行ロジックを踏襲。
- Fix Version の管理は Oracle 版専用の正準値 `21.0.x-oracle` を使用し、OpenJDK 版とは別リストとして保守する。

## アプローチ / タスク (Atomic Tasks)
1. Oracle 版 Issue を識別するための JIRA 検索条件 (JQL) の確定。
   - 例: `project = JDK AND status in (Closed, Resolved) AND fixVersion = {fix_version}`
   - Oracle 版は `fixVersion = 21.0.x-oracle` として管理されるため、追加フィールドは不要。
2. 新規モジュール骨子の作成。
   - 既存モジュール構造をベースにしつつ、定数・ドキュメント文字列・出力先名称などを Oracle 専用に調整。
3. JIRA リクエスト URL テンプレートの実装。
   - Oracle 条件を含む JQL を URL エンコードしたテンプレートを定義。
4. 実装および静的検証。
   - 型ヒント・例外処理は既存モジュールと整合させる。
   - 実際の HTTP リクエストは行わず、コード整合性を確認。
5. 必要に応じたテキスト出力・利用方法の README コメント整備 (最小限)。

## 成果物
- 新規 Python モジュール: `Phage2/run/fetch/fetch_oracle_fix_versions.py` (ファイル名は合意後に確定)
- 既存ロジックとの整合がとれること (CLI から単体実行可能)。

## 検証 / 受入基準
- `python Phage2/run/fetch/fetch_oracle_fix_versions.py` 実行時に対象 Fix Version ごとに Oracle 版 Issue の XML が生成される想定。
- HTTP エラー時のリトライは範囲外だが、レスポンスコード 200 以外で例外が送出される現行仕様を踏襲する。
- flake8 等の品質チェックは依頼範囲外。PEP 8 ベースのスタイルを維持。

- Oracle 版 Fix Version (`21.0.x-oracle`) の追加や更新が発生した際は、モジュール定義を手動更新する必要がある。
- JIRA 側で名前が変更されると検索 URL も更新が必要となる可能性がある。

## 想定外 / 対象外
- 既存モジュール (`fetch_openjdk_fix_versions.py`) への変更。
- Oracle Issue の追加加工や XML 解析ロジックの実装。
- ネットワークアクセスのテスト実行。

ご確認のうえ、Oracle 版 Issue を抽出するための具体的な条件 (フィールド名・値) と併せて承認をお願いします。
