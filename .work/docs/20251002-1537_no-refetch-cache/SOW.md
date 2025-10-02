# SOW: 未取得ビルドの再取得防止キャッシュ追加

## 目的
JIRA の Resolved in Build XML が 0 件だったビルドについて、次回以降の実行で同じリクエストを再送しないようキャッシュ処理を追加する。

## スコープ
- `Phage2/run/fetch/fetch_openjdk_resolved_builds.py`
  - `collect_resolved_in_build_xml` (L1405): 既存 XML の再利用判定に加えて「0件キャッシュ」を参照し、登録済みならリクエストをスキップする処理を追加。
  - `resolve_output_path` (L1330): ここを基点に同一ディレクトリへスキップ判定用マーカーを保存するため、新規ヘルパーを追加予定。
  - 新規関数（名称未定、`resolve_output_path` 付近）: NOT_FOUND 時にマーカーを生成し、成功時にはマーカーを削除する処理を切り出す。

## 影響シンボルと参照
- `collect_resolved_in_build_xml` → `fetch_build_xml` 呼び出し前後でマーカー処理を追加する。
- `resolve_output_path` → 同一命名規則でマーカーを配置するため、補助関数から呼び出す。

## 実施内容
1. スキップマーカーのパスを解決するヘルパー（例: `resolve_skip_marker_path`）を `resolve_output_path` 近傍に追加し、`Path` を返す。
2. `collect_resolved_in_build_xml` でマーカー存在時はネットワーク取得をスキップし、必要に応じて INFO ログを出力。
3. `fetch_build_xml` の戻り値処理で `FetchOutcome.NOT_FOUND` を受けたときにマーカーを作成し、`FetchOutcome.SUCCESS` 時はマーカーを削除する。

## アウトオブスコープ
- 既存 XML キャッシュの削除ポリシー変更
- 他ファイル／他プロダクトのキャッシュ方式変更
- マーカーを自動的に再取得へ切り替えるための期限管理

## 確認項目
- マーカー作成後の再実行で `fetch_build_xml` が呼び出されないこと。
- マーカーが存在しない（または削除された）場合は従来通り再取得されること。
- 既存 XML が利用されるケースには影響がないこと。

以上の内容で問題なければ実装を進めます。
