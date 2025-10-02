# SOW: OpenJDK/OracleJDK resolved_builds 統合ロジック拡張

## 背景と課題
- `Phage2/run/fetch/builds/xml/OracleJDK/resolved_builds.json` は OracleJDK の FixVersion/FixBuild と課題一覧を保持しているが、OpenJDK 側のビルド情報が含まれていない。
- 新たに投入された `Phage2/run/fetch/INPUT/OpenJDK/per_files` および `Phage2/run/fetch/INPUT/oraclejdk/per_files` に、FixVersion ごとの課題リストを整形済みで保持しており、これらを集約結果に反映する必要がある。
- `fetch_openjdk_resolved_builds.py` 実行時に、これら per_files データを取り込み、OpenJDK/OracleJDK 双方の resolved_builds JSON を毎回再生成する仕組みを構築する。

## 対応方針
1. **入力フォーマットの解析**
   - `INPUT/OpenJDK/per_files` / `INPUT/oraclejdk/per_files` 以下のファイルから FixVersion・ビルド番号・課題一覧を読み取るパーサを追加実装。
   - ファイル命名規則（例: `jdk-21_b01.txt`）から FixVersion と build を抽出し、行単位に課題情報を収集する。
2. **resolved_builds 生成処理の実装**
   - 新設のヘルパーを通じて per_files データを `dict` 構造に整備し、
     - OpenJDK 分: `Phage2/run/fetch/builds/xml/OpenJDK/resolved_builds.json`
     - OracleJDK 分: `Phage2/run/fetch/builds/xml/OracleJDK/resolved_builds.json`
     をそれぞれ `indent=2` で書き出す。
   - OracleJDK 側は OpenJDK の Issue 一覧をベースにしているため、OpenJDK per_files も統合結果に含める（要件通り）。
3. **既存スクリプトへの組み込み**
   - `fetch_openjdk_resolved_builds.py` 内で per_files パスを参照し、XML 収集処理と同一フローで JSON を再生成するステップを追加。
   - 実行のたびに前回生成物を上書きすることを前提とし、整形済み JSON を出力。
4. **例外・バリデーション**
   - ファイル形式が正準でない場合は例外化し、無視せずに早期検知。
   - 行末の余分な空白や空行はスキップするが、必須フィールド欠落はエラーとする。

## 対象ファイル / シンボル
- `Phage2/run/fetch/fetch_openjdk_resolved_builds.py`
  - per_files パーサ (新規)
  - resolved_builds JSON 書き出し処理 (新規)
  - main フローへの統合
- 生成出力: `Phage2/run/fetch/builds/xml/OpenJDK/resolved_builds.json`, `Phage2/run/fetch/builds/xml/OracleJDK/resolved_builds.json`

## 影響範囲とリスク
- JSON サイズ増により読み込み時間が増加する可能性。
- per_files のファイル命名規則変更があった場合に即座にエラーとなるため、命名揺れへの耐性が低い。
- 既存の XML ベース処理と重複する情報源が併存するため、将来的な一元化が必要になるかもしれない。

## 検証計画
- スクリプト実行後、生成された両 JSON を `json.load` で読み込み構文確認。
- 代表的な FixVersion (例: `21 b01`, `21.0.6 b05`, `21.0.8-oracle b04`) が含まれ、課題件数が per_files と一致するか突き合わせ。
- 既存の XML 取得処理に影響が無いことを、主要ログ (INFO/WARN) を目視確認して担保。
