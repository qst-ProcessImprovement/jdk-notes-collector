OpenJDK 21.0.6+7: 詳細な変更点レポート

1.0 はじめに (Introduction)

本レポートは、OpenJDKのメンテナンスリリースであるバージョン21.0.6および21.0.7に組み込まれた、注目すべき変更点、バグ修正、セキュリティ強化に関する詳細かつ包括的な概要を提供するものです。本文書は、開発者、システム管理者、およびその他の技術関係者がこのアップデートの影響を理解することを目的としています。本レポートを通じて、Javaプラットフォームの継続的な改善と安定化に向けた取り組みについて解説します。

2.0 主要なハイライト (Key Highlights)

提供されたJDKの課題リストを分析した結果、特に開発者やシステム管理者にとって影響が大きいと考えられる変更点は以下の通りです。

* JDK-8325203: System.exit(0) kills the launched 3rd party application
  * 21.0.2で発生した重大なリグレッション（動作退行）が修正されました。このリグレッションにより、Runtime.getRuntime().exec経由で起動した子プロセスが、JavaアプリケーションのSystem.exit(0)呼び出しによって予期せず終了されていました。この修正により、以前の期待された動作（Javaアプリケーション自体のみが終了する）が復元されます。
* JDK-8348625: [21u, 17u] Revert JDK-8185862 to restore old java.awt.headless behavior on Windows
  * Windows環境でのヘッドレスモードの検出方法に関する以前の変更（JDK-8185862）が、多くの自動テストフレームワークで問題を引き起こしたため、差し戻し（revert） されました。この対応により、以前の動作が復元され、テストにおけるリグレッションが解消されます。
* JDK-8337664: Distrust TLS server certificates issued after Oct 2024 and anchored by Entrust Root CAs
  * 2024年10月31日以降に発行され、特定のEntrustおよびAffirmTrustルートCAによってアンカーされたTLSサーバー証明書を信頼しないようにする、予防的なセキュリティ強化策です。この変更により、該当する証明書を使用しているサーバーとのTLSセッションは例外をスローして失敗する可能性があります。
* JDK-8225377, JDK-8320001, JDK-8360406: Series of issues related to type annotations
  * 型アノテーションの可視性に関する一連の修正とリグレッションの結果、より安定した修正が提供されるまでの間、型アノテーションをクラスファイルにアタッチするロジックが無効化されました。javacプラグインやアノテーションプロセッサを利用している開発者は、この変更による影響に注意する必要があります。
* JDK-8327501, JDK-8328366, JDK-8344993: Issues with ForkJoinPool.commonPool, class unloading, and setContextClassLoader
  * 共通のForkJoinPoolのワーカースレッドがクラスのアンロードを妨げる問題が修正されました。ただし、最初の修正がsetContextClassLoaderの呼び出しを妨げるリグレッションを引き起こしたため、このリリースサイクルで慎重に再適用されました。

3.0 詳細な変更点 (Detailed Changes)

3.1 セキュリティ (Security)

このリリースにおけるセキュリティ関連のアップデートは、Javaプラットフォームの信頼性と完全性を維持するための戦略的な重要性を持っています。これらの変更は、証明書の信頼ストアの更新や暗号化コンポーネントの修正に焦点を当てており、プラットフォーム全体の安全性を強化します。

* JDK-8337664: Distrust TLS server certificates issued after Oct 2024 and anchored by Entrust Root CAs
  * これは、特定のEntrustおよびAffirmTrustルートCAによってアンカーされたTLS証明書を、2024年10月31日以降に発行されたものについて信頼しないようにする予防的なセキュリティ措置です。この影響により、該当するサーバーとのTLSセッションはExceptionをスローして失敗する可能性があります。回避策として、jdk.security.caDistrustPoliciesセキュリティプロパティからENTRUST_TLSを削除することが可能です。
* JDK-8349870: Distrust TLS server certificates anchored by Camerfirma Root CAs
  * CamerfirmaのルートCAによってアンカーされたTLSサーバー証明書を信頼しないようにするセキュリティ強化です。この変更は、jdk.security.caDistrustPoliciesセキュリティプロパティにCamerfirmaのルートCAを追加することで、挙動レベルでの信頼無効化を行います。
