# Statement of Work: Temurin JDK Issue ID抽出モジュール

## 背景
- 入力: `Phage2/run/temurin/jdk-21.0.1+12.json`（相対パスでハードコーディング）
- 要求: JSONに含まれるIssueを列挙し、Backportエントリについては`backportOf`のIDを用いるIDリストを取得できるPythonモジュールを作成する。

## 影響調査 (LSPベース)
- 既存コードへの変更はなく新規モジュールを追加予定。既存シンボルへの影響はなし。

## 作業範囲 (Scope)
1. 入力JSONの構造調査（`release_notes`配列内の各要素の`id`/`backportOf`/`type`など）。
2. `Phage2/run`配下にPythonモジュールを新規作成し、以下を実装:
   - JSONファイルパスをハードコーディングした関数内で読み込み、Issue IDリストを返す。
   - Backportエントリは`backportOf`を優先し、存在しなければエラーを発生させる。
   - 正常系の簡易実行エントリ（例: `if __name__ == "__main__"`での利用例）を用意。
3. 最低限のユーティリティ的ドキュメント化（関数docstring・使用方法をコメントで記載）。
4. 動作確認（対象JSONに対する実行結果の取得）。

## アウトプット
- 新規ファイル: `Phage2/run/issue_ids.py`（予定）
- 実行例: CLIからの利用方法・結果を報告。

## 非対象 (Out of Scope)
- 複数ファイル対応の一般化やテストスイート整備。
- JSON以外のフォーマット対応。

## リスクと前提
- JSONスキーマの変動が発生した場合は追加対応が必要になる可能性。

## 承認依頼
上記内容で着手してよいかご確認ください。
