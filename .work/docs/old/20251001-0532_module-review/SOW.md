# Statement of Work: `Phage2/run/temurin/issue_ids.py` モジュール調査

## 目的
- Temurin リリースノート処理モジュールの役割と振る舞いを把握し、要約を提供する。

## 作業範囲
1. LSP シンボル情報を取得し、主要関数・定数を特定する。
2. ソースコードを確認し、入出力・副作用・エラー処理を分析する。
3. 調査結果として、モジュール全体の処理フローと各主要関数の責務をドキュメント化する。

## 想定成果物
- モジュール処理内容の日本語説明（ChatGPT 応答）。

## 影響シンボル
- `_iter_release_notes`
- `collect_issue_ids`
- `_sorted_unique`
- `_sorted_duplicates`
- `_canonical_output_filename`
- `_write_unique_ids`
- `main`

## 前提・制約
- 調査のみでコード修正は行わない。
- 既存のファイル構成・命名規則を尊重する。

## 進行状況
- [x] シンボル調査・コード確認
- [x] 調査結果まとめ
