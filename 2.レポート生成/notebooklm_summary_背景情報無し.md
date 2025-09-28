JDK 21.0.6, 21.0.7, 21.0.8 リリースノートサマリー

このドキュメントは、長期サポート（LTS）リリースであるJDK 21の3つの主要なアップデート（21.0.8, 21.0.7, 21.0.6）に含まれる重要なバグ修正と改善点をまとめたものです。対象読者は、日々の業務でJavaプラットフォームを利用する開発者やシステム管理者です。本サマリーは、これらのアップデートを自身の環境に適用する際の技術的な影響を理解し、意思決定を行うための情報を提供することを目的としています。

1. JDK 21.0.8+9: 主な修正内容

JDK 21.0.8は、JDK 21プラットフォームの安定性、パフォーマンス、セキュリティをさらに向上させるための重要な修正を含むメンテナンスリリースです。このアップデートでは、特にHotSpot VM、コアライブラリ、セキュリティライブラリ、そして開発者向けツールにおける改善に焦点が当てられています。

1.1. HotSpot VMの改善

HotSpot VMにおける修正は、Java仮想マシン（JVM）の信頼性、パフォーマンス、スケーラビリティに直接的な影響を及ぼします。今回のアップデートには、特定のワークロード下でのスケーラビリティ問題の解決や、稀に発生するクラッシュの防止、メモリリークの修正などが含まれています。

* [JDK-8180450]：secondary_super_cache does not scale well 複数のスレッドが特定のクラス階層を頻繁にチェックするような高負荷な状況で、キャッシュの競合によるパフォーマンス低下が発生していました。この修正により、キャッシュ更新の競合を検知し、過度な更新を抑制することで、マルチスレッド環境でのスケーラビリティが向上します。
* [JDK-8337958]：Out-of-bounds array access in secondary_super_cache 上記 JDK-8180450 の修正に関連して、稀に配列の範囲外アクセスが発生する可能性がありました。この修正は、その潜在的な問題を修正し、VMの安定性を高めます。
* [JDK-8338064]：Give better error for ConcurrentHashTable corruption ConcurrentHashTable の内部データが破損した場合に、より詳細で有用なエラーメッセージが出力されるようになりました。これにより、問題の根本原因の特定が容易になります。
* [JDK-8330106]：C2: VectorInsertNode::make() shouldn't call ConINode::make() directly C2コンパイラの内部実装を修正し、ベクトル演算のノード生成ロジックをより適切なものにしました。これにより、コード生成の正確性が向上します。
* [JDK-8330158]：C2: Loop strip mining uses ABS with min int C2コンパイラのループ最適化（ストリップマイニング）において、最小整数値（Integer.MIN_VALUE）の絶対値計算がオーバーフローを引き起こす可能性がありました。この修正は、そのようなエッジケースを正しく処理し、最適化の信頼性を高めます。
* [JDK-8331088]：Incorrect TraceLoopPredicate output ループ述語最適化のトレースログ（-XX:+TraceLoopPredicate）において、上限チェックに関する情報が誤って下限チェックのノードインデックスで出力されていました。この修正により、デバッグ時のログ出力が正確になります。
* [JDK-8340146]：ZGC: TestAllocateHeapAt.java should not run with UseLargePages ZGCのテストにおいて、ラージページ（-XX:+UseLargePages）が有効な場合に特定のファイルシステム（HugeTLBFS）が必要となり、テストが失敗する問題がありました。この修正により、互換性のない構成ではテストがスキップされるようになり、CIの安定性が向上します。
* [JDK-8344414]：ZGC: Another division by zero in rule_major_allocation_rate ZGCのヒューリスティック計算において、特定の条件下でゼロ除算が発生し、ランタイムエラーを引き起こす可能性がありました。この修正は、計算ロジックを保護し、ZGCの堅牢性を向上させます。これらの修正は、ZGCのヒューリスティック計算における堅牢性を向上させ、特定のテスト環境での安定性を確保するものです。
* [JDK-8349637]：Integer.numberOfLeadingZeros outputs incorrectly in certain cases 特定の条件下（配列を使用した短いループ内など）で、Integer.numberOfLeadingZeros のJITコンパイル済みコード（Intrinsic）が、値が変わる境界で1少ない誤った結果を返すことがありました。この修正により、計算の正確性が保証されます。
* [JDK-8350412]：[21u] AArch64: Ambiguous frame layout leads to incorrect traces in JFR AArch64プラットフォームにおいて、コンパイルされたコードからランタイム呼び出しを行う際のスタックフレームレイアウトが曖昧であったため、JFRなどのプロファイリングツールで不正確なスタックトレースが記録される問題がありました。この修正により、フレームレイアウトが明確になり、診断ツールの信頼性が向上します。

