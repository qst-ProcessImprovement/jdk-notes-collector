# Statement of Work (OracleJDK 対応拡張)

## 背景
- 現状スクリプトは OpenJDK のみを取得対象としており、OracleJDK の "Resolved in Build" XML は収集していない。
- OracleJDK は Fix Version に "-oracle" サフィックスが付く同一課題群であり、OpenJDK と同じビルド番号範囲で取得する必要がある。
- 1 実行で OpenJDK / OracleJDK の双方を収集し、それぞれの出力ディレクトリとファイル命名規則を統一することが要件。

## 影響範囲
- `Phage2/run/fetch/fetch_openjdk_resolved_builds.py`
  - 定数 `RESOLVED_BUILD_TARGETS`（OpenJDK 固有定義へ改名/再構成予定）
  - 追加定数（OracleJDK 向け Fix Version/Resolved in Build 定義）
  - `build_request_url` / `fetch_build_xml` / `collect_resolved_in_build_xml`
  - `save_individual_xml` / `build_aggregate_xml` / `write_aggregate_xml`
  - `main`

## 作業項目（AT）
1. 基本ターゲット定義の整理: OpenJDK 用ベース定義を保持し、OracleJDK 用に `-oracle` サフィックス付きのターゲット集合を派生させる。
2. 出力構造・データ構造の再設計: ディストリビューション（OpenJDK/OracleJDK）ごとに出力ディレクトリ・集約情報・Fix Version リストを管理するデータ構造を導入。
3. 取得および保存ロジックの多段化: `collect_resolved_in_build_xml` 以降の処理をディストリビューション単位で繰り返すように改修し、個別 XML と統合 XML を対応するディレクトリに保存。
4. 検証: `python -m compileall Phage2/run/fetch/fetch_openjdk_resolved_builds.py` 等で静的検証を行い、必要に応じてロジックのドライラン（URL 生成確認）を実施。

## 成果物
- 同スクリプトの改修済みコード（OpenJDK/OracleJDK 同時取得対応）
- 補足資料（必要時 `.work/tmp/` 配下）

## 留意点
- Fix Version の正準表現は OpenJDK / OracleJDK でそれぞれ一意に管理し、曖昧な別名を許容しない。
- 書き込み先ディレクトリは `OpenJDK/` および `OracleJDK/` で統一し、ファイル名は `jdk-{fix_version}_{build_number}.xml` を踏襲する。
- 取得失敗や対象なしの場合はディストリビューション単位で警告を出し、最終的な終了コードポリシーを維持する。

上記方針で実装を進めます。