* JDK-8356530: Remove two Camerfirma root CA certificates
  * 上記（JDK-8349870）のポリシー変更に続く、より恒久的な措置として、2つの特定のCamerfirmaルート証明書がcacerts信頼ストアから完全に削除されます。
* JDK-8340333: SHAKE256 does not work correctly if n >= 137
  * SHAKE256実装で確認されたバグが修正され、正しい動作が保証されるようになりました。
* JDK-8348065: Certificate name constraints improperly validated with leading period
  * 証明書の名前制約（name constraints）において、先頭にピリオドがある場合に検証が正しく行われない問題が解決されました。
* JDK-8351960: Remove Baltimore root certificate expiring in May 2025
  * 2025年5月に有効期限が切れるBaltimoreルート証明書を削除するメンテナンスアップデートです。これにより、信頼ストアの衛生状態が維持されます。
* JDK-8359349: Add 2 TLS and 2 CS Sectigo roots
  * 4つの新しいSectigoルート証明書が信頼ストアに追加されました。

これらのセキュリティアップデートがプラットフォームの防御を固める一方で、次のセクションでは、開発者の日々のコーディングに直接影響するコアライブラリの安定性向上について見ていきます。

3.2 コアライブラリ (Core Libraries)

このセクションでは、ネットワーキング(java.nio)、並行処理(java.util.concurrent)、I/O(java.io)、タイムゾーンデータなど、Javaのコアライブラリに対する修正と改善について説明します。

* JDK-8325203: System.exit(0) kills the launched 3rd party application
  * 21.0.2で発生した重大なリグレッションが修正されました。この問題は、Runtime.getRuntime().execを介して起動された子プロセスが、System.exit(0)によって親のJavaアプリケーションと共に終了してしまうというものでした。この修正により、以前の期待された動作（Javaアプリケーションのみが終了する）が復元されました。
* JDK-8327501, JDK-8328366, JDK-8344993: Issues with ForkJoinPool.commonPool, class unloading, and setContextClassLoader
  * これらの関連するチケットは、ForkJoinPool.commonPool()のワーカースレッドがクラスのアンロードを妨げるという初期の問題に対処します。最初の修正(JDK-8327501)がsetContextClassLoaderの動作を破壊するリグレッション(JDK-8328366)を引き起こしたため、JDK-8344993でこれらの修正を正しく再適用する取り組みが行われました。
* JDK-8337966: (fs) Files.readAttributes fails with Operation not permitted on older docker releases
  * 新しいstatxシステムコールの使用が、古いDockerバージョンのseccompポリシーによってFileSystemExceptionを引き起こす問題が確認されました。この問題は対処済みです。
* JDK-8344678, JDK-8348843, JDK-8352097, JDK-8353921: Timezone Data Updates
  * タイムゾーンデータがバージョン2024b、2025a、および2025bに更新されました。また、以前のアップデートで見落とされていたzone.tabの更新も適用されています。
* JDK-8353096: URLConnection.getLastModified() leaks file handles for jar:file and file: URLs
  * URLConnectionで見つかったリソースリークの問題が修正されました。この修正により、jar:fileおよびfile: URLに対するファイルハンドルが適切に閉じられるようになります。
* JDK-8343520: Repeated call of StringBuffer.reverse with double byte string returns wrong result
  * マルチバイト文字を含む文字列に対してStringBuffer.reverseを繰り返し呼び出すと誤った結果が返されるバグが修正され、正しい文字列反転が保証されるようになりました。
* JDK-8355760: Overflow in Collections.rotate
  * Collections.rotateにおける整数オーバーフローのバグが修正され、大きなコレクションサイズでも正しく動作するようになりました。

これらのライブラリレベルの修正はAPIの信頼性を向上させますが、続いては、Javaアプリケーションの実行基盤そのものであるHotSpot VMのパフォーマンスと安定性に関する重要な改善点を掘り下げます。

3.3 HotSpot VM / ランタイム (HotSpot VM / Runtime)

Java仮想マシン(HotSpot VM)への変更は、プラットフォームの安定性、パフォーマンス、および可観測性の向上に不可欠です。このセクションでは、ガベージコレクタ(ZGC, Shenandoah)、メモリ管理、診断機能に関する修正について詳述します。

