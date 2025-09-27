OpenJDK 21.0.8+9 詳細変更ログ

1.0 はじめに (Introduction)

このドキュメントは、OpenJDKバージョン 21.0.8+9 リリースに含まれるすべてのバグ修正、バックポート、および機能強化に関する詳細かつ包括的な概要を提供します。本リリースは、Javaプラットフォーム全体の安定性、パフォーマンス、セキュリティを向上させるための重要なアップデートを含んでいます。

本書の構成は、変更点をそれぞれのJDKコンポーネント（HotSpot VM、コアライブラリ、セキュリティライブラリなど）ごとに分類しています。この構成により、開発者は自身の業務に最も関連性の高い分野の変更内容を容易に把握し、その技術的影響を理解することができます。

2.0 HotSpot VMの変更点 (Changes in HotSpot VM)

このセクションでは、Java仮想マシン（JVM）自体に加えられた重要な修正と機能強化について詳述します。対象となる領域は、ガベージコレクタ（G1, ZGC, Shenandoah）、JITコンパイラ（C1, C2）、およびランタイム操作など多岐にわたります。これらの変更は、Javaアプリケーションのパフォーマンス、安定性、および可観測性に直接的な影響を与えるものです。

HotSpot VMの修正一覧

JDK Issue ID	Priority	Title
JDK-8354528	P2	Integer.numberOfLeadingZeros outputs incorrectly in certain cases
JDK-8356675	P2	Kitchensink.java and RenaissanceStressTest.java time out with jvmti module errors
JDK-8357820	P2	[AArch64] Incorrect result of VectorizedHashCode intrinsic on Cortex-A53
JDK-8350856	P3	[PPC64] Make intrinsic conversions between bit representations of half precision values and floats
JDK-8351030	P3	JFR Leak Profiler is broken with Shenandoah
JDK-8351340	P3	secondary_super_cache does not scale well
JDK-8351341	P3	Out-of-bounds array access in secondary_super_cache
JDK-8351637	P3	Out of bounds access on Linux aarch64 in os::print_register_info
JDK-8351924	P3	serviceability/dcmd/vm/SystemMapTest.java and SystemDumpMapTest.java may fail after JDK-8326586
JDK-8352436	P3	[AArch64] C1: guarantee(val < (1ULL << nbits)) failed: Field too big for insn
JDK-8352526	P3	Test serviceability/sa/ClhsdbCDSJstackPrintAll.java failed: ArrayIndexOutOfBoundsException
JDK-8353102	P3	G1: NUMA migrations cause crashes in region allocation
JDK-8353522	P3	Make os::Linux::active_processor_count() public
JDK-8353675	P3	Caller/callee param size mismatch in deoptimization causes crash
JDK-8353676	P3	SIGFPE In ObjectSynchronizer::is_async_deflation_needed()
JDK-8354444	P3	Hotspot should support multiple large page sizes on Windows
JDK-8355212	P3	Shenandoah/C2: TestVerifyLoopOptimizations test failure
JDK-8355552	P3	java -D-D crashes
JDK-8356676	P3	Stack overflow during C2 compilation when splitting memory phi
JDK-8357391	P3	ZGC: TestAllocateHeapAt.java should not run with UseLargePages
JDK-8359037	P3	C2: compilation fails with "assert(false) failed: empty program detected during loop optimization"
JDK-8350412	P4	[21u] AArch64: Ambiguous frame layout leads to incorrect traces in JFR
JDK-8350862	P4	Output JVMTI agent information in hserr files
JDK-8351031	P4	Problemlist jdk/jfr/event/oldobject/TestShenandoah.java after JDK-8279016
JDK-8351191	P4	3 gc/epsilon tests ignore external vm options
JDK-8351358	P4	Corrupted timezone string in JVM crash log
JDK-8351508	P4	[Testbug] g-tests for cgroup leave files in /tmp on linux
JDK-8351557	P4	Add jcmd to print annotated process memory map
JDK-8351559	P4	gc/stress/TestStressG1Uncommit.java gets OOM-killed
JDK-8351684	P4	"Total compile time" counter should include time spent in failing/bailout compiles
JDK-8351831	P4	Move BufferNode from PtrQueue files to new files
JDK-8351872	P4	Skip ValidateHazardPtrsClosure in non-debug builds
JDK-8351899	P4	Bug in jdk.jfr.event.gc.collection.TestSystemGC
JDK-8351920	P4	Improve Speed of System.map
JDK-8352026	P4	Replace NULL with nullptr in HotSpot gtests
JDK-8352167	P4	WB_IsFrameDeoptimized miss ResourceMark
JDK-8352183	P4	[x64] Fix useless padding
JDK-8352230	P4	CompileFramework: test library to conveniently compile java and jasm sources for fuzzing
JDK-8352283	P4	Shenandoah: Improve handshake closure labels
JDK-8352285	P4	CTW: Attempt to preload all classes in constant pool
JDK-8352286	P4	Give better error for ConcurrentHashTable corruption
JDK-8352516	P4	Update runtime/condy tests to be executed with VM flags
JDK-8352523	P4	Enable debug logging for vmTestbase/nsk/jvmti/scenarios/sampling/SP05/sp05t003/TestDescription.java
JDK-8352525	P4	serviceability/sa/ClhsdbWhere.java fails AssertionFailure: Corrupted constant pool
JDK-8352771	P4	Crash: assert(h_array_list.not_null()) failed: invariant
JDK-8352772	P4	OpenJDK fails to configure on linux aarch64 when CDS is disabled after JDK-8331942
JDK-8353128	P4	JFR: Split JFRCheckpoint VM operation
JDK-8353292	P4	Replaying compilation with null static final fields results in a crash
JDK-8353536	P4	More reliable OOM handling in ExceptionDuringDumpAtObjectsInitPhase test
JDK-8353648	P4	Remove unused UseNUMA in os_aix.cpp
JDK-8353650	P4	C2: Loop strip mining uses ABS with min int
JDK-8353651	P4	C2: VectorInsertNode::make() shouldn't call ConINode::make() directly
JDK-8353652	P4	Incorrect TraceLoopPredicate output
JDK-8353653	P4	Fatal error in auto-vectorizer with float16 kernel.
JDK-8353654	P4	ShenandoahHeap::is_in should check for alive regions
JDK-8353853	P4	[ubsan] block.cpp:1617:30: runtime error: 9.97582e+36 is outside the range of representable values of type 'int'
JDK-8353865	P4	memory_swap_current_in_bytes reports 0 as "unlimited"
JDK-8353867	P4	[TESTBUG] gtest CollectorPolicy.young_scaled_initial_ergo_vm fails if heap is too small
JDK-8353893	P4	CollectorPolicy.young_scaled_initial_ergo_vm gtest fails on ppc64 based platforms
JDK-8353901	P4	nsk.share.gc.Memory::getArrayLength returns wrong value
JDK-8353922	P4	G1: interpreter post-barrier x86 code asserts index size of wrong buffer
JDK-8354058	P4	AArch64: turn on signum intrinsics by default on Ampere CPUs
JDK-8354165	P4	compiler/vectorization/TestFloat16VectorConvChain.java fails with non-standard AVX/SSE settings
JDK-8354197	P4	compiler/vectorization/TestFloat16VectorConvChain.java timeouts on ppc64 platforms after JDK-8335860
JDK-8354253	P4	jcmd Compiler.codecache should print total size of code cache
JDK-8354271	P4	ZGC: Another division by zero in rule_major_allocation_rate
JDK-8354368	P4	Test jdk/incubator/vector/LoadJsvmlTest.java ignores VM flags
JDK-8354370	P4	zgc/genzgc tests ignore vm flags
JDK-8354579	P4	Extend printing for System.map
JDK-8354639	P4	serviceability/dcmd/vm tests fail for ZGC after JDK-8322475
JDK-8354642	P4	Test vmTestbase/nsk/jvmti/scenarios/sampling/SP05/sp05t003/TestDescription.java timed out: thread not suspended
JDK-8354644	P4	Improve diagnostic logging runtime/cds/DeterministicDump.java
JDK-8354647	P4	serviceability/dcmd/vm/SystemDumpMapTest.java and SystemMapTest.java fail on Linux Alpine after 8322475
JDK-8355075	P4	TestVectorZeroCount: counter not reset between iterations
JDK-8355096	P4	Add intrinsic for float/double modulo for x86 AVX2 and AVX512
JDK-8355152	P4	serviceability/sa/TestJhsdbJstackLineNumbers.java failed with "Didn't find enough line numbers"
JDK-8355316	P4	Include timings for leaving safepoint in safepoint logging
JDK-8355419	P4	Test TestCodeCacheFull.java fails with option -XX:-UseCodeCacheFlushing
JDK-8355551	P4	C2: assert(false) failed: node should be in igvn hash table
JDK-8355655	P4	[ASAN] Gtest os_linux.glibc_mallinfo_wrapper_vm fails
JDK-8355707	P4	Remove runtime platform check from frem/drem
JDK-8355715	P4	JFR GCHelper class recognizes "Archive" regions as valid
JDK-8355761	P4	[AArch64] C2 compilation hits offset_ok_for_immed: assert "c2 compiler bug"
JDK-8355762	P4	MacOS Zero cannot run gtests due to wrong JVM path
JDK-8356248	P4	MAX_SECS definition is unused in os_linux
JDK-8356254	P4	Use "/native" Run Option for TestAvailableProcessors Execution
JDK-8356489	P4	Test WaitNotifySuspendedVThreadTest.java timed out
JDK-8356490	P4	Rename nsk_strace.h
JDK-8356491	P4	Update nsk.share.jpda.BindServer to don't use finalization
JDK-8356507	P4	Clean up Finalizable.java and finalize terminology in vmTestbase/nsk/share
JDK-8356509	P4	serviceability/jvmti/StartPhase/AllowedFunctions/AllowedFunctions.java fails with unexpected exit code: 112
JDK-8356512	P4	Fix -Wzero-as-null-pointer-constant warnings in gtest framework
JDK-8356669	P4	x86 count_positives intrinsic broken for -XX:AVX3Threshold=0
JDK-8356670	P4	Compiler directives parser swallows a character after line comments
JDK-8356671	P4	jdk/jfr/event/runtime/TestResidentSetSizeEvent.java fails with "The size should be less than or equal to peak"
JDK-8356674	P4	NPE when HSDB visits bad oop
JDK-8356677	P4	LogCompilation doesn't reset lateInlining when it encounters a failure.
JDK-8356786	P4	Remove support of remote and manual debuggee launchers
JDK-8356992	P4	[JVMCI] fatal error: Never compilable: in JVMCI shutdown
JDK-8357023	P4	Replace NULL with nullptr in HotSpot jtreg test native code files
JDK-8357024	P4	Rename get_stack_trace.h
JDK-8357025	P4	Rename Injector.h
JDK-8357026	P4	Rename jvmti_FollowRefObjects.h
JDK-8357027	P4	Rename native_thread.h
JDK-8357028	P4	Rename nsk_list.h
JDK-8357029	P4	Rename nsk_mutex.h
JDK-8357030	P4	Rename mlvmJvmtiUtils.h
JDK-8357031	P4	Rename jnihelper.h
JDK-8357032	P4	Rename jvmti_aod.h
JDK-8357069	P4	[AIX] Adapt code for C++ VLA rule
JDK-8357112	P4	Improve test coverage for JVMTI GetThreadState on carrier and mounted vthread
JDK-8357113	P4	Rename agent_common.h
JDK-8357121	P4	Test: add more test case for string compare (UL case)
JDK-8357261	P4	Avoid sending per-region GCPhaseParallel JFR events in G1ScanCollectionSetRegionClosure
JDK-8357389	P4	jdk/jfr/startupargs/TestMemoryOptions.java fails with 32-bit build
JDK-8357437	P4	Use correct extension for C++ test headers
JDK-8357483	P4	Remove the appcds/javaldr/AnonVmClassesDuringDump.java test
JDK-8357487	P4	Incomplete logging in nsk/jvmti/ResourceExhausted/resexhausted00* tests
JDK-8357488	P4	[jittester] Remove TempDir debug output
JDK-8357544	P4	Clean up vmTestbase/vm/share
JDK-8357855	P4	Merge vm/share/InMemoryJavaCompiler w/ jdk/test/lib/compiler/InMemoryJavaCompiler
JDK-8357856	P4	failure_handler lldb command times out on macosx-aarch64 core file

