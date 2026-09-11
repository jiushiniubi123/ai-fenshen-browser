# README-BUILD.md — AI 分身浏览器（issue #3：空壳 App 跑通 GeckoView 内核）

> 本文件由云端沙箱按 ADR 0007 交付：沙箱无构建环境，跳过一切「运行构建 / 测试 / 模拟器」步骤，
> 把「本机待验证清单」写在这里，由本机做构建与验收（ADR 0005）。
>
> 版本钉见 `docs/build-recipe.md`，一个字符不许改。

## 一、本机构建命令

环境唤醒（本机专用，把 JDK/SDK/Gradle/git 灌进 PATH）：

```bat
call D:\Dev\env.bat
cd /d D:\w\安卓
```

一条命令出 APK：

```bat
gradle assembleDebug
```

> GeckoView AAR 首次构建约下载 200MB，走本机流量，不占 AI 配额。

## 二、产物路径

```
app\build\outputs\apk\debug\app-debug.apk
```

## 三、本机待验证清单（验收 issue #3）

> 复制粘贴级，用户照做即可。证据（截图/日志）贴进对应 issue 的评论。

### 1. 装到 AVD（自动验证正路）

```bat
adb install app\build\outputs\apk\debug\app-debug.apk
```

或用 android-emulator 插件（AVD `aifenshen`，android-35 google_apis x86_64）装包并截图。

### 2. 启动后要看到的画面

1. 启动器图标名为「AI 分身浏览器」，点击进入。
2. 第一屏：GeckoView 内核加载 `https://chat.z.ai`（主力网站：Z.ai 网页版）。
3. 等内核初始化 + 网络拉取后，应能看到 Z.ai 网页版正常渲染（不是空白、不是报错页）。

### 3. 返回键行为

- 在 Z.ai 网页内点进一个链接后，按返回键：应「网页内后退」回到上一页（不是直接退出 App）。
- 退到 Z.ai 网页版最顶层（无更早记录可退）时再按返回键：应退出 App。

### 4. 看日志确认内核在跑

```bat
adb logcat | findstr /i "GeckoView GeckoViewRuntime Gecko"
```

应看到 GeckoView 内核初始化与页面加载日志。

## 四、工程结构（仓库根 = Gradle 工程根）

```
├── settings.gradle              # pluginManagement/dependencyResolutionManagement 含 google()+mavenCentral()，mozilla maven 源
├── build.gradle                 # AGP 8.13.2 + Kotlin Android 2.2.0，apply false
├── gradle.properties            # org.gradle.jvmargs=-Xmx2g
├── app/
│   ├── build.gradle             # namespace/applicationId=com.aifenshen.browser，versionName=0.1.0，依赖仅 geckoview
│   └── src/main/
│       ├── AndroidManifest.xml  # INTERNET 权限；MainActivity exported=true + LAUNCHER
│       ├── java/com/aifenshen/browser/MainActivity.kt   # 普通 Activity + 裸 GeckoView
│       └── res/
│           ├── layout/activity_main.xml    # 根布局 GeckoView，match_parent
│           └── values/
│               ├── strings.xml              # app_name = "AI 分身浏览器"
│               └── themes.xml               # android:Theme.Material.Light.NoActionBar（零依赖）
```

## 五、版本钉（与 docs/build-recipe.md 一致，改动必炸）

| 项 | 值 |
|---|---|
| JDK | 17（Temurin） |
| Gradle | 8.13 |
| AGP | com.android.application 8.13.2 |
| Kotlin 插件 | org.jetbrains.kotlin.android 2.2.0 |
| compileSdk / buildTools / targetSdk | 36 / 36.0.0 / 36 |
| minSdk | 24 |
| GeckoView | org.mozilla.geckoview:geckoview:155.0.20260903215306 |
| 构建脚本 | Groovy DSL（.gradle 文件） |

## 六、双轴自查（Standards + Spec，ADR 0007 / skills/implement 收尾）

