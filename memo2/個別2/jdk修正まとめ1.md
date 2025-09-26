OpenJDK 21.0.6+7における変更点の詳細解説

1. はじめに

このドキュメントは、OpenJDKのアップデートリリース 21.0.6+7 に含まれる主要なバグ修正、機能改善、およびセキュリティ強化に関する詳細な技術的概要を提供します。このリリースは、OpenJDKプラットフォームの安定性、パフォーマンス、セキュリティを継続的に向上させることを目的とした、四半期ごとのメンテナンスリリースです。本稿では、Hotspot VM、コアライブラリ、クライアントライブラリ、セキュリティ、サービス性、そしてツールとインフラストラクチャの各領域における重要な変更点について、シニアJavaプラットフォームエンジニアの視点から解説します。

2. Hotspot VMの改善

Hotspot VMは、Javaプラットフォームの性能と安定性の中核を担う極めて重要なコンポーネントです。Just-In-Time (JIT) コンパイラによる動的なコード最適化、効率的なメモリ管理を実現するガベージコレクション（GC）、そしてJavaアプリケーションの実行時環境を提供するランタイムシステムなど、多岐にわたる機能を内包しています。このセクションで解説する修正は、これらの基盤機能における安定性を向上させ、特定のワークロード下でのエッジケースや、クロスプラットフォームにおける一貫性の問題を解決するものです。これらの改善は、プラットフォーム全体の信頼性を直接的に高めることに貢献します。

JITコンパイラ (JIT Compiler - C1/C2)

JDK-8343524: C2 compilation asserts with "no node with a side effect" in PhaseIdealLoop::try_sink_out_of_loop

C2コンパイラのループ最適化フェーズにおいて、副作用のない特定のノードをループ外に移動しようとする際にアサーションエラーが発生する問題が確認されました。この修正は、最適化ロジックの前提条件を強化し、不正なコード変換を未然に防ぐことでコンパイラの堅牢性を高めます。

JDK-8343349: C2: assert(!loop->is_member(get_loop(useblock))) failed: must be outside loop

C2コンパイラのループ最適化処理において、特定のコードブロックがループのメンバーシップ判定で矛盾した状態と判断され、アサーションエラーが発生する問題がありました。この修正は、ループ構造の解析ロジックを改善し、コンパイラの堅牢性を高めます。

JDK-8342516: [AArch64] C1 compilation fails with "Field too big for insn"

AArch64アーキテクチャにおいて、C1コンパイラが特定の命令の即値フィールドサイズを超える値を生成しようとしてコンパイルに失敗する問題がありました。この修正は、命令生成ロジックを修正し、アーキテクチャの制約内で正しいコードを生成するようにします。

JDK-8341322: C1: assert(0 <= i && i < _len) failed: illegal index 5 for length 5

C1コンパイラにおいて、配列のインデックスチェックで不正なアクセスが検知され、アサーションエラーが発生する問題がありました。この修正は、インデックス計算のロジックを修正し、コンパイラの安定性を確保します。

JDK-8341323: Parsing jsr broken: assert(bci>= 0 && bci < c->method()->code_size()) failed: index out of bounds

古い jsr バイトコード命令のパース処理にバグがあり、不正なバイトコードインデックス（bci）アクセスによりアサーションエラーが発生していました。この修正は、jsr のパースロジックを修正し、古い形式のクラスファイルでも安全に処理できるようにします。

JDK-8342056: C2: Fix UB of jlong overflow in PhaseIdealLoop::is_counted_loop()

C2コンパイラのループ解析フェーズにおいて、jlong 型のオーバーフローによる未定義動作（Undefined Behavior）が発生する可能性がありました。この修正は、オーバーフローを適切に処理し、ループカウンタの判定を安全に行うようにします。

JDK-8344406: [PPC64] Disallow OptoScheduling

PPC64アーキテクチャにおいて、不安定性の原因となることがあるOptoScheduling（最適化スケジューリング）を無効化しました。

JDK-8344805: [s390x] Disallow OptoScheduling

s390xアーキテクチャにおいても、不安定性の原因となることがあるOptoSchedulingを無効化しました。

JDK-8339624: AArch64: C2_MacroAssembler::fast_lock uses rscratch1 for cmpxchg result

AArch64において、C2のマクロアセンブラが高速ロック処理でcmpxchg命令の結果にrscratch1レジスタを使用する際の不整合を修正しました。

JDK-8340158: x86 MacroAssembler may over-align code

x86のマクロアセンブラが、必要以上にコードをアライメントすることがあり、コードサイズがわずかに増大する問題がありました。この修正は、アライメント処理を最適化します。

ガベージコレクション (Garbage Collection - G1, ZGC, Shenandoah)

JDK-8341192: Concurrent GC crashed due to GetMethodDeclaringClass

並行ガベージコレクション（Concurrent GC）の実行中に、特定の条件下で GetMethodDeclaringClass 内部でクラッシュが発生する問題が特定されました。これは、クラスアンローディングとGCマーキング間の競合状態に起因するものです。この修正は、関連処理に適切な同期を追加することで、GCプロセスの安定性を確保します。

JDK-8343538: C2/Shenandoah: SEGV in compiled code when running jcstress

Shenandoah GC環境下で jcstress テストを実行すると、C2コンパイラが生成したコード内でセグメンテーション違反が発生する問題が確認されました。これは、GCバリアとコンパイラ最適化の相互作用に起因するものでした。この修正は、Shenandoah GCバリアの処理を改善し、生成されるコードの安全性を確保します。

JDK-8341823: ZGC: Division by zero in rule_major_allocation_rate

ZGCのヒューリスティックにおいて、メジャーGCの割り当てレートを計算する際にゼロ除算が発生する可能性がありました。この修正は、計算前にゼロチェックを追加し、ランタイムエラーを防ぎます。

JDK-8343028: G1: Nmethod count statistics only count last code root set iterated

G1 GCにおいて、nmethod（コンパイル済みメソッド）の統計情報が、最後に処理されたコードルートセットの情報しかカウントしないというバグがありました。この修正により、全てのルートセットが正しく集計されるようになります。

JDK-8342851: Shenandoah: Unused ShenandoahSATBAndRemarkThreadsClosure::_claim_token

Shenandoah GCのコードベースから、現在使用されていない _claim_token メンバーを削除するクリーンアップです。

JDK-8343591: ubsan: shenandoahFreeSet.cpp:1347:24: runtime error: division by zero

Undefined Behavior Sanitizer (ubsan) によって、Shenandoah GCの空き領域管理コード内でゼロ除算ランタイムエラーが検出されました。この修正は、ゼロチェックを追加してエラーを回避します。

JDK-8344408: ZGC: Division by zero in heuristics after JDK-8332717

JDK-8332717の修正後に、ZGCのヒューリスティックで別のゼロ除算が発生する可能性が発見されました。この修正は、この新たなケースにも対応します。

JDK-8344591: Shenandoah: Parallel worker use in parallel_heap_region_iterate

Shenandoah GCにおいて、ヒープリージョンを並列に処理する際のワーカーの利用方法を改善し、効率を高めました。

JDK-8345228: UnsafeIntrinsicsTest.java#ZGenerationalDebug assert(!assert_on_failure) failed: Has low-order bits set

ZGC（Generational）環境下でのUnsafe組み込み関数のテストで、オブジェクトポインタの下位ビットが設定されていることを検出するアサーションが失敗する問題を修正しました。

ランタイムと仮想スレッド (Runtime & Virtual Threads)

JDK-8340886: Tests crash: assert(...) failed: sanity

VMの内部処理において、クラスやインターフェースのプロパティを検証する際のサニティチェック（健全性確認）でアサーションエラーが発生し、テストがクラッシュする問題が特定されました。エンコーディング範囲の検証ロジックに起因するもので、この修正により検証条件が適正化され、VMの安定性が向上しました。

JDK-8343520: Repeated call of StringBuffer.reverse with double byte string returns wrong result

StringBuffer.reverseメソッドを、2バイト文字（サロゲートペアなど）を含む文字列に対して繰り返し呼び出すと、不正な結果が返されるバグが確認されました。これは文字列反転ロジックがマルチバイト文字を正しく扱えていなかったためです。この修正は、反転アルゴリズムを修正し、いかなる文字セットでも一貫した正しい結果を保証します。

JDK-8339681: crash: pinned virtual thread will lead to jvm crash when running with the javaagent option

Javaエージェント（-javaagent）が有効な環境で、ピニングされた仮想スレッドが存在する場合にJVMがクラッシュする問題が特定されました。エージェントによるクラス変換と仮想スレッドの状態管理との間に競合が発生していたことが原因です。この修正は、両者の相互作用を改善し、エージェント利用時の仮想スレッドの安定性を確保します。