1.2. コアライブラリ () の修正

コアライブラリは、Javaの根幹をなす機能（I/O、コレクション、並行処理、ネットワークなど）を提供します。ここでの修正は、アプリケーションの安定性、リソース管理、APIの挙動の一貫性を直接的に改善します。

* [JDK-6956385]：URLConnection.getLastModified() leaks file handles for jar:file and file: URLs jar:file: または file: URLに対して URLConnection.getLastModified() を呼び出すと、内部的に開かれたファイルハンドルがクローズされずにリークする問題がありました。この修正により、リソースリークが防止され、ファイルハンドル枯渇のリスクがなくなります。
* [JDK-8136895]：Writer not closed with disk full error, file resource leaked ディスクフルエラーが発生した際に、try-with-resources構文を使用していてもBufferedWriterが内部でファイルリソースをリークする問題がありました。この修正により、例外発生時にもリソースが確実にクローズされるようになります。
* [JDK-8210471]：GZIPInputStream constructor could leak an un-end()ed Inflater GZIPInputStream のコンストラクタが例外をスローした場合に、内部の Inflater オブジェクトが適切に解放されず、リソースリークを引き起こす可能性がありました。この修正は、コンストラクタの例外パスでリソースを確実に解放します。
* [JDK-8313290]：Misleading exception message from STS.Subtask::get when task forked after shutdown シャットダウン後の StructuredTaskScope でタスクをフォークし、その結果を取得しようとすると、誤解を招く例外メッセージが表示されていました。この修正により、スコープがシャットダウン済みであることを示す、より適切な例外がスローされるようになります。
* [JDK-8314236]：Overflow in Collections.rotate Collections.rotate() メソッドで、引数によっては整数オーバーフローが発生し、IndexOutOfBoundsException を引き起こす可能性がありました。この修正は、オーバーフローを正しく処理し、メソッドの堅牢性を高めます。
* [JDK-8316629]：j.text.DateFormatSymbols setZoneStrings() exception is unhelpful DateFormatSymbols.setZoneStrings() に不正な形式の配列を渡した場合の IllegalArgumentException のメッセージが不親切でした。この修正により、問題の原因を特定しやすいように、より詳細な情報を含むメッセージが提供されます。
* [JDK-8317264]：Pattern.Bound has static fields that should be static final. java.util.regex.Pattern の内部クラス Bound の static フィールドが final でなかったため、変更可能になっていました。これらは定数であるため、final を付与して不変性を保証します。
* [JDK-8322141]：SequenceInputStream.transferTo should not return as soon as Long.MAX_VALUE bytes have been transferred SequenceInputStream.transferTo() が Long.MAX_VALUE バイトを転送した時点で、たとえまだデータが残っていても転送を終了してしまう問題がありました。この修正により、すべてのデータが転送されるまで処理が継続されるようになります。
* [JDK-8335181]：Incorrect handling of HTTP/2 GOAWAY frames in HttpClient HTTP/2クライアントがサーバーから GOAWAY フレームを受信した際の処理に問題があり、不要な IOException がスローされていました。この修正により、GOAWAY フレームがより適切に処理され、接続の安定性が向上します。
* [JDK-8339538]：Wrong timeout computations in DnsClient 内部DNSクライアントにおいて、タイムアウト計算に非単調な時間ソース（System.currentTimeMillis()）が使用されていたため、稀にタイムアウトが正しく機能しない可能性がありました。この修正により、System.nanoTime() を使用するように変更され、タイムアウト処理の信頼性が向上します。
* [JDK-8342075]：HttpClient: improve HTTP/2 flow control checks HTTP/2クライアントのフロー制御ロジックが改善され、フロー制御違反をサーバーに FLOW_CONTROL_ERROR として正しく報告するようになりました。
* [JDK-8343144]：UpcallLinker::on_entry racingly clears pending exception with GC safepoints 外部関数呼び出し（Project Panama）において、GCセーフポイントと競合して保留中の例外をクリアする際に競合状態が発生する可能性がありました。この修正により、スレッドセーフな方法で例外が処理されるようになり、VMの安定性が向上します。
* [JDK-8343855]：HTTP/2 ConnectionWindowUpdateSender may miss some unprocessed DataFrames from closed streams HTTP/2接続において、クローズされたストリームの未処理データが接続全体のフロー制御ウィンドウから差し引かれない競合状態がありました。これにより、WINDOW_UPDATEフレームの送信が遅れ、接続がストールする可能性がありました。この修正は、この競合を解決し、スループットを改善します。これらの修正を総合すると、高負荷なシナリオにおけるHTTP/2クライアントのフロー制御と接続管理の堅牢性が大幅に向上します。
* [JDK-8343019]：Primitive caches must use boxed instances from the archive クラスデータ共有（CDS）アーカイブを使用している場合に、Integer などのプリミティブラッパー型のキャッシュが実行時に再作成されると、アーカイブされたインスタンスとの同一性（==）比較が失敗する問題がありました。この修正により、キャッシュの一貫性が保たれ、予期せぬ動作を防ぎます。
* [JDK-8351933]：Inaccurate masking of TC subfield decrement in ForkJoinPool ForkJoinPool の内部状態を管理する ctl フィールドの更新時に、不正確なビットマスクが使用されていたため、ワーカー数のカウントが破損する可能性がありました。この修正は、正しいマスクを使用することで ForkJoinPool の動作の信頼性を高めます。
* [JDK-8356096]：ISO 4217 Amendment 179 Update ISO 4217通貨コードのデータを更新し、アラブ通貨基金の「アラブ会計ディナール（XAD）」が追加されました。

