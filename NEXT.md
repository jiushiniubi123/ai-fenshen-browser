# NEXT.md — 交接与下一步（给下一个会话的 agent）

> 开工前必读（配合 AGENTS.md 与 docs/install-ledger.md）。本文件是接力棒：每完成一个阶段，agent 必须更新它。

## 项目一句话

AI 分身浏览器（GeckoView 原生安卓 App）：多账号使用网页版 AI 网站。Spec=issue #1，术语表=`CONTEXT.md`，决策=`docs/adr/0001~0008`，环境台账=`docs/install-ledger.md`，构建版本钉=`docs/build-recipe.md`。

## 工作方式（ADR 0005 / 0008，2026-09-12 起）

代码写作在 **Z.ai 网页版沙箱（GLM-5.3）** 完成（省配额），产物经 **zip 人工搬运**回流（ADR 0008）：本机 agent 打快照 zip → 用户上传到 Z.ai 对话框 → 云端只写代码、交回 zip → 用户下载交给 agent → agent 解压 + 白名单校验 + 提交推送。**云端不连 GitHub，流程里没有任何令牌。** 本机只做 **构建 + 模拟器验证 + 技能流程**。仓库（origin: jiushiniubi123/ai-fenshen-browser，clone=D:\w\安卓，仓库根=Gradle 工程根）是唯一事实源。云端写码照仓库内 `skills/` 技能库执行：先读 `skills/README.md`，写码按 `skills/implement/SKILL.md`（ADR 0007）。

## 当前状态快照（2026-09-12）

| 事项 | 状态 |
|---|---|
| 构建链路（JDK17+SDK+Gradle，`D:\Dev`） | ✅ 全通，测试工程已出 APK |
| 项目记忆上云 | ✅ 约定/术语表/ADR/构建配方/NEXT 已推入 GitHub 仓库 |
| android-emulator 插件 | ✅ 已生效（2026-09-12 会话确认 `mcp__plugin_android-emulator__*` 工具可用） |
| 模拟器 + android-35 镜像 + AVD aifenshen | ✅ 已安装并核对文件齐全（2026-09-12 02:57，见台账）；首次真正开机在 issue #3 验证时确认 |
| BIOS SVM（AMD 虚拟化） | ✅ 已开启（2026-09-12，enable-svm.ps1 向导验证通过） |
| Issue 队列 | #3~#13 共 11 个待做；顺序 #3→#4→#5→#7→#8→#9→#10/#11→#12→#13 |
| matt skills 入库（`skills/`，30 个，ADR 0007） | ✅ 2026-09-12 已推送；快照 zip 会带上整个 `skills/`，云端照 SKILL.md 手册执行，本机负责同步与执行环节 |
| 云端交接方式（ADR 0008） | ✅ 2026-09-12 改为 zip 人工搬运：云端不再对接 GitHub，流程零令牌；打包脚本 `.scratch/make-upload-zip.py` 就绪，`issue3-upload.zip` 已生成待上传 |
| 旧万能令牌（ADR 0006 遗留） | ⚠️ 已作废，**待在 GitHub 后台吊销**（见用户侧待办 2） |
| issue #3 云端代码（`app/` 模块） | ⚠️ 上一轮云端报错后按用户要求已从仓库删除（commit 0217c94，2026-09-12）；代码未丢，恢复一条命令：`git checkout 734f338 -- app`。改用 zip 流程后重跑一遍即可 |

## 用户侧待办（不会编程，指令必须是复制粘贴级）