JDK-8340136: serviceability/jvmti/vthread/PopFrameTest failed with a timeout

仮想スレッド環境下でのJVMTI PopFrame 機能のテストがタイムアウトにより失敗する問題がありました。この修正は、テスト内の同期処理を改善し、安定して完了するようにします。

JDK-8341054: Hotspot should be able to use more than 64 logical processors on Windows

Windowsプラットフォームにおいて、Hotspot VMが64を超える論理プロセッサを認識・利用できないという制限が存在しました。この修正は、プロセッサグループのサポートを改善し、64コア以上の大規模なサーバー環境でも全てのCPUリソースを効率的に活用できるようにすることで、スケーラビリティを向上させます。

JDK-8341112: VM issues warning failure to find kernel32.dll on Windows nanoserver

Windows Nano Server環境において、存在しない kernel32.dll をVMが検索しようとして警告ログが出力される問題がありました。この修正は、プラットフォーム固有のライブラリ依存関係を正しく解決し、不要な警告の出力を抑制することで、クリーンな実行環境を提供します。

JDK-8341515: Update OS detection code to recognize Windows Server 2025

VMのOS検知ロジックが、次期バージョンのWindows Server 2025を正しく認識できませんでした。この修正は、OSバージョン情報を最新化し、新しいプラットフォーム上での適切な動作を保証するためのものです。

JDK-8345290: java.lang.Process is unresponsive and CPU usage spikes to 100%

java.lang.Processの実装において、特定条件下でプロセス管理のスレッドが応答不能になり、CPU使用率が100%に達する問題がありました。この修正は、プロセス状態のポーリングと同期のロジックを改善し、リソースの過剰消費を防ぎます。

JDK-8340782: Unintentional IOException in jdk.jdi module when JDWP end of stream occurs

JDWP（Java Debug Wire Protocol）のストリームが終端に達した際に、jdk.jdiモジュール内で意図しないIOExceptionがスローされる問題を修正しました。

アーキテクチャ固有の修正 (Architecture-Specific Fixes)

JDK-8340817: RISC-V: C ABI breakage for integer on stack

RISC-Vアーキテクチャにおいて、スタック経由で整数を渡す際のC言語ABI（Application Binary Interface）に非互換性が生じる問題が確認されました。この修正は、C ABIに準拠した正しいスタックアライメントとパラメータ渡しを実装し、クロスコンパイル環境での互換性を確保します。

JDK-8342060: AArch64: Save and restore FPCR in the call stub

AArch64アーキテクチャにおいて、特定の呼び出しスタブが浮動小数点制御レジスタ（FPCR）の状態を正しく保存・復元していなかったため、浮動小数点演算の結果に影響を与える可能性がありました。この修正は、FPCRの適切な管理を徹底し、演算の正確性を保証します。

JDK-8342571: AArch64: Restore FPU control state after JNI

AArch64アーキテクチャにおいて、JNI呼び出しから復帰する際に浮動小数点ユニット（FPU）の制御状態が正しくリストアされない問題がありました。この修正は、JNI境界でのFPU状態の復元を確実に行い、演算の一貫性を保ちます。

JDK-8343210: [PPC64] TestOSRLotsOfLocals.java crashes

PPC64アーキテクチャにおいて、多数のローカル変数を持つメソッドのOSR（On-Stack Replacement）コンパイルをテストする際にクラッシュが発生しました。この修正は、PPC64固有のスタックフレーム処理を改善し、OSRの安定性を向上させます。

JDK-8343301: [s390x] TestOSRLotsOfLocals.java crashes

s390xアーキテクチャにおいて、多数のローカル変数を持つメソッドのOSRコンパイルをテストする際にクラッシュが発生しました。この修正は、s390x固有のスタックフレーム処理を改善し、OSRの安定性を向上させます。

JDK-8339273: RISC-V: compiler/intrinsics/TestInteger/LongUnsignedDivMod.java failed with "counts: Graph contains wrong number of nodes"

RISC-Vプラットフォームにおいて、符号なし整数除算・剰余の組み込み関数に関するテストが、期待されるIRノード数と一致しないために失敗していました。この修正は、RISC-V向けのコード生成を修正し、テストが正しくパスするようにします。

JDK-8339397: RISC-V: C2: Change C calling convention for sp to NS

RISC-VアーキテクチャのC2コンパイラにおいて、スタックポインタ（sp）の扱いをC言語の呼び出し規約に準拠させるための修正です。

JDK-8339589: RISC-V: Remove li64 macro assembler routine and related code

RISC-Vのマクロアセンブラから、現在では使用されていない li64 ルーチン（64ビット即値ロード）と関連コードを削除するリファクタリングです。

JDK-8339841: AArch64: u32 _partial_subtype_ctr loaded/stored as 64

AArch64において、32ビットのサブタイプカウンター _partial_subtype_ctr が誤って64ビットとしてロード・ストアされていた問題を修正しました。

JDK-8340626: [s390x] Provide implementation for resolve_global_jobject

s390xアーキテクチャにおいて、これまで未実装だった resolve_global_jobject 関数の実装を提供しました。

JDK-8341479: [PPC64] SA determines wrong unextendedSP

PPC64アーキテクチャにおいて、Serviceability Agent (SA) が拡張されていないスタックポインタ（unextendedSP）の値を誤って判断する問題を修正しました。

JDK-8341960: RISC-V: Generate comments in -XX:+PrintInterpreter to link to source code

RISC-Vアーキテクチャにおいて、-XX:+PrintInterpreter オプションの出力に、対応するソースコードへのリンクとなるコメントを生成するよう改善しました。

JDK-8341973: RISC-V: C2: Small improvement to vector gather load and scatter store

RISC-VアーキテクチャのC2コンパイラにおいて、ベクターのギャザーロードおよびスカッターストア命令の生成をわずかに改善しました。

JDK-8342391: RISC-V: Unnecessary fences used for load-acquire in template interpreter

RISC-Vのテンプレートインタプリタにおいて、load-acquire 操作で不要なメモリフェンスが使用されていたため、これを削除しました。

JDK-8342395: Assertion on AIX - original PC must be in the main code section of the compiled method

AIXプラットフォームにおいて、コンパイルされたメソッドのコードセクションをPCが指していることを確認するアサーションが失敗する問題を修正しました。

JDK-8342396: RISC-V: Avoid passing t0 as temp register to MacroAssembler:: cmpxchg_obj_header/cmpxchgptr

RISC-Vのマクロアセンブラにおいて、cmpxchg 関連の命令で一時レジスタとして t0 を渡さないように修正しました。

JDK-8342532: RISC-V: ZStoreBarrierStubC2 clobbers rflags

RISC-Vにおいて、ZGCのストアバリアスタブが rflags レジスタの内容を破壊する問題を修正しました。

JDK-8342572: Aarch64: Generate comments in -XX:+PrintInterpreter to link to source code

AArch64アーキテクチャにおいても、-XX:+PrintInterpreter の出力にソースコードへのリンクとなるコメントを生成するよう改善しました。

JDK-8343203: [PPC64]: postalloc_expand_java_dynamic_call_sched does not copy all fields

PPC64アーキテクチャにおいて、動的呼び出しスケジューリングのデータ構造のフィールドが全てコピーされていなかった問題を修正しました。

JDK-8344404: [s390x] multiple test failures with ubsan

s390xプラットフォームにおいて、Undefined Behavior Sanitizer (ubsan) を有効にすると多数のテストが失敗する問題を修正しました。

JDK-8344405: Enhance register printing on x86_64 platforms

x86_64プラットフォームにおいて、クラッシュダンプなどに出力されるレジスタ情報の表示を強化し、より多くの情報が含まれるようにしました。

JDK-8344407: [s390x] ProblemList hotspot/jtreg/runtime/NMT/VirtualAllocCommitMerge.java

s390xプラットフォームで失敗するNMT（Native Memory Tracking）関連のテストを問題リストに追加しました。

JDK-8345227: [s390x] C1 unwind_handler fails to unlock synchronized methods with LM_MONITOR

s390xアーキテクチャにおいて、C1コンパイラが生成したコードの例外ハンドラが、特定の同期メソッドのロックを解除できない問題を修正しました。

内部ツールとテスト (Internal Tooling & Tests)

JDK-8340156: ResolvedReferencesNotNullTest.java failed with Incorrect resolved references array, quxString should not be archived

Class Data Sharing (CDS) のテストにおいて、特定の条件下で解決済みの参照配列が不正な状態になり、アーカイブされるべきでない文字列がアーカイブに含まれてしまう問題が確認されました。この修正は、CDSの参照解決ロジックを修正し、アーカイブの内容が常に正しく生成されることを保証します。

