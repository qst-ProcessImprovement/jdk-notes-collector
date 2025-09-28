JDK 21 アップデートリリースノートサマリー

1.0 はじめに

本文書は、提供された技術的な問題報告に基づき、JDK 21.0.8および21.0.6リリースに含まれる重要なバグ修正、機能強化、およびその他の変更点の概要をまとめたものです。開発者およびシステム管理者の皆様に明確に情報をお伝えするため、本要約はJDKのバージョンごと、さらに機能コンポーネントごとに整理されています。

2.0 JDK 21.0.8 リリースサマリー

このアップデートには、Javaプラットフォームのパフォーマンス、セキュリティ、および安定性の向上に焦点を当てた、様々なコンポーネントにわたる的を絞った修正と機能強化が含まれています。

HotSpot Virtual Machine

Issue ID	Type	Summary
JDK-8321204	Bug	C2: assert(false) failed: node should be in igvn hash table
JDK-8333890	Bug	Fatal error in auto-vectorizer with float16 kernel.
JDK-8335688	Bug	Interpreter frame size can grow unbounded with deoptimization
JDK-8350325	Bug	SA does not know about all aarch64 registers
JDK-8323795	Enhancement	jcmd Compiler.codecache should print total size of code cache
JDK-8350489	Enhancement	[aarch64] Enable UseSignumIntrinsic by default for Ampere
JDK-8351665	Enhancement	Remove unused UseNUMA in os_aix.cpp

Core Libraries

Issue ID	Type	Summary
JDK-8308291	Bug	GZIPInputStream constructor leaks Inflater
JDK-8351933	Bug	Inaccurate masking of TC subfield decrement in ForkJoinPool

Security Libraries

Issue ID	Type	Summary
JDK-8329624	Bug	PKCS12 keystore getEntry can return an entry with a mismatched key
JDK-8351980	Bug	jarsigner does not error out for timestamped jar with weak algorithms
JDK-8309841	Enhancement	Jarsigner should print a warning if an entry is removed
JDK-8349215	Enhancement	jarsigner -tsacert option does not work as expected
JDK-8350498	Enhancement	Remove two Camerfirma root CA certificates

Client Libraries

Issue ID	Type	Summary
JDK-8330349	Bug	JOptionPane may not be centered on screen
JDK-8337681	Bug	PNGImageWriter uses much more memory than necessary

Tools

Issue ID	Type	Summary
JDK-8348981	Bug	XSLT transform can create files outside target directory

続いて、JDK 21.0.7のリリース概要を説明します。

3.0 JDK 21.0.7 リリースサマリー

提供された資料に基づくと、JDK 21.0.7リリースに関して特定された修正や機能強化はありませんでした。

続いて、JDK 21.0.6のリリース内容について詳述します。

4.0 JDK 21.0.6 リリースサマリー

このリリースは、HotSpot VM、コアライブラリ、クライアントライブラリ、セキュリティインフラストラクチャを含む、JDKのほぼすべての主要コンポーネントにわたる広範なバグ修正と機能強化を提供する、大規模なメンテナンスアップデートです。

HotSpot Virtual Machine

