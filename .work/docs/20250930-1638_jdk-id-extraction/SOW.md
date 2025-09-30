# Statement of Work

- 対象: `Phage2/run/openjdk/OpenJDK` 配下の全ファイルから JDK 番号（`JDK-` に続く数値）を抽出し、実行時カレントディレクトリ配下にハードコードされた `issue_ids` フォルダを生成のうえ同名ファイルとして出力する Python モジュールを `Phage2/run/openjdk` に実装する。処理状況を把握するためのプリントログも保持する。
- LSP/影響範囲: `Phage2/run/openjdk` 配下のモジュールのみ（他シンボル依存なし）。
- タスク（AT 粒度）:
  1. `OpenJDK` ディレクトリ構成と抽出ルール（`JDK-\\d+`）を確認し、カレントディレクトリ配下の `issue_ids` フォルダ出力要件を再確認。
  2. モジュールの出力先を `Path.cwd() / "issue_ids"` に変更し、フォルダ生成とログ出力を更新する。
  3. 改修後モジュールを実行し、ルートおよび `Phage2/run/openjdk` の両方で `issue_ids` フォルダとファイルが生成されることを確認する。