1.3. セキュリティライブラリ () の修正

セキュリティライブラリの修正は、証明書処理、暗号化サービス、キーストアなど、Javaプラットフォームのセキュリティ基盤を強化します。これにより、脆弱性の修正、プロトコル互換性の向上、スレッドセーフティの確保が図られます。

* [JDK-8200566]：DistributionPointFetcher fails to fetch CRLs if the DistributionPoints field contains more than one DistributionPoint and the first one fails 証明書失効リスト（CRL）の配布ポイントが複数設定されている場合、最初の配布ポイントへのアクセスに失敗すると、後続の配布ポイントが試されずに失効チェックが失敗していました。この修正により、最初の配布ポイントが利用できなくても、リスト内の次の配布ポイントを試行するようになり、失効チェックの可用性が向上します。
* [JDK-8309667]：TLS handshake fails because of ConcurrentModificationException in PKCS12KeyStore.engineGetEntry PKCS12キーストアへのアクセスがスレッドセーフでなかったため、複数のスレッドが同時にTLSハンドシェイクを行うと ConcurrentModificationException が発生することがありました。この修正により、キーストアへのアクセスが同期され、マルチスレッド環境での安定性が向上します。
* [JDK-8325680]：Uninitialised memory in deleteGSSCB of GSSLibStub.c:179 GSS-APIのネイティブ実装において、未初期化メモリが使用される可能性があった問題を修正し、セキュリティと安定性を向上させました。
* [JDK-8327461]：KeyStore getEntry is not thread-safe KeyStore.getEntry() がスレッドセーフでなく、キーストアが同時に更新されると、秘密鍵と証明書チェーンが一致しないエントリが返される可能性がありました。この修正は、PKCS12キーストアの実装に同期を追加し、この問題を解決します。
* [JDK-8328864]：NullPointerException in sun.security.jca.ProviderList.getService() jdk.security.provider.preferred プロパティを使用して特定のプロバイダを優先するように設定した場合、存在しないサービスを要求すると NullPointerException が発生していました。この修正により、無効なサービスが返されなくなり、期待どおり NoSuchAlgorithmException がスローされます。
* [JDK-8336499]：Failure when creating non-CRT RSA private keys in SunPKCS11 SunPKCS11プロバイダで、非CRT形式のRSA秘密鍵を生成する際に、特定のPKCS#11トークンとの互換性問題で失敗することがありました。この修正により、属性の問い合わせ方法が改善され、互換性が向上します。
* [JDK-8344361]：Restore null return for invalid services from legacy providers レガシー形式のセキュリティプロバイダから無効なサービス（例：クラス名がnull）が返された場合に NullPointerException が発生する問題がありました。この修正により、無効なサービスは nullとして扱われ、後続の処理でのクラッシュを防ぎます。
* [JDK-8347506]：Compatible OCSP readtimeout property with OCSP timeout OCSPのタイムアウト設定プロパティ com.sun.security.ocsp.readtimeout のデフォルト値が、com.sun.security.ocsp.timeout の値と一致するように変更され、設定の一貫性が向上しました。
* [JDK-8347596]：Update HSS/LMS public key encoding HSS/LMS（階層型署名システム/レイトン-ミカリ-シュノール署名）の公開鍵エンコーディングが、最新のRFC 9708に準拠するように更新されました。具体的には、ASN.1によるラッピングが除去されました。