[JDK-8354528]: Integer.numberOfLeadingZeros outputs incorrectly in certain cases

属性	値
Priority	P2
Type	Backport

この修正は、特定のケースにおいてInteger.numberOfLeadingZerosメソッドが不正な結果を返していたバグに対処します。このメソッドはビット操作やパフォーマンスが重要なコードで頻繁に使用されるため、この修正により数値計算の正確性と信頼性が確保されます。

[JDK-8356675]: Kitchensink.java and RenaissanceStressTest.java time out with jvmti module errors

属性	値
Priority	P2
Type	Backport

この修正は、Kitchensink.javaやRenaissanceStressTest.javaといった特定のストレステストを実行した際に、JVMTIモジュールでエラーが発生し、テストがタイムアウトする問題を解決します。この修正によりJVMTIの安定性が向上し、デバッガやプロファイラなどのエージェントが高負荷な状況下でも安定して動作することが保証されます。

[JDK-8357820]: [AArch64] Incorrect result of VectorizedHashCode intrinsic on Cortex-A53

属性	値
Priority	P2
Type	Backport

AArch64アーキテクチャのCortex-A53プロセッサ上で、VectorizedHashCodeの組み込み関数（intrinsic）が誤った結果を生成するバグを修正します。この修正により、当該CPUでのハッシュ計算が正しく行われるようになり、ハッシュベースのコレクションの信頼性が回復します。

[JDK-8350856]: [PPC64] Make intrinsic conversions between bit representations of half precision values and floats

属性	値
Priority	P3
Type	Backport

PPC64プラットフォームにおいて、半精度浮動小数点数（half precision）と単精度浮動小数点数（float）のビット表現間の変換を高速化するための組み込み関数（intrinsic）を導入します。これにより、機械学習やグラフィックス処理など、半精度浮動小数点数を多用するアプリケーションのパフォーマンスが向上します。

[JDK-8351030]: JFR Leak Profiler is broken with Shenandoah

属性	値
Priority	P3
Type	Backport

この修正は、Shenandoah GCが有効な場合にJFR（Java Flight Recorder）のリークプロファイラが機能しない問題を解決します。原因は、JFRリークプロファイラとShenandoah GCが、オブジェクトのメタデータを格納するためにオブジェクトヘッダのマークワードを競合して使用していたことでした。Shenandoahのロードリファレンスバリアが、JFRが書き込んだデータをGC用の転送ポインタとして誤って解釈し、クラッシュを引き起こす可能性がありました。この修正は、両者のマークワード使用方法を分離し、競合を解消することで、Shenandoah環境下でのJFRリークプロファイラの安定動作を保証します。

[JDK-8351340]: secondary_super_cache does not scale well

属性	値
Priority	P3
Type	Backport

HotSpot VMの二次スーパークラスキャッシュ（secondary_super_cache）が、高並行環境下でスケーラビリティに乏しいというパフォーマンス上のボトルネックを修正します。この変更により、キャッシュのデータ構造やロック戦略が改善され、並行アクセス時のパフォーマンスが向上します。

[JDK-8351341]: Out-of-bounds array access in secondary_super_cache

属性	値
Priority	P3
Type	Backport

二次スーパークラスキャッシュ（secondary_super_cache）において、配列の境界外メモリアクセスが発生する可能性があった深刻なバグを修正します。この修正により、キャッシュへのアクセス時の境界チェックが厳格化され、VMの安定性が向上します。

[JDK-8351637]: Out of bounds access on Linux aarch64 in os::print_register_info

属性	値
Priority	P3
Type	Backport

Linux AArch64プラットフォームにおいて、VMクラッシュ時にレジスタ情報を出力する診断コード（os::print_register_info）内で境界外メモリアクセスが発生する問題を修正します。これにより、どのような状況でも信頼性の高いクラッシュログが生成されることが保証されます。

[JDK-8351924]: serviceability/dcmd/vm/SystemMapTest.java and SystemDumpMapTest.java may fail after JDK-8326586

属性	値
Priority	P3
Type	Backport

この修正は、System.map診断コマンドのパフォーマンス改善（JDK-8326586）後に、関連するテストが失敗するようになったリグレッションに対処するものです。修正により、テストが新しい実装の動作に合わせて更新され、診断コマンドの機能が正しく検証されるようになります。

[JDK-8352436]: [AArch64] C1: guarantee(val < (1ULL << nbits)) failed: Field too big for insn

属性	値
Priority	P3
Type	Backport

AArch64プラットフォーム上でC1 JITコンパイラがクラッシュする問題を修正します。コンパイラが命令の即値フィールドに収まらない大きさの値をエンコードしようとしたために発生していた内部的な保証チェックの失敗を防ぎ、コンパイラの安定性を向上させます。

[JDK-8352526]: Test serviceability/sa/ClhsdbCDSJstackPrintAll.java failed: ArrayIndexOutOfBoundsException

属性	値
Priority	P3
Type	Backport

Serviceability Agent（SA）のclhsdbツールが、Class Data Sharing (CDS) を使用しているプロセスに対してjstackコマンドを実行した際にArrayIndexOutOfBoundsExceptionで失敗する問題を修正します。これにより、CDS環境でのスタックトレース表示が正しく行われるようになります。

[JDK-8353102]: G1: NUMA migrations cause crashes in region allocation

属性	値
Priority	P3
Type	Backport

NUMAアーキテクチャのシステムで、OSによるメモリページのマイグレーションがG1ガベージコレクタのリージョン割り当てロジックと衝突し、VMがクラッシュする問題を修正します。この修正により、NUMA環境下でのG1 GCの安定性が向上します。

[JDK-8353522]: Make os::Linux::active_processor_count() public

属性	値
Priority	P3
Type	Backport

Linux環境でアクティブなプロセッサ数を取得する内部関数os::Linux::active_processor_count()をpublicに変更するリファクタリングです。これにより、VM内の他のサブシステムがこのロジックを再利用できるようになり、コードの重複が削減されます。

[JDK-8353675]: Caller/callee param size mismatch in deoptimization causes crash

属性	値
Priority	P3
Type	Backport

デ最適化プロセス中に、呼び出し元と呼び出し先のメソッドフレーム間でパラメータサイズの解釈に不整合が生じ、VMがクラッシュする問題を修正します。この修正により、デ最適化プロセスの信頼性が向上します。

[JDK-8353676]: SIGFPE In ObjectSynchronizer::is_async_deflation_needed()

属性	値
Priority	P3
Type	Backport

オブジェクトの同期処理において、非同期デフレーションが必要かを判断するロジックでゼロ除算が原因でSIGFPE（浮動小数点例外）が発生していたバグを修正します。これにより、モニタ管理に関するVMの安定性が向上します。

[JDK-8354444]: Hotspot should support multiple large page sizes on Windows

属性	値
Priority	P3
Type	Backport

Windowsプラットフォームにおいて、HotSpot VMが複数の異なるサイズのラージページをサポートするように機能を強化します。これにより、メモリ集約的なアプリケーションがハードウェアの能力をより最大限に活用できるようになります。

[JDK-8355212]: Shenandoah/C2: TestVerifyLoopOptimizations test failure

属性	値
Priority	P3
Type	Backport

Shenandoah GCとC2 JITコンパイラの組み合わせで、ループ最適化がShenandoahのGCバリアと正しく連携せずに不正な動作を引き起こしていたテストの失敗を修正します。この修正により、Shenandoah使用時のコード実行の信頼性が向上します。

[JDK-8355552]: java -D-D crashes

属性	値
Priority	P3
Type	Backport

-Dのようにプロパティ名が指定されていない不正なシステムプロパティ引数が与えられた場合に、JVMがクラッシュしていたバグを修正します。この修正により、引数パーサが不正な入力を適切に処理し、クラッシュを防ぐようになります。

[JDK-8356676]: Stack overflow during C2 compilation when splitting memory phi

属性	値
Priority	P3
Type	Backport

