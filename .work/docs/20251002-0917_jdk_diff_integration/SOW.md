# Statement of Work: fetch_openjdk_resolved_builds.py への JDK 差分レポート統合

## 背景 / 目的
- 現状 JDK 差分レポートは `Phage2/run/mapping/jdk_diff_report.py` で個別に生成している。
- 収集スクリプト (`Phage2/run/fetch/fetch_openjdk_resolved_builds.py`) 側で issue_ids 出力を纏める設計に一本化し、差分レポートの生成元を統合したい。
- 実行ディレクトリ内の `builds/issue_ids` を正準入力ディレクトリとして利用するよう変更する。

## 対応範囲 (スコープ)
1. `fetch_openjdk_resolved_builds.py` に差分レポート生成ロジックを移植・統合する。
2. レポート作成時に参照するファイルパスをカレントディレクトリ配下の `builds/issue_ids` 固定に変更する。
3. レポート出力処理を fetch スクリプトのメインフローに組み込み、`jdk_diff_report.md` を生成する。
4. 移植したロジックに合わせて例外クラスや補助関数（表生成、Fix Version 読込等）を整理し、重複しない正準定義へ統合する。
5. 既存処理（OpenJDK/OracleJDK/Temurin の issue_ids 出力）との連携を確認する。

## 非対象 (アウト・オブ・スコープ)
- `jdk_diff_report.py` の削除はユーザー側で実施予定のため、本作業では行わない。
- JIRA からの取得仕様や Temurin 入力仕様の変更は行わない。
- 新規テストコードの追加は必要性が生じた場合のみ検討する。

## 想定成果物
- `Phage2/run/fetch/fetch_openjdk_resolved_builds.py`: 差分レポート統合済みのコード。
- `builds/jdk_diff_report.md`: スクリプト実行時に生成される Markdown レポート (出力仕様が変わらないことを確認)。

## 影響シンボル (LSP 抽出)
- `Phage2/run/fetch/fetch_openjdk_resolved_builds.py`
  - 関数: `generate_issue_id_outputs`, `main`, `build_issue_backport_map`, `collect_issue_ids_from_directory`, `write_issue_lines`, `write_aggregate_xml`
  - 追加予定関数: `load_issue_ids`, `build_diff_table`, `render_table`, `generate_jdk_diff_report` など (元 `jdk_diff_report.py` より移植)
- `Phage2/run/mapping/jdk_diff_report.py`
  - 関数: `build_report`, `build_diff_table`, `load_issue_ids`, `make_fix_version_loader`, `render_table`, `main`

## 作業手順 (AT)
1. 差分レポート関連関数を `fetch_openjdk_resolved_builds.py` へ移植し、`builds/issue_ids` 参照に合わせたパス解決を実装する。
2. fetch メインフロー (`main`) にレポート生成処理を追加し、既存出力完了後に Markdown を生成する。
3. 必要な補助関数や例外ハンドリングを統合・整理する。
4. ローカル実行によりレポート生成が機能すること、および既存機能に回帰がないことを確認する。

## リスク / 留意点
- issue_ids 集約ファイルが存在しない場合のエラー処理を適切に行う必要がある。
- Temurin backport 情報のフォーマットが正準形であることを保持する。
- 大規模ファイルへの関数追加となるため、可読性と依存関係の整理に注意する。

## 確認事項
- 上記 SOW に問題なければ、作業を開始します。修正方針に調整が必要な場合はご指示ください。