JDK-8340160: runtime/cds/DeterministicDump.java fails with File content different at byte ...

Class Data Sharing (CDS) アーカイブの生成において、決定論的なダンプを行うテストが稀に失敗する問題が確認されました。この修正は、CDSダンププロセスにおけるデータ書き込み順序を厳密に制御することで、常に同一のアーカイブが生成されることを保証します。

JDK-8343645: TestLoadBypassesNullCheck.java fails improperly specified VM option

特定のVMオプションが不適切に指定された場合に、nullチェックのバイパスに関するテストが失敗する問題がありました。この修正は、テスト自体のオプションハンドリングを改善し、より信頼性の高い検証を可能にします。

JDK-8344416: [JFR] Long strings should be added to the string pool

Java Flight Recorder (JFR) において、長い文字列がイベントペイロードに直接埋め込まれていたため、JFRデータのサイズが肥大化する原因となっていました。この修正により、長い文字列は文字列プールに格納されるようになり、JFRファイルのサイズ削減と解析効率の向上が図られます。

JDK-8339146: Exclude Fingerprinter::do_type from ubsan checks

この変更は、Fingerprinter::do_type関数をUndefined Behavior Sanitizer (ubsan) のチェック対象から除外します。これは、特定の低レベルな型操作がubsanによって誤検知されるのを防ぐための措置です。

JDK-8339147: SeenThread::print_action_queue called on a null pointer

VMの内部診断機能において、SeenThread::print_action_queueが稀にnullポインタで呼び出され、クラッシュを引き起こす可能性がありました。この修正は、呼び出し前にnullチェックを追加することで、診断時の安定性を向上させます。

JDK-8339272: AArch64: enable tests compiler/intrinsics/Test(Long|Integer)UnsignedDivMod.java on aarch64

この変更は、AArch64プラットフォームでこれまで無効化されていた符号なし整数除算・剰余の組み込み関数に関するテストを有効化するものです。

JDK-8339315: [test] runtime/os/TestTracePageSizes move ppc handling

TestTracePageSizes テスト内のPowerPC (ppc) アーキテクチャ固有の処理ロジックを、より適切な場所に移動・整理するリファクタリングです。

JDK-8339323: map_or_reserve_memory_aligned Windows enhance remap assertion

Windowsプラットフォームにおけるメモリマッピング処理のアサーションメッセージを強化し、再マッピングに失敗した場合に、より詳細なデバッグ情報が出力されるように改善しました。

JDK-8339585: remove old remap assertion in map_or_reserve_memory_aligned after JDK-8338058

以前の修正（JDK-8338058）に伴い、古い冗長なアサーションを削除するコードクリーンアップです。

JDK-8339814: Clean up vmTestbase/nsk/stress/stack tests

スタック関連のストレステスト（vmTestbase/nsk/stress/stack）群を整理し、古くなったコードや冗長な部分を削除するクリーンアップ作業です。

JDK-8340154: Update several runtime/cds tests to use vm flags or mark as flagless

Class Data Sharing (CDS) に関連する複数のランタイムテストを更新し、必要なVMフラグを明示的に指定するか、フラグ不要としてマークしました。

JDK-8340155: TestCDSVMCrash fails on libgraal

Graal JITコンパイラ（libgraal）を使用している環境で、CDS関連のVMクラッシュテストが失敗する問題がありました。この修正により、libgraal環境でもテストが正しく動作するようになります。

JDK-8340157: Add JavacBench as a test case for CDS

Class Data Sharing (CDS) の性能と安定性を評価するため、新たなベンチマークテストとして JavacBench を追加しました。

JDK-8340159: Update vmTestbase/nsk/share/DebugeeProcess.java to don't use finalization

テストインフラの一部である DebugeeProcess.java から、非推奨となったファイナライゼーションの使用を取り除きました。

JDK-8340356: ubsan: bytecodeInfo.cpp:318:59: runtime error: division by zero

Undefined Behavior Sanitizer (ubsan) によって、bytecodeInfo.cpp 内でゼロ除算ランタイムエラーが検出されました。この問題を修正し、VMの安定性を向上させました。

JDK-8340430: MethodExitTest may fail with stack buffer overrun

MethodExit イベントを扱うJVMTIテストにおいて、スタックバッファオーバーランが発生する可能性がありました。この修正は、バッファ管理を改善し、テストの安全性を確保します。

JDK-8340500: TestAutoCreateSharedArchiveUpgrade.java should be updated with JDK 21

CDSの共有アーカイブ自動生成に関するテストを、JDK 21の仕様に合わせて更新しました。

JDK-8340502: Make 5 compiler tests use ProcessTools.executeProcess

5つのコンパイラ関連テストにおいて、プロセスの起動・管理方法を標準的なテストライブラリ ProcessTools.executeProcess に統一しました。

JDK-8340607: Exceptions::wrap_dynamic_exception() doesn't have ResourceMark

例外処理の内部関数 Exceptions::wrap_dynamic_exception において、ResourceMark が設定されていなかったため、リソースリークの可能性がありました。この修正により、適切なリソース管理が保証されます。

JDK-8340615: Update JCStress test suite

Java Concurrency Stress (JCStress) テストスイートを最新版に更新し、並行処理に関する検証カバレッジを向上させました。

JDK-8340630: vmTestbase/gc/g1/unloading/tests/unloading_keepRef_rootClass_inMemoryCompilation_keep_cl failed with Full gc happened. Test was useless.

G1 GCのクラスアンローディングに関するテストが、「Full GCが発生したためテストが無意味になった」という理由で失敗していました。この修正は、テストが意図しないFull GCをトリガーしないように調整します。

JDK-8341259: Improve CDSHeapVerifier in handling of interned strings

Class Data Sharing (CDS) のヒープ検証ツール CDSHeapVerifier を改善し、internされた文字列の扱いをより正確に行うようにしました。

JDK-8341821: The class LogSelection copies uninitialized memory

ログ選択を扱う LogSelection クラスにおいて、未初期化メモリをコピーする可能性がありました。この修正により、未定義動作を回避し、ロギングシステムの信頼性を向上させます。

JDK-8341943: Exclude two compiler/rtm/locking tests on ppc64le

ppc64leプラットフォームで不安定な動作を示す2つのRTM（Restricted Transactional Memory）関連のコンパイラテストを、一時的に実行対象から除外しました。

JDK-8341962: ubsan : dependencies.cpp:906:3: runtime error: load of value 4294967295, which is not a valid value for type 'DepType'

Undefined Behavior Sanitizer (ubsan) によって、依存関係を管理するコード内で不正な型の値をロードするランタイムエラーが検出されました。この修正は、型安全性を確保します。

JDK-8342020: [IR Framework] Add support for IR tests with @Stable

IR（中間表現）テストフレームワークに、@Stable アノテーションをサポートする機能を追加しました。

JDK-8342021: Test testlibrary_tests/ir_framework/tests/TestPrivilegedMode.java fails with release build

リリースビルド環境において、IRテストフレームワーク自体のテストである TestPrivilegedMode.java が失敗する問題を修正しました。

JDK-8342048: runtime/logging/ClassLoadUnloadTest.java doesn't reliably trigger class unloading

クラスのロード・アンロードをログ出力するテストが、確実にはクラスアンロードをトリガーできていませんでした。この修正は、テスト内でGCをより確実に実行させることで、検証の信頼性を高めます。

JDK-8342050: Test runtime/classFileParserBug/Bad_NCDFE_Msg.java won't compile

不正なクラスファイルに関するエラーメッセージを検証するテストが、コンパイルエラーを起こしていました。この修正により、テスト自体が正しくビルド・実行されるようになります。

JDK-8342527: Ubsan: ciEnv.cpp:1660:65: runtime error: member call on null pointer of type 'struct CompileTask'

Undefined Behavior Sanitizer (ubsan) によって、コンパイラインタフェース環境（ciEnv）内で CompileTask のnullポインタに対してメンバ呼び出しを行うランタイムエラーが検出されました。

JDK-8342551: Tests assume UnlockExperimentalVMOptions is disabled by default

いくつかのテストが、UnlockExperimentalVMOptions がデフォルトで無効であることを前提としており、有効になっている環境で失敗していました。この修正は、このオプションの状態に依存しないようにテストを修正します。

JDK-8342710: CTW: Add StressIncrementalInlining to stress options

Compile-Time Weaver (CTW) のストレステストオプションに、インクリメンタルなインライン化を強制する StressIncrementalInlining を追加しました。

JDK-8342722: [JVMCI] Unintuitive behavior of UseJVMCICompiler option

JVMCI（Java VM Compiler Interface）を有効にする UseJVMCICompiler オプションの挙動が直感的でなかった点を改善しました。