1.4. ツールとコマンド () の修正

javac や jar などの開発ツールに関する修正は、開発者の生産性向上に直結します。コンパイラのクラッシュ回避、リソース管理の改善、エラーメッセージの明確化などが含まれます。

* [JDK-8312475]：org.jline.util.PumpReader signed byte problem jshellなどで使用されるjlineライブラリの PumpReader クラスにおいて、バイトから文字への変換で符号付きバイトの問題があり、特定の入力で不正な文字が生成される可能性がありました。この修正は、正しい変換を行うことで問題を解決します。
* [JDK-8320948]：NPE due to unreported compiler error コンパイラがジェネリクスを含むコードで型推論エラーを報告し損ねた結果、後続の処理で NullPointerException が発生し、クラッシュする問題がありました。この修正により、根本的なエラーが正しく報告されるようになり、クラッシュが回避されます。
* [JDK-8337795]：Type annotation attached to incorrect type during class reading クラスファイルを読み込む際に、同じ型が複数回出現する場合、型アノテーションが誤った場所に関連付けられることがありました。この修正により、アノテーションが正しい型に正確に付与されるようになります。
* [JDK-8339810]：Clean up the code in sun.tools.jar.Main to properly close resources and use ZipFile during extract jar コマンドの実装において、リソースが適切にクローズされていなかった箇所が修正されました。また、展開処理で ZipInputStream の代わりに ZipFile を使用することで、効率と信頼性が向上しました。
* [JDK-8341779]：[REDO BACKPORT] type annotations are not visible to javac plugins across compilation boundaries (JDK-8225377) クラスパスから読み込まれたクラスの型アノテーションが、javacプラグインから見えないことがあるという JDK-8225377 の問題を再修正しました。これにより、アノテーションプロセッサや静的解析ツールが、コンパイル境界を越えてもアノテーションを正しく認識できるようになります。
* [JDK-8347296]：WinInstallerUiTest fails in local test runs if the path to test work directory is longer that regular Windowsにおいて、テスト用の作業ディレクトリのパスが長すぎると、jpackage関連のテストが失敗する問題がありました。これはmsi.exeのパス長制限によるもので、テスト内のファイル名を短くすることで回避されました。

1.5. その他の重要な修正 (Client-libs, Core-svcなど)

GUIアプリケーションの安定性やデバッグ機能の信頼性向上に寄与する、その他のコンポーネントにおける重要な修正を以下にまとめます。

* [JDK-8270269]：Desktop.browse method fails if earlier CoInitialize call as COINIT_MULTITHREADED (client-libs) Windowsにおいて、JNIなどを介してCOMがマルチスレッドモードで初期化されている場合、Desktop.browse() が失敗するリグレッションがありました。この修正により、COMの初期化状態に関わらず、ブラウザを正しく起動できるようになりました。
* [JDK-8348110, JDK-8348596, etc.]：Update third-party libraries (client-libs) 以下のグラフィックスおよびサウンド関連のサードパーティライブラリが最新バージョンに更新されました：LCMS 2.17, FreeType 2.13.3, HarfBuzz 10.4.0, Libpng 1.6.47, PipeWire 1.3.81。
* [JDK-8348936]：[Accessibility,macOS,VoiceOver] VoiceOver doesn't announce untick on toggling the checkbox with "space" key on macOS (client-libs) macOSのVoiceOver使用時に、スペースキーでチェックボックスのチェックを外しても「チェック解除」がアナウンスされないアクセシビリティの問題が修正されました。
* [JDK-8286789]：Test forceEarlyReturn002.java timed out (core-svc) JVMTIの機能である ForceEarlyReturn に関するテストのタイムアウト問題が修正されました。デバッグエージェントの安定性が向上します。
* [JDK-8308033]：The jcmd thread dump related tests should test virtual threads (core-svc) jcmd のスレッドダンプ関連テストが、仮想スレッドを対象に含んでいなかったため、テストカバレッジが向上するように修正されました。
* [JDK-8333680]：com/sun/tools/attach/BasicTests.java fails with "SocketException: Permission denied: connect" (core-svc) Attach APIのテストが、特定のネットワーク構成（VPN利用時など）で失敗する問題がありました。ワイルドカードアドレスの代わりにループバックアドレスを使用することで、テストの安定性が向上しました。
* [JDK-8357193]：[VS 2022 17.14] Warning C5287 in debugInit.c: enum type mismatch during build (core-svc) 最新のVisual Studio 2022でビルドする際に発生していたJDWPエージェントのコンパイル警告が修正されました。
* [JDK-8344925]：translet-name ignored when package-name is also set (xml) XSLTのTransletを生成する際に、package-name と translet-name 属性を同時に設定すると translet-name が無視される問題がありました。この修正により、両方の属性が正しく尊重され、GraalVM Native Imageなどでのビルド時クラス生成が容易になります。

