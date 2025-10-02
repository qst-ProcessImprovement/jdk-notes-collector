# Statement of Work: Temurin リリースノート単一JSON化対応

## 目的
Temurin のリリースノート入力を1ファイルに集約し、処理側で新しいフォーマット（単一ファイル内で複数リリースを扱う構造）を正しく解析できるようにする。また既存の複数ファイル構成から新構成への移行を完了させる。

## 対応範囲
- 入力ディレクトリ `Phage2/run/fetch/INPUT/temurin/json` のデータ構造見直し（単一ファイル化）
- `fetch_openjdk_resolved_builds.py` 内 Temurin 関連処理（主に `iter_temurin_release_notes`、`generate_temurin_issue_outputs` など）のフォーマット対応
- 既存リリースノートJSONの集約処理と新ファイル生成
- 新フォーマットへ切り替えた後のJDK差分レポート生成ロジックの整合性確認

## 対応内容 (AT)
1. 新フォーマット設計・既存ファイル集約
   - 既存9ファイルの内容を正準化し、単一JSON（例: `temurin_releases.json`）へ統合
   - 生成スクリプト or 一時処理で正当性チェック
2. Temurin入力解析ロジック改修
   - 対象シンボル: `iter_temurin_release_notes`, `generate_temurin_issue_outputs`, `collect_temurin_issue_ids` 等
   - 新フォーマット（単一ファイル内に複数リリース）を読み取るように実装変更
   - 旧フォーマットとの後方互換は不要だが、リリース毎の属性・Backout/Redo判定が維持されること
3. 出力・レポート再生成
   - Temurin issue_ids 出力、バックアウト記録、`jdk_diff_report.md` の再生成
   - 差分検証 (Temurin 列が期待通りか) の確認

## 非対応事項
- Temurin以外(OpenJDK/OracleJDK)の入力フォーマット変更
- XML取得処理および他プロダクトの出力仕様変更

## 成果物
- 新しい単一JSONファイル（例: `temurin_releases.json`）
- 更新された `Phage2/run/fetch/fetch_openjdk_resolved_builds.py`
- 再生成済み Temurin 関連出力および `jdk_diff_report.md`

## 検証
- 新フォーマットのみを配置した状態で `generate_temurin_issue_outputs` を実行し、Temurin issue_ids/バックアウト記録が生成されること
- `generate_jdk_diff_report` 実行後、差分表で不要な項目が表示されないことを確認
