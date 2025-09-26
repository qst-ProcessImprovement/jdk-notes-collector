OpenJDK 21.0.7+6 リリースノート：変更点と修正点の詳細分析

1. はじめに

このドキュメントは、OpenJDK 21.0.7+6のリリースノートです。本リリースは、JDK 21プラットフォームの安定性、セキュリティ、およびパフォーマンスを向上させるための重要なメンテナンスリリースです。このアップデートは、主にユーザーから報告されたバグの修正と、プラットフォーム全体にわたる重要な改善に焦点を当てています。新機能の追加ではなく、既存の機能セットの品質向上を目的としています。

このリリースノートは、開発者およびシステム管理者が本アップデートに含まれる変更内容を正確に理解し、アップグレード計画を策定するための技術的なリソースとして提供されます。次章以降では、特に影響の大きい修正点のハイライト、そしてコンポーネント別に分類された全修正項目の詳細なリストを解説します。

2. 主要な変更点とハイライト

本セクションでは、OpenJDK 21.0.7+6における最重要修正点をハイライトします。これらはシステムの安定性やセキュリティに直接影響を及ぼす優先度P1およびP2の課題であり、本アップデートの価値を最も端的に示すものです。

* JDK-8347095: JDK-8339902の変更に含まれる不適切な著作権表示
  * 影響の分析: 以前の修正で追加されたファイルに含まれていた誤った著作権表示を修正します。これにより、コードベースのライセンス整合性が維持され、法的な明確さが保たれます。
* JDK-8348068: JDK-8334305以降の様々なテスト失敗
  * 影響の分析: 以前のコードクリーンアップ（JDK-8334305）に起因して発生していた複数のテスト失敗を修正します。これにより、テストスイートの信頼性が回復し、将来のリグレッション防止に貢献します。
* JDK-8346625: JViewportテストのヘッドレス環境での失敗
  * 影響の分析: GUIコンポーネントであるJViewportに関するテストが、ヘッドレス（非GUI）環境で失敗する問題を修正します。CI/CDパイプラインなど、ヘッドレス環境でのテスト実行の安定性が向上します。
* JDK-8349089: JTabbedPane/8134116/Bug8134116.javaにライセンスヘッダーがない
  * 影響の分析: Swingコンポーネントのテストファイルに欠けていたライセンスヘッダーを追加します。これはコードの帰属とライセンスの明確性を保証するための、軽微ながら重要な修正です。
* JDK-8348625: [21u, 17u] Windowsでの古いjava.awt.headless挙動を復元するためにJDK-8185862を元に戻す
  * 影響の分析: Windows環境におけるヘッドレスモードの意図しない有効化を引き起こしていたリグレッション（JDK-8185862）を元に戻します。これにより、特にCI/CDパイプラインなどの自動テスト環境におけるGUIアプリケーションの互換性と安定した動作が復元されます。
* JDK-8346749: Alpine Linux上でlibCreationTimeHelper.cファイルのコンパイルが失敗する
  * 影響の分析: Alpine Linux環境で、ファイルの作成時刻を取得するためのネイティブヘルパーライブラリのコンパイルが失敗する問題を修正します。この修正により、Alpine Linux上でのJDKのビルド安定性が向上します。
* JDK-8346630: runtime/handshake/HandshakeDirectTest.javaがAArch64でアサーションエラーを引き起こす
  * 影響の分析: AArch64アーキテクチャにおいて、スレッドハンドシェイクのテストがJVMのアサーションエラーを引き起こす問題を修正します。これにより、AArch64プラットフォームでのJVMランタイムの信頼性が向上します。
* JDK-8346900: C1パッチ適用後の無効なoopによるクラッシュ
  * 影響の分析: C1コンパイラによるコードパッチング処理において、無効なオブジェクトポインタ（oop）が参照されJVMがクラッシュする可能性がある重大な問題を修正します。システムの安定性が大幅に向上します。
* JDK-8346973: C2: BoxLockノードのみを持つ基本ブロックが誤って空として扱われる
  * 影響の分析: C2コンパイラの最適化処理において、モニタロックに関連するノードのみを含む基本ブロックを誤って空として扱ってしまう問題を修正します。これにより、コンパイラの最適化の正確性が向上し、予期せぬ実行時エラーのリスクを低減します。
* JDK-8347884: SuperWordによるアライメント参照として使用された後のメモリアロケーション除去に関するテストの追加
  * 影響の分析: C2コンパイラのSuperWord最適化（ベクトル化）がメモリアロケーションの除去に与える影響を検証するためのテストを追加します。これにより、コンパイラの高度な最適化に関するコード品質が保証されます。
* JDK-8349657: ZGC: バリア除去解析におけるノードタイプのチェック漏れによるセグメンテーションフォールト
  * 影響の分析: ZGCガベージコレクタ使用時に、特定のノードタイプのチェックが漏れていたことに起因してJVMがセグメンテーションフォールトでクラッシュする問題を修正します。ZGC利用時のシステムの安定性が向上します。
* JDK-8348066: test/jdk/sun/security/x509/DNSName/LeadingPeriod.javaの妥当性チェックが失敗
  * 影響の分析: 先頭にピリオドを持つDNS名制約の証明書検証に関するテストが、意図せず失敗していた問題を修正します。これにより、セキュリティコンポーネントのテストカバレッジと信頼性が向上します。
* JDK-8348341: dlerror()でのSIGSEGVによるクラッシュ
  * 影響の分析: 特定の条件下で、共有ライブラリのエラー処理関数dlerror()の呼び出しがセグメンテーションフォールトを引き起こし、JVMがクラッシュする問題を修正します。ネイティブライブラリとの連携における安定性が向上します。

これらのハイライトは、本リリースが提供する品質向上の一部に過ぎません。次のセクションでは、修正されたすべての項目をコンポーネント別に分類し、より網羅的に解説します。

3. コンポーネント別の詳細な修正リスト

このセクションでは、OpenJDK 21.0.7+6に含まれる全ての修正項目を、関連するコンポーネント（機能領域）ごとに分類して提示します。これにより、特定の技術領域に関心を持つ開発者や管理者が、関連する変更点を効率的に確認し、その影響を評価することが可能になります。

3.1. Client Libraries ()

client-libsコンポーネントは、AWT、Swing、Java 2Dなどのグラフィカルユーザーインターフェース（GUI）に関連する、Javaの伝統的なクライアントサイド技術を担当します。このリリースでは、ヘッドレス環境での安定性向上や、特定のプラットフォームでのUIコンポーネントの動作改善が含まれています。

