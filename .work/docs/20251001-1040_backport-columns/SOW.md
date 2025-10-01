# Statement of Work: JDK差分レポートへのBackport列追加

## 要求整理
- 対象: `Phage2/run/mapping/jdk_diff_report.py`
- 目的: 生成される差分テーブル末尾に以下3列を追加し、各製品のbackport課題JDK番号を表示する。
  - JDK - OpenJDK backport
  - JDK - OracleJDK backport
  - JDK - Temurin backport
- 背景: 各プロダクト配下の`issue_ids.txt`は `JDK-xxxx[,<prefix>JDK-yyyy...]` 形式を許容し、カンマ以降が backport 情報となっている。prefixは `openjdk_` / `oraclejdk_` / `temurin_` のいずれかで、正準表現として末尾のアンダーバーを含む。

## 対応方針
1. `issue_ids.txt`ローダーの拡張
   - `JDK-`に続く数値のみを正規データとしつつ、カンマ区切りで付随する`<prefix>JDK-####`を解析。
   - prefixは上記3種類の正準値（末尾アンダーバー付）に限定し、未知prefixや非数値は例外化。
   - 読み込み結果として、(a)従来通りのベースJDK番号集合、(b)ベースJDK番号→製品→backport JDK番号のマップを収集する。
2. 差分テーブルビルダーの拡張
   - `build_diff_table`へbackportマップを渡し、行末に製品ごとのbackport列を追加。
   - backportが未定義の場合は空欄とし、複数入力から異なる値が来た場合は正準表現違反として例外化する。
3. ヘッダー／出力整形の更新
   - `build_report`で新列のヘッダーを追加し、`render_table`のレイアウトは既存のまま適用。

## 影響範囲 (LSP調査)
- `Phage2/run/mapping/jdk_diff_report.py:load_issue_ids` (参照先: `build_report`)
- `Phage2/run/mapping/jdk_diff_report.py:build_diff_table` (参照先: `build_report`)
- `Phage2/run/mapping/jdk_diff_report.py:build_report`

## タスク分割 (AT)
1. ローダーのインタフェース拡張とbackport情報取得ロジック実装
2. 差分テーブル生成処理のパラメータ・行構築拡張
3. ヘッダー更新とスクリプト全体の整合性確認（lint相当の静的確認、必要に応じてサンプル実行）

## 想定しない対応
- backport以外の列追加や既存フォーマットの変更
- `issue_ids.txt`ファイルの内容修正
- XML解析処理の振る舞い変更

## 確認事項
- Temurin列の表記について、要求文では "Temrin" とありましたが、既存コードと同じく "Temurin" を用いる想定です。別表記が必要な場合はご指示ください。

