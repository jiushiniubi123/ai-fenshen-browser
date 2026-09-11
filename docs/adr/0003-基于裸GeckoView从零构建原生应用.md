# 0003 - 基于裸 GeckoView 从零构建原生应用

日期：2026-09-12 ｜ 状态：已接受

App 为 100% 原生安卓应用：技术底座选用 Mozilla 官方发布的 GeckoView 内核组件（Firefox for Android 同源），外壳从零编写，不基于现成浏览器源码改造、不用跨端框架。理由：三大核心能力（分身隔离、在线装插件、桌面模式）均已验证有 GeckoView 官方 API 直接支撑；用户明确要求原生安卓与简洁；改造 Fenix 需在几十万行代码中做减法，升级跟随困难。

## Considered Options

- **Fork Fenix**（Firefox for Android 源码）：功能全但臃肿，做减法成本高、升级难，被否。
- **跨端/网页套壳框架**（Flutter、Capacitor 等）：不满足"原生安卓"，也无法直接驱动 GeckoView，被否。

## Consequences

- 插件安装采用双通道：App 内接 AMO 在线安装（`WebExtensionController.install`）+ 本地导入 .xpi 文件备用。
- 构建走纯命令行（Windows + cmdline-tools + Gradle），不依赖 Android Studio。