JDK 21.0.8の修正は、プラットフォームの成熟度をさらに高めるものです。次に、JDK 21.0.7の主な修正内容を見ていきます。

2. JDK 21.0.7+6: 主な修正内容

JDK 21.0.7は、主にクライアントライブラリ、コアライブラリ、およびツールの安定性向上に焦点を当てたリリースです。特筆すべき点として、古いアプレットベースのAWT/Swingテストを最新のフレームワークへ移行する近代化作業が大規模に継続されており、品質保証プロセスの信頼性が向上しています。

2.1. コアライブラリ () とネットワークの改善

このセクションの修正は、特にHttpClientの堅牢性とリソース管理を改善し、ネットワーク通信の信頼性を高めます。

* [JDK-8304701]：Request with timeout aborts later in-flight request on HTTP/1.1 cxn HTTP/1.1の持続的接続上で、タイムアウト付きのリクエストが時間切れになると、そのリクエストが完了済みであっても接続が強制的にクローズされ、同じ接続を使用中の他のリクエストが中断される問題がありました。この修正により、タイムアウトイベントが完了済みリクエストを不必要に中断しなくなり、接続の安定性が向上します。
* [JDK-8317808]：HTTP/2 stream cancelImpl may leave subscriber registered HTTP/2ストリームのキャンセル処理において、競合状態によって購読者（subscriber）が適切に登録解除されない可能性がありました。この修正により、キャンセル処理がより堅牢になり、リソースリークのリスクが低減されます。
* [JDK-8339687]：Rearrange reachabilityFence()s in jdk.test.lib.util.ForceGC テストライブラリの強制GCユーティリティにおいて、Reference.reachabilityFence() の呼び出し位置が不適切で、意図したガベージコレクションの抑止効果が得られていない可能性がありました。この修正により、ユーティリティの信頼性が向上します。
* [JDK-8339834]：Replace usages of -mx and -ms in some tests 一部のテストで、古い形式のJVMオプション -ms および -mx が使用されていました。これらは非推奨であり、将来のバージョンで削除される可能性があるため、標準の -Xms および -Xmx に置き換えられました。
* [JDK-8343144]：UpcallLinker::on_entry racingly clears pending exception with GC safepoints (21.0.8でも言及) 外部関数呼び出し（Project Panama）において、GCセーフポイントとの競合状態によりVMの安定性が損なわれる可能性があった問題が修正されました。
* [JDK-8345368]：java/io/File/createTempFile/SpecialTempFile.java fails on Windows Server 2025 Windows Server 2025において、OS予約名（例：com7）を持つ一時ファイルの作成テストが失敗していました。この修正により、テストが新しいOSバージョンを認識し、適切に動作するようになりました。
* [JDK-8352097]：(tz) zone.tab update missed in 2025a backport タイムゾーンデータ2025aのアップデートにおいて、zone.tabファイルの更新が漏れていたため、これを適用しました。

2.2. セキュリティライブラリ () の修正

セキュリティライブラリの修正は、証明書の検証ロジックとデータの一貫性を向上させ、プラットフォームの安全性を強化します。

* [JDK-8302111]：Serialization considerations デシリアライゼーション（直列化復元）時に、コンストラクタで実施されるようなデータ検証が不足している可能性があったため、追加のチェックが導入され、データの整合性が強化されました。
* [JDK-8311546]：Certificate name constraints improperly validated with leading period CA証明書の名前制約（Name Constraints）がピリオドで始まる場合（例：.example.com）、その制約の検証が不適切に行われ、正当な証明書が誤って拒否される問題がありました。この修正により、検証ロジックが修正され、RFCに準拠した動作となります。
* [JDK-8339356]：Test javax/net/ssl/SSLSocket/Tls13PacketSize.java failed with java.net.SocketException Windows環境でTLS 1.3関連のテストが、SocketException: An established connection was aborted で断続的に失敗していました。この修正により、テストの安定性が向上しました。
* [JDK-8345414]：Google CAInterop test failures GoogleのルートCAとの相互運用性テストにおいて、OCSP検証用のURLが変更されたため、テストが失敗していました。この修正により、URLが更新され、テストが正常に完了するようになりました。
* [JDK-8347424]：Fix and rewrite sun/security/x509/DNSName/LeadingPeriod.java test JDK-8311546 に関連するテストが、実際には意図した検証を行えていなかったため、テストケースが修正・簡素化され、修正内容の妥当性が正しく検証されるようになりました。

