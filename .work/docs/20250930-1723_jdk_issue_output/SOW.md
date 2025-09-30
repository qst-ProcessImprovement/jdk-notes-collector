# SOW: JDK issue ID extractor 出力ファイル命名変更

## 目的
- JDK issue ID 抽出結果の出力ファイル名を `jdk-` プレフィックス付き `*.md` 形式で `output_openjdk/` 配下に統一する

## スコープ
- `Phage2/run/openjdk/jdk_issue_id_extractor.py`

## 対応方針
1. `main` 内で決定している出力先ディレクトリを `output_openjdk/` に変更
2. 元の Markdown 名から拡張子を `.md` に固定しつつプレフィックス `jdk-` を付与する処理を維持
3. 既存処理（ID 抽出・重複検出・書き込みロジック）の挙動は変更しない

## 影響範囲（LSP 情報）
- `main`（出力パス組み立てを担当）
  - 呼び出し元: モジュール実行時のエントリポイント
- `write_issue_ids`（新ファイル名での書き込み）
  - 呼び出し元: `main`

## 検証方針
- スクリプトを対象ディレクトリで実行し、生成ファイル名が `output_openjdk/jdk-<元ファイル名のstem>.md` となることを確認
- 既存の重複警告出力が従来通り表示されることを目視確認
