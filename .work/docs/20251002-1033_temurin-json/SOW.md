# Statement of Work: Temurin JSON入力対応

## 目的
Temurin リリースノート入力形式変更（txt→JSON）および BACKOUT 指定 ID の除外・記録処理を実装し、既存の issue_ids 出力と集約処理を最新仕様に整合させる。

## 対応範囲
- JSON フォーマットのリリースノートを解析し `TemurinReleaseNoteEntry` を生成する処理。
- Temurin issue_ids 集約処理全体（重複検出、Backport 解決、tmp 出力）への影響調整。
- BACKOUT 指定の解析・除外・記録機構の追加。

## 対応内容 (AT)
1. `TemurinReleaseNoteEntry` 構造と JSON パース処理の改修。
   - 対象シンボル: `TemurinReleaseNoteEntry` (Phage2/run/fetch/fetch_openjdk_resolved_builds.py:117), `iter_temurin_release_notes` (同:128)。
2. issue_id 集約フローの JSON 対応および BACKOUT 除外ロジックの導入。
   - 対象シンボル: `collect_temurin_issue_ids` (Phage2/run/fetch/fetch_openjdk_resolved_builds.py:285), `generate_temurin_issue_outputs` (同:367)。
3. 除外 JDK 番号の tmp 出力と既存出力の整合確認。
   - 対象ディレクトリ: `Phage2/run/fetch/builds/issue_ids/temurin/tmp`。

## 非対応事項
- Temurin 以外の Distribution Target (OpenJDK / OracleJDK) の処理変更。
- 既存 XML 取得・差分レポートのロジック変更。

## 成果物
- 更新済み `Phage2/run/fetch/fetch_openjdk_resolved_builds.py`。
- BACKOUT 除外 ID 出力仕様（`temurin/tmp` 配下）を満たすコード。

## 検証
- JSON 入力ディレクトリに対する処理実行でエラーなく issue_ids/tmps が生成されることの確認。
- BACKOUT タイトルを含むサンプルで該当 JDK 番号が除外され、tmp に記録されることの確認（手動テスト予定）。
