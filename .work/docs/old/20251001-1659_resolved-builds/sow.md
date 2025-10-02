# Statement of Work

## 背景
- 現状は `Phage2/run/fetch/fetch_openjdk_resolved_builds.py` が `FIX_VERSION = "21"` と `BUILD_NUMBERS` の単一配列を前提に、JDK 21 系の特定ビルドのみを収集している。
- 要件では JDK 21.0.1〜21.0.8 の複数バージョンについて "Resolved in Build" の全ビルドを個別に取得し、ハードコーディングした定義に基づき取得・保存する必要がある。

## 影響範囲（シンボルと参照元）
- `Phage2/run/fetch/fetch_openjdk_resolved_builds.py`
  - `BUILD_NUMBERS` (`Phage2/run/fetch/fetch_openjdk_resolved_builds.py:14`) ← 参照: `main` (`Phage2/run/fetch/fetch_openjdk_resolved_builds.py:164`)
  - `FIX_VERSION` (`Phage2/run/fetch/fetch_openjdk_resolved_builds.py:15`) ← 参照: `build_request_url` (`Phage2/run/fetch/fetch_openjdk_resolved_builds.py:38`), `build_aggregate_xml` (`Phage2/run/fetch/fetch_openjdk_resolved_builds.py:126`)
  - `build_request_url` (`Phage2/run/fetch/fetch_openjdk_resolved_builds.py:38`) ← 参照: `fetch_build_xml` (`Phage2/run/fetch/fetch_openjdk_resolved_builds.py:92`)
  - `collect_resolved_in_build_xml` (`Phage2/run/fetch/fetch_openjdk_resolved_builds.py:147`) ← 参照: `main` (`Phage2/run/fetch/fetch_openjdk_resolved_builds.py:164`)
  - `save_individual_xml` (`Phage2/run/fetch/fetch_openjdk_resolved_builds.py:114`) ← 出力ファイル命名をバージョン別に変更予定
  - `build_aggregate_xml` (`Phage2/run/fetch/fetch_openjdk_resolved_builds.py:122`) ← ルート属性およびエントリ属性の見直し予定

## 作業項目（AT）
1. ハードコーディングされた対象定義の再設計: バージョンごとに `Resolved in Build` のビルド番号一覧を持つ正準データ構造を導入し、既存の `FIX_VERSION`/`BUILD_NUMBERS` を置き換える。
2. 取得ロジックの更新: `build_request_url`・`fetch_build_xml`・`collect_resolved_in_build_xml` をバージョン引数対応へリファクタし、全組み合わせを収集できるようにする。
3. 出力処理の更新: `save_individual_xml` と `build_aggregate_xml` をバージョン対応へ改修し、ファイル重複を避けつつ集約 XML にバージョン情報を保持する。
4. 動作確認: 実行ドライラン（必要に応じてモック/限定実行）で想定 URL 生成と保存パスを確認し、静的チェック（`python -m compileall` 等）で構文エラーがないことを検証。

## 成果物
- 上記対象スクリプトの改修済みコード
- 必要に応じた補助的な中間資料（`.work/tmp/` 配下を使用）

## 留意点
- バージョンとビルド番号は正準表現で一意に管理し、別名・省略形を許容しない。
- 既存の出力仕様に依存する後方互換性分岐は持たず、新仕様に統一する。
- URL テンプレートは変えずにパラメータ部分のみを更新する。

上記方針で問題ないか確認をお願いします。承認後に実装を開始します。