C2 JITコンパイラが特定の複雑なコードをコンパイルする際に、メモリPhiノードの分割という最適化フェーズでスタックオーバーフローを引き起こす問題を修正します。修正により、この最適化処理がより多くのスタックを消費しないように改善され、コンパイラの安定性が向上しました。

[JDK-8357391]: ZGC: TestAllocateHeapAt.java should not run with UseLargePages

属性	値
Priority	P3
Type	Backport

ZGCのTestAllocateHeapAt.javaテストが、互換性のない-XX:+UseLargePagesオプションと共に実行されないように修正します。これにより、誤ったテスト失敗が防がれ、テストスイートの信頼性が向上します。

[JDK-8359037]: C2: compilation fails with "assert(false) failed: empty program detected during loop optimization"

属性	値
Priority	P3
Type	Backport

C2 JITコンパイラのループ最適化フェーズで、コードブロックが空であると誤って判断し、内部的なアサーションに失敗していた問題を修正します。この修正により、ループ最適化のロジックが改善され、コンパイラの安定性が向上します。

その他のHotSpotの修正 (Other HotSpot Fixes)

* JDK-8350412 (P4): [21u] AArch64: Ambiguous frame layout leads to incorrect traces in JFR - AArch64プラットフォームで、曖昧なフレームレイアウトが原因でJFRのスタックトレースが不正確になる問題を修正しました。
* JDK-8350862 (P4): Output JVMTI agent information in hserr files - hs_errクラッシュログファイルにJVMTIエージェントの情報を出力するようにし、デバッグを容易にしました。
* JDK-8351031 (P4): Problemlist jdk/jfr/event/oldobject/TestShenandoah.java after JDK-8279016 - JDK-8279016の修正後に不安定になったJFRとShenandoahに関するテストを問題リストに追加しました。
* JDK-8351191 (P4): 3 gc/epsilon tests ignore external vm options - Epsilon GCに関する3つのテストが外部からのVMオプションを無視していた問題を修正しました。
* JDK-8351358 (P4): Corrupted timezone string in JVM crash log - JVMクラッシュログ内のタイムゾーン文字列が破損する問題を修正しました。
* JDK-8351508 (P4): [Testbug] g-tests for cgroup leave files in /tmp on linux - cgroup関連のgtestがLinuxの/tmpディレクトリに一時ファイルを残す問題を修正しました。
* JDK-8351557 (P4): Add jcmd to print annotated process memory map - プロセスのメモリマップに注釈を付けて表示する新しいjcmdコマンドを追加しました。
* JDK-8351559 (P4): gc/stress/TestStressG1Uncommit.java gets OOM-killed - G1のアンコミットに関するストレステストがOOMで強制終了される問題を修正しました。
* JDK-8351684 (P4): "Total compile time" counter should include time spent in failing/bailout compiles - コンパイル時間の合計カウンタに、失敗または中断したコンパイル時間も含まれるように修正しました。
* JDK-8351831 (P4): Move BufferNode from PtrQueue files to new files - 内部コードのリファクタリングとして、BufferNodeをPtrQueueファイルから新しいファイルに移動しました。
* JDK-8351872 (P4): Skip ValidateHazardPtrsClosure in non-debug builds - デバッグビルド以外ではValidateHazardPtrsClosureをスキップするようにしました。
* JDK-8351899 (P4): Bug in jdk.jfr.event.gc.collection.TestSystemGC - System.gc()呼び出しに関連するJFRイベントのテストのバグを修正しました。
* JDK-8351920 (P4): Improve Speed of System.map - System.map診断コマンドのパフォーマンスを改善しました。
* JDK-8352026 (P4): Replace NULL with nullptr in HotSpot gtests - HotSpotのgtestコードベースでNULLをnullptrに置き換え、コードの現代化を図りました。
* JDK-8352167 (P4): WB_IsFrameDeoptimized miss ResourceMark - WB_IsFrameDeoptimized関数でResourceMarkが欠落していた問題を修正しました。
* JDK-8352183 (P4): [x64] Fix useless padding - x64アーキテクチャのコード生成で不要なパディングを修正しました。
* JDK-8352230 (P4): CompileFramework: test library to conveniently compile java and jasm sources for fuzzing - ファジングテスト用にJavaおよびjasmソースをコンパイルするためのテストライブラリCompileFrameworkを導入しました。
* JDK-8352283 (P4): Shenandoah: Improve handshake closure labels - Shenandoah GCのハンドシェイククロージャのラベルを改善し、診断を容易にしました。
* JDK-8352285 (P4): CTW: Attempt to preload all classes in constant pool - Compile-Time-for-the-World (CTW)で、定数プール内の全クラスをプリロードする試みを追加しました。
* JDK-8352286 (P4): Give better error for ConcurrentHashTable corruption - ConcurrentHashTableの破損が検出された際、より詳細なエラーメッセージを出力するようにしました。
* JDK-8352516 (P4): Update runtime/condy tests to be executed with VM flags - condy（invokedynamicの定数）関連のテストがVMフラグを尊重するように更新しました。
* JDK-8352523 (P4): Enable debug logging for vmTestbase/nsk/jvmti/scenarios/sampling/SP05/sp05t003/TestDescription.java - 特定のJVMTIテストでデバッグロギングを有効にしました。
* JDK-8352525 (P4): serviceability/sa/ClhsdbWhere.java fails AssertionFailure: Corrupted constant pool - clhsdb whereコマンドが定数プールの破損で失敗する問題を修正しました。
* JDK-8352771 (P4): Crash: assert(h_array_list.not_null()) failed: invariant - 不変条件の違反によるアサーション失敗（クラッシュ）を修正しました。
* JDK-8352772 (P4): OpenJDK fails to configure on linux aarch64 when CDS is disabled after JDK-8331942 - JDK-8331942の変更後、CDSを無効にした場合にLinux aarch64での設定に失敗する問題を修正しました。
* JDK-8353128 (P4): JFR: Split JFRCheckpoint VM operation - JFRのチェックポイントVM操作を分割し、パフォーマンスを改善しました。
* JDK-8353292 (P4): Replaying compilation with null static final fields results in a crash - nullのstatic finalフィールドを持つコンパイルをリプレイするとクラッシュする問題を修正しました。
* JDK-8353536 (P4): More reliable OOM handling in ExceptionDuringDumpAtObjectsInitPhase test - 特定のテストにおけるOutOfMemoryErrorの処理をより信頼性の高いものにしました。
* JDK-8353648 (P4): Remove unused UseNUMA in os_aix.cpp - AIXのコードから未使用のUseNUMAフラグを削除しました。
* JDK-8353650 (P4): C2: Loop strip mining uses ABS with min int - C2コンパイラのループストリップマイニング最適化が最小整数値の絶対値計算で問題を抱えていたのを修正しました。
* JDK-8353651 (P4): C2: VectorInsertNode::make() shouldn't call ConINode::make() directly - C2コンパイラでVectorInsertNode::make()がConINode::make()を直接呼び出さないように修正しました。
* JDK-8353652 (P4): Incorrect TraceLoopPredicate output - TraceLoopPredicateの出力が不正確であった問題を修正しました。
* JDK-8353653 (P4): Fatal error in auto-vectorizer with float16 kernel. - float16カーネルを使用する際の自動ベクトル化で発生していた致命的なエラーを修正しました。
* JDK-8353654 (P4): ShenandoahHeap::is_in should check for alive regions - ShenandoahHeap::is_inが生存しているリージョンをチェックするように修正しました。
* JDK-8353853 (P4): [ubsan] block.cpp:1617:30: runtime error: 9.97582e+36 is outside the range of representable values of type 'int' - ubsan（未定義動作サニタイザ）によって検出された整数オーバーフローの問題を修正しました。
* JDK-8353865 (P4): memory_swap_current_in_bytes reports 0 as "unlimited" - memory_swap_current_in_bytesが0を「無制限」として報告していた問題を修正しました。
* JDK-8353867 (P4): [TESTBUG] gtest CollectorPolicy.young_scaled_initial_ergo_vm fails if heap is too small - ヒープが小さすぎる場合に失敗するgtestを修正しました。
* JDK-8353893 (P4): CollectorPolicy.young_scaled_initial_ergo_vm gtest fails on ppc64 based platforms - ppc64プラットフォームで失敗するgtestを修正しました。
* JDK-8353901 (P4): nsk.share.gc.Memory::getArrayLength returns wrong value - テストライブラリのMemory::getArrayLengthが不正な値を返す問題を修正しました。
* JDK-8353922 (P4): G1: interpreter post-barrier x86 code asserts index size of wrong buffer - G1 GCのインタプリタ用ポストバリア（x86）が間違ったバッファのインデックスサイズをアサートしていた問題を修正しました。
* JDK-8354058 (P4): AArch64: turn on signum intrinsics by default on Ampere CPUs - Ampere CPUを搭載したAArch64システムで、signum組み込み関数をデフォルトで有効にしました。
* JDK-8354165 (P4): compiler/vectorization/TestFloat16VectorConvChain.java fails with non-standard AVX/SSE settings - 非標準のAVX/SSE設定で失敗するベクトル化テストを修正しました。
* JDK-8354197 (P4): compiler/vectorization/TestFloat16VectorConvChain.java timeouts on ppc64 platforms after JDK-8335860 - 特定のベクトル化テストがppc64プラットフォームでタイムアウトする問題を修正しました。
* JDK-8354253 (P4): jcmd Compiler.codecache should print total size of code cache - jcmd Compiler.codecacheコマンドがコードキャッシュの合計サイズを出力するように改善しました。
* JDK-8354271 (P4): ZGC: Another division by zero in rule_major_allocation_rate - ZGCのヒューリスティクスにおける別のゼロ除算バグを修正しました。
* JDK-8354368 (P4): Test jdk/incubator/vector/LoadJsvmlTest.java ignores VM flags - Vector APIのテストがVMフラグを無視していた問題を修正しました。
* JDK-8354370 (P4): zgc/genzgc tests ignore vm flags - Generational ZGCのテストがVMフラグを無視していた問題を修正しました。
* JDK-8354579 (P4): Extend printing for System.map - System.map診断コマンドの出力を拡張し、より詳細な情報を提供するようにしました。
* JDK-8354639 (P4): serviceability/dcmd/vm tests fail for ZGC after JDK-8322475 - 特定の診断コマンドテストがZGCで失敗する問題を修正しました。
* JDK-8354642 (P4): Test vmTestbase/nsk/jvmti/scenarios/sampling/SP05/sp05t003/TestDescription.java timed out: thread not suspended - 特定のJVMTIテストがスレッドを中断できずにタイムアウトする問題を修正しました。
* JDK-8354644 (P4): Improve diagnostic logging runtime/cds/DeterministicDump.java - CDSの決定論的ダンプに関するテストの診断ログを改善しました。
* JDK-8354647 (P4): serviceability/dcmd/vm/SystemDumpMapTest.java and SystemMapTest.java fail on Linux Alpine after 8322475 - 特定の診断コマンドテストがLinux Alpineで失敗する問題を修正しました。
* JDK-8355075 (P4): TestVectorZeroCount: counter not reset between iterations - ベクトル化テストでイテレーション間にカウンタがリセットされていなかった問題を修正しました。
* JDK-8355096 (P4): Add intrinsic for float/double modulo for x86 AVX2 and AVX512 - x86 AVX2/AVX512向けに浮動小数点数の剰余演算の組み込み関数を追加しました。
* JDK-8355152 (P4): serviceability/sa/TestJhsdbJstackLineNumbers.java failed with "Didn't find enough line numbers" - Jhsdbのjstackで行番号が十分に表示されないテストの失敗を修正しました。
* JDK-8355316 (P4): Include timings for leaving safepoint in safepoint logging - セーフポイントのログに、セーフポイントからの離脱にかかる時間を含めるようにしました。
* JDK-8355419 (P4): Test TestCodeCacheFull.java fails with option -XX:-UseCodeCacheFlushing - コードキャッシュのフラッシュを無効にするオプションで失敗するテストを修正しました。
* JDK-8355551 (P4): C2: assert(false) failed: node should be in igvn hash table - C2コンパイラで、ノードがIGVNハッシュテーブルに存在しないというアサーション失敗を修正しました。
* JDK-8355655 (P4): [ASAN] Gtest os_linux.glibc_mallinfo_wrapper_vm fails - AddressSanitizer (ASAN) 有効時に失敗するgtestを修正しました。
* JDK-8355707 (P4): Remove runtime platform check from frem/drem - frem/drem命令からランタイムプラットフォームチェックを削除しました。
* JDK-8355715 (P4): JFR GCHelper class recognizes "Archive" regions as valid - JFRのGCHelperがCDSアーカイブ領域を有効な領域として誤認識していた問題を修正しました。
* JDK-8355761 (P4): [AArch64] C2 compilation hits offset_ok_for_immed: assert "c2 compiler bug" - AArch64でC2コンパイル中にアサーションに失敗する問題を修正しました。
* JDK-8355762 (P4): MacOS Zero cannot run gtests due to wrong JVM path - macOSのZero VMで、JVMパスが間違っているためにgtestを実行できない問題を修正しました。
* JDK-8356248 (P4): MAX_SECS definition is unused in os_linux - LinuxのOS固有コードから未使用のMAX_SECS定義を削除しました。
* JDK-8356254 (P4): Use "/native" Run Option for TestAvailableProcessors Execution - TestAvailableProcessorsテストで/native実行オプションを使用するようにしました。
* JDK-8356489 (P4): Test WaitNotifySuspendedVThreadTest.java timed out - 仮想スレッドの中断に関するテストがタイムアウトする問題を修正しました。
* JDK-8356490 (P4): Rename nsk_strace.h - テスト用のヘッダファイル名を変更しました。
* JDK-8356491 (P4): Update nsk.share.jpda.BindServer to don't use finalization - テストライブラリでファイナライゼーションの使用をやめるよう更新しました。
* JDK-8356507 (P4): Clean up Finalizable.java and finalize terminology in vmTestbase/nsk/share - テストコードベースからファイナライゼーション関連の用語やクラスをクリーンアップしました。
* JDK-8356509 (P4): serviceability/jvmti/StartPhase/AllowedFunctions/AllowedFunctions.java fails with unexpected exit code: 112 - 特定のJVMTIテストが予期せぬ終了コードで失敗する問題を修正しました。
* JDK-8356512 (P4): Fix -Wzero-as-null-pointer-constant warnings in gtest framework - gtestフレームワークでGCCのコンパイラ警告を修正しました。
* JDK-8356669 (P4): x86 count_positives intrinsic broken for -XX:AVX3Threshold=0 - 特定のAVX設定でx86のcount_positives組み込み関数が壊れていた問題を修正しました。
* JDK-8356670 (P4): Compiler directives parser swallows a character after line comments - コンパイラディレクティブのパーサが行コメントの後の文字を飲み込んでしまう問題を修正しました。
* JDK-8356671 (P4): jdk/jfr/event/runtime/TestResidentSetSizeEvent.java fails with "The size should be less than or equal to peak" - JFRのメモリ関連イベントのテストが失敗する問題を修正しました。
* JDK-8356674 (P4): NPE when HSDB visits bad oop - HSDBが不正なoopを訪れた際にNullPointerExceptionが発生する問題を修正しました。
* JDK-8356677 (P4): LogCompilation doesn't reset lateInlining when it encounters a failure. - コンパイルログ機能が、失敗時にlateInliningの状態をリセットしていなかった問題を修正しました。
* JDK-8356786 (P4): Remove support of remote and manual debuggee launchers - リモートおよび手動のデバッグ対象起動サポートを削除しました。
* JDK-8356992 (P4): [JVMCI] fatal error: Never compilable: in JVMCI shutdown - JVMCIシャットダウン中に致命的なエラーが発生する問題を修正しました。
* JDK-8357023 (P4): Replace NULL with nullptr in HotSpot jtreg test native code files - HotSpotのjtregテストのネイティブコードでNULLをnullptrに置き換えました。
* JDK-8357024 (P4): Rename get_stack_trace.h - テスト用のヘッダファイル名を変更しました。
* JDK-8357025 (P4): Rename Injector.h - テスト用のヘッダファイル名を変更しました。
* JDK-8357026 (P4): Rename jvmti_FollowRefObjects.h - テスト用のヘッダファイル名を変更しました。
* JDK-8357027 (P4): Rename native_thread.h - テスト用のヘッダファイル名を変更しました。
* JDK-8357028 (P4): Rename nsk_list.h - テスト用のヘッダファイル名を変更しました。
* JDK-8357029 (P4): Rename nsk_mutex.h - テスト用のヘッダファイル名を変更しました。
* JDK-8357030 (P4): Rename mlvmJvmtiUtils.h - テスト用のヘッダファイル名を変更しました。
* JDK-8357031 (P4): Rename jnihelper.h - テスト用のヘッダファイル名を変更しました。
* JDK-8357032 (P4): Rename jvmti_aod.h - テスト用のヘッダファイル名を変更しました。
* JDK-8357069 (P4): [AIX] Adapt code for C++ VLA rule - AIXでのビルドのため、C++のVLA（可変長配列）ルールにコードを適合させました。
* JDK-8357112 (P4): Improve test coverage for JVMTI GetThreadState on carrier and mounted vthread - 仮想スレッドとキャリアスレッドに対するJVMTI GetThreadStateのテストカバレッジを向上させました。
* JDK-8357113 (P4): Rename agent_common.h - テスト用のヘッダファイル名を変更しました。
* JDK-8357121 (P4): Test: add more test case for string compare (UL case) - 文字列比較（大文字小文字を区別しないケース）のテストケースを追加しました。
* JDK-8357261 (P4): Avoid sending per-region GCPhaseParallel JFR events in G1ScanCollectionSetRegionClosure - G1 GCの特定のフェーズで、リージョンごとにJFRイベントを送信しないようにしました。
* JDK-8357389 (P4): jdk/jfr/startupargs/TestMemoryOptions.java fails with 32-bit build - 32ビットビルドで失敗するJFRの起動引数テストを修正しました。
* JDK-8357437 (P4): Use correct extension for C++ test headers - C++テストヘッダに正しい拡張子を使用するように修正しました。
* JDK-8357483 (P4): Remove the appcds/javaldr/AnonVmClassesDuringDump.java test - 不要になったCDS関連のテストを削除しました。
* JDK-8357487 (P4): Incomplete logging in nsk/jvmti/ResourceExhausted/resexhausted00* tests - 特定のJVMTIテストでロギングが不完全であった問題を修正しました。
* JDK-8357488 (P4): [jittester] Remove TempDir debug output - jittesterからTempDirのデバッグ出力を削除しました。
* JDK-8357544 (P4): Clean up vmTestbase/vm/share - テストコードベースのvmTestbase/vm/shareディレクトリをクリーンアップしました。
* JDK-8357855 (P4): Merge vm/share/InMemoryJavaCompiler w/ jdk/test/lib/compiler/InMemoryJavaCompiler - 2つのインメモリJavaコンパイラテストライブラリを1つに統合しました。
* JDK-8357856 (P4): failure_handler lldb command times out on macosx-aarch64 core file - macOS aarch64のコアファイルに対してlldbコマンドがタイムアウトする問題を修正しました。