JDK-8342669: [21u] Fix TestArrayAllocatorMallocLimit after backport of JDK-8315097

JDK-8315097のバックポートに伴い、TestArrayAllocatorMallocLimit テストに不整合が生じたため、これを修正しました。

JDK-8342765: [21u] RTM tests assume UnlockExperimentalVMOptions is disabled by default

JDK 21アップデートリリースにおいて、RTM関連のテストが UnlockExperimentalVMOptions が無効であることを前提としていた問題を修正しました。

JDK-8343909: runtime/cds/appcds/ProhibitedPackage.java can fail with UseLargePages

-XX:+UseLargePages オプションが有効な場合に、AppCDSの禁止パッケージに関するテストが失敗する可能性がありました。この修正は、ラージページ使用時でもテストの安定性を向上させます。

JDK-8343914: Update nsk.share.Log to don't print summary during VM shutdown hook

テスト用のロギングライブラリが、VMのシャットダウンフック中にサマリーを出力することで問題を引き起こす可能性があったため、この挙動を修正しました。

JDK-8344290: The makefiles should set problemlist and adjust timeout basing on the given VM flags

ビルドシステム（makefiles）を改善し、指定されたVMフラグに応じて、問題リストの適用やテストのタイムアウト値を自動的に調整するようにしました。

JDK-8344409: ubsan: division by zero in sharedRuntimeTrans.cpp

ubsanによって、共有ランタイムのコード内でゼロ除算が検出されました。この問題を修正し、安定性を向上させました。

JDK-8344410: Ubsan: ciEnv.cpp:1614:65: runtime error: member call on null pointer of type 'struct CompileTask'

ubsanによって、ciEnv内でCompileTaskのnullポインタに対するメンバ呼び出しが再び検出されました。この修正は、別のコードパスにおける同様の問題を修正します。

JDK-8344605: docker tests do not work when ubsan is configured

ubsanを有効にしてビルドした場合に、Docker関連のテストが動作しない問題を修正しました。

JDK-8344623: Do libubsan1 installation in test container only if requested

テストコンテナ内で、ubsanライブラリのインストールを、ubsanが要求された場合にのみ行うようにビルドスクリプトを修正しました。

JDK-8344676: Fix some warnings as errors when building on Linux with toolchain clang

Linux上でClangツールチェインを使用してビルドする際に、警告がエラーとして扱われることでビルドが失敗する問題を修正しました。

JDK-8344803: VectorGatherMaskFoldingTest.java failed when maximum vector bits is 64

最大ベクターサイズが64ビットの環境で、ベクターのギャザーマスクフォールディングに関するテストが失敗する問題を修正しました。

JDK-8344864: Fix nonnull-compare warnings

コードベース内の、non-nullとマークされたポインタをnullと比較している警告を修正しました。

JDK-8344962: Test TestPrivilegedMode.java intermittent fails java.lang.NoClassDefFoundError: jdk/test/lib/Platform

TestPrivilegedMode.java テストが、テストライブラリのクラスを見つけられずに稀に失敗する問題を修正しました。

JDK-8345180: Problemlist vmTestbase/vm/mlvm/meth/stress/compiler/deoptimize/Test.java#id1 until JDK-8320865 is fixed

根本的な問題（JDK-8320865）が修正されるまで、関連する不安定なテストを問題リストに追加しました。

JDK-8345055: [21u] ProblemList failing rtm tests on ppc platforms

PowerPCプラットフォームで失敗するRTM関連テストを問題リストに追加しました。

JDK-8345311: Test TestEnableJVMCIProduct.java run with virtual thread intermittent fails

仮想スレッドを使用してJVMCI製品版を有効にするテストが、稀に失敗する問題を修正しました。

JDK-8343920: compiler/c1/TestTraceLinearScanLevel.java occasionally times out with -Xcomp

-Xcompモードで実行した際に、C1コンパイラの線形スキャンレジスタ割り当てのトレースに関するテストが稀にタイムアウトする問題を修正しました。

Hotspot VMの安定性向上は、Javaプラットフォーム全体の信頼性の基盤を固める上で不可欠です。これらの低レベルな修正は、次に解説するコアライブラリの改善と相まって、より堅牢な実行環境を提供します。

3. コアライブラリの修正

Java SEプラットフォームのコアライブラリは、java.lang, java.util, java.io, java.nio といった基本的なパッケージ群から構成され、あらゆるJavaアプリケーションの基盤を形成します。これらのライブラリの信頼性と効率は、開発者が構築するシステムの品質に直接影響します。このアップデートに含まれる修正は、ネットワーキング（NIO）、並行処理（concurrency）、ファイルI/O、そして言語機能の基盤となるリフレクションやメソッドハンドルといった領域に及びます。これらの改善により、日常的なJava操作の安定性が向上し、エッジケースにおける予期せぬ挙動が解消されます。

JDK-8342726: Tests create files in src tree instead of scratch dir

一部のテストが、作業用の一時ディレクトリではなく、ソースコードツリー内にファイルを生成してしまう問題がありました。この修正は、テストが正しい作業ディレクトリを使用するように変更し、ソースツリーの汚染を防ぎます。

JDK-8343612: LambdaForm customization via MethodHandle::updateForm is not thread safe

MethodHandle::updateForm を介した LambdaForm のカスタマイズ処理にスレッドセーフティの問題があり、競合状態が発生する可能性がありました。この修正は、関連するデータ構造へのアクセスを適切に同期することで、マルチスレッド環境下での安全性を保証します。

JDK-8338748: [17u,21u] Test Disconnect.java compile error: cannot find symbol after JDK-8299813

JDK-8299813のバックポート後、Disconnect.java テストがJDK 17/21環境でコンパイルエラーを起こす問題が特定されました。テストコードがJDK 22で導入された InetAddress.ofLiteral APIを使用していたためです。この修正は、古いJDKバージョンでも利用可能なAPIに書き換えることで、互換性を回復させます。

JDK-8340783: java/util/concurrent/locks/Lock/OOMEInAQS.java still times out with ZGC, Generational ZGC, and SerialGC

特定のGC（ZGC, Generational ZGC, SerialGC）を使用した場合に、AQS（AbstractQueuedSynchronizer）のOOM（OutOfMemoryError）ハンドリングに関するテストがタイムアウトする問題が継続していました。この修正は、GCの挙動とテストのタイミング依存性を考慮し、テストが安定して完了するように調整します。

JDK-8341941: (se) Deferred close of SelectableChannel may result in a Selector doing the final close before concurrent I/O on channel has completed

SelectableChannel の遅延クローズ処理において、競合するI/O操作が完了する前に Selector がチャネルを最終的にクローズしてしまう競合状態が存在しました。この修正は、クローズ処理の同期を強化し、I/O操作の完了を待ってからチャネルを閉じることで、データの損失や予期せぬエラーを防ぎます。

JDK-8343828: generic type information lost on mandated parameters of record's compact constructors

レコード（Record）のコンパクトコンストラクタにおいて、必須パラメータに付与されたジェネリック型情報がリフレクションAPIを通じて取得できない問題がありました。この修正は、コンパイラが型情報を正しく保持するようにし、リフレクションの正確性を向上させます。

JDK-8344678: (tz) Update Timezone Data to 2024b

IANAが提供するタイムゾーンデータベースをバージョン 2024b に更新しました。これにより、世界各国の夏時間ルールの変更やタイムゾーンの修正が反映され、日付・時刻計算の正確性が維持されます。

JDK-8344964: Test AsyncClose.java intermittent fails - Socket.getInputStream().read() wasn't preempted

ソケットの非同期クローズに関するテストが、read() 操作が期待通りに中断されずに稀に失敗する問題がありました。この修正は、非同期クローズの割り込みメカニズムを改善し、テストの信頼性を高めます。

JDK-8337966: (fs) Files.readAttributes fails with Operation not permitted on older docker releases

古いバージョンのDocker環境（v19以前）において、Files.readAttributes が statx システムコールを使用しようとして Operation not permitted エラーで失敗するリグレッションが確認されました。この修正は、statx が失敗した場合に従来の stat へとフォールバックするロジックを導入し、古い環境との互換性を回復させます。

JDK-8340447: Improve parsing of Day/Month in tzdata rules

タイムゾーンデータベース（tzdata）のルールファイルをパースする際の、日（Day）と月（Month）の解析ロジックを改善し、より柔軟なフォーマットに対応できるようにしました。

JDK-8340550: Files.isReadable/isWritable/isExecutable expensive when file does not exist

存在しないファイルに対して Files.isReadable/isWritable/isExecutable を呼び出すと、内部で不要な処理が行われ、パフォーマンスが低下する問題がありました。この修正は、ファイルが存在しない場合の処理パスを最適化し、オーバーヘッドを削減します。

