# README-BUILD —— issue #3 本机构建与验收清单

> 云端沙箱没有构建环境（ADR 0005），本文件就是「本机待验证清单」：要跑什么命令、要看什么结果。
> 版本钉以 `docs/build-recipe.md` 为准：JDK 17 / Gradle 8.13 / AGP 8.13.2 / Kotlin Android 插件 2.2.0 /
> compileSdk 36 / buildTools 36.0.0 / targetSdk 36 / minSdk 24 / GeckoView 155.0.20260903215306。

## 一、这个工程是什么

- 仓库根 = Gradle 工程根（Groovy DSL；未生成 gradle-wrapper，用本机 Gradle 8.13 直接跑；无 local.properties）。
- 100% 原生 Kotlin + 裸 GeckoView（ADR 0003）：一个普通 Activity（不是 AppCompatActivity），
  打开 App 直接加载主力网站（Z.ai 网页版 `https://chat.z.ai`）。
- App 模块只声明一个依赖：`org.mozilla.geckoview:geckoview:155.0.20260903215306`
  （只存在于 `https://maven.mozilla.org/maven2/`，settings.gradle 已声明该源）。
- 本 issue 只打地基：不含分身管理、侧边栏、电脑版模式（后续 issue 的内容）。

## 二、云端已知的两个必要说明（本机如遇报错先看这里）

1. **gradle.properties 开了 `android.useAndroidX=true`**：这不是引 androidx 写码——App 自身代码
   零 androidx 引用（普通 Activity + 平台内置主题）。原因是 GeckoView 155 的官方 POM 自带
   androidx 传递依赖（core / lifecycle / media3 / play-services-fido 等，Mozilla 官方声明），
   AGP 8.13 在未开启该开关时会对其直接报错 `ANDROID_X_PROPERTY_NOT_ENABLED`。云端已核实
   AGP 8.13.2 字节码与 GeckoView 155 POM，此开关是钉死版本组合下的硬性要求。
2. **Java/Kotlin 字节码目标 = 17**：`compileOptions` 与 `kotlin { compilerOptions { } }` 成对
   设置（Kotlin 2.2.0 的现行写法），与本机 JDK 17（Temurin）一致。

## 三、构建（验收标准：一条命令出 APK）

Windows 本机，仓库 clone 于 `D:\w\安卓`：

```bat
call D:\Dev\env.bat
cd /d D:\w\安卓
git pull
gradle assembleDebug
```

- 产物路径：`app\build\outputs\apk\debug\app-debug.apk`
- GeckoView AAR 实测 241,244,587 字节（约 230MB），首次构建下载走本机流量，属预期，请耐心等待。

## 四、安装与验证

正路（AGENTS.md 固定路线）：android-emulator 插件 + AVD `aifenshen` 安装并截图验证。
备用（插件不可用才降级）：adb 安装；`adb devices` 先确认列表里只有模拟器（iQOO 真机不做
自动验证靶机，只留给用户人工验收）：

```bat
adb devices
adb install -r app\build\outputs\apk\debug\app-debug.apk
```

### 验收清单（要看什么）

1. 应用列表出现「AI 分身浏览器」，图标为系统默认图标（本工程未配置图标，属预期）。
2. 打开 App 不崩溃，直接加载主力网站（Z.ai 网页版 `https://chat.z.ai`），页面可滚动、可点击。
3. 在网页内点开若干链接后按系统返回键：先在网页内逐级后退；退无可退时再按一次，退出 App。
4. 旋转屏幕 App 不崩溃（Activity 重建后重新加载主力网站，空壳版本的预期行为）。
5. `adb logcat` 无 GeckoView 致命报错、无 ANR。

## 五、若构建失败

1. 先核对版本钉有没有被改动：`docs/build-recipe.md`。
2. 依赖解析失败 → 确认本机网络可达 `https://maven.mozilla.org/maven2/`。
3. 按 ADR 0005：云端只写代码、本机首次构建报错属预期流程——把完整报错原样贴回云端对话，
   等修复代码推回仓库后再验；本机不要手改代码。

## 六、本次新增文件清单（Code Review 对照用）

```
.gitignore                                          # 在原文件末尾纯追加：*.apk、*.keystore、*.jks 等（原有条目全部保留）
README-BUILD.md                                     # 本文件
settings.gradle
build.gradle
gradle.properties
app/build.gradle
app/src/main/AndroidManifest.xml
app/src/main/java/com/aifenshen/browser/MainActivity.kt
app/src/main/res/layout/activity_main.xml
app/src/main/res/values/strings.xml
app/src/main/res/values/themes.xml
```

未生成（按任务书约束）：gradle-wrapper.jar、local.properties。
未改动（按任务书约束）：docs/ 全部、skills/ 全部、AGENTS.md、CLAUDE.md、CONTEXT.md、NEXT.md。
