# 工作约定（每个会话必读必守）

> 本文件是项目规则的**唯一正本**（ZCode 工作区级指令，会话自动加载）。CLAUDE.md 是它的兼容副本。另：用户级个人记忆在 `C:\Users\A\.zcode\AGENTS.md`（所有项目通用），本文件只放本项目专属规则。

## 用户画像（最高优先级）

用户**不会编程**。因此：

- 一切需要人做的操作，给"复制粘贴级"指令：完整命令、按哪个键、点哪个按钮，绝不让人改代码或配置文件
- 能自动化的全部由 agent 亲手做；只有物理/人类步骤（BIOS、UAC 弹窗、插线）才交给用户
- 解释用大白话：先说结论再说原因，少用术语；用了术语要当场用类比解释

## 开工仪式（每个新会话第一步）

1. 读本文件 + `NEXT.md`（交接与下一步）+ `docs/install-ledger.md`（装了什么、装在哪）
2. 终端先执行 `call D:\Dev\env.bat` 再跑任何构建/adb/模拟器命令（JAVA_HOME、ANDROID_HOME、PATH 全在里面；系统环境变量未配置，全靠这个脚本）

## 善后纪律（每步完成必做，按序执行）

1. **装了什么、装在哪、怎么撤销** → 追加进 `docs/install-ledger.md`
2. **证据**（截图/日志/构建产物路径）→ 贴进对应 issue 的评论
3. **issue 收尾** → `gh issue close <n> -R jiushiniubi123/ai-fenshen-browser`；有新决策 → 补 ADR 到 `docs/adr/`
4. **临时文件** → 删除或移进 `.scratch/<issue>/` 归档
5. **提醒用户 `/clear`** 再开下一个 issue（省 GLM 配量，每 issue 一个干净会话）

## APP 验证（固定路线）

- 用 android-emulator 插件（工具名 `mcp__android_emulator__*`，技能名 android-dev）+ AVD `aifenshen`（android-35 google_apis x86_64）
- 用户真机（iQOO Z11 Turbo / iQOO Neo 8）**不进自动验证**，只留给用户做最终人工验收
- 插件不可用时才降级：adb 命令 + computer-use 技能操作模拟器窗口（备用，不是首选）

## GLM 配额纪律

- 配额优先花在写代码（/implement 各 issue）；验证靠插件工具 + 截图批量判读，不逐轮对话盯屏
- 机械步骤（环境安装、装包）用脚本后台跑，不在对话里一步步做

## 云端流水线（见 docs/adr/0005）

- 配额硬约束下，代码写作放 **Z.ai 网页版沙箱（GLM-5.3）**，经 Git 回流；本机只做构建、模拟器验证与技能流程。
- **仓库（origin: jiushiniubi123/ai-fenshen-browser，clone 在 D:\w\安卓，仓库根=Gradle 工程根）是唯一事实源**：云端 agent 能读到的项目记忆 = 仓库内容 + 对话任务书；版本钉死见 `docs/build-recipe.md`，云端一个字符不许改。
- 云端任务书模板存 `.scratch/`（现成：`issue3-sandbox-brief.md`）；云端产物 = 未编译代码，首次本机构建报错属预期，修 diff 回流入库。
- matt skills 只在本机存在：涉技能流程（/implement、/code-review、/triage、/wayfinder…）一律本机跑，不派云端。

## Agent skills

### Issue tracker

Issues 在 GitHub 仓库 `jiushiniubi123/ai-fenshen-browser` 上跟踪（用 `gh` CLI，命令需带 `-R`）。See `docs/agents/issue-tracker.md`.

### Triage labels

保留五个默认 triage role，label 字符串与 role 名相同。See `docs/agents/triage-labels.md`.

### Domain docs

Single-context：根目录 `CONTEXT.md`（术语表）+ `docs/adr/`（决策记录）。See `docs/agents/domain.md`.
