# SOW: Backport Issue 出力拡張

## 対応概要
- バックポート課題に紐づく元 Issue ID に加えて、バックポート側の JDK 番号も出力し、カンマ区切り形式で1行にまとめる
- バックポートの JDK 番号は引数で受け取る接頭辞を付与した上で列挙し、同一元 Issue に複数存在する場合は重複排除・ソート後に出力する
- 個別出力/集約出力ともに新形式へ揃え、既存の非バックポート課題は従来通り単独の JDK 番号のみを出力する
- CLI からバックポート接頭辞を受け取れるよう引数処理を追加する

## 想定タスク
1. 既存の抽出処理を拡張し、item 要素から (元 Issue, バックポート Issue) 関係を取得できるようにする
2. 抽出結果をまとめて元 Issue ごとのバックポート集合を生成する正規化処理を追加する
3. 出力フォーマットを `JDK-xxxx[,<prefix>JDK-yyyy...]` 形式へ更新し、個別/集約の双方に適用する
4. CLI でバックポート接頭辞を任意指定できるよう `main` の引数処理を拡張する

## 影響シンボル (LSP)
- `Phage2/run/fetch/issue_id_extractor.py:26` `extract_issue_ids_from_item`
- `Phage2/run/fetch/issue_id_extractor.py:64` `extract_issue_ids`
- `Phage2/run/fetch/issue_id_extractor.py:100` `collect_issue_ids`
- `Phage2/run/fetch/issue_id_extractor.py:117` `write_issue_ids`
- `Phage2/run/fetch/issue_id_extractor.py:138` `main`

## 非対応範囲
- XML 解析ロジック自体の仕様変更
- 出力先ディレクトリ構成やファイル名の変更