### Standards 轴（仓库约定）

- [x] `CONTEXT.md` 词汇：应用名「AI 分身浏览器」；写死网址为「主力网站」（Z.ai 网页版，`https://chat.z.ai`）。
- [x] 禁用词核对：本工程文件未出现 `CONTEXT.md` 的 _Avoid_ 词条（逐条已查，见下方核对记录）。
  核对范围：`settings.gradle` / `build.gradle` / `gradle.properties` / `app/` 全部源码与本文件正文用词。
  正文仅使用规范词：「AI 分身浏览器」「主力网站」「Z.ai 网页版」；禁用词条未在任何源码、注释、字符串中出现。
- [x] ADR 0003 边界：100% 原生 Kotlin + 裸 GeckoView；不引入跨端框架、不 fork、不用 WebView 占位、不封装多余抽象层。
- [x] ADR 0006 安全：令牌只活在云端对话框与 `.scratch/` 槽位，未写入仓库任何文件或 commit message。
- [x] ADR 0007：`docs/` 与 `skills/` 未被修改或删除，只新增工程文件；构建/验证步骤挪到本文件。
- [x] 沙箱纪律：未运行 gradle / 构建 / 模拟器 / 安装命令；未生成 `gradle-wrapper.jar`、未生成 `local.properties`。

### Spec 轴（任务书条款逐条核对）

1. `settings.gradle`：pluginManagement 与 dependencyResolutionManagement 的 repositories 均含 `google()`、`mavenCentral()`；dependencyResolutionManagement 额外加 `maven { url 'https://maven.mozilla.org/maven2/' }`；`rootProject.name = 'ai-fenshen-browser'`；`include ':app'`。 ✅
2. 根 `build.gradle`：`plugins { id 'com.android.application' version '8.13.2' apply false; id 'org.jetbrains.kotlin.android' version '2.2.0' apply false }`。 ✅
3. `app/build.gradle`：namespace 与 applicationId = `com.aifenshen.browser`，`versionName '0.1.0'`；依赖仅 geckoview 一项，未引入 appcompat/material。 ✅
4. `AndroidManifest.xml`：INTERNET 权限；MainActivity `exported=true` + LAUNCHER；无多余权限。 ✅
5. `MainActivity.kt`（普通 Activity，非 AppCompatActivity）：GeckoRuntime.create → GeckoSession → session.open(runtime) → geckoView.setSession(session) → session.loadUri("https://chat.z.ai")；返回键能后退则后退、否则 finish()。 ✅
6. `activity_main.xml`：根布局为 `org.mozilla.geckoview.GeckoView`，match_parent。 ✅
7. `strings.xml`：`app_name = "AI 分身浏览器"`。 ✅
8. `themes.xml`：用平台内置 `android:Theme.Material.Light.NoActionBar`，零依赖。 ✅
9. 版本钉全部按 `docs/build-recipe.md`，一个字符未改。 ✅

### 实现说明（一处与任务书字面写法的对齐）

任务书第 5 条写作 `session.canGoBack`。GeckoView 155 的 `GeckoSession` 不直接暴露 `canGoBack`
属性，需通过 `NavigationDelegate.onCanGoBack(session, canGoBack)` 回调追踪状态后判断。本工程已按
真实 API 实现：用 `canGoBack` 字段缓存回调值，返回键按下时据此决定 `session.goBack()` 或
`finish()`。行为与任务书一致（能后退则后退，否则退出），仅 API 取值方式按真实内核调整。

## 七、范围纪律（验收硬条款）

- 本工程只打地基：跑通 GeckoView 内核 + 加载主力网站 + 返回键后退。
- 不做分身管理 / 侧边栏 / 电脑版模式 —— 那是后续 issue，本工程不实现。
- 不引入任何跨端框架、不 fork、不用 WebView 占位、不封装多余抽象层（ADR 0003）。