JDK ID	優先度	タイプ	タイトル	概要
JDK-8347095	P1	Backport	Bad copyright notices in changes from JDK-8339902	JDK-8339902の修正で追加されたファイルに含まれていた、誤った著作権表示を修正します。
JDK-8346625	P2	Backport	JViewport Test headless failure	GUIコンポーネントJViewportのテストが、ヘッドレス（非GUI）環境で実行された際に失敗する問題を修正します。
JDK-8349089	P2	Backport	JTabbedPane/8134116/Bug8134116.java has no license header	SwingコンポーネントJTabbedPaneのテストファイルに欠落していたライセンスヘッダーを追加します。
JDK-8348625	P2	Bug	[21u, 17u] Revert JDK-8185862 to restore old java.awt.headless behavior on Windows	Windows環境におけるヘッドレスモードの意図しない有効化を引き起こしていたリグレッション（JDK-8185862）を元に戻します。これにより、特にCI/CDパイプラインなどの自動テスト環境におけるGUIアプリケーションの互換性と安定した動作が復元されます。
JDK-8346812	P3	Backport	Get rid of JApplet in test/jdk/sanity/client/lib/SwingSet2/src/DemoModule.java	SwingSet2デモから非推奨のJAppletへの依存を削除し、テストを最新のJavaプラクティスに合わせて更新します。
JDK-8346858	P3	Backport	[XWayland] JavaFX hangs when calling java.awt.Robot.getPixelColor	XWayland環境でjava.awt.Robot.getPixelColorを呼び出すとJavaFXアプリケーションがハングする問題を修正します。
JDK-8346899	P3	Backport	[XWayland] test/jdk/java/awt/Mouse/EnterExitEvents/ResizingFrameTest.java	XWayland環境で発生するResizingFrameTestのマウスイベントに関する問題を修正リストに追加します。
JDK-8349439	P3	Backport	[TestBug] DefaultCloseOperation.java test not working as expected wrt instruction after JDK-8325851 fix	PassFailJFrameのテストユーティリティ修正（JDK-8325851）後、ウィンドウのクローズ操作テストが期待通りに動作しなくなった問題を修正します。
JDK-8349443	P3	Backport	Limit the length of inflated text chunks	テキストの展開処理において、チャンクの長さに制限を設けることで、極端に大きな入力によるパフォーマンス問題を緩和します。
JDK-8350505	P3	Backport	[Accessibility,Windows,JAWS] Bug in the getKeyChar method of the AccessBridge class	WindowsのスクリーンリーダーJAWS連携において、AccessBridgeクラスのgetKeyCharメソッドが正しく動作しないアクセシビリティの問題を修正します。
JDK-8350531	P3	Backport	TrayIcon tests fail in Ubuntu 24.10 Wayland	Ubuntu 24.10のWayland環境で、システムトレイアイコン関連のテストが失敗する問題を修正します。
JDK-8350669	P3	Backport	javax/swing/JFileChooser/FileSystemView/WindowsDefaultIconSizeTest.java creates tmp file in src dir	JFileChooserのテストが、一時ファイルをソースツリー内に誤って作成する問題を修正します。
JDK-8345701	P4	Backport	Remove applet usage from JColorChooser tests Test4222508	JColorChooserのテストから非推奨のAppletを除去し、スタンドアロンアプリケーションとして実行できるようにリファクタリングします。
JDK-8345702	P4	Backport	[TESTBUG] XparColor.java test fails with Error. Parse Exception: Invalid or unrecognized bugid: @	テストメタデータ内の不正なbugidによりテストが失敗する問題を修正します。
JDK-8345707	P4	Backport	Test javax/swing/JFileChooser/8080628/bug8080628.java doesn't test for GTK L&F	JFileChooserのテストが、GTKルックアンドフィールを対象としていなかった問題を修正し、テストカバレッジを向上させます。
JDK-8346395	P4	Backport	Remove applet usage from JColorChooser tests Test4319113	JColorChooserのテストから非推奨のAppletを除去し、スタンドアロンアプリケーションとして実行できるようにリファクタリングします。
JDK-8346396	P4	Backport	Remove applet usage from JColorChooser tests Test4759306	JColorChooserのテストから非推奨のAppletを除去し、スタンドアロンアプリケーションとして実行できるようにリファクタリングします。
JDK-8346397	P4	Backport	Remove applet usage from JColorChooser tests Test6348456	JColorChooserのテストから非推奨のAppletを除去し、スタンドアロンアプリケーションとして実行できるようにリファクタリングします。
JDK-8346398	P4	Backport	Convert java/awt/print/PageFormat/SetOrient.html applet test to main	印刷の向きを設定するAppletベースのテストを、スタンドアロンアプリケーションに変換します。
JDK-8346401	P4	Backport	Remove applet usage from JColorChooser tests Test4887836	JColorChooserのテストから非推奨のAppletを除去し、スタンドアロンアプリケーションとして実行できるようにリファクタリングします。
JDK-8346402	P4	Backport	Remove applet usage from JColorChooser tests Test6977726	JColorChooserのテストから非推奨のAppletを除去し、スタンドアロンアプリケーションとして実行できるようにリファクタリングします。
JDK-8346407	P4	Backport	Open source few Undecorated Frame tests	内部で利用されていた、装飾なしウィンドウ（Undecorated Frame）に関するテストをオープンソース化します。
JDK-8346408	P4	Backport	java/awt/Frame/MaximizeUndecoratedTest.java fails in OEL due to a slight color difference	Oracle Enterprise Linux（OEL）環境で、装飾なしウィンドウの最大化テストが僅かな色の違いにより失敗する問題を修正します。
JDK-8346409	P4	Backport	PrintNullString.java doesn't use float arguments	テストコードPrintNullString.javaから、使用されていない浮動小数点数の引数を削除します。
JDK-8346417	P4	Backport	Open source couple TextField related tests	内部で利用されていたTextFieldコンポーネントに関するテストをオープンソース化します。
JDK-8346425	P4	Backport	Improve JButton/bug4490179.java	JButtonに関する古いバグのテストコードを改善し、より信頼性の高いものにします。
JDK-8346451	P4	Backport	Open some swing tests 2	内部で利用されていたSwing関連のテストを複数オープンソース化します。
JDK-8346452	P4	Backport	Open some swing tests 4	内部で利用されていたSwing関連のテストを複数オープンソース化します。
JDK-8346458	P4	Backport	Open some swing tests 5	内部で利用されていたSwing関連のテストを複数オープンソース化します。
JDK-8346459	P4	Backport	Open some swing tests 6	内部で利用されていたSwing関連のテストを複数オープンソース化します。
JDK-8346537	P4	Backport	Convert java/awt/image/MemoryLeakTest/MemoryLeakTest.java applet test to main	AWTイメージ処理のメモリリークを検証するAppletベースのテストを、スタンドアロンアプリケーションに変換します。
JDK-8346539	P4	Backport	Convert java/awt/print/Dialog/PrintApplet.java applet test to main	印刷ダイアログのAppletベースのテストを、スタンドアロンアプリケーションに変換します。
JDK-8346540	P4	Backport	Convert javax/swing/JColorChooser/8065098/bug8065098.java applet test to main	JColorChooserに関するAppletベースのテストを、スタンドアロンアプリケーションに変換します。
JDK-8346542	P4	Backport	Convert java/awt/print/PrinterJob/PrinterDialogsModalityTest/PrinterDialogsModalityTest.html applet test to main	印刷ダイアログのモーダル動作を検証するAppletベースのテストを、スタンドアロンアプリケーションに変換します。
JDK-8346624	P4	Backport	Open source several Swing JTree JViewport KeyboardManager tests	JTree, JViewport, KeyboardManagerに関する内部テストをオープンソース化します。
JDK-8346626	P4	Backport	Remove applet usage from JColorChooser tests Test4759934	JColorChooserのテストから非推奨のAppletを除去し、スタンドアロンアプリケーションとして実行できるようにリファクタリングします。
JDK-8346627	P4	Backport	Convert java/awt/im/JTextFieldTest.java applet test to main	JTextFieldのインプットメソッド（IM）に関するAppletベースのテストを、スタンドアロンアプリケーションに変換します。
JDK-8346629	P4	Backport	Frame not disposed in java/awt/dnd/DropActionChangeTest.java	ドラッグ＆ドロップのテストにおいて、テスト終了後にフレームが破棄されずに残ってしまう問題を修正します。
JDK-8346635	P4	Backport	PassFailJFrame.java test result: Error. Bad action for script: build}	PassFailJFrameテストユーティリティのビルドスクリプトに構文エラーがあり、テストが失敗する問題を修正します。
JDK-8346640	P4	Backport	java/awt/Graphics2D/ScaledTransform/ScaledTransform.java dialog does not get disposed	Graphics2Dのスケーリング変換テストにおいて、ダイアログが破棄されずに残ってしまう問題を修正します。
JDK-8346646	P4	Backport	Exclude List/KeyEventsTest/KeyEventsTest.java from running on macOS	macOS上で失敗するListコンポーネントのキーイベントテストを、一時的に実行対象から除外します。
JDK-8346746	P4	Backport	Open source several Swing JToolbar JTooltip JTree tests	JToolbar, JTooltip, JTreeに関する内部テストをオープンソース化します。
JDK-8346804	P4	Backport	Open source several Swing JTree tests	JTreeに関する内部テストをオープンソース化します。
JDK-8346806	P4	Backport	Open source several Swing JToolbar tests	JToolbarに関する内部テストをオープンソース化します。
JDK-8346807	P4	Backport	Delete Redundant Printer Dialog Modality Test	冗長となっていた印刷ダイアログのモーダル動作に関するテストを削除します。
JDK-8346816	P4	Backport	Remove JButton/PressedButtonRightClickTest test	JButtonの右クリック動作に関する、現在では冗長なテストを削除します。
JDK-8346851	P4	Backport	Open source several AWT/2D related tests	AWTおよびJava 2Dに関する内部テストをオープンソース化します。
JDK-8346894	P4	Backport	Open some swing tests	内部で利用されていたSwing関連のテストを複数オープンソース化します。
JDK-8346895	P4	Backport	Convert javax/swing/JCheckBox/8032667/bug8032667.java applet test to main	JCheckBoxに関するAppletベースのテストを、スタンドアロンアプリケーションに変換します。
JDK-8347096	P4	Backport	Open source AWT List tests	AWTのListコンポーネントに関する内部テストをオープンソース化します。
JDK-8347103	P4	Backport	Clean up a few ExtendedRobot tests	AWTの自動テスト用クラスExtendedRobotに関するテストコードをクリーンアップします。
JDK-8347442	P4	Backport	Convert java/awt/image/multiresolution/MultiDisplayTest/MultiDisplayTest.java applet test to main	マルチ解像度イメージのAppletベースのテストを、スタンドアロンアプリケーションに変換します。
JDK-8347443	P4	Backport	[TEST_BUG]GTK L&F: There is no swatches or RGB tab in JColorChooser	GTKルックアンドフィール使用時にJColorChooserにスウォッチやRGBタブが表示されないUIの問題を、テストの失敗として記録します。
JDK-8347589	P4	Backport	[macos] Test java/awt/Frame/ExceptionOnSetExtendedStateTest/ExceptionOnSetExtendedStateTest.java fails	macOS環境で、Frameの拡張状態設定に関するテストが失敗する問題を修正します。
JDK-8347878	P4	Backport	Remove applet usage from JFileChooser tests bug6698013	JFileChooserのテストから非推奨のAppletを除去し、スタンドアロンアプリケーションとして実行できるようにリファクタリングします。
JDK-8347879	P4	Backport	Manual printer tests have no Pass/Fail buttons, instructions close set 2	手動実行が必要な印刷関連テストにおいて、合否判定ボタンがなく、指示ウィンドウがすぐに閉じてしまう問題を修正します。
JDK-8347882	P4	Backport	Open source closed frame tests #1	内部で利用されていたFrame関連のテストをオープンソース化します。
JDK-8347883	P4	Backport	Write a test to check various components events are triggered properly	様々なUIコンポーネントでイベントが正しくトリガーされることを確認するテストを追加します。
JDK-8347930	P4	Backport	DrawFocusRect() may cause an assertion failure	AWTのフォーカス矩形描画処理DrawFocusRect()が、特定の条件下でアサーションエラーを引き起こす問題を修正します。
JDK-8348057	P4	Backport	[macOS] java/awt/dnd/NextDropActionTest/NextDropActionTest.java fails with java.lang.RuntimeException: wrong next drop action!	macOS環境で、ドラッグ＆ドロップ操作のテストがランタイム例外で失敗する問題を修正します。
JDK-8348059	P4	Backport	Manual printer tests have no Pass/Fail buttons, instructions close set 1	手動実行が必要な印刷関連テストにおいて、合否判定ボタンがなく、指示ウィンドウがすぐに閉じてしまう問題を修正します。
JDK-8348060	P4	Backport	Convert PageFormat/Orient.java to use PassFailJFrame	印刷の向きに関する手動テストを、PassFailJFrameユーティリティを使用して自動化・改善します。
JDK-8348069	P4	Backport	[macos] javax/swing/ProgressMonitor/ProgressMonitorEscapeKeyPress.java fails sometimes in macos	macOS環境で、ProgressMonitorのEscapeキー押下テストが時折失敗する問題を修正します。
JDK-8348070	P4	Backport	java/awt/a11y/AccessibleJTableTest.java fails in some cases where the test tables are not visible	JTableのアクセシビリティテストが、テーブルが不可視の場合に失敗することがある問題を修正します。
JDK-8348071	P4	Backport	Simplify JButton/bug4323121.java	JButtonに関する古いバグのテストコードを簡素化し、メンテナンス性を向上させます。
JDK-8348072	P4	Backport	javax/swing/text/StyledEditorKit/4506788/bug4506788.java fails in ubuntu22.04	Ubuntu 22.04環境で、StyledEditorKitに関するテストが失敗する問題を修正します。
JDK-8348331	P4	Backport	Simplify awt/print/PageFormat/NullPaper.java test	PageFormatにnullのPaperオブジェクトを設定するテストを簡素化します。
JDK-8348332	P4	Backport	Use standard layouts in DefaultFrameIconTest.java and MenuCrash.java	古いテストコードでnullレイアウトを使用していた部分を、標準的なレイアウトマネージャを使用するように修正します。
JDK-8348333	P4	Backport	open source several AWT tests including menu shortcut tests	AWTのメニューショートカットなどに関する内部テストをオープンソース化します。
JDK-8348339	P4	Backport	[TESTBUG] java/awt/PrintJob/PrintCheckboxTest/PrintCheckboxManualTest.java fails with rror. Can't find HTML file PrintCheckboxManualTest.html	チェックボックスの印刷に関する手動テストが、必要なHTMLファイルを見つけられずに失敗する問題を修正します。
JDK-8348947	P4	Backport	Convert java/awt/Frame/FrameStateTest/FrameStateTest.html applet test to main	Frameの状態に関するAppletベースのテストを、スタンドアロンアプリケーションに変換します。
JDK-8349277	P4	Backport	test/jdk/javax/swing/JScrollBar/4865918/bug4865918.java fails in ubuntu22.04	Ubuntu 22.04環境で、JScrollBarに関するテストが失敗する問題を修正します。
JDK-8349429	P4	Backport	Add more details to FrameStateTest.java test instructions	FrameStateTestの手動テスト指示をより詳細で分かりやすく改善します。
JDK-8349436	P4	Backport	Open source several 2D tests	Java 2Dグラフィックスに関する内部テストをオープンソース化します。
JDK-8349437	P4	Backport	[TEST_BUG]GTK L&F: There is no Details button in FileChooser Dialog	GTKルックアンドフィール使用時にJFileChooserに「詳細」ボタンが表示されないUIの問題を、テストの失敗として記録します。
JDK-8349642	P4	Backport	open source several 2D imaging tests	Java 2Dのイメージングに関する内部テストをオープンソース化します。
JDK-8350003	P4	Backport	Error output in libjsound has non matching format strings	Java Soundライブラリのネイティブコードで、フォーマット文字列と引数が一致しないことによる警告や潜在的な問題を修正します。
JDK-8350407	P4	Backport	Convert java/awt/print/bug8023392/bug8023392.html applet test to main	印刷関連のAppletベースのバグテストを、スタンドアロンアプリケーションに変換します。
JDK-8350408	P4	Backport	Remove jtreg tag manual=yesno for java/awt/print/PrinterJob/PrintTextTest.java	PrintTextTestから、現在では不要となった手動テスト用のmanual=yesnoタグを削除します。
JDK-8350409	P4	Backport	Write a test to compare the images	画像を比較するためのテストユーティリティまたはテストケースを追加します。
JDK-8350529	P4	Backport	javax/swing/JScrollBar/4865918/bug4865918.java fails in CI	JScrollBarに関するテストがCI環境で失敗する問題を修正します。
JDK-8350530	P4	Backport	javax/swing/JScrollBar/4865918/bug4865918.java still fails in CI	JScrollBarに関するテストの以前の修正が不完全であったため、再度修正を行います。
JDK-8350670	P4	Backport	javax/imageio/plugins/wbmp/WBMPStreamTruncateTest.java creates temp file in src dir	WBMPイメージプラグインのテストが、一時ファイルをソースツリー内に誤って作成する問題を修正します。
JDK-8350677	P4	Backport	[TESTBUG] java/awt/Robot/ScreenCaptureRobotTest.java failing on macOS	macOS環境で、Robotクラスによるスクリーンキャプチャのテストが失敗する問題を修正します。
JDK-8347892	P5	Backport	Use latch in BasicMenuUI/bug4983388.java instead of delay	BasicMenuUIのテストで、信頼性の低いThread.sleepによる待機を、より堅牢なCountDownLatchに置き換えます。