VMの安定性は最優先事項ですが、プラットフォームのセキュリティ確保もまた、このリリースにおける同様に重要な焦点です。

3.0 セキュリティライブラリの変更点 (Changes in Security Libraries)

このセクションでは、Javaプラットフォームのセキュリティ基盤に加えられたアップデートについて説明します。これには、JSSE (TLS)、暗号化プロバイダ、証明書管理などが含まれます。これらのアップデートは、進化し続ける脅威に対して堅牢なセキュリティを維持するための戦略的に重要な変更です。

セキュリティライブラリの修正一覧

JDK Issue ID	Priority	Title
JDK-8359349	P2	Add 2 TLS and 2 CS Sectigo roots
JDK-8351512	P3	Jarsigner should print a warning if an entry is removed
JDK-8351960	P3	Remove Baltimore root certificate expiring in May 2025
JDK-8353894	P3	Restore null return for invalid services from legacy providers
JDK-8355549	P3	Uninitialised memory in deleteGSSCB of GSSLibStub.c:179
JDK-8355729	P3	Update HSS/LMS public key encoding
JDK-8355731	P3	Compatible OCSP readtimeout property with OCSP timeout
JDK-8351239	P4	Failure when creating non-CRT RSA private keys in SunPKCS11
JDK-8352540	P4	Upgrade NSS binaries for interop tests
JDK-8352548	P4	Test sun/security/tools/jarsigner/TimestampCheck.java is failing
JDK-8353086	P4	Test sun/security/tools/jarsigner/ConciseJarsigner.java failed: unable to find valid certification path to requested target
JDK-8353881	P4	jdk/test/lib/security/timestamp/TsaServer.java warnings
JDK-8353899	P4	Test sun/security/tools/jarsigner/TsacertOptionTest.java failed: Warning found in stdout
JDK-8353915	P4	NullPointerException in sun.security.jca.ProviderList.getService()
JDK-8355099	P4	TLS handshake fails because of ConcurrentModificationException in PKCS12KeyStore.engineGetEntry
JDK-8355101	P4	DistributionPointFetcher fails to fetch CRLs if the DistributionPoints field contains more than one DistributionPoint and the first one fails
JDK-8355170	P4	Refactor ClassLoaderDeadlock.sh and Deadlock.sh to run fully in java
JDK-8355713	P4	KeyStore getEntry is not thread-safe
JDK-8355732	P4	security/auth/callback/TextCallbackHandler/Password.java make runnable with JTReg and add the UI
JDK-8356181	P4	Relocate supporting classes in security/testlibrary to test/lib/jdk tree
JDK-8356519	P4	Test sun/security/mscapi/nonUniqueAliases/NonUniqueAliases.java is marked with @ignore
JDK-8356530	P4	Remove two Camerfirma root CA certificates
JDK-8356650	P4	Update sun/security/pkcs12/KeytoolOpensslInteropTest.java to use a recent Openssl version
JDK-8357545	P4	Better cleanup for jdk/test/sun/security/pkcs12/P12SecretKey.java

