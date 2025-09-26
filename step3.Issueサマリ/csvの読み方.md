CSVの意味と使い方

  - jdk_issues_summary_detail.csv は個別Issueの一覧です。impact_status（除外/要確認）、除外理由(applied_rules/impact_notes)、機能領域(feature_area)、強調タグ(highlight_tags)、対象リリースなどが列に並びます。各行を確認しながら「要確認」分の影響調査や説明資料づくりに利用します。
  - jdk_issues_summary_release.csv はリリース別 × 影響判定（除外/要確認）の件数集計です。21.0.6/21.0.7/21.0.8それぞれでどれくらい確認すべきIssueが残っているかの概数把握に使います。
  - jdk_issues_summary_area.csv はリリース別 × 機能領域 × 影響判定の件数集計です。どの領域（例: runtime_core、classlib、security）が工数の焦点になるかを把握するためのヒートマップ的な見方ができます。

  意図

  - 21.0.5→21.0.8 の差分調査で「除外条件に当たるIssueを自動で弾く」「残りの要確認Issueを領域別・リリース別に俯瞰する」ための補助資料として作成しました。

  閲覧のポイント

  1. まず jdk_issues_summary_release.csv でリリースごとの要確認件数を把握します。
  2. 次に jdk_issues_summary_area.csv でどの領域に注力すべきかを特定します。
  3. 実際の精査は jdk_issues_summary_detail.csv の「要確認」行を順に確認し、影響判定メモ(impact_notes)やラベル情報を参考に調査を進めてください。