3.2. Core Libraries ()

core-libsコンポーネントは、コレクションフレームワーク、NIO（New I/O）、ネットワーキングAPI、日付/時刻APIなど、Javaプラットフォームの基本的なライブラリ群をカバーします。このリリースでは、タイムゾーンデータの更新、HTTPクライアントの安定性向上、ファイルシステム操作の互換性修正などが含まれています。

JDK ID	優先度	タイプ	タイトル	概要
JDK-8346749	P2	Backport	File libCreationTimeHelper.c compile fails on Alpine	Alpine Linux環境において、ファイルの作成時刻を取得するためのネイティブヘルパーライブラリのビルドが失敗する問題を修正します。
JDK-8346748	P3	Backport	[REDO] java/nio/file/attribute/BasicFileAttributeView/CreationTime.java#tmp fails on alinux3	Alinux3環境でファイルの作成時刻に関するテストが失敗する問題（リグレッション）を再修正します。
JDK-8347876	P3	Backport	Request with timeout aborts later in-flight request on HTTP/1.1 cxn	HTTP/1.1接続上で、タイムアウトしたリクエストが、後続の正常なリクエストを誤って中断させてしまう問題を修正します。HTTPクライアントの堅牢性が向上します。
JDK-8348843	P3	Backport	(tz) Update Timezone Data to 2025a	IANAのタイムゾーンデータベースを2025aバージョンに更新します。これにより、世界各国の最新の夏時間ルールやタイムゾーンの変更が反映されます。
JDK-8349827	P3	Backport	java/nio/file/Files/probeContentType/Basic.java fails on Windows 2025	Windows Server 2025環境で、Files.probeContentTypeのテストが失敗する問題を修正します。
JDK-8349987	P3	Backport	java/io/File/createTempFile/SpecialTempFile.java failing	Windows Server 2025環境で、特殊な文字を含む一時ファイルの作成テストが失敗する問題を修正します。
JDK-8354711	P3	Backport	UpcallLinker::on_exit races with GC when copying frame anchor	FFM (Foreign Function & Memory API) のアップコール処理において、ガベージコレクションとの競合状態によりデータが破損する可能性がある問題を修正します。
JDK-8345496	P4	Backport	Fix usages of jtreg-reserved properties	テストコード内で、jtregテストハーネスが予約しているシステムプロパティを誤って使用している箇所を修正します。
JDK-8345710	P4	Backport	Update jdk/java/time/tck/java/time/TCKInstant.java now() to be more robust	java.time.Instant.now()のTCK（互換性検証キット）テストを、実行環境のタイマー精度に左右されにくい、より堅牢なものに改善します。
JDK-8346416	P4	Backport	Rearrange reachabilityFence()s in jdk.test.lib.util.ForceGC	ForceGCテストライブラリ内のreachabilityFence()の呼び出し順序を調整し、GCの動作をより確実に制御できるようにします。
JDK-8346631	P4	Backport	Test java/nio/channels/Selector/WakeupNow.java failed	NIOのSelectorに関するWakeupNowテストが失敗する問題を修正し、非同期I/O処理の信頼性を確保します。
JDK-8346641	P4	Backport	java/net/httpclient/PlainProxyConnectionTest.java failed: Unexpected connection count: 5	HTTPクライアントのプロキシ接続テストが、予期しない接続数で失敗する問題を修正します。
JDK-8348200	P4	Backport	Update IANA Language Subtag Registry to Version 2024-11-19	IANA言語サブタグレジストリを2024-11-19バージョンに更新し、java.util.Localeが最新の言語タグを認識できるようにします。
JDK-8348340	P4	Backport	Improve debuggability of test/jdk/java/net/Socket/CloseAvailable.java	Socketのクローズとavailable()メソッドの競合に関するテストのデバッグ情報を拡充し、問題の診断を容易にします。
JDK-8348397	P4	Backport	Improve AnnotationFormatError message for duplicate annotation interfaces	クラスファイル内でアノテーションインターフェースが重複している場合にスローされるAnnotationFormatErrorのメッセージを、より分かりやすく改善します。
JDK-8348676	P4	Backport	(ch) java/nio/channels/AsynchronousSocketChannel/StressLoopback.java times out (aix)	AIX環境でAsynchronousSocketChannelのストレステストがタイムアウトする問題を修正します。
JDK-8349830	P4	Backport	java/io/File/createTempFile/SpecialTempFile.java fails on Windows Server 2025	File.createTempFileがWindows Server 2025で失敗する問題に対応します。
JDK-8349947	P4	Backport	[JMH] jdk.incubator.vector.SpiltReplicate fails NoClassDefFoundError	Vector APIのJMHマイクロベンチマークテストがNoClassDefFoundErrorで失敗する問題を修正します。
JDK-8349948	P4	Backport	Replace usages of -mx and -ms in some tests	古いヒープサイズ指定オプション-mx, -msを、標準の-Xmx, -Xmsに置き換えます。
JDK-8349998	P4	Backport	(dc) java/nio/channels/DatagramChannel/InterruptibleOrNot.java fails with virtual thread factory	仮想スレッド使用時にDatagramChannelの割り込みテストが失敗する問題を修正します。
JDK-8350000	P4	Backport	Test java/nio/channels/FileChannel/LoopingTruncate.java fails sometimes with IOException: There is not enough space on the disk	FileChannelの切り詰めテストが、ディスク容量不足のIOExceptionで時折失敗する問題を修正します。
JDK-8350183	P4	Backport	[aix] java/lang/ProcessHandle/InfoTest.java still fails: "reported cputime less than expected"	AIX環境でProcessHandleのCPU時間に関するテストが、期待値よりも小さい値を報告して失敗する問題を修正します。
JDK-8350310	P4	Backport	[ubsan] ProcessImpl_md.c:561:40: runtime error: applying zero offset to null pointer on macOS aarch64	macOS aarch64で、UBSan（未定義動作サニタイザ）がプロセス実装のネイティブコードでヌルポインタへのオフセット適用を検知した問題を修正します。
JDK-8350684	P4	Backport	HTTP/2 stream cancelImpl may leave subscriber registered	HTTP/2クライアントにおいて、ストリームのキャンセル処理がサブスクライバを登録したままにしてしまい、リソースリークにつながる可能性がある問題を修正します。
JDK-8352097	P4	Bug	(tz) zone.tab update missed in 2025a backport	タイムゾーンデータ2025aへの更新時に、古いJDKバージョンに残っているzone.tabファイルの更新が漏れていた問題を修正します。
JDK-8354712	P4	Backport	UpcallLinker::on_entry racingly clears pending exception with GC safepoints	FFMのアップコール処理において、GCセーフポイントとの競合により保留中の例外が意図せずクリアされる可能性がある問題を修正します。
JDK-8354713	P4	Backport	ProgrammableUpcallHandler::on_entry/on_exit access thread fields from native	FFMのアップコールハンドラが、ネイティブコードからスレッドフィールドにアクセスする際の安全性を向上させます。
JDK-8345498	P5	Backport	Cleanups and JUnit conversion of test/jdk/java/util/zip/Available.java	java.util.zip.AvailableのテストをJUnitに変換し、コードをクリーンアップします。
JDK-8347587	P5	Backport	Update code gen in CallGeneratorHelper	コード生成ヘルパーのロジックを更新し、品質を向上させます。