[JDK-8359349]: Add 2 TLS and 2 CS Sectigo roots

属性	値
Priority	P2
Type	Backport

JDKのデフォルトトラストストアであるcacertsファイルに、Sectigo認証局の新しいルート証明書（TLS用2つ、コード署名用2つ）を追加します。これにより、JavaアプリケーションはSectigoによって発行された証明書を持つサーバーやソフトウェアとの間で、安全な通信を継続できます。

[JDK-8351512]: Jarsigner should print a warning if an entry is removed

属性	値
Priority	P3
Type	Backport

jarsignerツールを改善し、署名プロセス中にJARファイルからエントリが削除された場合に警告メッセージを出力するようにします。これにより、署名プロセスの透明性が高まり、開発者は意図しないファイルの欠落に気づきやすくなります。

[JDK-8351960]: Remove Baltimore root certificate expiring in May 2025

属性	値
Priority	P3
Type	Backport

セキュリティ衛生を維持するための予防的な措置として、2025年5月に有効期限が切れるBaltimore CyberTrustのルート証明書をcacertsトラストストアから削除します。これにより、将来的な証明書検証エラーを防ぎます。

[JDK-8353894]: Restore null return for invalid services from legacy providers

属性	値
Priority	P3
Type	Backport

レガシーなセキュリティプロバイダから無効なサービスを要求した場合の動作を、例外をスローするのではなくnullを返すように復元します。この後方互換性のための変更により、古いアプリケーションが予期せず動作しなくなる事態を防ぎます。

[JDK-8355549]: Uninitialised memory in deleteGSSCB of GSSLibStub.c:179

属性	値
Priority	P3
Type	Backport

GSS-APIのネイティブラッパーコードに存在する、初期化されていないメモリが使用される可能性があった脆弱性を修正します。この修正により、関連するメモリ領域が確実に初期化され、GSS-API機能の安定性と安全性が向上します。

[JDK-8355729]: Update HSS/LMS public key encoding

属性	値
Priority	P3
Type	Backport

ポスト量子暗号署名スキームであるHSS (Hierarchical Signature System) および LMS (Leighton-Micali Signature) の公開鍵エンコーディングを更新します。これは、関連する標準規格の改訂に対応し、将来の暗号技術への準拠を確実にするためのものです。

[JDK-8355731]: Compatible OCSP readtimeout property with OCSP timeout

属性	値
Priority	P3
Type	Backport

OCSP (Online Certificate Status Protocol) のタイムアウト設定に関する一貫性を向上させます。この変更により、com.sun.security.ocsp.readtimeoutプロパティと他のOCSPタイムアウト設定がより互換性を持つように調整され、証明書失効確認のタイムアウト設定がより予測可能になります。

その他のセキュリティライブラリの修正 (Other Security Library Fixes)

* JDK-8351239 (P4): Failure when creating non-CRT RSA private keys in SunPKCS11 - SunPKCS11プロバイダで非CRT形式のRSA秘密鍵を作成する際の失敗を修正しました。
* JDK-8352540 (P4): Upgrade NSS binaries for interop tests - 相互運用性テストで使用されるNSSバイナリをアップグレードしました。
* JDK-8352548 (P4): Test sun/security/tools/jarsigner/TimestampCheck.java is failing - タイムスタンプのチェックに関するjarsignerのテストが失敗する問題を修正しました。
* JDK-8353086 (P4): Test sun/security/tools/jarsigner/ConciseJarsigner.java failed: unable to find valid certification path to requested target - jarsignerのテストが有効な証明書パスを見つけられずに失敗する問題を修正しました。
* JDK-8353881 (P4): jdk/test/lib/security/timestamp/TsaServer.java warnings - タイムスタンプ局（TSA）サーバーのテストライブラリで発生していた警告を修正しました。
* JDK-8353899 (P4): Test sun/security/tools/jarsigner/TsacertOptionTest.java failed: Warning found in stdout - jarsignerのtsacertオプションに関するテストが標準出力の警告が原因で失敗する問題を修正しました。
* JDK-8353915 (P4): NullPointerException in sun.security.jca.ProviderList.getService() - JCAプロバイダリストのgetService()メソッドでNullPointerExceptionが発生する可能性があった問題を修正しました。
* JDK-8355099 (P4): TLS handshake fails because of ConcurrentModificationException in PKCS12KeyStore.engineGetEntry - PKCS12KeyStore.engineGetEntryメソッドでのConcurrentModificationExceptionが原因でTLSハンドシェイクが失敗する問題を修正しました。
* JDK-8355101 (P4): DistributionPointFetcher fails to fetch CRLs if the DistributionPoints field contains more than one DistributionPoint and the first one fails - 複数のCRL配布ポイントがあり、最初の配布ポイントが失敗した場合にCRLの取得に失敗する問題を修正しました。
* JDK-8355170 (P4): Refactor ClassLoaderDeadlock.sh and Deadlock.sh to run fully in java - 2つのデッドロック関連のシェルスクリプトテストを、完全にJavaで実行されるようにリファクタリングしました。
* JDK-8355713 (P4): KeyStore getEntry is not thread-safe - KeyStore.getEntryメソッドがスレッドセーフでなかった問題を修正しました。
* JDK-8355732 (P4): security/auth/callback/TextCallbackHandler/Password.java make runnable with JTReg and add the UI - 特定のセキュリティコールバックテストをJTRegで実行可能にし、UIを追加しました。
* JDK-8356181 (P4): Relocate supporting classes in security/testlibrary to test/lib/jdk tree - セキュリティテストライブラリのサポートクラスを、より適切なtest/lib/jdkツリーに再配置しました。
* JDK-8356519 (P4): Test sun/security/mscapi/nonUniqueAliases/NonUniqueAliases.java is marked with @ignore - MSCAPIプロバイダに関するテストが@ignoreでマークされていた問題を調査・修正しました。
* JDK-8356530 (P4): Remove two Camerfirma root CA certificates - 2つのCamerfirmaルートCA証明書をトラストストアから削除しました。
* JDK-8356650 (P4): Update sun/security/pkcs12/KeytoolOpensslInteropTest.java to use a recent Openssl version - PKCS12の相互運用性テストで、より新しいバージョンのOpenSSLを使用するように更新しました。
* JDK-8357545 (P4): Better cleanup for jdk/test/sun/security/pkcs12/P12SecretKey.java - PKCS12の秘密鍵に関するテストの後処理を改善しました。

ランタイムとセキュリティの改善と並行して、開発者向けツールの機能強化もこのリリースの重要な一部です。

4.0 ツールの変更点 (Changes in Tools)

このセクションでは、JDKに含まれるツール、特に javac コンパイラや jpackage ツールなどに対するアップデートに焦点を当てます。これらの変更は、開発者のワークフロー、ビルドプロセス、そしてコンパイルやパッケージングタスクの信頼性を向上させることを目的としています。

ツールの修正一覧

JDK Issue ID	Priority	Title
JDK-8354893	P2	[REDO BACKPORT] javac crashes while adding type annotations to the return type of a constructor (JDK-8320001)
JDK-8360406	P2	[21u] Disable logic for attaching type annotations to class files until 8359336 is fixed
JDK-8341779	P3	[REDO BACKPORT] type annotations are not visible to javac plugins across compilation boundaries (JDK-8225377)
JDK-8354923	P3	Type annotation attached to incorrect type during class reading
JDK-8355057	P3	CompletionFailure in getEnclosingType attaching type annotations
JDK-8356013	P3	NPE due to unreported compiler error
JDK-8357116	P3	Ctrl+C does not call shutdown hooks after JLine upgrade
JDK-8351022	P4	Test FailOverDirectExecutionControlTest.java fails with -Xcomp
JDK-8352735	P4	Clean up the code in sun.tools.jar.Main to properly close resources and use ZipFile during extract
JDK-8354630	P4	org.jline.util.PumpReader signed byte problem
JDK-8354948	P4	In ClassReader, extract a constant for the superclass supertype_index
JDK-8356517	P4	WinInstallerUiTest fails in local test runs if the path to test work directory is longer that regular

[JDK-8354893]: [REDO BACKPORT] javac crashes while adding type annotations to the return type of a constructor (JDK-8320001)

属性	値
Priority	P2
Type	Bug