2.3. ツール () と HotSpot VM () の修正

jpackageやjarなどの開発者向けツールの使いやすさ向上と、HotSpot VMの安定性強化を目的とした修正が行われました。

* [JDK-8227529]：With malformed --app-image the error messages are awful (tools) jpackage コマンドで不正な形式の --app-image を指定した場合のエラーメッセージが不親切でした。この修正により、NullPointerException ではなく、原因を特定しやすい具体的なメッセージが出力されるようになりました。
* [JDK-8339810]：Clean up the code in sun.tools.jar.Main to properly close resources and use ZipFile during extract (tools) (21.0.8でも言及) jar ツールの内部実装が改善され、リソースリークの防止と効率化が図られました。
* [JDK-8342609]：jpackage test helper function incorrectly removes a directory instead of its contents only (tools) jpackage のテスト用ヘルパー関数が、ディレクトリの内容だけでなくディレクトリ自体を誤って削除していました。この修正により、テストの挙動が意図通りになりました。
* [JDK-8343102]：Remove --compress from jlink command lines from jpackage tests (tools) jpackage のテスト内で使用されていた jlink の --compress オプションは非推奨であるため、テストコードから削除されました。
* [JDK-8295159]：DSO created with -ffast-math breaks Java floating-point arithmetic (hotspot) GCCの -ffast-math オプション付きでビルドされたネイティブ共有ライブラリをロードすると、JVMの浮動小数点演算のセマンティクスが破壊される問題がありました。この修正は、System.loadLibrary() の前後で浮動小数点制御ワードを保存・復元することで、この問題を緩和します。このアプローチは完全ではありませんが（実行時に別の共有ライブラリがロードされる可能性があるため）、従来よりも大幅に改善されています。
* [JDK-8284620, JDK-8336692]：CodeBuffer may leak _overflow_arena (hotspot) JITコンパイラのコード生成バッファである CodeBuffer で、特定の条件下でメモリリークが発生する可能性がありました。この問題が修正され、VMのメモリフットプリントが改善されました。
* [JDK-8337994]：[REDO] Native memory leak when not recording any events (hotspot) JFR（Java Flight Recorder）において、イベントを何も記録していない場合でも、スレッドの開始・終了時にネイティブメモリがリークする問題がありました。この修正は、RecordingStream を使用するアプリケーションの長期安定稼働に寄与します。
* [JDK-8340824]：C2: Memory for TypeInterfaces not reclaimed by hashcons() (hotspot) C2コンパイラが型情報を処理する際に、重複したインターフェース情報を削除しても、関連するメモリが解放されないことがありました。この修正により、コンパイル時のメモリ使用量が削減されます。

2.4. クライアントライブラリ () の近代化と修正

このリリースでは、古いAppletベースのSwing/AWTテストを、スタンドアロンのメインプログラムとして実行できる最新のテストフレームワーク（PassFailJFrame）に移行する作業が大規模に行われました。これにより、テストの保守性と信頼性が大幅に向上し、GUIコンポーネントの品質維持に貢献しています。

