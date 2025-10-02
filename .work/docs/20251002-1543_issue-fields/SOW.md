# SOW: Resolved Build Issue詳細フィールドの網羅的出力（description除外）

## 目的
`resolved_builds.json` に含まれる Issue 情報について、JIRA XML `<item>` 内の全フィールド（`<description>` を除く）を正準表現で抽出・出力し、マージ後の Issue 詳細不足を解消する。

## スコープ
- `Phage2/run/fetch/fetch_openjdk_resolved_builds.py`
  - `parse_resolved_build_item` (L789-L817): `<item>` 要素から取得する情報を拡張し、下記の値を JSON に反映する。
  - 必要に応じて同ファイルに補助関数を追加し、テキスト抽出・複数値フィールド・ネスト構造・カスタムフィールドを整理して返却する。

## 追加するフィールド（description を除く `<item>` 直下）
- `link`: `<link>` テキスト。
- `project`: `<project>` の `id` / `key` 属性とテキスト（名称）。
- `environment`: `<environment>` テキスト。
- `issue_id`: 既存で `<key>` テキストを正準化済みのため継続利用（重複フィールドは追加しない）。
- `summary`: `<summary>` テキスト。
- `issue_type`: 既存フィールドに `<type>` テキストを格納済み。加えて `type_id` / `type_icon_url` を新規出力。
- `parent`: `<parent>` の `id` 属性（存在する場合）。
- `priority`: `<priority>` テキストと `priority_id` / `priority_icon_url`。
- `status`: `<status>` テキストと `status_id` / `status_icon_url` / `status_description`。
- `status_category`: `<statusCategory>` の `id` / `key` / `colorName`。
- `resolution`: `<resolution>` テキストと `resolution_id`。
- `assignee`: `<assignee>` の `username` とテキスト（表示名）。
- `reporter`: `<reporter>` の `username` とテキスト（表示名）。
- `labels`: `<labels>` 配下の `<label>` テキスト一覧。
- `created`, `updated`, `resolved`: 各日時テキスト。
- `versions`: `<version>` の複数値（存在すれば）。
- `fix_versions`: `<fixVersion>` の複数値。
- `components`: `<component>` の複数値。
- `due`: `<due>` テキスト。
- `votes`: `<votes>` 数値。
- `watches`: `<watches>` 数値。
- `comments`: `<comments>` 内 `comment` の `id` / `author` / `created` / 本文（HTML を CDATA として保持）。
- `issue_links`: `<issuelinks>` 内 `issuelinktype` 毎の `outwardlinks` / `inwardlinks` を整理した構造。
- `attachments`: `<attachments>` 内 `attachment` 情報（ファイル名・URL など）を辞書化。
- `subtasks`: `<subtasks>` 内 `subtask` の `id` / `key` / `summary` / `type` / `status` 等。
- `custom_fields`: `<customfields>` 内の各 `customfield` を `customfieldname`（正準キー化）でマッピングし、複数値は配列として保持。

## 表現ルール
- 文字列は `strip()` 後、空文字は未設定として除外。
- 数値項目（votes / watches）は整数変換。変換不能時はエラーにせず除外。
- 配列の順序は XML 出現順を維持。
- カスタムフィールドは `customfieldname` を lower snake case に正準化し、値は文字列配列。重複定義は検知時に例外を発生させる。

## 影響シンボルと参照
- `collect_resolved_in_build_xml` → `parse_resolved_build_xml` → `parse_resolved_build_item`
  - パイプライン全体で返却オブジェクトが拡張されるため、`parse_resolved_build_item` の戻り値スキーマが唯一の変更点。
- 出力 JSON (`resolved_builds.json`) を読み取る後続処理
  - 追加キーの出力のみで既存キーは保持。後方互換条件分岐は導入しない。

## アウトオブスコープ
- JIRA 検索条件・HTTP リクエストの変更。
- Description フィールドの出力。
- 取得値のフォーマット変換（日付パース等）の高度化。

## 確認項目
- 各フィールドが JIRA XML に存在する場合に JSON へ正しく反映されること。
- 存在しない場合はキー自体が省略され、`null` 等を出力しないこと。
- カスタムフィールドの正準キー化が一意に完了していること。

上記内容で実装を進めてもよいか、確認をお願いします。
