# SOW: Temurin出力ファイル名と出力ディレクトリの正準化

## 背景
- `Phage2/run/temurin/issue_ids.py`の`_write_unique_ids`で出力ファイル名に元JSONの名前を用いており、`jdk-XX+YY.json`の`+YY`がそのまま`.txt`側にも残る。
- 出力ファイルを格納するディレクトリ名が`issue_ids`となっており、`output_temurin`で統一したい。

## 対応方針
- 正規表現で`+数字`以降を除去した正準ファイル名を算出し、`.txt`拡張子に差し替えて出力する。
- 出力ディレクトリを`output_temurin`に変更し、正準表現へ統一する。
- 例外や後方互換分岐を追加せず、常に正準表現に統一する。

## 作業項目 (AT)
1. `_write_unique_ids`内で出力ファイル名を生成する処理を見直し、`+数字`サフィックスを除去する関数を追加または内蔵する。
2. 出力ディレクトリを`output_temurin`へ切り替え、ユニークID書き出し処理を調整する。
3. 生成されるファイル名とディレクトリが意図通りであることを既存JSONファイルで確認する（ローカル実行または目視確認）。

## 想定影響範囲（LSP調査）
- `Phage2/run/temurin/issue_ids.py:_write_unique_ids`
  - 呼び出し元: 同ファイル`main`

## 検証
- `python Phage2/run/temurin/issue_ids.py` を実行し、出力ファイル名が`+数字`なしで作成されること、および出力先が`output_temurin`ディレクトリになっていることを確認。

ご確認ください。合意後に実装へ進みます。
