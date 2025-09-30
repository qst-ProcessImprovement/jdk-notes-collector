# Statement of Work: OpenJDK Issue ID 抽出モジュール

## 背景 / ゴール
- `Phage2/run/fetch` 配下にある OpenJDK のバージョン別 XML から、含まれる Issue ID 一覧を抽出し、Backport の場合は元 Issue ID のみを記録したファイルを生成する独立モジュールを追加する。

## スコープ
- 対象ファイル: `Phage2/run/fetch/**/*.xml`
- 成果物: 抽出ロジックを持つ新規 Python モジュール、および出力ファイル。
- 出力ファイルは以下の 2 種類を常時生成する。
  - 各 XML と同じベース名（拡張子 `.txt`）の個別ファイル。個別ファイル内の Issue ID は重複排除後に JDK 番号順（数値昇順）でソートする。
  - 全 Issue ID を結合した集約ファイル（例: `issue_ids.txt`）。集約ファイル内の Issue ID も重複排除後に JDK 番号順でソートする。
- 出力ファイルは XML が存在するディレクトリとは異なる専用ディレクトリ（例: `Phage2/run/fetch/issue_ids_output/`）配下に保存し、個別ファイルも同ディレクトリ配下へ相対パスを再現して配置する。
- 既存モジュール・設定ファイルの修正は行わない。

## 対応方針
- Python 標準ライブラリ `xml.etree.ElementTree` を利用して XML を解析する。
- 各 `<item>` 要素から `<key>` の値を取得し Issue ID とする。
- Backport の判定:
  - `<item>` 内の `<issuelinks>` に `<name>Backport</name>` が存在し、配下の `<inwardlinks description="backport of">` に元 Issue を示す `<issuekey>` が列挙されていることを確認した。
  - Backport と判定した場合は `<issuekey>` の値を出力対象 ID とし、当該 Backport Issue 自体の `<key>` は記録しない。
  - 元 Issue ID が複数列挙されるケースに備え、全てを取得し一意化する。
- XML 解析中に想定外データ（例: Backport と記述されているにもかかわらず元 Issue が存在しない等）を検出した場合は、標準出力へ警告メッセージを出力する。
- 抽出した ID はすべて正準表現（`JDK-<番号>`）のまま扱い、文字列を整数部で比較して昇順ソートする。
- 解析対象 XML はサブディレクトリを含め再帰的に探索し、`*.xml` のみ処理する。

## 影響調査 (LSP 情報)
- 新規追加モジュールのため既存シンボルへの影響・参照はなし。

## タスク分解 (AT)
1. XML 構造の再確認とモジュール設計詳細の整理。
2. 抽出モジュールの実装（XML 走査、Backport 判定、ID 出力）。
3. 個別ファイルおよび集約ファイルの保存処理実装と想定外データ時の標準出力ログを含めた動作検証。
4. 実装コードと生成ファイルの最終確認。

## 成果物
- `Phage2/run/fetch` 配下に追加する Python モジュール（例: `issue_id_extractor.py`）。
- 抽出結果を保存した個別テキストファイル（各 XML に対応）と集約テキストファイル（例: `issue_ids.txt`）。

## 検証
- `Phage2/run/fetch/OpenJDK/21.0.1.xml` など既存 XML でスクリプトを実行し、Backport Issue から元 Issue ID が抽出されること、想定外データ検出時に標準出力へ警告が表示されることを確認する。
- 個別ファイル・集約ファイル双方で重複がなく、JDK 番号で昇順ソートされ、かつ出力ディレクトリが専用ディレクトリ配下であることを確認する。
