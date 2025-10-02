# Statement of Work: OpenJDK / OracleJDK 21 GA resolved-in-build 拡張

## 背景 / 目的
- OpenJDK 21 GA (fixVersion = 21) の課題が "resolved in build" b35 まで存在するが、現行スクリプトには対象ビルドが定義されておらず取得できない。
- OracleJDK 側も同様に GA 時点の "resolved in build" を網羅したい。OracleJDK の GA は fixVersion=21 を用いるため、OpenJDK 側のビルド範囲と同一の b01〜b35 を OracleJDK 収集でも利用する。

## 対応範囲 (スコープ)
1. `OPENJDK_RESOLVED_BUILD_TARGETS` に GA 用ターゲットを追加し、`b01`〜`b35` を網羅する。
2. `ORACLEJDK_RESOLVED_BUILD_TARGETS` にも GA (fixVersion=21) を追加し、OpenJDK と同じビルド範囲 (`b01`〜`b35`) を取得対象に含める。
3. 追加に伴う `OPENJDK_FIX_VERSIONS` および `ORACLEJDK_FIX_VERSIONS` の派生定義が正しく更新されることを確認する。
4. 増えたターゲットにより issue_ids 集約・差分レポート生成へ副作用がないことを確認する。

## 非対象
- GA 以外の既存バージョンのビルド範囲変更。
- Temurin 側の処理変更。
- 新たなロギングや設定ファイル追加。

## 影響シンボル (LSP抽出)
- `Phage2/run/fetch/fetch_openjdk_resolved_builds.py`
  - 定数: `OPENJDK_RESOLVED_BUILD_TARGETS`, `ORACLEJDK_RESOLVED_BUILD_TARGETS`, `OPENJDK_FIX_VERSIONS`, `ORACLEJDK_FIX_VERSIONS`
  - 関数: `collect_resolved_in_build_xml`, `generate_issue_id_outputs`, `main`（取得対象が増えるため）

## 作業手順 (AT)
1. GA 用ターゲットを OpenJDK/OracleJDK の各ターゲット定義に追加し、ビルド番号範囲が `b01`〜`b35` となることを確認する。
2. 定義追加後に派生タプル (`*_FIX_VERSIONS`) が GA を含むようになるか確認する。
3. ローカルで `generate_issue_id_outputs` や差分レポートが新ターゲットを扱えるか確認する。
4. 必要に応じて JIRA 側の HTTP レスポンス (400 等) をログ出力で確認する。

## リスク / 留意点
- ビルド番号範囲が広がることで JIRA からの取得回数が増え、実行時間が伸びる可能性がある。
- 既存の bXX で未提供なビルドがある場合、HTTP 400 → NOT_FOUND として処理されるが、ログ上で認識できることを確認する。

## 確認事項
- 上記 SOW に問題がなければ作業を進めます。調整事項があればご指示ください。