* [JDK-8315825, etc.]：AppletベースのAWT/Swingテストのメインプログラムへの移行 多数のクローズドソースだったSwingテストがオープンソース化され、Appletへの依存が排除されました。これにより、テストスイート全体の近代化が進みました。（JDK-8315882, JDK-8315883, JDK-8315952, JDK-8316056, JDK-8316146, JDK-8316149, JDK-8316218, JDK-8316371 など多数のチケットが含まれます。）
* [JDK-8327857, etc.]：JColorChooserテストのApplet使用廃止 JColorChooserコンポーネントに関連する一連のテストから、非推奨のAppletが削除されました。（JDK-8327859, JDK-8328121, JDK-8328130, JDK-8328227, JDK-8328380, JDK-8328403 などが含まれます。）
* [JDK-8339728]：[Accessibility,Windows,JAWS] Bug in the getKeyChar method of the AccessBridge class WindowsのAccessBridgeにおいて、JMenuItem のショートカットキー（例：「Ctrl + Comma」）がスクリーンリーダーによって誤ってアナウンスされる（例：「Ctrl + C」）アクセシビリティの問題が修正されました。
* [JDK-8347911]：Limit the length of inflated text chunks PNGイメージ内の圧縮テキストチャンク（zTXt, iTXt）を伸長する際に、過大なメモリ消費を防ぐためのサイズ制限が導入されました。これにより、不正な形式の画像ファイルを処理する際の堅牢性が向上します。
* [JDK-8348625]：[21u, 17u] Revert JDK-8185862 to restore old java.awt.headless behavior on Windows Windows環境でのヘッドレスモードの検出ロジック変更（JDK-8185862）が、自動テスト環境などで問題を引き起こしたため、以前の動作に戻されました。これにより、既存環境との互換性が回復します。

JDK 21.0.7は、特にテストインフラの近代化を通じて、長期的な品質向上に貢献するリリースでした。最後に、JDK 21.0.6の修正内容を確認します。

3. JDK 21.0.6+7: 主な修正内容

JDK 21.0.6は、HotSpot VM、セキュリティ、コアライブラリにわたる広範な安定性向上を目的としたリリースです。このアップデートには、特定のCPUアーキテクチャ（AArch64, RISC-V）における修正や、デバッグ体験の向上に貢献する重要な変更が含まれています。

3.1. HotSpot VMの安定性向上

このセクションの修正は、特定アーキテクチャでの互換性、メモリ管理、およびVM全体の堅牢性を強化するものです。

* [JDK-8308429]：jvmti/StopThread/stopthrd007 failed with "NoClassDefFoundError" 仮想スレッドが有効な環境で、特定のJVMTIテストが NoClassDefFoundError で失敗していました。この修正により、仮想スレッド関連のデバッグ機能の安定性が向上します。
* [JDK-8316428]：G1: Nmethod count statistics only count last code root set iterated G1 GCの統計情報において、コンパイル済みメソッド（nmethod）の数が不正確にカウントされていました。この修正により、GC関連のモニタリングと診断がより正確になります。
* [JDK-8319960]：RISC-V: compiler/intrinsics/TestInteger/LongUnsignedDivMod.java failed RISC-Vアーキテクチャにおいて、符号なし64ビット整数の除算・剰余演算に関するIntrinsic（JITコンパイラによる高速化）のテストが失敗していました。この修正は、RISC-Vポートの正確性を向上させます。
* [JDK-8319973]：AArch64: Save and restore FPCR in the call stub AArch64アーキテクチャにおいて、Javaコードの実行前後で浮動小数点制御レジスタ（FPCR）の状態が保存・復元されていませんでした。これにより、JNI経由で呼び出された場合に、Javaの浮動小数点セマンティクスに準拠しない可能性がありました。この修正により、互換性が向上します。
* [JDK-8320892]：AArch64: Restore FPU control state after JNI 一部のネイティブライブラリが浮動小数点制御レジスタを破壊することがあるため、JNI呼び出し後にFPUの状態を復元する仕組みが導入されました（x86のRestoreMXCSROnJNICallsに相当）。これにより、ネイティブコードとの連携における安定性が向上します。
* [JDK-8336911]：ZGC: Division by zero in heuristics after JDK-8332717 ZGCのヒューリスティック計算において、ゼロ除算が発生する可能性があった別のケースが修正され、GCの安定性がさらに高まりました。
* [JDK-8337066]：Repeated call of StringBuffer.reverse with double byte string returns wrong result 2バイト文字（サロゲートペアなど）を含む StringBuffer や StringBuilder に対して reverse() を繰り返し呼び出すと、誤った結果が返されることがありました。このJITコンパイラのバグが修正され、文字列操作の正確性が保証されます。
* [JDK-8340383]：VM issues warning failure to find kernel32.dll on Windows nanoserver Windows Nanoserver環境でJVMを起動する際に、kernel32.dll が見つからないという不要な警告が表示されていました。この修正により、警告が出力されなくなりました。
* [JDK-8340387]：Update OS detection code to recognize Windows Server 2025 OS検出ロジックが更新され、Windows Server 2025を正しく認識できるようになりました。

3.2. セキュリティとコアライブラリの修正

デバッグログの統一性、暗号化アルゴリズムの正確性、およびコアAPIの挙動に関する修正が含まれています。

