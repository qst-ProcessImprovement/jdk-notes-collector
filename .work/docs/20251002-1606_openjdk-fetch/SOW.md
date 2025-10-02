# Statement of Work: fetch_openjdk_resolved_builds.py 仕様変更

## 目的
`fetch_openjdk_resolved_builds.py` 実行時、`INPUT/OpenJDK/per_files` に必要な XML がすべて揃っている場合はそのまま再利用し、Web からの再取得を行わないよう挙動を変更する。また、必要な XML が欠けている場合にはエラー終了とする。

## スコープ
- 対象プロダクト: OpenJDK resolved-in-build XML
- 対象スクリプト: `Phage2/run/fetch/fetch_openjdk_resolved_builds.py`
- 影響シンボル (Serena LSP 抽出)
  - `collect_resolved_in_build_xml`
  - `fetch_build_xml`
  - `resolve_output_path`
  - `collect_resolved_builds_from_per_files`
  - `OPENJDK_PER_FILES_ROOT`
  - `cleanup_generated_outputs`

## タスク
1. `collect_resolved_in_build_xml` の再取得ロジックを改修し、`builds/xml` へのキャッシュ参照を廃し、`INPUT` 内 XML を必須入力とする。
2. 入力欠落時の検出とエラー終了を実装する（再取得フォールバック禁止）。
3. 後段の集約処理が新ロジックと整合するかを確認し、必要な箇所を更新する。
4. 動作確認（乾式）とドキュメント/ログ出力の調整が必要であれば実施する。

## アウトプット
- 更新された `fetch_openjdk_resolved_builds.py`
- 必要に応じた補助的な更新内容（例: ログメッセージ、コメント等）

## 非スコープ
- OracleJDK / Temurin 関連処理の変更
- 実際の Web 取得やファイル配置のオペレーション

## 前提
- XML 入力は `INPUT/OpenJDK/per_files` に事前配置されている。
- 既存のキャッシュ (`builds/xml`) は使用しない方針に切り替える。