* JDK-8348625: [21u, 17u] Revert JDK-8185862 to restore old java.awt.headless behavior on Windows
  * これは重要な差し戻しです。 以前のリリースで導入されたWindowsのヘッドレスモード検出方法の変更が、自動テストフレームワークなどで問題を引き起こしていました。このアップデートでは、その変更が差し戻され、以前の動作が復元されたことで、関連するリグレッションが解消されました。
* JDK-8279016, JDK-8351030: JFR Leak Profiler is broken with Shenandoah
  * JFR Leak ProfilerのオブジェクトマーキングスキームとShenandoah GCのフォワーディングポインタメカニズムが競合し、JVMクラッシュを引き起こす可能性がありました。この非互換性を解決するための修正が実装されました。
* JDK-8332717, JDK-8344408, JDK-8354271: ZGC: Division by zero in heuristics
  * ZGCのヒューリスティックにおいて「ゼロ除算」エラーが発見され、その後の修正でリグレッションや関連するアロケーションレートのルールにおける問題が対処されました。
* JDK-8322475, JDK-8326586, JDK-8351920, JDK-8354579: System.map improvements
  * 診断機能であるSystem.mapおよびSystem.dump_mapが大幅に強化されました。これにより、RSSメモリ使用量、ページサイズ、THP（Transparent Huge Pages）の状態、スワップ状態など、より有用な情報が提供されるようになりました。また、ルックアップのパフォーマンスも改善されています。
* JDK-8341054: Hotspot should be able to use more than 64 logical processors on Windows
  * HotSpot VMがWindowsシステム上で利用できる論理プロセッサ数の上限（64）が撤廃されました。
* JDK-8284620, JDK-8346413: CodeBuffer may leak _overflow_arena
  * リソースとして確保されたCodeBufferインスタンスに関連するメモリリークの問題が修正されました。
* JDK-8346000, JDK-8346108: Native memory leak when not recording any events
  * JFRのネイティブメモリリークに対する修正が含まれましたが、テストの失敗（TestChunkIntegrity.java）が原因で、その後バックアウト（取り消し） されました。これは、このリリースでは元のメモリリークが依然として存在する可能性があることを意味します。

VMの実行基盤が強化されたことに加え、Javaコードのコンパイル時および実行時の両方に関わるjavacとJITコンパイラの修正も行われています。

3.4 コンパイラ (Compiler - javac & JIT)

このセクションでは、Javaコンパイラ(javac)およびJust-In-Time (JIT)コンパイラ(C1/C2)に関連する変更について説明します。

* JDK-8225377, JDK-8320001, JDK-8341779, JDK-8354893, JDK-8360406: Series of issues related to type annotations
  * これは一連の複雑な修正とリグレッションのサイクルです。最初の問題(JDK-8225377)は、javacプラグインがコンパイル境界を越えて型アノテーションを認識できないというものでした。これを修正したところ、コンストラクタの戻り値の型にアノテーションを付けるとクラッシュするリグレッション(JDK-8320001)が発生しました。複数回のバックポートを経て、最終的に、より安定した修正が提供されるまで、このリリースでは型アノテーションをクラスファイルにアタッチするロジックが無効化(JDK-8360406)されました。これはアノテーションプロセッサを使用する開発者にとって重要な情報です。
* JDK-8343828: generic type information lost on mandated parameters of record's compact constructors
  * レコードのコンパクトコンストラクタのパラメータからジェネリック型情報が失われるjavacのバグが修正されました。

これらの変更は、Javaコードのコンパイル時および実行時の両方における正確性と安定性に寄与します。

4.0 全ての修正一覧 (Complete List of Fixes)

本リリースには、本書で詳述した主要な変更点に加え、数百にのぼる小規模なバグ修正、テストの改善、コードのクリーンアップが含まれています。すべての変更点の完全なリストについては、公式のOpenJDKリリースノートをご参照ください。

[公式OpenJDKリリースノートへのリンク]

5.0 結論 (Conclusion)

OpenJDK 21.0.6および21.0.7アップデートは、セキュリティの強化、重大なリグレッションの解決、そしてプラットフォーム全体の安定性と可観測性の向上に焦点を当てた重要なメンテナンスリリースです。特に、子プロセスの意図しない終了やWindowsヘッドレスモードの動作復元など、開発者の生産性に直接影響するリグレッションが修正されました。ユーザーは、自身のアプリケーションへの潜在的な影響を理解するために、本レポートで詳述された変更点を確認することが推奨されます。
