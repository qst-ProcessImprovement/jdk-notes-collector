# Statement of Work: JDK差分テーブル生成

## 背景
Phage2/run/mapping 配下の openjdk・oraclejdk・temurin の各 issue_ids.txt に含まれる JDK 番号の差異を把握するため、差分を抽出し表形式で可視化する Python モジュールが求められている。

## 対応範囲
- Phage2/run/mapping/ 配下に新規 Python モジュールを作成し、3プロダクト間で JDK 番号の差異を抽出する処理を実装する。
- 差分のある JDK 番号（=3製品すべてには存在しない番号）だけを抽出し、OpenJDK/OracleJDK/Temurin 各製品での有無を示すテーブルを標準出力に表示する機能を提供する。
- 入力ファイルパスはリポジトリルートからの相対パスでアクセスし、フォルダ名は openjdk・oraclejdk・temurin を正準名としてハードコードする。

## 非対応範囲
- issue_ids.txt の内容更新や前処理。
- CLI 引数や外部入出力インターフェースの拡張。
- 自動テストの追加。

## 想定成果物
- Phage2/run/mapping/jdk_diff_report.py（仮称）: 標準出力に差分テーブルを表示する Python モジュール。

## 作業手順 (AT)
1. 既存ディレクトリ構造と issue_ids.txt の内容を確認する。
2. LSP にて該当ディレクトリ内の既存シンボルを調査（該当なしの場合は記録）。
3. Python モジュールを実装し、差分抽出ロジックとテーブル出力を追加する。
4. ローカルでモジュールを実行し、期待通りのテーブルが出力されることを検証する。
5. 生成物と検証結果を報告する。

## 影響シンボル / 参照箇所 (LSP)
- 新規モジュール追加のため既存シンボルへの影響なし。

## 検証計画
- `python Phage2/run/mapping/jdk_diff_report.py` を手動実行し、表形式で差分が表示されることを確認する。

