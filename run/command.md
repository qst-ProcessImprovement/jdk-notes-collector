cd run/command.md
python extract_jdk.py
python fetch_jdk_issues.py
python merge_jdk_issues.py --content-mode summary
python aggregate_jdk_issues.py