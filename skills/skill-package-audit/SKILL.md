---
name: skill-package-audit
description: 体检并优化第三方/交接来的 skill 压缩包。适用于用户给一个 skill zip/文件夹要求"优化""审查""体检"，或安装前想先排查问题时。配合 writing-for-agents 使用。
---

# Skill package audit · 交接 skill 体检

按此清单体检一个 skill 包，再动手改。每类问题给出探测方法；修法遵循 `writing-for-agents`（单一真相源、pointer 不复制、正向前瞻）。

## 体检清单

1. **结构盘点**：解压（或读 zip 目录）→ 对照 `SKILL.md` 声称的文件清单与 `files/` 实际内容。典型 drift：清单数量对不上、运行时被引用的脚本（wait/monitor/daemon）不在复制清单里、文件跑到包外（如 zip 根目录的散件）、双层嵌套同名目录。
2. **过期声称**：正文说"占位空文件/由用户提供"，包里却已是真实实现（大体积 HTML/PY 是信号）。流程步骤要改成"用随包实现启动"，hard gate 改成可检查的联通性标准（如测试消息落盘）。
3. **版本沉积**：契约/文档按 v3→v13 增量堆叠，含"X 起已废除，见下章"的死规则、同一规则多处矛盾（如四档 vs 五档状态词）。检测信号与完整修法见 `contract-sediment-cleanup` skill。
4. **跨文件重复**：同一协议细则同时住在契约与子 agent 指令里（状态词表、编号对号、角色口径）。修法：协议住契约，行为住指令，指令用一句话 pointer 指到契约小节。
5. **数值一致性**：把文档里的阈值与代码常量交叉核对——心跳间隔 vs 新鲜度窗口 vs 阻塞等待 timeout（例：90s 窗口 + 120s timeout = 假离线；timeout 须 < 窗口并留余量）。同口径数值必须全包一致。
6. **文档自伤**：重复标题、指向旧版行号/旧章节名的注释与 pointer、frontmatter 与目录名不匹配。代码注释里的章节引用随文档重构一并更新。
7. **frontmatter**：user-invoked（`disable-model-invocation: true`）的 description 面向人类写一行摘要；model-invoked 才写触发 branches。

## 交付

- 原包不动，产出 `<原名>-optimized.zip` 放原包旁边；打包前在临时目录重组结构。
- 打包后跑自动自检：zip 完整性 + 交叉引用断言（关键小节存在、无重复标题、无过期关键词、清单数量正确、pointer 路径正确）。
- 汇报：按体检清单分类列出发现的问题与修法，标注哪些没改（如 site-specific 样例脚本只加注释警示）。