JDK-8340589: update manual test/jdk/TEST.groups

手動テストのグループ定義ファイルである TEST.groups を更新し、最新のテスト構成を反映させました。

JDK-8340603: Retire binary test vectors in test/jdk/java/util/zip/ZipFile

java.util.zip.ZipFile のテストで使用されていた古いバイナリ形式のテストベクターを廃止し、よりモダンで管理しやすい形式に置き換えました。

JDK-8340604: Add test case for ZipFile opening a ZIP with no entries

エントリを一つも含まないZIPファイルを ZipFile で開く場合のテストケースを追加し、エッジケースのカバレッジを向上させました。

JDK-8340612: DeflaterDictionaryTests should use Deflater.getBytesWritten instead of Deflater.getTotalOut

Deflater のテストにおいて、圧縮バイト数の検証に getTotalOut の代わりに getBytesWritten を使用するように修正しました。後者はより正確な値を提供するため、テストの信頼性が向上します。

JDK-8340734: Add tests for virtual threads doing Selector operations

仮想スレッドが java.nio.channels.Selector を使用するシナリオのテストを追加しました。これにより、仮想スレッドとNIOの連携に関する安定性が保証されます。

JDK-8340776: Java file extension missing in AuthenticatorTest

AuthenticatorTest のテストファイル名に .java 拡張子が欠けていたため、これを修正しました。

JDK-8340989: update jdk_core at open/test/jdk/TEST.groups

TEST.groups ファイル内の jdk_core テストグループの定義を更新しました。

JDK-8341016: java/nio/channels/Selector/SelectWithConsumer.java#id0 failed in testWakeupDuringSelect

Selector の select 操作中に wakeup を呼び出すテストが失敗する問題がありました。この修正は、NIOの内部的な同期処理を改善し、テストの安定性を確保します。

JDK-8341824: ProcessHandleImpl os_getChildren sysctl call - retry in case of ENOMEM and enhance exception message

ProcessHandle が子プロセスを取得する際に sysctl を呼び出して ENOMEM エラーが発生した場合に、リトライ処理を追加しました。また、例外メッセージをより詳細にすることで、問題の診断を容易にしました。

JDK-8342057: ProblemList java/nio/channels/DatagramChannel/ for Macos

macOSプラットフォームで不安定な DatagramChannel 関連のテストを問題リストに追加しました。

JDK-8342063: [21u][aix] Backport introduced redundant line in ProblemList

AIXプラットフォーム向けのバックポート作業において、問題リストに重複した行が追加されてしまったため、これを削除しました。

JDK-8342900: SaslInputStream.read() may return wrong value

SaslInputStream の read() メソッドが、特定の条件下で不正な値（読み込んだバイト数）を返す可能性がありました。この修正は、内部バッファの管理を改善し、正しい値を返すことを保証します。

JDK-8343354: Add extra diagnostic to java/net/InetAddress/ptr/Lookup.java

InetAddress の逆引き（PTR）ルックアップに関するテストに、診断用の追加ログ出力を加え、デバッグを容易にしました。

JDK-8343363: Reading from an input stream backed by a closed ZipFile has no test coverage

クローズされた ZipFile からの入力ストリーム読み込みに関するテストカバレッジが不足していたため、これを検証するテストケースを追加しました。

JDK-8343368: Add some additional diagnostic output to java/net/ipv6tests/UdpTest.java

IPv6環境でのUDP通信テストに、診断用の追加ログ出力を加え、問題解析を支援します。

JDK-8343464: ClassicFormat::parseObject (from DateTimeFormatter) does not conform to the javadoc and may leak DateTimeException

DateTimeFormatter から得られる Format オブジェクトの parseObject メソッドが、Javadocの仕様と異なり、ParseException でラップされるべき DateTimeException をリークする可能性がありました。この修正は、仕様通りに例外をラップするように挙動を修正します。

JDK-8343611: Acknowledge case insensitive unambiguous keywords in tzdata files

タイムゾーンデータベース（tzdata）ファイル内のキーワードについて、大文字・小文字を区別しない曖昧さのないものについては受け入れるようにパーサーを改善しました。

JDK-8344296: java/net/httpclient/ManyRequests2.java fails intermittently on Linux

Linux環境において、多数のリクエストを送信するHTTPクライアントのテストが稀に失敗する問題がありました。この修正は、テスト内のタイミングやリソース管理を調整し、安定性を向上させます。

JDK-8344574: ThreadLocal.nextHashCode can be static final

ThreadLocal クラスの内部フィールド nextHashCode は static final として宣言できるため、そのように変更しました。これは、コードの意図を明確にする小規模なリファクタリングです。

JDK-8344679: Several tests from corelibs areas ignore VM flags

コアライブラリ関連のいくつかのテストが、外部から渡されたVMフラグを無視していました。この修正により、テスト実行時に TESTJAVAOPTS が適切に適用されるようになります。

JDK-8344958: Harden TzdbZoneRulesCompiler against missing zone names

TzdbZoneRulesCompilerの堅牢性を強化し、タイムゾーンデータベースのコンパイル時にゾーン名が存在しないエッジケースを処理できるようにしました。これにより、不正なtzdataファイルに対する回復力が高まります。

JDK-8344993: [21u] [REDO] Backport JDK-8327501 and JDK-8328366 to JDK 21

ForkJoinPool.commonPool に起因するクラスアンロード妨害の問題（JDK-8327501）と、それに伴う互換性の問題（JDK-8328366）の修正を、関連する追加修正と共に再度JDK 21にバックポートしました。これにより、アプリケーションサーバ等でのメモリリークを防ぎつつ、互換性の問題も解決されます。

JDK-8345417: Thread.setContextClassloader from thread in FJP commonPool task no longer works after JDK-8327501 redux

上記の ForkJoinPool の修正再適用後、commonPool内のタスクから setContextClassLoader を呼び出すと SecurityException が発生するリグレッションが再発しました。この修正は、セキュリティを維持しつつコンテキストクラスローダの設定を許可するように、再度アクセス制御の仕組みを調整します。

JDK-8342942: Unused ClassValue in VarHandles

java.lang.invoke.VarHandles の内部実装で、使用されていない ClassValue フィールドが存在したため、これを削除しました。コードのクリーンアップです。

JDK-8345437: Add an operation mode to the jar command when extracting to not overwriting existing files

jarコマンドに、既存のファイルを上書きしない新しい操作モードを追加しました。この機能は、展開時に設定ファイルやユーザーデータを保持したい場合に特に有用です。

これらのコアライブラリの修正は、Javaプラットフォームの信頼性を高め、開発者がより安定した基盤の上でアプリケーションを構築できることを保証します。次に、主にデスクトップアプリケーションに影響するクライアントライブラリの更新点について見ていきます。

4. クライアントライブラリの更新

AWT（Abstract Window Toolkit）やSwingは、JavaでデスクトップGUIアプリケーションを構築するためのクライアントライブラリです。これらのライブラリは、OSネイティブのUIコンポーネントとの連携や、Java独自のLook & Feelを提供し、クロスプラットフォームで一貫したユーザーインターフェースを実現する役割を担います。このセクションで紹介する修正は、特定のプラットフォーム（特にmacOS）でのウィンドウ管理やコンポーネント描画に関する不具合、UIコンポーネントのイベント処理におけるエッジケース、そしてテストインフラの改善に焦点を当てています。これらの更新は、エンドユーザーの体験向上に直接的に貢献します。

JDK-8340023: [macos13] setFullScreenWindow() shows black screen on macOS 13 & above

macOS 13以降の環境で、AWT/Swingアプリケーションが setFullScreenWindow() メソッドを呼び出すと、ウィンドウが黒一色で表示されるリグレッションが発生していました。この修正は、macOSの新しいウィンドウ管理APIに適切に対応することで、フルスクリーン表示を正常に復元します。

JDK-8340170: Update ProblemList.txt with tests known to fail on XWayland

XWayland環境で既知の失敗が確認されているAWT/Swing関連のテストを、問題リスト（ProblemList.txt）に追加しました。これにより、CIシステムでの不要な失敗報告を抑制し、開発者が真の問題に集中できるようになります。

JDK-8342554: Crash in ImageIO JPEG decoding when MEM_STATS in enabled

メモリ統計（MEM_STATS）を有効にしてビルドしたJDKにおいて、ImageIOライブラリでJPEG画像をデコードする際にクラッシュが発生する問題がありました。この修正は、内部のメモリ管理ロジックを修正し、診断ビルドでの安定性を確保します。

JDK-8343042: When the Tab Policy is checked,the scroll button direction displayed incorrectly.