この修正は、コンストラクタの戻り値型に型アノテーションを追加しようとするとjavacがクラッシュするリグレッション（JDK-8320001）に再び対処するものです。内部的に、コンストラクタの戻り値型はVOIDとして扱われ、この型にはメタデータを付加できないというjavacの内部アサーションに違反していました。この修正により、ClassReaderのロジックが修正され、コンストラクタのアノテーション処理が正しく行われるようになり、コンパイラの安定性が回復します。

[JDK-8360406]: [21u] Disable logic for attaching type annotations to class files until 8359336 is fixed

属性	値
Priority	P2
Type	Bug

これは、プラットフォームの安定性を優先するための予防的な措置です。以前のアップデート（JDK-8341779）でバックポートされた、クラスファイルをまたいで型アノテーションを可視化する機能が、深刻なクラッシュ（JDK-8359336）を引き起こすことが判明しました。根本的な修正が完了するまでの間、このパッチはその新機能のロジックを一時的に無効にします。これにより、ユーザーがクラッシュに遭遇するのを防ぎつつ、将来的に安全な形で機能を再導入する道を残しています。

[JDK-8341779]: [REDO BACKPORT] type annotations are not visible to javac plugins across compilation boundaries (JDK-8225377)

属性	値
Priority	P3
Type	Bug

この修正は、javacプラグインが、ソースコードからではなくクラスパスからロードされたシンボル（.classファイル内の型）に関連付けられた型アノテーションを認識できないという制限（JDK-8225377）に対処するものです。これにより、アノテーションプロセッサがコンパイル境界を越えて型情報を完全に分析することが困難でした。この変更（後にJDK-8360406で一時的に無効化）は、クラスファイルからシンボルを読み込む際に型アノテーションを正しく復元し、プラグインからアクセスできるようにすることを目的としていました。

[JDK-8354923]: Type annotation attached to incorrect type during class reading

属性	値
Priority	P3
Type	Backport

javacがクラスファイルを読み込む際に、型アノテーションを誤った型要素に関連付けてしまうバグを修正します。この修正により、アノテーションがクラスファイルから読み込まれる際に正しい型にアタッチされることが保証され、アノテーション処理の正確性が向上します。

[JDK-8355057]: CompletionFailure in getEnclosingType attaching type annotations

属性	値
Priority	P3
Type	Backport

特定の状況下で、型アノテーションを付加するプロセス中に、シンボルの完全な情報をロードできないCompletionFailureエラーが発生していたjavacのバグを修正します。この修正により、シンボル解決のロジックが改善され、コンパイラの堅牢性が向上します。

[JDK-8356013]: NPE due to unreported compiler error

属性	値
Priority	P3
Type	Backport

コンパイルの初期段階で発生したエラーが適切に報告されず、javacが不整合な状態で処理を続行しようとした結果、後続の処理でNullPointerExceptionが発生していた問題に対処します。この修正では、初期エラーが確実に報告され、コンパイルが安全に停止するようになります。

[JDK-8357116]: Ctrl+C does not call shutdown hooks after JLine upgrade

属性	値
Priority	P3
Type	Backport

jshellなどのコマンドラインツールで使用されているJLineライブラリのアップグレードに伴い、Ctrl+Cでプロセスを中断した際にシャットダウンフックが呼び出されなくなったリグレッションを修正します。この修正により、シグナルハンドリングが復元され、リソースのクリーンアップなどが適切に実行されるようになります。

その他のツールの修正 (Other Tool Fixes)

* JDK-8351022 (P4): Test FailOverDirectExecutionControlTest.java fails with -Xcomp - -Xcompモードで失敗するテストを修正しました。
* JDK-8352735 (P4): Clean up the code in sun.tools.jar.Main to properly close resources and use ZipFile during extract - jarコマンドの実装をクリーンアップし、リソースが正しく閉じられるようにしました。
* JDK-8354630 (P4): org.jline.util.PumpReader signed byte problem - JLineライブラリのPumpReaderにおける符号付きバイトの問題を修正しました。
* JDK-8354948 (P4): In ClassReader, extract a constant for the superclass supertype_index - ClassReader内でスーパークラスのインデックスを表す定数を抽出し、コードの可読性を向上させました。
* JDK-8356517 (P4): WinInstallerUiTest fails in local test runs if the path to test work directory is longer that regular - WindowsインストーラのUIテストが、テスト作業ディレクトリのパスが長い場合に失敗する問題を修正しました。

開発者向けツールに加え、ほとんどのJavaアプリケーションの基盤となるコアライブラリも、重要なアップデートを受けています。

5.0 コアライブラリの変更点 (Changes in Core Libraries)

このセクションでは、Javaの基本的なAPI、すなわちネットワーキング（java.net）、I/O（java.io, java.nio）、コレクション、並行処理ユーティリティなど、コアライブラリに加えられた修正と改善について詳述します。これらの変更は、幅広いアプリケーションの堅牢性とパフォーマンスを向上させる可能性があります。

コアライブラリの修正一覧

JDK Issue ID	Priority	Title
JDK-8350948	P3	UpcallLinker::on_exit races with GC when copying frame anchor
JDK-8352513	P3	Incorrect handling of HTTP/2 GOAWAY frames in HttpClient
JDK-8353301	P3	Primitive caches must use boxed instances from the archive
JDK-8353921	P3	(tz) Update Timezone Data to 2025b
JDK-8354429	P3	(ch) sun.nio.ch.Poller.register throws AssertionError
JDK-8355035	P3	HTTP/2 ConnectionWindowUpdateSender may miss some unprocessed DataFrames from closed streams
JDK-8355100	P3	Enhance checks in BigDecimal.toPlainString()
JDK-8355738	P3	Increased number of SHA-384-Digest java.util.jar.Attributes$Name instances leading to higher memory footprint
JDK-8356707	P3	GZIPInputStream constructor could leak an un-end()ed Inflater
JDK-8357548	P3	ISO 4217 Amendment 179 Update
JDK-8350610	P4	HttpClient: improve HTTP/2 flow control checks
JDK-8350949	P4	UpcallLinker::on_entry racingly clears pending exception with GC safepoints
JDK-8350950	P4	ProgrammableUpcallHandler::on_entry/on_exit access thread fields from native
JDK-8351190	P4	[JMH] time.format.ZonedDateTimeFormatterBenchmark fails
JDK-8351934	P4	Inaccurate masking of TC subfield decrement in ForkJoinPool
JDK-8352000	P4	java/net/ipv6tests/UdpTest.java fails with checkTime failed
JDK-8352076	P4	[21u] Problem list tests that fail in 21 and would be fixed by 8309622
JDK-8352220	P4	assert fired in java/net/httpclient/DependentPromiseActionsTest (infrequent)
JDK-8352227	P4	java/net/Socket/UdpSocket.java fails with "java.net.BindException: Address already in use" (macos-aarch64)
JDK-8352234	P4	(fs) Remove some extensions from java/nio/file/Files/probeContentType/Basic.java
JDK-8352238	P4	test/jdk/java/net/httpclient/HttpsTunnelAuthTest.java fails intermittently
JDK-8352425	P4	HttpClient with StructuredTaskScope does not close when a task fails
JDK-8352438	P4	[JMH] vector.IndexInRangeBenchmark failed with IndexOutOfBoundsException for size=1024
JDK-8352586	P4	Some java/lang jtreg tests miss requires vm.hasJFR
JDK-8352658	P4	[JMH] Cannot access class jdk.internal.vm.ContinuationScope
JDK-8353096	P4	URLConnection.getLastModified() leaks file handles for jar:file and file: URLs
JDK-8353645	P4	java/io/File/GetXSpace.java fails on Windows with CD-ROM drive
JDK-8353646	P4	Wrong timeout computations in DnsClient
JDK-8353647	P4	com/sun/jndi/dns/ConfigTests/Timeout.java failed intermittent
JDK-8353900	P4	Race condition in jdk/java/net/httpclient/offline/FixedResponseHttpClient.java
JDK-8354267	P4	java/net/httpclient/ShutdownNow.java fails with java.lang.AssertionError: client was still running, but exited after further delay: timeout should be adjusted
JDK-8354349	P4	Several java/net/InetAddress tests fails UnknownHostException
JDK-8354533	P4	Writer not closed with disk full error, file resource leaked
JDK-8355112	P4	java/util/Properties/StoreReproducibilityTest.java times out
JDK-8355550	P4	SequenceInputStream.transferTo should not return as soon as Long.MAX_VALUE bytes have been transferred
JDK-8355709	P4	Test java/net/httpclient/CancelRequestTest.java failed: WARNING: tracker for HttpClientImpl(42) has outstanding operations
JDK-8355712	P4	java/net/vthread/BlockingSocketOps.java timeout/hang intermittently on Windows
JDK-8355728	P4	HTTP/2 flow control checks may count unprocessed data twice
JDK-8355730	P4	java/net/DatagramSocket/InterruptibleDatagramSocket.java fails with virtual thread factory
JDK-8355734	P4	(fc) Make java/nio/channels/FileChannel/BlockDeviceSize.java test manual
JDK-8355736	P4	java/net/httpclient/Http1ChunkedTest.java fails with java.util.MissingFormatArgumentException: Format specifier '%s'
JDK-8355737	P4	httpclient HeadTest does not run on HTTP2
JDK-8355760	P4	Overflow in Collections.rotate
JDK-8356637	P4	Pattern.Bound has static fields that should be static final.
JDK-8356672	P4	Misleading exception message from STS.Subtask::get when task forked after shutdown
JDK-8356802	P4	j.text.DateFormatSymbols setZoneStrings() exception is unhelpful
JDK-8357117	P4	Incorrect error message during startup if working directory does not exist
JDK-8357477	P4	AIX: sporadic unexpected errno when calling setsockopt in Net.joinOrDrop
JDK-8357484	P4	Bug in com/sun/net/httpserver/bugs/B6361557.java test
JDK-8356784	P5	Misformatted copyright messages in FFM

[JDK-8350948]: UpcallLinker::on_exit races with GC when copying frame anchor

属性	値
Priority	P3
Type	Backport

Foreign Function & Memory (FFM) APIのネイティブコード呼び出し（アップコール）からの復帰処理に存在する競合状態を解決します。UpcallLinker::on_exit関数がフレームアンカーをコピーする処理と、ガベージコレクタの動作が衝突する可能性があった問題を修正し、FFM APIの安定性を向上させます。