3.3. HotSpot VM ()

hotspotコンポーネントは、Java仮想マシン（JVM）の心臓部であり、JIT（Just-In-Time）コンパイラ（C1/C2）、ガベージコレクタ（G1, ZGC, Shenandoahなど）、およびランタイムシステムを含みます。このリリースでは、様々なアーキテクチャでのJVMクラッシュの修正、コンパイラの最適化に関する不具合の解消、およびGCの安定性向上が主な改善点です。

JDK ID	優先度	タイプ	タイトル	概要
JDK-8348068	P1	Backport	Various test failures after JDK-8334305	以前のコードクリーンアップ（JDK-8334305）に起因する複数のテスト失敗を修正し、VMの信頼性を回復させます。
JDK-8346630	P2	Backport	runtime/handshake/HandshakeDirectTest.java causes "monitor end should be strictly below the frame pointer" assertion failure on AArch64	AArch64アーキテクチャ上で、スレッドハンドシェイクのテストがフレームポインタに関するアサーションエラーを引き起こす問題を修正します。
JDK-8346900	P2	Backport	Crash due to invalid oop in nmethod after C1 patching	C1コンパイラによるコードパッチング処理において、無効なオブジェクトポインタ（oop）が参照されJVMがクラッシュする可能性がある重大な問題を修正します。システムの安定性が大幅に向上します。
JDK-8346973	P2	Backport	C2: basic blocks with only BoxLock nodes are wrongly treated as empty	C2コンパイラの最適化処理において、モニタロックに関連するノードのみを含む基本ブロックを誤って空として扱ってしまう問題を修正します。これにより、コンパイラの最適化の正確性が向上し、予期せぬ実行時エラーのリスクを低減します。
JDK-8347884	P2	Backport	Add test for Allocation elimination after use as alignment reference by SuperWord	C2コンパイラのSuperWord最適化（ベクトル化）が、メモリアロケーションの除去に与える影響を検証するためのテストを追加します。
JDK-8349657	P2	Backport	ZGC: segmentation fault due to missing node type check in barrier elision analysis	ZGCガベージコレクタ使用時に、特定のノードタイプのチェックが漏れていたことに起因してJVMがセグメンテーションフォールトでクラッシュする問題を修正します。ZGC利用時のシステムの安定性が向上します。
JDK-8345499	P3	Backport	C2: Memory for TypeInterfaces not reclaimed by hashcons()	C2コンパイラ内で、型インターフェース情報のために確保されたメモリが適切に解放されないメモリリークの問題を修正します。
JDK-8346000	P3	Backport	[REDO] Native memory leak when not recording any events	JFR（Java Flight Recorder）がイベントを記録していない状態でもネイティブメモリリークが発生する問題を再修正します。
JDK-8346004	P3	Backport	C2: assert(!n_loop->is_member(get_loop(lca))) failed: control must not be back in the loop	C2コンパイラのループ最適化中に、制御フローがループ内に戻ってはならないというアサーションが失敗する問題を修正します。
JDK-8346189	P3	Backport	AArch64: VM crashes with SIGILL when prctl is disallowed	AArch64環境で、prctlシステムコールが許可されていない場合に、VMが不正命令（SIGILL）でクラッシュする問題を修正します。
JDK-8346332	P3	Backport	C2: Use after free in PhaseChaitin::Register_Allocate()	C2コンパイラのレジスタ割り当てフェーズで、解放済みのメモリにアクセスしてしまう（Use-after-free）脆弱性を修正します。
JDK-8346891	P3	Backport	Checked_cast assert in CDS compare_by_loader	クラスデータ共有（CDS）のクラスローダー比較ロジックで、checked_castのアサーションが失敗する問題を修正します。
JDK-8347028	P3	Backport	[s390x] minimal build failure	s390xアーキテクチャで、最小構成ビルドが失敗する問題を修正します。
JDK-8348201	P3	Backport	Kmem limit and max values swapped when printing container information	コンテナ情報（cgroups）を表示する際に、カーネルメモリの制限値と最大値が入れ替わって表示される問題を修正します。
JDK-8348394	P3	Backport	Shenandoah: Test TestJcmdHeapDump.java#aggressive intermittent assert(gc_cause() == GCCause::_no_gc) failed: Over-writing cause	Shenandoah GC使用時に、ヒープダンプのjcmdテストがGC発生理由に関するアサーションで時折失敗する問題を修正します。
JDK-8348942	P3	Backport	cpuset cgroups controller is required for no good reason	cgroupsのcpusetコントローラが、本来不要な場面で必須と判定されてしまう問題を修正し、コンテナ環境での柔軟性を向上させます。
JDK-8350001	P3	Backport	[ubsan] adjustments to filemap.cpp and virtualspace.cpp for macOS aarch64	macOS aarch64環境で、UBSanが検知したファイルマッピングおよび仮想空間管理コードの未定義動作を修正します。
JDK-8345494	P4	Backport	JitTester: Implement temporary folder functionality	JITコンパイラのテストフレームワークに、一時フォルダを扱う機能を追加します。
JDK-8345495	P4	Backport	Add counting leading/trailing zero tests for Integer	Integerクラスの先頭/末尾ゼロのビット数を数えるメソッドに関するテストを追加します。
JDK-8345508	P4	Backport	PPC64: C1 unwind_handler fails to unlock synchronized methods with LM_MONITOR	PPC64アーキテクチャで、C1コンパイラが生成したコードの例外ハンドラが、特定の同期メソッドのロックを解除し損なう問題を修正します。
JDK-8345771	P4	Backport	PPC64: ObjectMonitor::_owner should be reset unconditionally in nmethod unlocking	PPC64アーキテクチャで、コンパイル済みコード内のロック解除処理において、モニタの所有者情報を無条件でリセットするように修正します。
JDK-8345866	P4	Backport	jdk/jfr/startupargs/TestStartDuration.java should be marked as flagless	JFRの起動時間に関するテストが、VMフラグなしで実行可能であることを示すようにメタデータを更新します。
JDK-8345914	P4	Backport	Misc crash dump improvements on more platforms after JDK-8294160	以前の改善（JDK-8294160）を他のプラットフォームにも展開し、JVMクラッシュ時のダンプ情報の品質を向上させます。
JDK-8345915	P4	Backport	Cleanup os::print_tos_pc on AIX	AIXプラットフォーム固有のクラッシュダンプ出力コードをクリーンアップします。
JDK-8345983	P4	Backport	CompileBroker::possibly_add_compiler_threads excessively polls available memory	コンパイラスレッドを追加する際に、利用可能なメモリを過度にポーリングしてパフォーマンスに影響を与える問題を修正します。
JDK-8346001	P4	Backport	DSO created with -ffast-math breaks Java floating-point arithmetic	-ffast-mathオプションでコンパイルされたネイティブライブラリをロードすると、Javaの浮動小数点演算の精度が破壊される問題を修正します。
JDK-8346021	P4	Backport	[REDO] Implement C2 VectorizedHashCode on AArch64	AArch64アーキテクチャ向けに、System.identityHashCodeのベクトル化（SuperWord）実装を再導入します。
JDK-8346075	P4	Backport	jcmd: Compiler.CodeHeap_Analytics cmd does not inform about missing aggregate	jcmd Compiler.CodeHeap_Analyticsコマンドが、必要なデータがない場合にその旨を通知しない問題を修正します。
JDK-8346108	P4	Bug	[21u][BACKOUT] 8337994: [REDO] Native memory leak when not recording any events	JFRのネイティブメモリリーク修正（JDK-8337994）が、他のテストでリグレッションを引き起こしたため、一時的に取り消します。
JDK-8346155	P4	Backport	jdk/jfr/event/gc/stacktrace/TestParallelMarkSweepAllocationPendingStackTrace.java failed with "OutOfMemoryError: GC overhead limit exceeded"	JFRのGCイベントテストが、GCオーバーヘッドによるOutOfMemoryErrorで失敗する問題を修正します。
JDK-8346191	P4	Backport	Check return value of hcreate_r	ネイティブコード内でhcreate_r関数の戻り値をチェックし、エラーハンドリングを改善します。
JDK-8346286	P4	Backport	Disable unstable check of ThreadsListHandle.sanity_vm ThreadList values	ThreadsListHandleの不安定なサニティチェックを無効にし、デバッグビルドでの不要なアサーション失敗を回避します。
JDK-8346403	P4	Backport	pthread_attr_init handle return value and destroy pthread_attr_t object	pthread_attr_initの戻り値を適切にチェックし、使用後にpthread_attr_tオブジェクトを破棄することで、リソースリークを防ぎます。
JDK-8346413	P4	Backport	Redo fix for JDK-8284620	CodeBufferが_overflow_arenaをリークする可能性があった問題（JDK-8284620）を再度修正します。
JDK-8346578	P4	Backport	SA core file support is broken on macosx-x64 starting with macOS 12.x	macOS 12以降で、Serviceability Agent（SA）によるコアファイルの解析機能が壊れていた問題を修正します。
JDK-8346647	P4	Backport	The libjsig deprecation warning should go to stderr not stdout	非推奨のlibjsigライブラリに関する警告メッセージが、標準出力ではなく標準エラー出力に表示されるように修正します。
JDK-8346808	P4	Backport	Add jtreg test for large arrayCopy disjoint case.	System.arraycopyの巨大な非重複配列コピーに関するテストを追加します。
JDK-8346809	P4	Backport	C2 SuperWord: some additional PopulateIndex tests	C2コンパイラのSuperWord最適化に関するインデックス生成のテストケースを追加します。
JDK-8346842	P4	Backport	vmTestbase/nsk/stress/strace/strace015.java failed with 'Cannot read the array length because "" is null'	スタックトレースのストレステストがヌルポインタ例外で失敗する問題を修正します。
JDK-8347440	P4	Backport	Use google test string comparison macros	HotSpotのgtestで、文字列比較に標準のマクロを使用するように統一します。
JDK-8347579	P4	Backport	[TESTBUG] Jtreg compiler/loopopts/superword/TestDependencyOffsets.java fails on 512-bit SVE	512-bit SVEを搭載したAArch64環境で、SuperWord最適化のテストが失敗する問題を修正リストに追加します。
JDK-8347584	P4	Backport	Improve heap walking API tests to verify correctness of field indexes	ヒープウォーキングAPIのテストを改善し、フィールドインデックスの正確性を検証するようにします。
JDK-8347592	P4	Backport	Normalize Random usage by incubator vector tests	Vector APIのテストにおけるRandomクラスの使用方法を正規化し、再現性を高めます。
JDK-8347593	P4	Backport	compiler/codecache/CheckSegmentedCodeCache.java fails	セグメント化されたコードキャッシュのチェックテストが失敗する問題を修正します。
JDK-8348058	P4	Backport	com/sun/tools/attach/BasicTests.java does not verify AgentLoadException case	Attach APIの基本テストが、エージェントロード時の例外ケースを検証していなかった点を改善します。
JDK-8348061	P4	Backport	Remove all code for nsk.share.Log verbose mode	テストライブラリnsk.share.Logから、現在は使用されていない冗長モードのコードを削除します。
JDK-8348329	P4	Backport	test_nmt_locationprinting.cpp broken in the gcc windows build	Windows上でGCCを使用してビルドした場合に、NMT（Native Memory Tracking）のテストが壊れる問題を修正します。
JDK-8348395	P4	Backport	Epsilon: Demote heap size and AlwaysPreTouch warnings to info level	Epsilon GC使用時のヒープサイズやAlwaysPreTouchに関する警告を、情報レベルのログに格下げします。
JDK-8348946	P4	Backport	GTest needs larger combination limit	GTestフレームワークで、組み合わせテストの上限値を引き上げます。
JDK-8348952	P4	Backport	ASAN reports use-after-free in DirectivesParserTest.empty_object_vm	AddressSanitizer (ASAN) が、コンパイラ指示子パーサーのテストで解放済みメモリへのアクセスを検出した問題を修正します。
JDK-8349045	P4	Backport	java/util/zip/EntryCount64k.java failing with java.lang.RuntimeException: '\A\Z' missing from stderr	64k以上のエントリを持つZIPファイルのテストが、標準エラー出力の期待値と一致せずに失敗する問題を修正します。
JDK-8349430	P4	Backport	Two CDS tests fail with -UseCompressedOops and UseSerialGC/UseParallelGC	圧縮オブジェクトポインタを有効にし、シリアルGCまたはパラレルGCを使用した場合に、2つのCDSテストが失敗する問題を修正します。
JDK-8349453	P4	Backport	[AIX] Beginning with AIX 7.3 TL1 mmap() supports 64K memory pages	AIX 7.3 TL1以降でmmap()が64Kページをサポートするようになったことに対応し、ラージページ機能の互換性を向上させます。
JDK-8349640	P4	Backport	Update failure handler to don't generate Error message if cores actions are empty	JVMクラッシュ時のfailure handlerが、コアアクションが空の場合にエラーメッセージを生成しないように修正します。
JDK-8349856	P4	Backport	[testsuite] NeverActAsServerClassMachine breaks TestPLABAdaptToMinTLABSize.java TestPinnedHumongousFragmentation.java TestPinnedObjectContents.java	特定のテスト設定フラグが、いくつかのGCテストを破壊する問題を修正します。
JDK-8349983	P4	Backport	AArch64: Build failure with clang due to -Wformat-nonliteral warning	AArch64環境でclangを使用してビルドする際に、フォーマット文字列に関する警告がエラーとして扱われビルドが失敗する問題を修正します。
JDK-8350002	P4	Backport	[ubsan] logSelection.cpp:154:24 / logSelectionList.cpp:72:94 : runtime error: applying non-zero offset 1 to null pointer	UBSanがログ選択コードでヌルポインタへのオフセット適用を検出した問題を修正します。
JDK-8350191	P4	Backport	Linux ppc64le with toolchain clang - detection failure in early JVM startup	Linux ppc64le環境でclangツールチェーンを使用した場合に、JVM起動の早い段階でCPU機能の検出に失敗する問題を修正します。
JDK-8350291	P4	Backport	Virtual Threads: exclude 2 tests	仮想スレッドに関連する不安定なテストを2つ、一時的に実行対象から除外します。
JDK-8350311	P4	Backport	[ubsan] logOutput.cpp:357:21: runtime error: applying non-zero offset 1 to null pointer	UBSanがログ出力コードでヌルポインタへのオフセット適用を検出した問題を修正します。
JDK-8350527	P4	Backport	gc/TestDisableExplicitGC.java fails due to unexpected CodeCache GC	System.gc()を無効化するテストが、予期しないコードキャッシュのGCにより失敗する問題を修正します。
JDK-8350528	P4	Backport	Add more linesize for MIME decoder in macro bench test Base64Decode	Base64デコードのマイクロベンチマークテストに、より多くの行サイズのテストケースを追加します。
JDK-8350658	P4	Backport	Adjust exception No type named in database	Serviceability Agentで「データベースに指定された名前の型がない」という例外メッセージを調整します。
JDK-8349432	P5	Backport	failure_handler should execute gdb "info threads" command on linux	Linux上でJVMがクラッシュした際に、failure handlerがgdbのinfo threadsコマンドを実行して、より詳細なデバッグ情報を収集するように改善します。

