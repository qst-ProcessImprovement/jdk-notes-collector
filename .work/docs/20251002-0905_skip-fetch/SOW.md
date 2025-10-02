# 対応概要 (SOW)

## 背景
- `Phage2/run/fetch/fetch_openjdk_resolved_builds.py` 実行時、既に保存済みの Issue XML に対しても `[INFO] ... 保存しました` ログが出力される。
- 現行実装では `collect_resolved_in_build_xml` で既存ファイルを再利用するが、その後の `save_individual_xml` が無条件に書き出すため、実質的に毎回同一ファイルを上書きしている。
- 要望: 取得済み (ローカルにファイルが存在する) 場合はダウンロードおよび再保存をスキップし、不要な上書きやログを抑止する。

## 対応方針
1. `collect_resolved_in_build_xml` で新規取得か再利用かを識別し、呼び出し側へ伝える仕組みを追加する。
2. `main` で再利用判定を参照し、新規取得時のみ `save_individual_xml` で保存・ログ出力を行うよう制御する。
3. 既存ファイルを再利用した場合は保存処理とログをスキップすることで、ネットワークアクセスとディスク書き込みの両方を抑制する。

## 影響範囲 (Serena LSP)
- `Phage2/run/fetch/fetch_openjdk_resolved_builds.py:638` `write_xml`
- `Phage2/run/fetch/fetch_openjdk_resolved_builds.py:662` `fetch_build_xml`
- `Phage2/run/fetch/fetch_openjdk_resolved_builds.py:702` `save_individual_xml`
- `Phage2/run/fetch/fetch_openjdk_resolved_builds.py:741` `collect_resolved_in_build_xml`
- `Phage2/run/fetch/fetch_openjdk_resolved_builds.py:777` `main`

## タスク分解 (AT)
1. 既存フローの再確認と「再利用判定」データの受け渡し設計。
2. `collect_resolved_in_build_xml` および `main` を改修し、新規取得時のみ保存するロジックを実装。
3. ログ出力の変化を確認し、再実行時に保存ログが抑止されることを確認するためのテスト／手順を整理。

## 懸念・前提
- XML が更新されるケースを想定し、意図的に再取得したい場合は既存ファイルを削除する運用とする。
- 既存の集約処理 (`write_aggregate_xml` や issue ID 出力) は再利用データでも同様に実行するため、データ構造の変更に伴う副作用に注意する。
