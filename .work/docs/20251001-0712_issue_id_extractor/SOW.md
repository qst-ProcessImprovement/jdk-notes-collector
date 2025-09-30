# Statement of Work: issue_id_extractor モジュール調査

## 目的
- `Phage2/run/fetch/issue_id_extractor.py` の処理内容とモジュール全体の役割を明確化し、利用者に説明できるよう整理する。

## スコープ
- 対象ファイル: `Phage2/run/fetch/issue_id_extractor.py`
- 影響シンボル: LSP 取得より以下の関数・定数群を調査対象とする。
  - 定数: `XML_DIR`, `OUTPUT_DIR`, `OUTPUT_FILENAME`, `ISSUE_KEY_PATTERN`
  - 関数: `iter_xml_files`, `extract_issue_ids_from_item`, `extract_issue_ids`, `issue_sort_key`, `normalize_issue_ids`, `collect_issue_ids`, `ensure_parent_directory`, `write_issue_ids`, `write_individual_outputs`, `write_aggregated_output`, `main`
- コード修正は実施しない。既存ロジックの理解・説明のみ。

## アプローチ
1. LSP 情報を基に対象シンボルを洗い出す（実施済み）。
2. ソースコードを精読し、入出力・処理フローを整理する（実施中）。
3. 調査結果を日本語でまとめ、ユーザーへ報告する。

## 成果物
- モジュールの目的・データフロー・主要関数の役割を整理した説明（テキスト）。

## 想定スケジュール
- 本セッション内で完了予定。

## リスク・前提
- XML 構造や出力ディレクトリ構成が前提通りであること。
- 調査のみのためシステムへの副作用は発生しない。

上記方針で進めてもよろしいでしょうか？