1. ✅ BIOS SVM 已开启、ZCode 已重启插件生效（2026-09-12）
2. **吊销旧万能令牌**（安全项，建议先做）：打开 https://github.com/settings/tokens → 找到那个 classic token → 点它右边的 `Delete` → 弹窗点 `I understand, delete this token`。**令牌已作废、之后不再用到，删掉只是把风险清零。** 删完回来对 agent 说「令牌删好了」。
3. **开始 issue #3 的 zip 流程**：按下面「提示词 A」操作——把 `.scratch/upload/issue3-upload.zip` 拖进 Z.ai 对话框，再粘贴那段短提示词。
4. **云端写完后**：把云端给的 zip 下载下来，放进 `D:\w\安卓\.scratch\download\`（没有这个文件夹就新建），然后对 agent 说「云端写完了，zip 在 .scratch/download」。**不用解压，agent 会自己解。**

> 附：上一次云端报的错误原文如果还在，可以一并贴给 agent 判断——不过那轮报错很可能就是 Git/推送相关的，换成 zip 流程后大概率不再出现。

## 下一步队列（agent 照此执行）

1. **issue #3 云端写作（zip 流程）**：确认 `.scratch/upload/issue3-upload.zip` 是最新快照（本机有新提交就重跑 `.scratch/make-upload-zip.py 3`）→ 用户上传 zip + 粘提示词 A → 用户把云端 zip 放进 `.scratch/download/` → agent 解压进 `D:\w\安卓` → **白名单校验**（只许新增/覆盖 `app/**`、`settings.gradle`、`build.gradle`、`gradle.properties`、`README-BUILD.md`、`.gitignore`；`docs/`、`skills/`、`AGENTS.md`、`CLAUDE.md`、`CONTEXT.md`、`NEXT.md` 被改动即拒收并回报用户）→ git commit + push
2. **本机验证**：`call D:\Dev\env.bat` → `gradle assembleDebug` → android-emulator 插件装到 AVD aifenshen 截图验证；SVM 未开时可临时 adb 装真机由用户人工验收（模拟器仍是自动验证正路）
3. 收尾：善后纪律五连 → 提醒用户 `/clear` → 领下一个 issue

### 提示词（用户直接粘贴）

**A · 云端写作（贴到 Z.ai 网页版，与 `.scratch/upload/issue3-upload.zip` 一起发）**：

```
先解压我上传的 zip。读里面的 TASK.md（任务书），按它执行。
CONTEXT.md 是术语表，skills/README.md 与 skills/implement/SKILL.md 是操作手册，docs/ 是决策记录。

沙箱没有 Android 构建环境：只写代码文件，不要运行 gradle、不要构建、不要开模拟器，
也不要联网 clone 或推送任何仓库（本流程不使用 GitHub）。

写完后把产物文件打包成 zip 给我下载。
```

**B · 本机验收（贴到 ZCode 新会话）**：

```
读 D:\w\安卓\AGENTS.md 和 NEXT.md 对齐。然后：git pull；call D:\Dev\env.bat；gradle assembleDebug 打 APK；用 android-emulator 插件装到 AVD aifenshen 截图验证 issue #3（SVM 没开就 adb 装到我的真机让我人工看）。证据存 .scratch/issue-3/，收尾走善后五连，最后提醒我 /clear。
```

## 打上传包（agent 用）

```bat
call D:\Dev\env.bat
cd /d D:\w\安卓
python .scratch\make-upload-zip.py 3
```

产物：`.scratch/upload/issue3-upload.zip`（仓库 tracked 快照 + `TASK.md`）。脚本走 `git ls-files`，自动排除 `docs/install-ledger.md`、`.scratch/` 等不入库内容，也永远不含令牌。

## Suggested skills

- `/code-review` —— issue 收尾 Standards+Spec 双轴审查（本机）
- `/diagnosing-bugs` —— 难缠 bug（先建紧反馈环）
- `/wizard` —— 只有用户本人能做的步骤
- android-dev 技能 + `mcp__android_emulator__*` —— 验证主力
- computer-use —— 模拟器窗口的兜底操作
- ⚠️ 云端沙箱没有技能运行时，但快照 zip 里带着整个 `skills/`（ADR 0007），云端可读 SKILL.md 当手册；自动触发与执行环节仍只在本机

## 沟通红线

用户不会编程：给人做的每一步给"按哪个键/点哪个钮/粘贴哪条命令"级别；禁止让人改任何代码或配置文件；汇报先结论后原因，用大白话。
