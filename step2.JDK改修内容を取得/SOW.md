# SOW: JDK 課題 XML 収集モジュール作成

## 背景と調査結果
- `jdk.txt` に 130 件超の JDK 課題 ID (正準表記 `JDK-<number>`) が格納されていることを確認済み。
- 各課題の XML は `https://bugs.openjdk.org/si/jira.issueviews:issue-xml/{issue}/{issue}.xml` で取得可能 (例: `JDK-8325937`)。
- 標準ライブラリ (`urllib.request`) で取得可能な想定。HTTP 404 等で取得不可となる ID が存在する前提でスキップ処理が必要。
- Serena LSP についてはプロジェクト未設定でシンボル取得不可 (`No active project. Ask user to select a project from this list: ['VBA-Server']`) のため、影響シンボルは手動整理。

## 対応方針 (AT)
1. `jdk.txt` を読み込み、空行や重複を除外した正準 ID リストを生成する処理を実装。
2. 各 ID について、出力ルート配下に `{issue}` ディレクトリを作成し、`jdk-{number}.xml` にコンテンツを保存。HTTP 200 以外はスキップ対象として記録。
3. スキップした ID を `skipped.txt` (まとめ用) に追記し、処理結果を標準出力へサマリ表示。

## 影響範囲 (暫定)
- 新規モジュール `fetch_jdk_issues.py` (仮称) を追加予定。
- 既存の `extract_jdk.py` とのインターフェースは独立しており、既存処理への影響は想定なし。

## 確認事項
- 出力先のルートディレクトリ名称 (例: `jdk_issues/`) に指定はあるか。なければ `jdk_issues/` とする予定。
- スキップ一覧ファイルの配置場所 (同一ルート直下で問題ないか)。

ご確認のうえ、問題なければ着手します。修正方針の追加・変更要望があればお知らせください。