[JDK-8352513]: Incorrect handling of HTTP/2 GOAWAY frames in HttpClient

属性	値
Priority	P3
Type	Backport

java.net.http.HttpClientがHTTP/2のGOAWAYフレームを不適切に処理していたバグを修正します。この修正により、クライアントはHTTP/2プロトコル仕様に沿ってコネクションのシャットダウンを正しく処理するようになり、コネクション管理の信頼性が向上します。

[JDK-8353301]: Primitive caches must use boxed instances from the archive

属性	値
Priority	P3
Type	Backport

Class Data Sharing (CDS) 機能において、Integer.valueOf(int)などで使用されるプリミティブラッパー型のキャッシュが、CDSアーカイブに格納された共有インスタンスを確実に使用するように修正します。これにより、CDSによるメモリフットプリント削減効果が最大化されます。

[JDK-8353921]: (tz) Update Timezone Data to 2025b

属性	値
Priority	P3
Type	Backport

IANAタイムゾーンデータベースをバージョン2025bに更新します。この定期的なメンテナンスにより、世界各国の夏時間（DST）ルールの変更などが反映され、Javaアプリケーションが常に正確な時刻情報を扱えるようになります。

[JDK-8354429]: (ch) sun.nio.ch.Poller.register throws AssertionError

属性	値
Priority	P3
Type	Backport

java.nioの非同期チャネルで使用される内部ポーリング機構sun.nio.ch.PollerでAssertionErrorがスローされる問題を解決します。この修正により、内部状態の管理が改善され、NIOチャネルの堅牢性が向上します。

[JDK-8355035]: HTTP/2 ConnectionWindowUpdateSender may miss some unprocessed DataFrames from closed streams

属性	値
Priority	P3
Type	Backport

java.net.http.HttpClientのHTTP/2フロー制御におけるバグを修正します。ストリームが閉じた直後にまだ処理されていないデータフレームの量がフロー制御の計算から漏れてしまう可能性がありましたが、この修正によりすべてのデータが正確に計上されるようになり、通信の安定性が向上します。

[JDK-8355100]: Enhance checks in BigDecimal.toPlainString()

属性	値
Priority	P3
Type	Backport

BigDecimal.toPlainString()メソッドの堅牢性を高めます。非常に大きなスケールを持つBigDecimalオブジェクトに対して内部的なチェックを強化し、過剰なリソース消費を抑制することで、サービス拒否（DoS）攻撃に対する耐性を向上させます。

[JDK-8355738]: Increased number of SHA-384-Digest java.util.jar.Attributes$Name instances leading to higher memory footprint

属性	値
Priority	P3
Type	Backport

JARファイルの署名情報を処理する際に、java.util.jar.Attributes$Nameオブジェクトが不必要に多数生成され、メモリ使用量が増加していたリグレッションを修正します。これらのオブジェクトを適切に再利用することで、メモリフットプリントを以前のレベルに戻します。

[JDK-8356707]: GZIPInputStream constructor could leak an un-end()ed Inflater

属性	値
Priority	P3
Type	Backport

GZIPInputStreamのコンストラクタで例外が発生した場合に、内部のInflaterオブジェクトがクローズされず、ネイティブリソースがリークする可能性があったバグを修正します。この修正により、例外発生時でもリソースが確実にクリーンアップされるようになります。

[JDK-8357548]: ISO 4217 Amendment 179 Update

属性	値
Priority	P3
Type	Backport

java.util.Currencyクラスが使用する通貨データを、ISO 4217規格の改訂179に基づいて更新します。これにより、Javaアプリケーションが最新の国際通貨情報を利用できるようになります。

その他のコアライブラリの修正 (Other Core Library Fixes)

* JDK-8350610 (P4): HttpClient: improve HTTP/2 flow control checks - HTTP/2クライアントのフロー制御チェックを改善しました。
* JDK-8350949 (P4): UpcallLinker::on_entry racingly clears pending exception with GC safepoints - FFM APIで、GCセーフポイントとの競合により保留中の例外がクリアされる問題を修正しました。
* JDK-8350950 (P4): ProgrammableUpcallHandler::on_entry/on_exit access thread fields from native - FFM APIで、ネイティブコードからスレッドフィールドにアクセスする際の問題を修正しました。
* JDK-8351190 (P4): [JMH] time.format.ZonedDateTimeFormatterBenchmark fails - ZonedDateTimeFormatterのJMHベンチマークが失敗する問題を修正しました。
* JDK-8351934 (P4): Inaccurate masking of TC subfield decrement in ForkJoinPool - ForkJoinPoolでのタスクカウンタのデクリメント処理における不正確なマスキングを修正しました。
* JDK-8352000 (P4): java/net/ipv6tests/UdpTest.java fails with checkTime failed - IPv6 UDPテストが時間チェックで失敗する問題を修正しました。
* JDK-8352076 (P4): [21u] Problem list tests that fail in 21 and would be fixed by 8309622 - JDK 21で失敗する特定のテストを、将来の修正を待つ形で問題リストに追加しました。
* JDK-8352220 (P4): assert fired in java/net/httpclient/DependentPromiseActionsTest (infrequent) - HTTPクライアントのテストで稀に発生するアサーション失敗を修正しました。
* JDK-8352227 (P4): java/net/Socket/UdpSocket.java fails with "java.net.BindException: Address already in use" (macos-aarch64) - macOS aarch64でUDPソケットテストが「アドレスは既に使用中です」エラーで失敗する問題を修正しました。
* JDK-8352234 (P4): (fs) Remove some extensions from java/nio/file/Files/probeContentType/Basic.java - Files.probeContentTypeのテストからいくつかの拡張子を削除しました。
* JDK-8352238 (P4): test/jdk/java/net/httpclient/HttpsTunnelAuthTest.java fails intermittently - HTTPSトンネル認証に関するHTTPクライアントのテストが断続的に失敗する問題を修正しました。
* JDK-8352425 (P4): HttpClient with StructuredTaskScope does not close when a task fails - StructuredTaskScope内で使用されたHTTPクライアントが、タスク失敗時にクローズされない問題を修正しました。
* JDK-8352438 (P4): [JMH] vector.IndexInRangeBenchmark failed with IndexOutOfBoundsException for size=1024 - 特定のサイズのVector APIベンチマークがIndexOutOfBoundsExceptionで失敗する問題を修正しました。
* JDK-8352586 (P4): Some java/lang jtreg tests miss requires vm.hasJFR - JFRを必要とする一部のjava.langテストに、requires vm.hasJFRの指定が欠けていたのを修正しました。
* JDK-8352658 (P4): [JMH] Cannot access class jdk.internal.vm.ContinuationScope - JMHベンチマークからContinuationScopeクラスにアクセスできない問題を修正しました。
* JDK-8353096 (P4): URLConnection.getLastModified() leaks file handles for jar:file and file: URLs - jar:やfile: URLに対するURLConnectionがファイルハンドルをリークする問題を修正しました。
* JDK-8353645 (P4): java/io/File/GetXSpace.java fails on Windows with CD-ROM drive - WindowsでCD-ROMドライブがある場合にFile.getFreeSpace()などのテストが失敗する問題を修正しました。
* JDK-8353646 (P4): Wrong timeout computations in DnsClient - DnsClientでのタイムアウト計算が間違っていた問題を修正しました。
* JDK-8353647 (P4): com/sun/jndi/dns/ConfigTests/Timeout.java failed intermittent - JNDI DNSのタイムアウトテストが断続的に失敗する問題を修正しました。
* JDK-8353900 (P4): Race condition in jdk/java/net/httpclient/offline/FixedResponseHttpClient.java - HTTPクライアントのテスト用クラスにおける競合状態を修正しました。
* JDK-8354267 (P4): java/net/httpclient/ShutdownNow.java fails with java.lang.AssertionError... - HTTPクライアントのシャットダウンテストがタイムアウトで失敗する問題を修正しました。
* JDK-8354349 (P4): Several java/net/InetAddress tests fails UnknownHostException - いくつかのInetAddress関連テストがUnknownHostExceptionで失敗する問題を修正しました。
* JDK-8354533 (P4): Writer not closed with disk full error, file resource leaked - ディスクフルエラー時にWriterが閉じられず、ファイルリソースがリークする問題を修正しました。
* JDK-8355112 (P4): java/util/Properties/StoreReproducibilityTest.java times out - Propertiesの保存に関する再現性テストがタイムアウトする問題を修正しました。
* JDK-8355550 (P4): SequenceInputStream.transferTo should not return as soon as Long.MAX_VALUE bytes have been transferred - SequenceInputStream.transferToがLong.MAX_VALUEバイト転送した時点で即座に復帰してしまう問題を修正しました。
* JDK-8355709 (P4): Test java/net/httpclient/CancelRequestTest.java failed... - HTTPクライアントのリクエストキャンセルテストが失敗する問題を修正しました。
* JDK-8355712 (P4): java/net/vthread/BlockingSocketOps.java timeout/hang intermittently on Windows - 仮想スレッドでのブロッキングソケット操作テストがWindowsで断続的にハングする問題を修正しました。
* JDK-8355728 (P4): HTTP/2 flow control checks may count unprocessed data twice - HTTP/2のフロー制御チェックが未処理データを二重にカウントする可能性があった問題を修正しました。
* JDK-8355730 (P4): java/net/DatagramSocket/InterruptibleDatagramSocket.java fails with virtual thread factory - 仮想スレッド使用時にDatagramSocketの割り込みテストが失敗する問題を修正しました。
* JDK-8355734 (P4): (fc) Make java/nio/channels/FileChannel/BlockDeviceSize.java test manual - ブロックデバイスのサイズに関するFileChannelのテストを手動テストに変更しました。
* JDK-8355736 (P4): java/net/httpclient/Http1ChunkedTest.java fails with java.util.MissingFormatArgumentException... - HTTP/1.1のチャンクエンコーディングテストでフォーマット文字列の例外が発生する問題を修正しました。
* JDK-8355737 (P4): httpclient HeadTest does not run on HTTP2 - HTTPクライアントのHEADリクエストテストがHTTP/2で実行されていなかった問題を修正しました。
* JDK-8355760 (P4): Overflow in Collections.rotate - Collections.rotateメソッドでオーバーフローが発生する可能性があった問題を修正しました。
* JDK-8356637 (P4): Pattern.Bound has static fields that should be static final. - Pattern.Boundクラスのstaticフィールドをstatic finalに変更しました。
* JDK-8356672 (P4): Misleading exception message from STS.Subtask::get when task forked after shutdown - シャットダウン後にフォークされたタスクからget()を呼び出した際の例外メッセージが誤解を招くものだったのを修正しました。
* JDK-8356802 (P4): j.text.DateFormatSymbols setZoneStrings() exception is unhelpful - DateFormatSymbols.setZoneStrings()がスローする例外のメッセージが分かりにくかったのを改善しました。
* JDK-8357117 (P4): Incorrect error message during startup if working directory does not exist - 存在しない作業ディレクトリから起動した際のエラーメッセージが不正確だったのを修正しました。
* JDK-8357477 (P4): AIX: sporadic unexpected errno when calling setsockopt in Net.joinOrDrop - AIXでsetsockopt呼び出し時に予期せぬエラーが発生する問題を修正しました。
* JDK-8357484 (P4): Bug in com/sun/net/httpserver/bugs/B6361557.java test - com.sun.net.httpserverのテストにあったバグを修正しました。
* JDK-8356784 (P5): Misformatted copyright messages in FFM - FFM API関連のファイルで著作権メッセージのフォーマットが間違っていたのを修正しました。