Issue ID	Type	Summary
JDK-8308429	Bug	jvmti/StopThread/stopthrd007 failed with "NoClassDefFoundError..."
JDK-8311301	Bug	MethodExitTest may fail with stack buffer overrun
JDK-8316428	Bug	G1: Nmethod count statistics only count last code root set iterated
JDK-8317575	Bug	AArch64: C2_MacroAssembler::fast_lock uses rscratch1 for cmpxchg result
JDK-8319960	Bug	RISC-V: compiler/intrinsics/TestInteger/LongUnsignedDivMod.java failed
JDK-8319973	Bug	AArch64: Save and restore FPCR in the call stub
JDK-8320682	Bug	[AArch64] C1 compilation fails with "Field too big for insn"
JDK-8320892	Bug	AArch64: Restore FPU control state after JNI
JDK-8321299	Bug	runtime/logging/ClassLoadUnloadTest.java doesn't reliably trigger class unloading
JDK-8323688	Bug	C2: Fix UB of jlong overflow in PhaseIdealLoop::is_counted_loop()
JDK-8324861	Bug	Exceptions::wrap_dynamic_exception() doesn't have ResourceMark
JDK-8325038	Bug	runtime/cds/appcds/ProhibitedPackage.java can fail with UseLargePages
JDK-8326121	Bug	vmTestbase/gc/g1/unloading/... failed with Full gc happened. Test was useless.
JDK-8328665	Bug	serviceability/jvmti/vthread/PopFrameTest failed with a timeout
JDK-8329353	Bug	ResolvedReferencesNotNullTest.java failed...
JDK-8329533	Bug	TestCDSVMCrash fails on libgraal
JDK-8332461	Bug	ubsan: dependencies.cpp... runtime error: load of value 4294967295
JDK-8332724	Bug	x86 MacroAssembler may over-align code
JDK-8333098	Bug	ubsan: bytecodeInfo.cpp: runtime error: division by zero
JDK-8333144	Bug	docker tests do not work when ubsan is configured
JDK-8334475	Bug	UnsafeIntrinsicsTest.java#ZGenerationalDebug assert... failed
JDK-8334560	Bug	[PPC64]: postalloc_expand_java_dynamic_call_sched does not copy all fields
JDK-8335142	Bug	compiler/c1/TestTraceLinearScanLevel.java occasionally times out with -Xcomp
JDK-8335664	Bug	Parsing jsr broken: assert(bci>= 0 && bci < c->method()->code_size()) failed
JDK-8335709	Bug	C2: assert(!loop->is_member(get_loop(useblock))) failed: must be outside loop
JDK-8337066	Bug	Repeated call of StringBuffer.reverse with double byte string returns wrong result
JDK-8337067	Bug	Test runtime/classFileParserBug/Bad_NCDFE_Msg.java won't compile
JDK-8337331	Bug	crash: pinned virtual thread will lead to jvm crash when running with javaagent
JDK-8339384	Bug	Unintentional IOException in jdk.jdi module when JDWP end of stream occurs
JDK-8339386	Bug	Assertion on AIX - original PC must be in the main code section of the compiled method
JDK-6942632	Enhancement	Hotspot should be able to use more than 64 logical processors on Windows
JDK-8311656	Enhancement	Shenandoah: Unused ShenandoahSATBAndRemarkThreadsClosure::_claim_token
JDK-8319970	Enhancement	AArch64: enable tests compiler/intrinsics/Test(Long
JDK-8320397	Enhancement	RISC-V: Avoid passing t0 as temp register to MacroAssembler...
JDK-8321474	Enhancement	TestAutoCreateSharedArchiveUpgrade.java should be updated with JDK 21
JDK-8321550	Enhancement	Update several runtime/cds tests to use vm flags or mark as flagless
JDK-8321940	Enhancement	Improve CDSHeapVerifier in handling of interned strings
JDK-8325610	Enhancement	CTW: Add StressIncrementalInlining to stress options
JDK-8326611	Enhancement	Clean up vmTestbase/nsk/stress/stack tests
JDK-8330621	Enhancement	Make 5 compiler tests use ProcessTools.executeProcess
JDK-8331393	Enhancement	AArch64: u32 _partial_subtype_ctr loaded/stored as 64
JDK-8332112	Enhancement	Update nsk.share.Log to don't print summary during VM shutdown hook
JDK-8332777	Enhancement	Update JCStress test suite
JDK-8333108	Enhancement	Update vmTestbase/nsk/share/DebugeeProcess.java to don't use finalization
JDK-8313878	Sub-task	Exclude two compiler/rtm/locking tests on ppc64le
JDK-8316895	Sub-task	SeenThread::print_action_queue called on a null pointer
JDK-8316907	Sub-task	Fix nonnull-compare warnings
JDK-8325906	Sub-task	Problemlist vmTestbase/vm/mlvm/meth/stress/compiler/deoptimize/Test.java#id1...

Core Libraries

Issue ID	Type	Summary
JDK-8309218	Bug	java/util/concurrent/locks/Lock/OOMEInAQS.java still times out with ZGC...
JDK-8318442	Bug	java/net/httpclient/ManyRequests2.java fails intermittently on Linux
JDK-8319640	Bug	ClassicFormat::parseObject ... does not conform to the javadoc and may leak...
JDK-8320575	Bug	generic type information lost on mandated parameters of record's compact constructors
JDK-8322166	Bug	Files.isReadable/isWritable/isExecutable expensive when file does not exist
JDK-8323562	Bug	SaslInputStream.read() may return wrong value
JDK-8333824	Bug	Unused ClassValue in VarHandles
JDK-8334405	Bug	java/nio/channels/Selector/SelectWithConsumer.java#id0 failed in testWakeupDuringSelect
JDK-8334719	Bug	(se) Deferred close of SelectableChannel may result in a Selector doing the final close...
JDK-8335530	Bug	Java file extension missing in AuthenticatorTest
JDK-8335912	Enhancement	Add an operation mode to the jar command when extracting to not overwriting existing files
JDK-821470	Enhancement	ThreadLocal.nextHashCode can be static final
JDK-8321616	Enhancement	Retire binary test vectors in test/jdk/java/util/zip/ZipFile
JDK-8322830	Enhancement	Add test case for ZipFile opening a ZIP with no entries
JDK-8325399	Enhancement	Add tests for virtual threads doing Selector operations
JDK-8326100	Enhancement	DeflaterDictionaryTests should use Deflater.getBytesWritten instead of Deflater.getTotalOut
JDK-8320586	Task	update manual test/jdk/TEST.groups
JDK-8320665	Task	update jdk_core at open/test/jdk/TEST.groups
JDK-8319678	Sub-task	Several tests from corelibs areas ignore VM flags

Security Libraries

Issue ID	Type	Summary
JDK-8028127	Bug	Regtest java/security/Security/SynchronizedAccess.java is incorrect
JDK-8296787	Bug	Unify debug printing format of X.509 cert serial numbers
JDK-8318105	Bug	[jmh] the test java.security.HSS failed with 2 active threads
JDK-8320192	Bug	SHAKE256 does not work correctly if n >= 137
JDK-8321543	Bug	Update NSS to version 3.96
JDK-8324841	Bug	PKCS11 tests still skip execution
JDK-8328723	Bug	IP Address error when client enables HTTPS endpoint check on server socket
JDK-8330278	Bug	Have SSLSocketTemplate.doClientSide use loopback address
JDK-8331391	Bug	Enhance the keytool code by invoking the buildTrustedCerts method for essential options
JDK-8333317	Bug	Test sun/security/pkcs11/sslecc/ClientJSSEServerJSSE.java failed...
JDK-8333754	Bug	Add a Test against ECDSA and ECDH NIST Test vector
JDK-8325506	Enhancement	Ensure randomness is only read from provided SecureRandom object
JDK-8319673	Sub-task	Few security tests ignore VM flags

Client Libraries

Issue ID	Type	Summary
JDK-8195675	Bug	Call to insertText with single character from custom Input Method ignored
JDK-8225220	Bug	When the Tab Policy is checked,the scroll button direction displayed incorrectly.
JDK-8283214	Bug	[macos] Screen magnifier does not show the magnified text for JComboBox
JDK-8296972	Bug	[macos13] java/awt/Frame/MaximizedToIconified/...: getExtendedState() != 6 as expected
JDK-8312518	Bug	[macos13] setFullScreenWindow() shows black screen on macOS 13 & above
JDK-8315701	Bug	[macos] Regression: KeyEvent has different keycode on different keyboard layouts
JDK-8320673	Bug	PageFormat/CustomPaper.java has no Pass/Fail buttons; multiple instructions
JDK-8322754	Bug	click JComboBox when dialog about to close causes IllegalComponentStateException
JDK-8325851	Bug	Hide PassFailJFrame.Builder constructor
JDK-8327924	Bug	Simplify TrayIconScalingTest.java
JDK-8328021	Bug	Convert applet test java/awt/List/SetFontTest/SetFontTest.html to main program
JDK-8328379	Bug	Convert URLDragTest.html applet test to main
JDK-8332901	Bug	Select{Current,New}ItemTest.java for Choice don't open popup on macOS
JDK-8317116	Enhancement	Provide layouts for multiple test UI in PassFailJFrame
JDK-8325762	Enhancement	Use PassFailJFrame.Builder.splitUI() in PrintLatinCJKTest.java
JDK-8328242	Enhancement	Add a log area to the PassFailJFrame
JDK-8328402	Enhancement	Implement pausing functionality for the PassFailJFrame

Core Services

Issue ID	Type	Summary
JDK-8207908	Bug	JMXStatusTest.java fails assertion intermittently
JDK-8240343	Bug	JDI stopListening/stoplis001 "FAILED: listening is successfully stopped..."
JDK-8306446	Bug	java/lang/management/ThreadMXBean/Locks.java transient failures
JDK-8328303	Bug	3 JDI tests timed out with UT enabled
JDK-8328619	Bug	sun/management/jmxremote/bootstrap/SSLConfigFilePermissionTest.java failed...
JDK-8333235	Bug	vmTestbase/nsk/jdb/kill/kill001/kill001.java fails with C1
JDK-8326898	Enhancement	NSK tests should listen on loopback addresses only

Infrastructure

Issue ID	Type	Summary
JDK-8313374	Bug	--enable-ccache's CCACHE_BASEDIR breaks builds
JDK-8316893	Enhancement	Compile without -fno-delete-null-pointer-checks

Tools

Issue ID	Type	Summary
JDK-8322809	Bug	SystemModulesMap::classNames and moduleNames arrays do not match the order
JDK-8325203	Bug	System.exit(0) kills the launched 3rd party application
JDK-8325525	Enhancement	Create jtreg test case for JDK-8325203

5.0 結論

これらのアップデートは、Javaプラットフォームの進化に対する継続的な取り組みを示すものであり、現代のアプリケーション開発にとって安全で高性能、かつ信頼性の高い環境であり続けることを保証します。