3.4. Security Libraries ()

security-libsコンポーネントは、JSSE (SSL/TLS)、JAAS (認証・認可)、JCE (暗号化)、公開鍵基盤 (PKI) など、Javaプラットフォームのセキュリティ機能全般を担当します。このリリースでは、証明書の失効ポリシー更新、PKCS#11プロバイダの安定性向上、および証明書検証ロジックの修正が含まれています。

JDK ID	優先度	タイプ	タイトル	概要
JDK-8348066	P2	Backport	test/jdk/sun/security/x509/DNSName/LeadingPeriod.java validity check failed	DNS名制約を含むX.509証明書の検証テストが、先頭にピリオドがある場合に失敗する問題を修正します。
JDK-8345708	P3	Backport	Test sun/security/validator/samedn.sh CertificateNotYetValidException: NotBefore validation	証明書の有効期間開始前（NotBefore）の検証テストが、CertificateNotYetValidExceptionで失敗する問題を修正します。
JDK-8345884	P3	Backport	SunPKCS11 provider checks on PKCS11 Mechanism are problematic	SunPKCS11プロバイダが、サポートされている暗号メカニズムをチェックする際のロジックに問題があり、一部のHSMデバイスとの互換性に影響を与えていた点を修正します。
JDK-8346636	P3	Backport	Test sun/security/pkcs11/Provider/RequiredMechCheck.java needs write access to src tree	PKCS#11プロバイダのテストが、ソースツリーへの書き込みアクセスを不適切に要求する問題を修正します。
JDK-8346813	P3	Backport	SunPKCS11 initialization will call C_GetMechanismInfo on unsupported mechanisms	SunPKCS11プロバイダの初期化時に、サポートされていないメカニズムに対してもC_GetMechanismInfoを呼び出してしまい、一部のHSMでエラーを引き起こす問題を修正します。
JDK-8346817	P3	Backport	Google CAInterop test failures	Googleのルート証明書との相互運用性テストが失敗する問題を修正します。
JDK-8348065	P3	Backport	Certificate name constraints improperly validated with leading period	証明書のDNS名制약の検証において、先頭にピリオド（.）を持つドメイン名が不適切に扱われる問題を修正します。
JDK-8349870	P3	Backport	Distrust TLS server certificates anchored by Camerfirma Root CAs	セキュリティポリシーを更新し、Camerfirma社のルートCAによって署名されたTLSサーバー証明書を信頼しないように変更します。
JDK-8354709	P3	Backport	Jarsigner should print a warning if an entry is removed	jarsignerツールがJARファイルからエントリを削除した場合に、警告メッセージを出力するように改善します。
JDK-8345709	P4	Backport	Logs truncated in test javax/net/ssl/DTLS/DTLSRehandshakeTest.java	DTLSの再ハンドシェイクテストで、ログが切り捨てられてしまいデバッグが困難になる問題を修正します。
JDK-8346421	P4	Backport	Update PKCS#11 Cryptographic Token Interface to v3.1	PKCS#11暗号トークンインターフェースのサポートをv3.1仕様に更新します。
JDK-8346634	P4	Backport	test/jdk/sun/security/tools/jarsigner/PreserveRawManifestEntryAndDigest.java can fail due to regex	jarsignerのテストが、正規表現のマッチングに失敗して不安定になる問題を修正します。
JDK-8348067	P4	Backport	Fix and rewrite sun/security/x509/DNSName/LeadingPeriod.java test	先頭ピリオドを持つDNS名の証明書検証テストを修正し、より信頼性の高いものに書き直します。
JDK-8349986	P4	Backport	Serialization considerations	セキュリティコンポーネントにおけるシリアライゼーションの考慮事項をレビューし、安全性を向上させます。
JDK-8350671	P4	Backport	Test javax/net/ssl/SSLSocket/Tls13PacketSize.java failed with java.net.SocketException: An established connection was aborted by the software in your host machine	TLS 1.3のパケットサイズに関するテストが、SocketExceptionで失敗する問題を修正します。
JDK-8343928	P5	Backport	Fix typo of property name in TestOAEPPadding after 8341927	OAEPパディングのテストで、プロパティ名のタイポを修正します。
JDK-8340779	P5	Backport	Test com/sun/crypto/provider/Cipher/DES/PerformanceTest.java fails with java.lang.ArithmeticException	DES暗号のパフォーマンステストが、ゼロ除算によるArithmeticExceptionで失敗する問題を修正します。

