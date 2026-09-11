# NEXT.md — 交接与下一步（给下一个会话的 agent）

> 开工前必读（配合 AGENTS.md 与 docs/install-ledger.md）。本文件是接力棒：每完成一个阶段，agent 必须更新它。

## 项目一句话

AI 分身浏览器（GeckoView 原生安卓 App）：多账号使用网页版 AI 网站。Spec=issue #1，术语表=`CONTEXT.md`，决策=`docs/adr/0001~0005`，环境台账=`docs/install-ledger.md`，构建版本钉=`docs/build-recipe.md`。

## 工作方式（ADR 0005，2026-09-12 起）

代码写作在 **Z.ai 网页版沙箱（GLM-5.3）** 完成（省配额），经 Git 回流；本机只做 **构建 + 模拟器验证 + 技能流程**。仓库（origin: jiushiniubi123/ai-fenshen-browser，clone=D:\w\安卓，仓库根=Gradle 工程根）是唯一事实源。

## 当前状态快照（2026-09-12）

| 事项 | 状态 |
|---|---|
| 构建链路（JDK17+SDK+Gradle，`D:\Dev`） | ✅ 全通，测试工程已出 APK |
| 项目记忆上云 | ✅ 约定/术语表/ADR/构建配方/NEXT 已首推入 GitHub 仓库 |
| android-emulator 插件 | ✅ 已写入启用配置（api_level=35 / AVD aifenshen / sdk=D:\Dev\android-sdk），**等用户重启 ZCode 生效**，生效标志=出现 `mcp__android_emulator__*` 工具 |
| 模拟器 + android-35 镜像 + AVD aifenshen | ⏳ 后台安装中（脚本 `D:\Dev\setup\install-emulator.bat`，日志同目录；脚本曾因 LF 行尾损坏，已重写修复） |
| BIOS SVM（AMD 虚拟化） | ❌ 未开 —— **唯一必须用户亲手做的步骤**（向导 `.scratch\enable-svm.ps1` 跑两次） |
| Issue 队列 | #3~#13 共 11 个待做；顺序 #3→#4→#5→#7→#8→#9→#10/#11→#12→#13 |

## 用户侧待办（不会编程，指令必须是复制粘贴级）

1. **Win + R** 粘贴运行两次向导 `.scratch\enable-svm.ps1`：第一次跟它进 BIOS 开 SVM（OC → Advanced CPU Configuration → SVM Mode → Enabled → F10），回来再跑一次自动验证
2. 重启 ZCode（让 android-emulator 插件生效）

## 下一步队列（agent 照此执行）

1. **issue #3 云端写作**：用户把 `.scratch/issue3-sandbox-brief.md` 任务书粘贴到 Z.ai 网页版（agent 模式，只写代码不跑构建）→ 下载代码 zip 交给 agent → agent 解压进 `D:\w\安卓`（仓库根）→ git commit + push
2. **本机验证**：`call D:\Dev\env.bat` → `gradle assembleDebug` → android-emulator 插件装到 AVD aifenshen 截图验证；SVM 未开时可临时 adb 装真机由用户人工验收（模拟器仍是自动验证正路）
3. 收尾：善后纪律五连 → 提醒用户 `/clear` → 领下一个 issue

### 提示词（用户直接粘贴）

**A · 云端写作（贴到 Z.ai 网页版）**：整段复制 `.scratch/issue3-sandbox-brief.md` 的内容；若沙箱能 clone 仓库，让它先读 CONTEXT.md 与 docs/adr/0003。

**B · 本机验收（贴到 ZCode 新会话）**：

```
读 D:\w\安卓\AGENTS.md 和 NEXT.md 对齐。然后：git pull；call D:\Dev\env.bat；gradle assembleDebug 打 APK；用 android-emulator 插件装到 AVD aifenshen 截图验证 issue #3（SVM 没开就 adb 装到我的真机让我人工看）。证据存 .scratch/issue-3/，收尾走善后五连，最后提醒我 /clear。
```

## Suggested skills

- `/code-review` —— issue 收尾 Standards+Spec 双轴审查（本机）
- `/diagnosing-bugs` —— 难缠 bug（先建紧反馈环）
- `/wizard` —— 只有用户本人能做的步骤
- android-dev 技能 + `mcp__android_emulator__*` —— 验证主力
- computer-use —— 模拟器窗口的兜底操作
- ⚠️ 云端沙箱（Z.ai 网页版）没有以上任何技能——那边只负责写代码

## 沟通红线

用户不会编程：给人做的每一步给"按哪个键/点哪个钮/粘贴哪条命令"级别；禁止让人改任何代码或配置文件；汇报先结论后原因，用大白话。