* [JDK-8296787]：Unify debug printing format of X.509 cert serial numbers (security-libs) X.509証明書のシリアル番号が、デバッグログ内で3つの異なる形式で出力されていました。この修正により、出力形式が統一され、ログの可読性と解析のしやすさが向上しました。
* [JDK-8318105]：[jmh] the test java.security.HSS failed with 2 active threads (security-libs) HSS/LMS署名アルゴリズムのベンチマークテストが、マルチスレッド実行時に失敗していました。この修正により、スレッドセーフティが改善され、テストが安定しました。
* [JDK-8320192]：SHAKE256 does not work correctly if n >= 137 (security-libs) SHAKE256ハッシュ関数の実装にバグがあり、特定の出力長（137バイト以上）でNISTのテストベクターに失敗していました。この修正により、アルゴリズムが正しく実装され、信頼性が向上します。
* [JDK-8321543]：Update NSS to version 3.96 (security-libs) PKCS#11プロバイダのテストで使用されるNSS (Network Security Services) ライブラリがバージョン3.96に更新されました。
* [JDK-8342181, etc.]：Update tests to use stronger algorithms and keys (security-libs) セキュリティ関連のテストにおいて、弱い鍵や古いアルゴリズムが使用されていた箇所が、より強力なものに更新されました。これにより、テストスイート自体のセキュリティが向上しました。（JDK-8342183, JDK-8342188 を含む）
* [JDK-8320575]：generic type information lost on mandated parameters of record's compact constructors (core-libs) Recordのコンパクトコンストラクタのパラメータから、リフレクション経由でジェネリック型情報が取得できないというリグレッションがありました。この修正により、JDK 17以前の挙動が復元され、型情報が正しく取得できるようになります。
* [JDK-8323562]：SaslInputStream.read() may return wrong value (core-libs) SaslInputStream.read() メソッドが、InputStream の仕様（0-255の範囲の値を返す）に反して、負の値を返す可能性がありました。この修正により、仕様に準拠した正しい値が返されるようになります。
* [JDK-8344993]：[21u] [REDO] Backport JDK-8327501 and JDK-8328366 to JDK 21 (core-libs) ForkJoinPool.commonPool() がクラスアンロードを妨げる問題（JDK-8327501）と、その修正に起因するsetContextClassLoaderの互換性問題（JDK-8328366）が、一度バックアウトされた後、再修正として適用されました。これにより、動的なクラスアンロードを行うアプリケーションの安定性が向上します。

3.3. ツールとビルドインフラの修正

jlinkによるランタイムイメージ作成時の問題解決や、外部アプリケーション起動時の挙動変更など、開発およびデプロイメントに影響する修正が含まれています。

* [JDK-8322809]：SystemModulesMap::classNames and moduleNames arrays do not match the order (tools) jlinkでランタイムイメージを作成する際に、モジュール名が com. で始まり、かつ jdk.httpserver に依存していると Module ... not in boot Layer というエラーで起動に失敗する問題がありました。この修正により、内部のモジュールマップが正しく構築され、問題が解決します。
* [JDK-8325203]：System.exit(0) kills the launched 3rd party application (tools) Windowsにおいて、Javaアプリケーションから Runtime.exec() で起動した外部プロセスが、元のJavaアプリが System.exit(0) で終了すると一緒に終了してしまうというリグレッションがありました。この修正により、以前のバージョンのように、子プロセスは独立して実行を継続するようになりました。
* [JDK-8338402]：GHA: some of bundles may not get removed (infrastructure) GitHub Actionsのビルドプロセスにおいて、生成された成果物（バンドル）の一部が削除されないことがある問題が修正されました。CIの安定性とリソース管理が改善されます。
* [JDK-8342578]：GHA: RISC-V: Bootstrap using Debian snapshot is still failing (infrastructure) RISC-Vアーキテクチャ向けのクロスビルド環境の構築に関する問題が修正され、ビルドの信頼性が向上しました。
* [JDK-8343474]：[updates] Customize README.md to specifics of update project (infrastructure) アップデートリポジトリの README.md ファイルが、プロジェクト固有の情報を含むようにカスタマイズされ、新規貢献者へのガイドが改善されました。

これらの定期的なアップデートは、JDK 21プラットフォームの安定性、セキュリティ、および全体的な品質を着実に向上させるための継続的な取り組みの成果です。開発者および運用担当者は、自身の環境と要件に基づいて、これらのアップデートの適用を検討することが推奨されます。
