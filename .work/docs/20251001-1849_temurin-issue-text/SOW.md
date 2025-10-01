# SOW: temurin issue一覧テキスト入力対応

## 背景
- `Phage2/run/temurin/issue_ids.py` はこれまで `temurin/*.json` を読み込み、issue IDとBackport対応表を生成していた。
- 入力がテキスト(`temurin/*.txt`)に変更されたため、既存ロジックではJSONとしてのパースに失敗し、処理が停止する。
- テキスト形式ではBackport元Issue IDなどの一部情報が欠落しており、補完のために `issue_ids_output/` 配下の既存出力または `jdk_issues/` のソースIssue XMLを参照する必要があることが判明した。

## 対応範囲
- `Phage2/run/temurin/issue_ids.py` 内のテキストパーサ実装、Backport解決ロジック、出力生成処理の更新。
- `temurin/*.txt` + `/Users/irieryuuhei/Documents/qst-ProcessImprovement/jdk-notes-collector/Phage1/run/jdk_issues/<ISSUE>/<issue>.xml` を組み合わせて必要情報を復元する。
- スクリプトが生成する `issue_ids_output/` (集約・ファイル別) の体裁・内容を現行仕様に合わせて維持することを確認する。

## 影響シンボル (Serena LSP調査結果)
- `_iter_release_notes` (Phage2/run/temurin/issue_ids.py:28)
- `collect_issue_ids` (Phage2/run/temurin/issue_ids.py:78)
- `_load_reference_backports` (Phage2/run/temurin/issue_ids.py:109)
- `_write_unique_ids` (Phage2/run/temurin/issue_ids.py:181)
- `main` (Phage2/run/temurin/issue_ids.py:200)

## タスク
1. テキスト入力(`temurin/*.txt`)のフォーマットを整理し、優先度・種別・コンポーネント・Issue ID・概要の5行ブロックとして解析可能なことを確認する。異常行がある場合の検証も実施。
2. カレント直下に `tmp/` ディレクトリを設け、テキストから抽出したユニークなJDK Issue ID一覧を中間成果物として `tmp/temurin_jdk_ids.txt` に出力するロジックを組み込む。補助的な中間ファイルは現時点で追加不要とし、必要性が生じた際に再検討する。
3. `issue_ids_output/per_file/<release>.txt` および `/Users/irieryuuhei/Documents/qst-ProcessImprovement/jdk-notes-collector/Phage1/run/jdk_issues/<ISSUE>/<issue>.xml` から Backport Issue ID → 元Issue ID のマッピングを抽出するユーティリティを実装し、欠落情報補完に利用できるか確認する。
4. `_iter_release_notes` もしくは同等のヘルパーをテキスト用に再設計し、`collect_issue_ids` が従来どおり `issue_ids` / `backport_map` を返せるようロジックを改修する。正準表現維持のためIDフォーマット検証は `_require_jdk_issue_id` を再利用する。
5. `main` および `_write_unique_ids` 等の出力処理が新しい入力にも対応するか確認し、必要なら出力パスの初期化・重複検出が機能するよう調整する。
6. Backport元を参照できなかったIssue IDをXMLから解決した結果で補完し、解決不能な場合は例外として通知する。処理完了後に未解決のIDを標準出力しつつ例外を送出する仕組みを整備する。
7. 手動実行または既存スクリプトでの検証により `issue_ids_output/` 配下の集計結果が期待値と一致することを確認し、必要であれば差分をレビューする。

## 成果物と検証
- 更新済み `issue_ids.py`
- `tmp/temurin_jdk_ids.txt` による中間検証結果
- テキスト入力に対する正常実行ログ/検証結果 (CLI出力確認 or 差分確認)
- Backport補完が行われていることの根拠 (サンプル issue での検証メモ)
- 未解決Backport Issue ID一覧の標準出力記録（同時に例外で処理停止）

## 想定外事項
- `jdk_issues/<ISSUE>` に欠落があった場合は今回新たにエラーとする方針。補完用データを整備してから再実行する想定。
- 既存出力ファイルを上書きする際のベースラインはユーザー確認後に実施する。

上記内容で対応を進めてよいかご確認ください。
