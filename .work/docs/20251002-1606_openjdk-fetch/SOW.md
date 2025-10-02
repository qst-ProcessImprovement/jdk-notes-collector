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
1. `collect_resolved_in_build_xml` を中心に、`builds/xml` 参照を排し `INPUT` を唯一の入力源とするよう改修する。
2. 正準ターゲット定義を再整理し、取得対象外のビルドを除外したうえで欠落検出ポリシーを明確化する。
3. 入力欠落時の検出とエラー終了を実装し、フォールバックを禁止する。
4. 後段の集約処理との整合を確認し、必要な補正と乾式検証を行う。

## アウトプット
- 更新された `fetch_openjdk_resolved_builds.py`
- 必要に応じた補助的な更新内容（例: ログメッセージ、コメント等）

## 非スコープ
- OracleJDK / Temurin 関連処理の変更
- 実際の Web 取得やファイル配置のオペレーション

## 前提
- XML 入力は `INPUT/OpenJDK/per_files` に事前配置されている。
- 既存のキャッシュ (`builds/xml`) は使用しない方針に切り替える。
