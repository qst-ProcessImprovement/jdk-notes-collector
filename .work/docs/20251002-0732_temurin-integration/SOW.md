# Statement of Work: Temurin Issue ID 統合

## ゴール
- Temurin リリースノート由来の Issue ID 抽出処理を `fetch_openjdk_resolved_builds.py` に統合し、単一スクリプトで OpenJDK/OracleJDK/Temurin の集約を実行できるようにする。
- 統合後は `Phage2/run/temurin/issue_ids.py` を廃止し、出力先を `builds/issue_ids/all_issue_ids_temurin.txt` に集約する。

## 対応方針
1. `fetch_openjdk_resolved_builds.py` に Temurin 用の抽出ロジックを移植し、入力ディレクトリをカレント配下の `INPUT/temurin` へ切り替える。
2. Temurin 特有の backport 解決・フォーマット処理を既存の Issue ID 出力ユーティリティへ組み込み、余計な重複を避ける。
3. 統合完了後に `Phage2/run/temurin/issue_ids.py` を削除し、旧出力ディレクトリ依存を解消する。

## LSPで確認した影響シンボル
- `Phage2/run/fetch/fetch_openjdk_resolved_builds.py:199` `generate_issue_id_outputs`
- `Phage2/run/fetch/fetch_openjdk_resolved_builds.py:413` `main`

## 想定成果物
- `builds/issue_ids/all_issue_ids_temurin.txt`
- 必要に応じて `builds/issue_ids/temurin/per_file/*.txt`（Temurin 個別ファイル出力が求められる場合）

## 確認事項 / リスク
- `INPUT/temurin` が未作成の場合、エラーとして明示し処理を中断する。
- Temurin Backport 元 Issue を照合するために参照する `Phage1/run/jdk_issues` のパスは CWD 基準で再解決する。

問題なければこの方針で実装を進めます。修正進行の可否をご確認ください。
