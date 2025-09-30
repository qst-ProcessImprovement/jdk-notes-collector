# Statement of Work: OpenJDK XMLダウンロードスクリプト

## 背景と目的
- 指定JQLのOpenJDK課題検索結果をXML形式で保存する定型作業を自動化し、再現性を確保する。

## 成果物
- `Phage2/run/openjdk/...` 配下に配置するダウンロードスクリプト（言語: Python予定）。
- 出力先: `Phage2/1.INPUT作成/1.情報源/OpenJDK/SearchRequest.xml` を更新/生成。
- 実行手順メモ（必要に応じて作業メモへ反映）。

## スコープ
- HTTPSでのXML取得とファイル保存処理の実装。
- 既存ディレクトリ構成に即したスクリプト配置と命名。
- ネットワークエラー/HTTP異常に対する最小限の例外処理。

## 非スコープ
- 取得XML内容の整形や解析。
- スケジューラや常駐実行の仕組み導入。

## 影響調査 (LSP)
- 参考解析: `Phage2/run/openjdk/jdk_issue_id_extractor.py` に以下の既存シンボルを確認（変更予定なし）。
  - `BASE_DIR`, `INPUT_DIR`, `_JDK_ID_PATTERN`, `extract_jdk_issue_ids`, `write_issue_ids`, `iter_input_files`, `deduplicate_issue_ids`, `sort_issue_ids`, `format_duplicates`, `main`
- 新規スクリプト追加のため既存シンボルへの直接影響は想定せず。

## AT (Atomic Tasks)
1. 既存`Phage2/run/openjdk`配下の命名・役割を確認し、スクリプト配置方針を確定。
2. ダウンロードスクリプトの骨子（引数無しで指定URLから保存）を実装。
3. HTTP応答検証とエラー処理（ステータスコード、保存パス存在確認）を追加。
4. `Phage2/1.INPUT作成/1.情報源/OpenJDK/SearchRequest.xml` への書き込み動作を確認。
5. 実行・検証結果をまとめ、利用手順を記載。

## テスト計画
- 手動テスト: スクリプトをローカル実行し、正常終了と生成ファイル内容を確認。
- ネットワーク制限により実行できない場合は、モック/証跡を示し利用者実行を前提とした確認ポイントを提示。