Swingの JTabbedPane において、タブポリシーがスクロールに設定されている場合、スクロールボタンの向きが不正に表示されることがありました。この修正は、レイアウト計算ロジックを修正し、正しい向きのボタンを描画するようにします。

JDK-8343043: click JComboBox when dialog about to close causes IllegalComponentStateException

ダイアログが閉じられる直前のタイミングで JComboBox をクリックすると、IllegalComponentStateException が発生する競合状態が存在しました。この修正は、コンポーネントの状態遷移をより安全に処理することで、例外の発生を防ぎます。

JDK-8343254: [macos] Screen magnifier does not show the magnified text for JComboBox

macOSのスクリーンリーダー機能「画面拡大」を使用している際に、JComboBox のテキストが拡大表示されないアクセシビリティの問題がありました。この修正は、macOSのアクセシビリティAPIとの連携を改善し、コンポーネントの内容が正しく拡大されるようにします。

JDK-8343255: [macos] Regression: KeyEvent has different keycode on different keyboard layouts

macOSにおいて、異なるキーボードレイアウトを使用すると KeyEvent が返すキーコードが異なるというリグレッションが発生していました。この修正は、キーイベント処理を修正し、レイアウトに依存しない一貫したキーコードを返すようにします。

JDK-8343364: Remove wildcard bound in PositionWindows.positionTestWindows

テストライブラリ内の PositionWindows.positionTestWindows メソッドから、不要なワイルドカード境界（wildcard bound）を削除するリファクタリングです。コードの可読性と保守性を向上させます。

JDK-8339815: gtk headers : Fix typedef redeclaration of GMainContext and GdkPixbuf

GTKライブラリのヘッダーファイルにおいて、GMainContext と GdkPixbuf の typedef が再宣言されることでコンパイル警告が発生していました。この修正は、重複する宣言を排除し、クリーンなビルドを実現します。

JDK-8340169: [macos13] java/awt/Frame/MaximizedToIconified/MaximizedToIconified.java: getExtendedState() != 6 as expected.

macOS 13環境で、最大化されたフレームをアイコン化（最小化）した際の getExtendedState() の戻り値が期待通りでないテスト失敗がありました。この修正は、プラットフォームの挙動変化に対応し、テストが正しくパスするようにします。

JDK-8340429: java/awt/Mouse/EnterExitEvents/ResizingFrameTest.java duplicate in ProblemList

問題リストに ResizingFrameTest.java が重複して記載されていたため、一方を削除しました。

JDK-8340508: [XWayland] move screencast tokens from .awt to .java folder

XWayland関連のテストで使用されるスクリーンキャスト用のトークンファイルを、より適切なディレクトリに移動しました。テストインフラの整理の一環です。

JDK-8340879: java.desktop/share/classes/javax/swing/text/html/default.css typo in margin settings

SwingのHTMLレンダリングで使用されるデフォルトCSSファイルにおいて、マージン設定にタイポがありました。この修正により、デフォルトのHTML表示スタイルが意図通りになります。

JDK-8341699: Refactor KeyEvent/FunctionKeyTest.java

KeyEvent/FunctionKeyTest.java テストコードをリファクタリングし、可読性と保守性を向上させました。

JDK-8341942: Convert applet test java/awt/List/SetFontTest/SetFontTest.html to main program

古いアプレットベースのテストを、スタンドアロンのJava mainプログラムに変換しました。これにより、モダンなテストハーネスでの実行が容易になります。

JDK-8342054: KeyEvent/KeyTyped/Numpad1KeyTyped.java has 15 seconds timeout

特定のキーイベントテストに設定されていた15秒のタイムアウトが、CI環境で不安定さの原因となっていたため、これを調整しました。

JDK-8342685: Use PassFailJFrame.Builder.splitUI() in PrintLatinCJKTest.java

印刷テストにおいて、テストUIの構築に新しい PassFailJFrame.Builder.splitUI() APIを使用するように更新しました。

JDK-8342793: Implement pausing functionality for the PassFailJFrame

手動テスト用のUIフレームワーク PassFailJFrame に、テスト実行を一時停止・再開する機能を追加しました。

JDK-8342922: Add a log area to the PassFailJFrame

PassFailJFrame に、テスト中の診断メッセージなどを表示するためのログエリアを追加しました。

JDK-8343045: PageFormat/CustomPaper.java has no Pass/Fail buttons; multiple instructions

手動の印刷テストUIに、合否を判定するPass/Failボタンがなく、指示も複数で分かりにくかったため、UIを改善しました。

JDK-8342073: Call to insertText with single character from custom Input Method ignored

カスタムインプットメソッド（IME）から単一文字を insertText で挿入する呼び出しが無視されることがありました。この修正は、テキストコンポーネントのインプットメソッドハンドリングを改善し、あらゆるIMEからの入力を正しく受け入れるようにします。

JDK-8343199: Convert URLDragTest.html applet test to main

URLのドラッグ＆ドロップに関するアプレットテストを、スタンドアロンのmainプログラムに変換しました。

JDK-8343303: ConfigureNotify behavior has changed in KWin 6.2

KDE PlasmaのウィンドウマネージャであるKWin 6.2以降で、ウィンドウ設定通知の挙動が変更されたことに対応しました。これにより、最新のLinuxデスクトップ環境でのウィンドウイベント処理の互換性が向上します。

JDK-8343351: Select{Current,New}ItemTest.java for Choice don't open popup on macOS

macOSにおいて、AWTの Choice コンポーネントのテストがポップアップを正しく開けずに失敗する問題がありました。この修正は、macOS上でのロボット操作を改善し、テストが安定して実行されるようにします。

JDK-8343353: Add positionTestUI() to PassFailJFrame.Builder

PassFailJFrame.Builder に、テストUIの位置を指定する positionTestUI() メソッドを追加しました。

JDK-8343356: Add border around instructions in PassFailJFrame

PassFailJFrame の指示テキストエリアの周りにボーダーを追加し、視認性を向上させました。

JDK-8343357: PassFailJFrame: Make rows default to number of lines in instructions

PassFailJFrame の指示テキストエリアの行数を、デフォルトで指示テキストの行数に合わせるように改善しました。

JDK-8343360: Amend description for logArea

PassFailJFrame のログエリアに関する説明文を修正しました。

JDK-8343362: Position the first window of a window list

複数のウィンドウを使用するテストにおいて、最初のウィンドウの位置を適切に設定するよう改善しました。

JDK-8343371: Add description for PassFailJFrame constructors

PassFailJFrame のコンストラクタに説明的なJavadocコメントを追加しました。

JDK-8343518: Provide layouts for multiple test UI in PassFailJFrame

PassFailJFrame が、複数のテストUIコンポーネントを配置するためのレイアウトマネージャを提供するようになりました。

JDK-8343519: Update description of PassFailJFrame and samples

PassFailJFrame の説明とサンプルコードを最新の状態に更新しました。

JDK-8343613: Add border inside instruction frame in PassFailJFrame

PassFailJFrame の指示フレームの内側にボーダーを追加し、UIデザインを改善しました。

JDK-8343614: Improve default instruction frame title in PassFailJFrame

PassFailJFrame の指示フレームのデフォルトタイトルを、より分かりやすいものに改善しました。

JDK-8343746: ProblemList BasicDirectoryModel/LoaderThreadCount.java on Windows

Windowsプラットフォームで不安定なSwingのテストを問題リストに追加しました。

JDK-8344295: Disable ubsan checks in some awt/2d coding

AWTおよび2D関連のコードの一部において、Undefined Behavior Sanitizer (ubsan) による誤検知を防ぐため、チェックを無効化しました。

JDK-8343348: Hide PassFailJFrame.Builder constructor

PassFailJFrame.Builder のコンストラクタを private にし、代わりに builder() ファクトリメソッドの使用を強制するように設計を改善しました。

JDK-8343910: Simplify TrayIconScalingTest.java

TrayIcon のスケーリングに関するテストコードを簡素化し、保守性を向上させました。

これらのクライアントライブラリに関する修正は、デスクトップアプリケーションの安定性と品質を向上させ、エンドユーザー体験を直接的に改善します。堅牢なUIは、信頼性の高いアプリケーションの重要な要素です。次に、プラットフォーム全体の安全性を支えるセキュリティライブラリの強化点について説明します。

5. セキュリティライブラリの強化

Javaプラットフォームにおけるセキュリティは、エンタープライズアプリケーションからモバイルデバイスまで、あらゆる領域で最重要視される要素です。セキュリティライブラリは、暗号化通信（TLS/SSL）、デジタル署名、証明書管理、安全な認証といった機能を提供し、アプリケーションとデータを保護する根幹を担います。このセクションで解説する変更点は、セキュリティプロバイダの更新、暗号アルゴリズムのバグ修正、そして証明書関連ユーティリティの改善など、堅牢なセキュリティ体制を維持するために不可欠なものです。