3.5. Tools ()

toolsコンポーネントには、javac（コンパイラ）、javadoc（ドキュメンテーションツール）、jpackage（パッケージングツール）、jshell（対話型評価ツール）などの開発ツールが含まれます。このリリースでは、JVMクラッシュの修正や、ツールの安定性向上に関する改善が行われています。

JDK ID	優先度	タイプ	タイトル	概要
JDK-8348341	P2	Backport	Crash: SIGSEGV in dlerror()	特定の条件下で共有ライブラリのエラー処理関数dlerror()を呼び出すと、セグメンテーションフォールトでツールがクラッシュする問題を修正します。
JDK-8346079	P3	Backport	Consolidate EmptyFolderTest and EmptyFolderPackageTest jpackage tests into single java file	jpackageツールの空フォルダに関する2つのテストを、1つのJavaファイルに統合し、メンテナンス性を向上させます。
JDK-8346699	P3	Backport	Incorrect format string after JDK-8339475	以前の修正（JDK-8339475）で導入された、ネイティブコードのフォーマット文字列の誤りを修正します。
JDK-8346815	P3	Backport	Test BasicTest.java javac compile fails cannot find symbol	BasicTest.javaというテストファイルのコンパイルが、シンボル未解決で失敗する問題を修正します。
JDK-8346077	P4	Backport	test/jdk/tools/jpackage/share/ServiceTest.java test fails	jpackageで作成されたWindowsサービスに関するテストが失敗する問題を修正します。
JDK-8346078	P4	Backport	Remove --compress from jlink command lines from jpackage tests	jpackageのテストで使用されているjlinkコマンドから、現在は非推奨の--compressオプションを削除します。
JDK-8346187	P4	Backport	tools/jpackage/windows/Win8282351Test.java fails with java.lang.AssertionError: Expected [0]. Actual [1618]:	jpackageのWindows向けテストが、予期しない終了コードでアサーションエラーとなる問題を修正します。
JDK-8346428	P4	Backport	Move common properties from jpackage jtreg test declarations to TEST.properties file	jpackageのjtregテストで共通して使用されるプロパティを、個別のテスト宣言から共通のTEST.propertiesファイルに移動させます。
JDK-8346577	P4	Backport	tools/jpackage/windows/Win8301247Test.java fails on localized Windows platform	ローカライズされたWindows環境で、jpackageのテストが失敗する問題を修正します。
JDK-8346698	P4	Backport	Clean up return code handling for pthread calls in library coding	ライブラリコード内のpthread呼び出しにおける戻り値のハンドリングをクリーンアップし、堅牢性を向上させます。
JDK-8346814	P4	Backport	Rework BasicTest.testTemp test cases	BasicTestの一時ファイルに関するテストケースを再設計し、信頼性を向上させます。
JDK-8346857	P4	Backport	jpackage test helper function incorrectly removes a directory instead of its contents only	jpackageのテストヘルパー関数が、ディレクトリの内容だけでなくディレクトリ自体を誤って削除してしまう問題を修正します。
JDK-8347012	P4	Backport	Move jpackage tests from "jdk.jpackage.tests" package to the default package	jpackageのテストを、名前付きパッケージからデフォルトパッケージに移動させます。
JDK-8347100	P4	Backport	Use OperatingSystem, Architecture, and OSVersion in jpackage tests	jpackageのテストで、OS、アーキテクチャ、OSバージョンを判定するためのユーティリティを使用するように改善します。
JDK-8347317	P4	Backport	Improve test coverage for class loading elements with annotations of different retentions	異なるリテンションポリシーを持つアノテーションが付与されたクラス要素のロードに関するテストカバレッジを向上させます。
JDK-8347580	P4	Backport	jpackage tests run osx-specific checks on windows and linux	jpackageのテストが、WindowsやLinux環境でmacOS固有のチェックを誤って実行する問題を修正します。
JDK-8347583	P4	Backport	RuntimePackageTest.testUsrInstallDir test fails on Linux	Linux環境で、jpackageのインストール先ディレクトリに関するテストが失敗する問題を修正します。
JDK-8347644	P4	Backport	Remove unused imports from ModuleGenerator test file	モジュール生成器のテストファイルから、未使用のimport文を削除します。
JDK-8347877	P4	Backport	With malformed --app-image the error messages are awful	jpackageで不正な--app-imageオプションが指定された際のエラーメッセージが分かりにくい問題を改善します。
JDK-8349996	P4	Backport	BasicAnnoTests doesn't handle multiple annotations at the same position	アノテーションの基本テストが、同じ位置に複数のアノテーションが存在するケースを正しく扱えない問題を修正します。
JDK-8350568	P4	Backport	Upgrade JLine to 3.26.1	jshellが内部で使用しているJLineライブラリをバージョン3.26.1にアップグレードします。
JDK-8354710	P4	Backport	Clean up the code in sun.tools.jar.Main to properly close resources and use ZipFile during extract	jarツールのメインクラスをリファクタリングし、リソースが適切にクローズされるように修正します。

