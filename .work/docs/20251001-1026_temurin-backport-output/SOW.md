# Statement of Work – Temurin Backport出力拡張

## 背景
`Phage2/run/temurin/issue_ids.py` は Temurin のリリースノート(JSON)から Issue ID を抽出し、Backport 項目では元 Issue ID(`backportOf`)のみを出力しています。新要件では、出力ファイルに元 Issue ID と併せて Backport 側の Issue ID を `temurin_` 接頭辞付きで同じ行に列挙し、同じ元 Issue に紐づく Backport が複数ある場合はカンマ区切りで追記する必要があります。集約ファイル(`issue_ids_output/all_issue_ids.txt`)も同じフォーマットに統一します。

## 対応方針
1. `collect_issue_ids` を拡張し、(a)既存どおり元 Issue ID の一覧を返しつつ (b)元 Issue ID ごとの Backport Issue ID を収集するマップを構築します。Backport 以外の項目は空集合として扱い、正準表現( `JDK-` + 数値 )を満たさない値は例外とします。
2. `_write_unique_ids` に Backport マップを渡せるようシグネチャを更新し、ユニーク化した元 Issue ID ごとに `temurin_<Backport ID>` をカンマ区切りで追加した行へ書き換えます。既存のソート順・改行フォーマットは保持します。
3. `main` で各 JSON ファイルの Backport マップを集約し、`aggregate_ids` と並行して `aggregate_backports` を構築します。集約出力(`all_issue_ids.txt`)でも同じフォーマットで書き出せるよう出力処理を調整します。
4. 重複検出・例外処理・標準出力ログなど現行のガードを維持しつつ、`temurin_` 接頭辞の付与やマップ初期化での抜け漏れがないかを確認します。

## 影響シンボル（Serena）
- `collect_issue_ids` — `Phage2/run/temurin/issue_ids.py:33` ／ 参照: `main/issue_ids` (`Phage2/run/temurin/issue_ids.py:92`)
- `_write_unique_ids` — `Phage2/run/temurin/issue_ids.py:70` ／ 参照: `main/unique_ids` (`Phage2/run/temurin/issue_ids.py:93`)
- `main` — `Phage2/run/temurin/issue_ids.py:80` ／ 参照: `issue_ids.py` 末尾の呼び出し (`Phage2/run/temurin/issue_ids.py:111`)

## スコープ外
- JSON ソースの取得・更新や新規ファイル生成仕様の追加
- Backport 以外の `type` に対する抽出ルール変更

## テスト
- `python Phage2/run/temurin/issue_ids.py` を実行し、`issue_ids_output/per_file/*.txt` と `issue_ids_output/all_issue_ids.txt` が新フォーマットで出力され、例外が発生しないことを確認します。

上記方針で進めてよろしいでしょうか。