JDK-8343927: Replace hardcoded security providers with new test.provider.name system property

セキュリティ関連のテストにおいて、ハードコードされていたセキュリティプロバイダ名を、新しいシステムプロパティ test.provider.name を介して動的に指定できるように変更しました。これにより、異なるプロバイダ実装でのテストが容易になります。

JDK-8344276: Update tests to use stronger Key and Salt size

セキュリティテストで使用される鍵長およびソルト長を、現代のセキュリティ基準に合わせてより強力なものに更新しました。これにより、テストの妥当性が向上します。

JDK-8344398: Update tests to use stronger key parameters and certificates

テストで使用する鍵パラメータと証明書を、より強力なアルゴリズムと設定を使用するように更新しました。

JDK-8344400: Update tests to use stronger algorithms and keys

様々なセキュリティテストにわたり、使用される暗号アルゴリズムと鍵をより強力なものに更新し、セキュリティプラクティスの向上を反映させました。

JDK-8339816: IP Address error when client enables HTTPS endpoint check on server socket

クライアント側でHTTPSのエンドポイント識別を有効にした際に、特定の条件下でサーバーソケットのIPアドレス検証エラーが発生する問題がありました。この修正は、エンドポイント検証ロジックを改善し、正当な接続が確立されるようにします。

JDK-8339817: Update Public Suffix List to 1cbd6e7

Public Suffix List（PSL）を最新のバージョンに更新しました。PSLは、HTTPクライアントがクッキーのスコープを正しく制限するために使用するドメインリストです。この更新により、セキュリティポリシーが最新の状態に保たれます。

JDK-8340204: Regtest java/security/Security/SynchronizedAccess.java is incorrect

java.security.Security クラスへの同期アクセスを検証するテストが、テストロジック自体に誤りがあり、本来検出するべき問題を検出できていませんでした。この修正は、テストを正しく動作するように修正します。

JDK-8340333: SHAKE256 does not work correctly if n >= 137

SHAKE256ハッシュ関数の実装において、出力長が137バイト以上の場合に不正な結果を生成するバグがありました。この修正は、アルゴリズムの実装を修正し、任意の出力長で正しいハッシュ値が生成されることを保証します。

JDK-8340504: test/jdk/sun/security/tools/keytool/NssTest.java fails to compile

keytool とNSS（Network Security Services）の相互運用性をテストする NssTest.java が、コンパイルエラーを起こしていました。この修正により、テストが正常にビルド・実行できるようになります。

JDK-8342049: Update NSS to version 3.96

JDKに同梱されているNSS（Network Security Services）ライブラリをバージョン3.96に更新しました。これにより、最新のセキュリティ修正と機能改善が取り込まれます。

JDK-8343350: Test sun/security/pkcs11/sslecc/ClientJSSEServerJSSE.java failed with: Invalid ECDH ServerKeyExchange signature

PKCS#11プロバイダを介したECC（楕円曲線暗号）ベースのTLSハンドシェイクテストが、Invalid ECDH ServerKeyExchange signature エラーで失敗していました。この修正は、PKCS#11実装との相互運用性を改善します。

JDK-8343514: Add a Test against ECDSA and ECDH NIST Test vector

NIST（米国国立標準技術研究所）が提供する公式のテストベクターを使用して、ECDSAおよびECDHの実装を検証するテストを追加しました。これにより、アルゴリズムの正当性がより強固に保証されます。

JDK-8344657: Improve logging in OCSPTimeout and SimpleOCSPResponder to help diagnose JDK-8309754

OCSP（Online Certificate Status Protocol）のタイムアウトに関する問題（JDK-8309754）の診断を容易にするため、関連するテストのロギングを強化しました。

JDK-8339254: CAInterop.java#actalisauthenticationrootca conflicted with /manual and /timeout

認証局（CA）の相互運用性テストにおいて、特定のルート証明書に関するテストが、手動実行やタイムアウトの指定と競合する問題がありました。この修正は、テスト構成を整理し、競合を解消します。

JDK-8340151: Unify debug printing format of X.509 cert serial numbers

デバッグログに出力されるX.509証明書のシリアル番号のフォーマットを統一しました。これにより、ログの可読性が向上します。

JDK-8340503: Automate com/sun/security/auth/callback/TextCallbackHandler/Default.java test

これまで手動で実行されていた認証コールバックハンドラのテストを自動化しました。

JDK-8340611: [jmh] the test java.security.HSS failed with 2 active threads

2つのスレッドで実行するとHSS/LMS（Hierarchical Signature System）のJMHベンチマークが失敗する問題を修正しました。

JDK-8340781: Add manual steps to run security/auth/callback/TextCallbackHandler/Password.java test

パスワード入力用のコールバックハンドラのテストに、手動での実行手順を追加しました。

JDK-8341017: Enhance the keytool code by invoking the buildTrustedCerts method for essential options

keytoolツールの内部コードを強化し、重要なオプションが指定された際に buildTrustedCerts メソッドが呼び出されるようにしました。

JDK-8341320: PKCS11 tests still skip execution

特定の条件下でPKCS#11関連のテストがスキップされてしまう問題を修正し、テストが確実に実行されるようにしました。

JDK-8341620: Unaddressed comments during code review of JDK-8337664

以前の修正（JDK-8337664）のコードレビューで指摘された未対応のコメントに対処するフォローアップ修正です。

JDK-8341698: Update TLSCommon/interop/AbstractServer to specify an interface to listen for connections

TLS相互運用性テストのサーバー実装を更新し、接続を待ち受けるネットワークインターフェースを明示的に指定できるようにしました。

JDK-8343046: Ensure randomness is only read from provided SecureRandom object

暗号化操作において、提供された SecureRandom オブジェクトからのみ乱数が読み取られることを保証するよう修正しました。

JDK-8343913: Have SSLSocketTemplate.doClientSide use loopback address

テスト用の SSLSocketTemplate が、外部ネットワークではなくループバックアドレスを使用するように修正し、テストの安定性を向上させました。

JDK-8344292: Several security shell tests don't set TESTJAVAOPTS

いくつかのシェルスクリプトベースのセキュリティテストが、外部から渡されたVMオプションを設定していなかったため、これを修正しました。

JDK-8344390: Few security tests ignore VM flags

いくつかのJavaベースのセキュリティテストもVMフラグを無視していたため、修正しました。

JDK-8340779: Test com/sun/crypto/provider/Cipher/DES/PerformanceTest.java fails with java.lang.ArithmeticException

DES暗号のパフォーマンステストが、ゼロ除算により ArithmeticException で失敗する問題を修正しました。

JDK-8343928: Fix typo of property name in TestOAEPPadding after 8341927

JDK-8341927の修正で導入されたプロパティ名にタイポがあったため、これを修正しました。

セキュリティの継続的な強化は、Javaエコシステム全体の信頼性を維持するための重要な活動です。これらの修正は、プラットフォームを最新の脅威から保護し、開発者が安全なアプリケーションを構築するための基盤を提供します。次に、アプリケーションの運用とデバッグを支援する「サービス性」の向上について見ていきましょう。

6. サービス性（Serviceability）の向上

「サービス性」とは、稼働中のJavaアプリケーションの監視、診断、およびトラブルシューティングを支援する機能群を指します。これには、JMX（Java Management Extensions）によるリモート管理、JVMTI（JVM Tool Interface）を通じたプロファイリングツールの連携、そしてクラッシュ時に生成されるエラーレポートなどが含まれます。このアップデートにおける修正は、これらのデバッグおよび管理ツールの機能性と信頼性を向上させるものです。これにより、開発者や運用担当者は、問題発生時に迅速かつ正確に根本原因を特定できるようになります。

JDK-8344392: Additional tests in jmxremote/startstop to match on PID not app name

JMXのリモート起動・停止に関するテストを強化し、対象プロセスをアプリケーション名ではなく、より一意性の高いプロセスID（PID）で照合するようにしました。これにより、同じ名前のプロセスが複数存在する環境でもテストの信頼性が向上します。

JDK-8344291: JMXStatusTest.java fails assertion intermittently

JMXStatusTest.java が、タイミングの問題で稀にアサーションエラーで失敗することがありました。この修正は、テスト内の同期を改善することで、このような間欠的な失敗を解消し、CIの安定性を高めます。

JDK-8340152: 3 JDI tests timed out with UT enabled

UseTransparentHugePages (UT) オプションが有効な環境で、3つのJDI (Java Debug Interface) テストがタイムアウトする問題がありました。この修正は、巨大ページの利用がデバッグエージェントの動作に与える影響を考慮し、テストが正常に完了するようにします。

