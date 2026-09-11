# 构建配方（版本钉）

> 从 install-ledger 抽出的「可移植」构建事实，供云端沙箱与任何新机器使用。机器路径、环境开关等不可移植部分留在本地 `docs/install-ledger.md`（不入库）。
>
> **云端写作纪律**：版本一个字符不许改；只交付源码文件；禁止执行 gradle / 构建 / 模拟器；不生成 gradle-wrapper.jar 与 local.properties。

## 版本钉（2026-09-12 已在 hello-android 工程实测打出 APK）

| 项 | 值 |
|---|---|
| JDK | 17（Temurin） |
| Gradle | 8.13 |
| AGP | com.android.application 8.13.2 |
| Kotlin 插件 | org.jetbrains.kotlin.android 2.2.0 |
| compileSdk / buildTools / targetSdk | 36 / 36.0.0 / 36 |
| minSdk | 24 |
| GeckoView | org.mozilla.geckoview:geckoview:155.0.20260903215306（只存在于 https://maven.mozilla.org/maven2/ ，settings.gradle 的 dependencyResolutionManagement 必须声明此源） |
| 构建脚本 | Groovy DSL（.gradle 文件） |

## 本机构建与验收（issue 验收标准：一条命令出 APK）

```bat
call D:\Dev\env.bat
cd /d D:\w\安卓
gradle assembleDebug
adb install app\build\outputs\apk\debug\app-debug.apk
```

`call D:\Dev\env.bat` 是本机专用唤醒（JDK/SDK/Gradle/git 进 PATH）；GeckoView AAR 首次构建约下载 200MB，走本机流量，不占 AI 配额。