コアとなるサーバーサイドのライブラリに加えて、デスクトップおよびクライアントサイドのライブラリも更新されています。

6.0 その他のコンポーネントの変更点 (Changes in Other Components)

この最終セクションでは、クライアントライブラリ（AWT/Swing）、コアサービス（JMX/JVMTI）、インフラストラクチャ、パフォーマンス、XMLなど、その他の重要なJDKコンポーネントにわたるアップデートをまとめています。

クライアントライブラリ (Client Libraries)

* JDK-8351528 (P3): Update PipeWire to 1.3.81 - PipeWireライブラリをバージョン1.3.81に更新しました。
* JDK-8351532 (P3): [Accessibility,macOS,VoiceOver] VoiceOver doesn't announce untick on toggling the checkbox with "space" key on macOS - macOSでVoiceOverがチェックボックスのチェック解除を読み上げないアクセシビリティの問題を修正しました。
* JDK-8351533 (P3): [Accessibility,macOS,Screen Magnifier]: JCheckbox unchecked state does not magnify but works for checked state - macOSのスクリーンマグニファイアがチェックされていないJCheckboxを拡大しないアクセシビリティの問題を修正しました。
* JDK-8351538 (P3): Update FreeType to 2.13.3 - FreeTypeフォントレンダリングライブラリをバージョン2.13.3に更新しました。
* JDK-8351879 (P3): print/Dialog/PaperSizeError.java fails with MediaSizeName is not A4: A4 - 印刷ダイアログの用紙サイズに関するテストの失敗を修正しました。
* JDK-8352543 (P3): [XWayland] No displayChanged event after setDisplayMode call - XWayland環境でsetDisplayMode呼び出し後にdisplayChangedイベントが発生しない問題を修正しました。
* JDK-8352544 (P3): Update LCMS to 2.17 - Little CMS (LCMS) カラーマネジメントエンジンをバージョン2.17に更新しました。
* JDK-8353140 (P3): Desktop.browse method fails if earlier CoInitialize call as COINIT_MULTITHREADED - 特定のCOM初期化モードでDesktop.browseが失敗する問題を修正しました。
* JDK-8353538 (P3): Update HarfBuzz to 10.4.0 - HarfBuzzテキストシェーピングエンジンをバージョン10.4.0に更新しました。
* JDK-8353540 (P3): Update Libpng to 1.6.47 - Libpngライブラリをバージョン1.6.47に更新しました。
* JDK-8353852 (P3): [ubsan] exclude function BilinearInterp and ShapeSINextSpan in libawt java2d from ubsan checks - ubsanチェックからAWTの特定の2D関数を除外しました。
* JDK-8354649 (P3): [Accessibility,macOS,VoiceOver] VoiceOver reads the spinner value 10 as 1 when user iterates to 10 for the first time on macOS - macOSでVoiceOverがスピナーの値を誤って読み上げるアクセシビリティの問題を修正しました。
* JDK-8355149 (P3): Test javax/swing/JTabbedPane/8007563/Test8007563.java fails - JTabbedPaneに関するテストの失敗を修正しました。

コアサービス (Core Services)

* JDK-8354640 (P3): javax/management/security/HashedPasswordFileTest.java creates tmp file in src dir - JMXセキュリティのテストがソースディレクトリに一時ファイルを作成する問題を修正しました。
* JDK-8357534 (P3): [VS 2022 17.14] Warning C5287 in debugInit.c: enum type mismatch during build - Visual Studio 2022でのビルド時に発生するコンパイラ警告を修正しました。
* JDK-8352524 (P4): Adjust timeout in test javax/management/monitor/DerivedGaugeMonitorTest.java - JMXモニターのテストのタイムアウト値を調整しました。
* JDK-8354367 (P4): java/lang/instrument/modules/AppendToClassPathModuleTest.java ignores VM flags - java.lang.instrumentのテストがVMフラグを無視する問題を修正しました。
* JDK-8355117 (P4): Test ThreadCpuTime.java should pause like ThreadCpuTimeArray.java - ThreadCpuTimeテストに一時停止処理を追加しました。
* JDK-8355714 (P4): Update nsk.share.jpda.Jdb to don't use finalization - JPDAテストライブラリでファイナライゼーションの使用をやめるよう更新しました。
* JDK-8355716 (P4): Replace usage of -noclassgc with -Xnoclassgc in test/jdk/java/lang/management/MemoryMXBean/LowMemoryTest2.java - 古い-noclassgcオプションを-Xnoclassgcに置き換えました。
* JDK-8355727 (P4): Fix incorrect log message in JDI stop002t test - JDIテストの不正確なログメッセージを修正しました。
* JDK-8355759 (P4): sun.jvmstat.monitor.MonitoredHost.getMonitoredHost() throws unexpected exceptions when invoked concurrently - getMonitoredHost()が並行呼び出しで例外をスローする問題を修正しました。
* JDK-8356178 (P4): Update vmTestbase/nsk/share/LocalProcess.java to don't use finalization - テストライブラリでファイナライゼーションの使用をやめるよう更新しました。
* JDK-8356180 (P4): com/sun/tools/attach/BasicTests.java fails with "SocketException: Permission denied: connect" - Attach APIのテストがPermission deniedで失敗する問題を修正しました。
* JDK-8356481 (P4): Test forceEarlyReturn002.java timed out - JVMTIの早期リターン機能のテストがタイムアウトする問題を修正しました。
* JDK-8356508 (P4): Update nsk/jdwp tests to use driver instead of othervm - JDWPテストでothervmの代わりにdriverを使用するように更新しました。
* JDK-8357388 (P4): The jcmd thread dump related tests should test virtual threads - jcmdのスレッドダンプ関連テストが仮想スレッドも対象とするように改善しました。
* JDK-8357482 (P4): DynamicLauncher for JDP test needs to try harder to find a free port - JDPテスト用のランチャーが空きポートを見つけるロジックを改善しました。
* JDK-8353073 (P5): vmTestbase/nsk/jdb/stop_at/stop_at002/stop_at002.java failure goes undetected - JDBテストの失敗が検出されていなかった問題を修正しました。

インフラストラクチャ (Infrastructure)

* JDK-8354494 (P3): Debug symbols bundle should contain full debug files when building --with-external-symbols-in-bundles=public - 特定のビルドオプションで、デバッグシンボルバンドルに完全なデバッグファイルが含まれるように修正しました。
* JDK-8350650 (P4): Bump update version for OpenJDK: jdk-21.0.8 - OpenJDKのアップデートバージョン番号を21.0.8に更新しました。
* JDK-8356785 (P4): Many test files have the wrong Copyright header - 多数のテストファイルの著作権ヘッダーが間違っていたのを修正しました。
* JDK-8357114 (P4): [test] improve assertEquals failure output - テストライブラリのassertEqualsの失敗時出力を改善しました。
* JDK-8361672 (P4): [21u] Remove designator DEFAULT_PROMOTED_VERSION_PRE=ea for release 21.0.8 - リリース21.0.8に向けて、バージョン文字列からeaプレフィックスを削除しました。

パフォーマンス (Performance)

* JDK-8353017 (P4): Use jvmArgs consistently in microbenchmarks -マイクロベンチマークでjvmArgsを一貫して使用するようにしました。
* JDK-8353018 (P4): Use -jvmArgsPrepend when running microbenchmarks in RunTests.gmk -マイクロベンチマーク実行時に-jvmArgsPrependを使用するようにしました。

XML

* JDK-8356943 (P4): translet-name ignored when package-name is also set - package-nameが設定されている場合にtranslet-nameが無視されるXSLTの問題を修正しました。

7.0 詳細不明の変更点 (Changes with Limited Details)

以下の課題は本リリースの一部としてリストされていますが、提供された資料には詳細な説明が含まれていませんでした。これらの変更は、タイトルから推測されるように、HTTP接続、グリフ描画、Swingサポート、TLSプロトコルサポート、HTTPクライアントのヘッダー処理の改善に関連している可能性があります。

* JDK-8345625: Better HTTP connections
* JDK-8348989: Better Glyph drawing
* JDK-8349111: Enhance Swing supports
* JDK-8349594: Enhance TLS protocol support
* JDK-8350991: Improve HTTP client header handling
* JDK-8360147: Better Glyph drawing redux

8.0 まとめ (Conclusion)

OpenJDK 21.0.8+9リリースは、プラットフォーム全体にわたって多数の的を絞った修正と機能強化を提供します。VMの安定性向上から、セキュリティライブラリの強化、コアAPIの堅牢性向上、開発者ツールの改善まで、これらのアップデートはJavaプラットフォーム上で実行される開発者とアプリケーションのパフォーマンス、安定性、およびセキュリティの向上に貢献します。