JDK-8340153: NSK tests should listen on loopback addresses only

NSK（Netscape-Sun-Kenai）テストスイートの一部が、ループバックアドレスだけでなく、すべてのネットワークインターフェースで待ち受けてしまう可能性がありました。この修正は、テストが安全なループバックアドレスのみを使用することを保証します。

JDK-8343602: java/lang/management/ThreadMXBean/Locks.java transient failures

ThreadMXBean を使用してロック情報を取得するテストが、稀に失敗する問題がありました。この修正は、スレッド状態の取得とロック情報の整合性に関するタイミングの問題を解決し、テストの信頼性を向上させます。

JDK-8343912: JDI stopListening/stoplis001 "FAILED: listening is successfully stopped without starting listening"

JDIのリスニング停止機能に関するテストが、「リスニングを開始する前に停止に成功した」という不正なロジックで失敗していました。この修正は、テストの前提条件を正しく設定し、リスニング状態を適切に検証するようにします。

JDK-8343919: vmTestbase/nsk/jdb/kill/kill001/kill001.java fails with C1

C1コンパイラ（クライアントコンパイラ）を使用した場合に、jdb（Java Debugger）のプロセス強制終了テストが失敗する問題がありました。この修正は、C1でコンパイルされたコードでもデバッガが正しく動作することを保証します。

JDK-8344677: sun/management/jmxremote/bootstrap/SSLConfigFilePermissionTest.java failed with BindException: Address already in use

JMXリモートのSSL設定ファイルパーミッションをテストする際に、ポートが既に使用されていることによる BindException で稀に失敗する問題がありました。この修正は、テストが利用可能なポートを動的に見つけるように改善し、他のプロセスとの競合を回避します。

サービス性の向上は、開発者や運用担当者が直面する問題の解決時間を短縮し、システムの可用性を高める上で極めて重要です。これらの改善は、Javaプラットフォームの運用管理をより容易にします。最後に、JDK自体の開発プロセスを支えるツールとインフラストラクチャの更新について解説します。

7. ツールとインフラストラクチャ

JDKを取り巻くビルドシステム、テストフレームワーク（jtreg）、そして jpackage のような開発者向けツールは、OpenJDKプロジェクト自体の品質と一貫性を保証するための重要な基盤です。このセクションで紹介する更新は、これらのツールの機能改善、ビルドプロセスの安定化、そしてテストカバレッジの向上に貢献します。これらの内部的な改善は、最終的にエンドユーザーが手にするJDKの品質を直接的に高めることに繋がります。

JDK-8345317: SystemModulesMap::classNames and moduleNames arrays do not match the order

jlink が生成するシステムモジュールマップにおいて、クラス名とモジュール名の配列の順序が一致しない内部的なバグがありました。この修正は、マップ生成ロジックを修正し、データの整合性を保証します。

JDK-8343302: Some tests have name which confuse jtreg

一部のテストファイル名が、jtregテストハーネスの命名規則と競合し、テストの発見や実行に問題を引き起こす可能性がありました。この修正は、これらのファイル名を変更し、jtregとの互換性を確保します。

JDK-8343515: JLinkReproducibleTest.java support receive test.tool.vm.opts

jlink の再現性テストが、外部からVMオプション（test.tool.vm.opts）を受け取れるように改善しました。これにより、様々なVM構成でのテストが容易になります。

JDK-8344613: Create jtreg test case for JDK-8325203

System.exit(0) が子プロセスを意図せず終了させるリグレッション（JDK-8325203）の修正を検証するため、新しいjtregテストケースを作成しました。これにより、将来的なリグレッションの再発を防止します。

JDK-8344614: tools/jpackage/windows/WinChildProcessTest.java Failed: Check is calculator process is alive

Windows上で jpackage が生成したインストーラの子プロセス起動をテストする際に、電卓プロセスが生存しているかのチェックに失敗する問題がありました。この修正は、プロセスの状態チェックをより堅牢にし、テストの安定性を向上させます。

JDK-8345174: langtools/tools/javac/newlines/NewLineTest.java is failing on Japanese Windows

日本語版Windows環境において、javac の改行コード処理に関するテストが失敗する問題がありました。この修正は、プラットフォームやロケール固有の改行コードの挙動を正しく処理するようにテストを修正します。

JDK-8339080: Bump update version for OpenJDK: jdk-21.0.6

OpenJDK 21の開発ブランチのバージョン番号を、次のアップデートリリースである 21.0.6 に更新しました。これはリリースサイクルの標準的な手続きです。

JDK-8339839: GHA: some of bundles may not get removed

GitHub Actions (GHA) のCIワークフローにおいて、ビルド後に一部の成果物バンドルが削除されないことがありました。この修正は、クリーンアップ処理を改善し、ストレージの不要な消費を防ぎます。

JDK-8339991: GHA: RISC-V: Use Debian snapshot archive for bootstrap

RISC-V向けのGHAビルドにおいて、ブートストラップJDKの取得元をDebianのスナップショットアーカイブに変更しました。これにより、より安定したビルド環境が提供されます。

JDK-8340513: Mark jdk/jshell/ExceptionMessageTest.java intermittent

jshell の例外メッセージに関するテストが稀に失敗するため、一時的に不安定（intermittent）としてマークしました。

JDK-8341092: Add SECURITY.md file

OpenJDKリポジトリに SECURITY.md ファイルを追加しました。このファイルは、セキュリティ脆弱性の報告手順を定義するもので、コミュニティとの連携を円滑にします。

JDK-8341537: GHA: MacOS AArch64 bundles can be removed prematurely

macOS AArch64向けのGHAワークフローにおいて、ビルド成果物が時期尚早に削除されてしまう問題がありました。この修正は、アーティファクトの保持期間を調整します。

JDK-8341583: doc/building.md update Xcode instructions to note that full install is required

ビルド手順書（building.md）を更新し、macOSでビルドする際にはXcodeの完全なインストールが必要であることを明記しました。

JDK-8342491: [test] build/AbsPathsInImage.java fails with OOM when using ubsan-enabled binaries

ubsanを有効にしてビルドしたバイナリを使用すると、ビルド後のイメージ内の絶対パスをチェックするテストがOOMで失敗する問題がありました。この修正は、テストのメモリ使用量を削減します。

JDK-8342573: Gcc version detection failure on Alinux3

Alinux3環境において、GCCのバージョン検出に失敗し、ビルド構成が正しく設定されない問題がありました。この修正は、バージョン検出スクリプトを改善します。

JDK-8343253: --enable-ccache's CCACHE_BASEDIR breaks builds

ビルド高速化ツール ccache を --enable-ccache オプションで有効にし、かつ CCACHE_BASEDIR を設定している場合にビルドが失敗する問題を修正しました。

JDK-8343425: GHA: RISC-V: Bootstrap using Debian snapshot is still failing

RISC-V向けのGHAブートストラップが、Debianスナップショットを使用しても依然として失敗する問題に対するフォローアップ修正です。

JDK-8343474: [updates] Customize README.md to specifics of update project

アップデートリリースのリポジトリにある README.md をカスタマイズし、プロジェクト固有の情報を追加しました。

JDK-8344421: GHA: Switch to Xcode 15 on MacOS AArch64 runners

macOS AArch64のGHAランナーで使用するXcodeのバージョンを15に更新しました。

JDK-8344961: Compile without -fno-delete-null-pointer-checks

コンパイラオプション -fno-delete-null-pointer-checks を使用せずにビルドするように変更しました。これにより、特定の最適化に起因する潜在的な問題を回避します。

JDK-8347010: [21u] Remove designator DEFAULT_PROMOTED_VERSION_PRE=ea for release 21.0.6

リリース 21.0.6 の最終ビルドに向けて、バージョン文字列から早期アクセス（ea）の識別子を削除しました。

開発プロセスの改善は、JDK自体の品質と信頼性を高めるための継続的な取り組みです。これらの修正は、OpenJDKコミュニティがより効率的かつ安定して高品質なリリースを提供するための基盤を強化します。

8. 結論

OpenJDK 21.0.6+7は、Javaプラットフォームの成熟度をさらに高める重要なメンテナンスリリースです。本稿で概説したように、このアップデートはHotspot VMの安定性向上、コアライブラリのバグ修正、クライアントUIの互換性改善、セキュリティ体制の強化、そして開発・運用ツールの機能向上まで、プラットフォーム全体にわたる重要な修正を提供します。これらの地道な改善の積み重ねが、Javaをエンタープライズシステムやミッションクリティカルなアプリケーションにとって信頼できる選択肢であり続けさせるための鍵となります。開発者および運用担当者は、このアップデートを適用することで、より安定し、安全で、信頼性の高いJava実行環境の恩恵を受けることができます。
