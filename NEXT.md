# NEXT.md — 交接与下一步（给下一个会话的 agent）

> 开工前必读（配合 AGENTS.md 与 docs/install-ledger.md）。本文件是接力棒：每完成一个阶段，agent 必须更新它。

## 项目一句话

AI 分身浏览器（GeckoView 原生安卓 App）：多账号使用网页版 AI 网站。Spec=issue #1，术语表=`CONTEXT.md`，决策=`docs/adr/0001~0006`，环境台账=`docs/install-ledger.md`，构建版本钉=`docs/build-recipe.md`。

## 工作方式（ADR 0005/0006，2026-09-12 起）

代码写作在 **Z.ai 网页版沙箱（GLM-5.3）** 完成（省配额），沙箱凭一次性细粒度令牌直连仓库 clone→commit→push（ADR 0006）；本机只做 **构建 + 模拟器验证 + 技能流程**。仓库（origin: jiushiniubi123/ai-fenshen-browser，clone=D:\w\安卓，仓库根=Gradle 工程根）是唯一事实源。

## 当前状态快照（2026-09-12）

| 事项 | 状态 |
|---|---|
| 构建链路（JDK17+SDK+Gradle，`D:\Dev`） | ✅ 全通，测试工程已出 APK |
| 项目记忆上云 | ✅ 约定/术语表/ADR/构建配方/NEXT 已首推入 GitHub 仓库 |
| android-emulator 插件 | ✅ 已生效（2026-09-12 会话确认 `mcp__plugin_android-emulator__*` 工具可用） |
| 模拟器 + android-35 镜像 + AVD aifenshen | ✅ 已安装并核对文件齐全（2026-09-12 02:57，见台账）；首次真正开机在 issue #3 验证时确认 |
| BIOS SVM（AMD 虚拟化） | ✅ 已开启（2026-09-12，enable-svm.ps1 向导验证通过） |
| Issue 队列 | #3~#13 共 11 个待做；顺序 #3→#4→#5→#7→#8→#9→#10/#11→#12→#13 |

## 用户侧待办（不会编程，指令必须是复制粘贴级）

1. ✅ BIOS SVM 已开启、ZCode 已重启插件生效（2026-09-12 完成）
2. **签发一次性门禁卡（当前唯一待办）**：Win + R → 粘贴 `notepad D:\w\安卓\.scratch\github-token-guide.md` → 回车，照里面 9 步建好细粒度令牌并粘进任务书槽位，然后对 agent 说「令牌已就位」

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