3.6. Infrastructure ()

infrastructureコンポーネントは、OpenJDKのビルドシステム、テストハーネス、継続的インテグレーション（CI）パイプラインなど、開発とテストを支える基盤に関連する改善を対象とします。

JDK ID	優先度	タイプ	タイトル	概要
JDK-8347176	P3	Backport	Compile tests with the same visibility rules as product code	テストコードを、製品コードと同じシンボル可視性ルールでコンパイルするようにビルド設定を修正します。
JDK-8349729	P3	Bug	[21u] AIX jtreg tests fail to compile with qvisibility=hidden	AIX環境で、-qvisibility=hiddenオプションを付けてjtregのネイティブテストをコンパイルすると失敗する問題を修正します。
JDK-8345370	P4	Enhancement	Bump update version for OpenJDK: jdk-21.0.7	バージョン文字列を次期アップデートリリースである21.0.7に更新します。
JDK-8346266	P4	Backport	[macos] [build]: install-file macro may run into permission denied error	macOSのビルドプロセスで、ファイルのインストールマクロがパーミッションエラーで失敗する可能性がある問題を修正します。
JDK-8346267	P4	Backport	Make target mac-jdk-bundle fails on chmod command	macOSでJDKバンドルを作成するmakeターゲットが、chmodコマンドで失敗する問題を修正します。
JDK-8346617	P4	Backport	GHA: Collect hs_errs from build time failures	GitHub Actions (GHA) のCIワークフローを改善し、テスト実行時だけでなくビルド時のJVMクラッシュ（hs_err）ファイルも収集するようにします。
JDK-8346618	P4	Backport	GHA: Report truncation is broken after JDK-8341424	GHAのレポート切り捨て機能が、以前の修正（JDK-8341424）後に壊れていた問題を修正します。
JDK-8347403	P4	Backport	GHA: Build JTReg in single step	GHAワークフローで、JTRegのビルドを単一ステップで実行するように効率化します。
JDK-8349426	P4	Backport	Timeout handler on Windows takes 2 hours to complete	Windows環境のテストで、タイムアウトハンドラの処理が完了するまでに最大2時間かかることがあるパフォーマンス問題を修正します。
JDK-8349603	P4	Bug	[21u, 17u, 11u] Update GHA JDKs after Jan/25 updates	GitHub Actions (GHA) のCI/CDワークフローで使用するJDKのバージョンを、2025年1月アップデート後の最新版に更新します。
JDK-8353904	P4	Bug	[21u] Remove designator DEFAULT_PROMOTED_VERSION_PRE=ea for release 21.0.7	GAリリースに向けて、バージョン文字列から早期アクセス（ea）の識別子を削除します。

これらの詳細なリストは、開発者や管理者が特定の機能領域における変更点を深く理解し、システムへの影響を評価するためのものです。

4. 結論

OpenJDK 21.0.7+6は、JDK 21プラットフォームの成熟度と信頼性をさらに高めるための、重要なメンテナンスリリースです。本リリースでは、HotSpot VMのクラッシュ修正から、コアライブラリの安定性向上、セキュリティポリシーの更新、クライアントライブラリの互換性改善まで、広範なコンポーネントにわたる多数のバグ修正と改善が提供されています。これらの変更は、Javaアプリケーションの安定稼働とセキュリティ維持に直接的に貢献します。すべてのJDK 21ユーザーに対して、最新のセキュリティパッチと安定性の向上を活用するために、このバージョンへのアップグレードを強く推奨します。
