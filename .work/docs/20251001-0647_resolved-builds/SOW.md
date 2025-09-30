# Statement of Work: OpenJDK "resolved in build" XML 収集スクリプト作成

## 背景 / 目的
既存の `fetch_openjdk_fix_versions.py` をベースにした知見を参考にしつつも、依存しない独立モジュールとして、JDK 21 の "Resolved In Build" 値 `b1`〜`b35` を対象とした JIRA XML を取得し、各ビルドごとの XML 保存と、取得済み XML の統合ファイルを生成するスクリプトを整備する。

## スコープ
- 対象リポジトリ: `jdk-notes-collector`
- 対象ディレクトリ: `Phage2/run/fetch/`
- 追加コンポーネント: 新規 Python モジュール（名称案: `fetch_openjdk_resolved_builds.py`）
- 既存モジュールとのコード共有・インポート禁止（独立した実装）

## 参考・影響シンボル（LSP 抽出）
- `Phage2/run/fetch/fetch_openjdk_fix_versions.py`
  - 定数: `FIX_VERSIONS`, `JIRA_SEARCH_URL_TEMPLATE`, `OUTPUT_DIRECTORY_NAME`, `REQUEST_TIMEOUT_SECONDS`, `USER_AGENT`
  - 関数: `build_request_url`, `fetch_xml`, `write_xml`, `download_fix_version_xml`, `download_all_fix_versions`, `main`
  - ※構造把握の参照のみ。新規モジュールはインポート・共通化せず、自前で実装する。

## 作業項目（Atomic Tasks）
1. `fetch_openjdk_fix_versions.py` の構造・例外処理方針の確認。
2. 新規モジュール `fetch_openjdk_resolved_builds.py` の雛形作成（定数・処理フローを独立実装）。
3. `b1`〜`b35` の各ビルドに対して XML を取得するロジック実装。
   - HTTP エラー時のリトライは行わず、エラー内容を `stderr` に出力。
   - XML 内 `<issue total="0">` の場合は「存在しない」と見なし、標準出力にメッセージを表示して保存をスキップ。
4. 正常取得した XML を出力ディレクトリ（案: `output/resolved_in_build/`）に `bXX.xml` として保存。
5. 取得済み XML を統合する大きな XML を生成し、別ファイル（案: `output/resolved_in_build/all_builds.xml`）へ出力。
   - ルート要素にメタ情報（生成日時、対象 fixVersion など）を付与。
   - 各ビルドの XML コンテンツを子要素として内包。
6. 実行手順・出力概要を docstring またはコメントで記述。
7. 動作確認としてスクリプトを実行し、XML が生成されることを確認（ネットワークアクセス前提）。

## 成果物
- 新規ファイル: `Phage2/run/fetch/fetch_openjdk_resolved_builds.py`
- 出力ファイル（実行時生成）:
  - `output/resolved_in_build/bXX.xml` （存在するビルドのみ）
  - `output/resolved_in_build/all_builds.xml`
- 実行ログ（標準出力 / 標準エラー）

## 想定外事項・除外事項
- 既存スクリプトへの機能追加・改修は行わない。
- XML の内容変換（XSLT 等）は行わない。
- ネットワーク障害時の再試行やレート制限対策は対象外。

## 承認依頼
上記内容で作業を進めてもよろしいでしょうか。ご確認をお願いします。
