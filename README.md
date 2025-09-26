# jdk-notes-collector

pptx作成はstep4です。INPUTにissueの集計結果があった方が良いと思うので、step1-3で作って下さい。
merge_jdk_issues.py でissueのtitle/descriptionを1ファイルにまとめられます。これをNotebookLMに渡して、Chatに使ってください。

# memo

issueの取得処理（fetch_jdk_issues.py）がものすごく遅いです・・並列化すればよかった。