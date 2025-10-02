# SOW: OpenJDK/OracleJDK の BACKOUT/REDO 判定整備

## 背景と課題
- 現状 `fetch_openjdk_resolved_builds.py` が生成する OpenJDK / OracleJDK 向け `issue_ids` 集約では、[BACKOUT] / [REDO] の判定が Temurin 相当の厳密さで実装されておらず、`JDK-8277573` のような BACKOUT 済み課題が残存している。
- Temurin 側では `[BACKOUT]`/`[REDO]` を release note JSON から検知し、対象 Issue を除外/再収載する実装が整備済み。OpenJDK / OracleJDK 側も JIRA XML を横断して同様の制御を実施する必要がある。
- OracleJDK 集約は OpenJDK の Issue 一覧を取り込んだ上で FixVersion を Oracle 仕様に差し替える設計のため、OpenJDK 側での除外結果を尊重しつつ Oracle 独自の BACKOUT/REDO も反映できる構造が求められる。

## 対応方針
1. **BACKOUT/REDO 抽出ロジックの汎用化**
   - `[BACKOUT]`/`[REDO]` マーカー検出用の正規表現および抽出関数を Temurin 専用命名から一般化し、JIRA XML でも再利用可能にする。
2. **JIRA XML 走査の拡張**
   - `extract_issue_pairs_from_item` (`Phage2/run/fetch/fetch_openjdk_resolved_builds.py`:663-697) に BACKOUT/REDO 検知と対象 Issue ID 抽出処理を追加し、
     - BACKOUT/REDO チケット自体は集約対象から除外。
     - BACKOUT が指示するオリジナル Issue を除外対象集合へ追加。
     - REDO が指示する Issue は除外集合から復帰させ、必要に応じて Backport ペアを保持。
   - 当該関数を呼ぶ `extract_issue_pairs_from_xml_content` (700-718) / `extract_issue_pairs_from_xml_file` (721-727) へ排他集合の受け渡しを追加。
3. **集約結果のフィルタリング**
   - `collect_issue_ids_from_directory` (749-759) で BACKOUT/REDO, 除外チケット集合を収集し、呼び出し元へ返却するよう拡張。
   - `generate_issue_id_outputs` (779-808) にて、
     - 受け取った集合を基に per-file および集約出力から BACKOUT 対象 Issue を除外。
     - REDO 指定がある Issue は除外対象から復帰させる。
     - OracleJDK 集約時は OpenJDK 側のマップとマージした後に同じフィルタリングを適用し、両方の BACKOUT/REDO を反映。
4. **横断用統合 XML の活用**
   - 既存の `write_aggregate_xml` により生成される `all_builds_openjdk.xml`／`all_builds_oraclejdk.xml` をバックアウト検知のテストデータとして活用し、開発中にフィルタリング結果を検証可能とする。

## 対象ファイル / シンボル (LSP 取得結果)
- `Phage2/run/fetch/fetch_openjdk_resolved_builds.py`
  - `extract_issue_pairs_from_item` (line 663-697)
  - `extract_issue_pairs_from_xml_content` (700-718)
  - `extract_issue_pairs_from_xml_file` (721-727)
  - `collect_issue_ids_from_directory` (749-759)
  - `generate_issue_id_outputs` (779-808)
  - `extract_temurin_backout_targets` / `extract_temurin_redo_targets` (248-314) ※汎用化対象

## 影響範囲とリスク
- issue_ids テキスト出力の内容が変化するため、既存のレポート生成 (`generate_jdk_diff_report`) に影響する可能性がある。BACKOUT/REDO の除外が過剰にならないよう、REDO 処理と除外集合の整合を重視する。
- Temurin 向け出力で利用している共通ヘルパーを汎用化する際、既存ロジックの挙動変更に注意。既存の Temurin 判定と同一結果になるか差分確認を実施する。

## 検証計画
- 既存の `Phage2/run/fetch/builds/xml/all_builds_openjdk.xml` および `.../all_builds_oraclejdk.xml` を用いて `python fetch_openjdk_resolved_builds.py` を実行し、
  - `builds/issue_ids/all_issue_ids_openjdk.txt` および `...oraclejdk.txt` から BACKOUT 対象が除去されていること。
  - Temurin 集約 (`all_issue_ids_temurin.txt`) にリグレッションが無いこと。
- 差分として `jdk_diff_report.md` を確認し、問題箇所が想定通り変化しているか目視チェック。

## 非対応事項
- JIRA の取得対象 FixVersion 範囲や Temurin JSON の仕様変更には手を入れない。
- BACKOUT/REDO 以外の特別扱い (例: WITHDRAWN 等) は今回対象外。
