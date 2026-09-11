# skills/ — matt 工程技能库（随仓库分发，云端必读）

> 本目录是本机 ZCode 所装工程技能（matt engineering skills）的**只读快照**，随仓库分发（ADR 0007）。
> 本机 ZCode 有技能运行时，同名技能自动触发；**云端沙箱（Z.ai 网页版）没有技能运行时——
> 把对应 SKILL.md 当操作手册逐条照做，就是"使用技能"在云端的形式**。
> 云端不得修改本目录（只读快照；更新由本机 agent 从源 `C:\Users\A\.zcode\skills\` 重新同步）。

## 云端写码的标准动作（每次任务书开工前执行）

1. 读 [`ask-matt/SKILL.md`](ask-matt/SKILL.md)——它是路由器：按当前任务类型查它的路由表，选定该用哪些技能。
2. 写代码 → 读 [`implement/SKILL.md`](implement/SKILL.md) 并照做：把任务书当 spec，小步切片推进；每片写完做双轴自查——
   **Standards**＝仓库约定（`CONTEXT.md` 禁用词、`docs/adr/` 边界）；**Spec**＝任务书条款逐条核对。
3. 测试与验证的组织方式参考 [`tdd/SKILL.md`](tdd/SKILL.md)；但沙箱没有构建环境，
   **跳过一切"运行构建/测试/模拟器"步骤**，把"本机待验证清单"写进交付文档（如 README-BUILD.md），由本机验收（ADR 0005）。
4. 术语与边界拿不准 → `CONTEXT.md` 与 `docs/adr/`；需要写仓库文档 → [`writing-for-agents/SKILL.md`](writing-for-agents/SKILL.md)。

## 全部技能一览（30 个）

「云端可用」含义：✅＝在沙箱照手册执行；⚠️＝只参考其流程/自查部分；❌＝依赖本机环境或与用户对话，仅本机。

| 技能 | 一句话用途 | 云端可用 |
|---|---|---|
| ask-matt | 技能路由器：拿不准用哪个就先读它 | ✅ 必读 |
| implement | 按 spec/ticket 小步实现一段工作 | ✅ 写码主手册 |
| tdd | 测试先行的 red-green-refactor 纪律 | ⚠️ 流程参考（不运行） |
| code-review | 对变更做 Standards+Spec 双轴审查 | ⚠️ 当自查清单用；执行在本机 |
| codebase-design | 深模块词汇：module/interface/seam 设计 | ✅ 设计参考 |
| domain-modeling | 打磨领域语言、沉淀 ADR | ✅ 参考 |
| writing-for-agents | 为 agent 写文档（skills、AGENTS.md） | ✅ 参考 |
| handoff | 写会话交接文档 | ✅ 可用 |
| resolving-merge-conflicts | 逐 hunk 解 merge/rebase 冲突 | ✅ 可用 |
| long-horizon-kit | 多步骤任务防跑偏的最小骨架（状态进文件） | ✅ 可用 |
| wait-what | 把没说清的话用缺失的 context 重述 | ✅ 可用 |
| grilling | 追问式访谈原语（rounds/frontier） | ⚠️ 自问自查时可借其框架 |
| grill-me / grill-with-docs | 面向用户想法的访谈（无痕/留痕） | ❌ 需与用户对话，本机 |
| to-spec | 把讨论收束成 spec 并发到 tracker | ❌ 本机 |
| to-tickets | 把 plan/spec 拆成带 blocking edges 的 tickets | ❌ 本机 |
| triage | issues/外部 PR 过 triage 状态机，产出 agent-ready brief | ❌ 本机 |
| wayfinder | 大型模糊任务铺 decision tickets 共享地图 | ❌ 本机 |
| diagnosing-bugs | 难缠 bug 诊断循环（需紧反馈环） | ❌ 无构建环境跑不了，本机 |
| improve-codebase-architecture | 架构巡检，找 deepening opportunities | ❌ 本机 |
| prototype | 一次性原型回答设计问题 | ⚠️ 仅纯逻辑/UI 原型可用 |
| research | 委托后台对照一手来源调研并留档 | ⚠️ 可用 |
| deep-explore | 深度探索主题并产出 HTML 报告 | ⚠️ 可用 |
| single-file-ui-prototype | 自包含 HTML 出多套 UI 方案对比 | ⚠️ 可用 |
| to-questionnaire | 把阻塞的 decision 转成问卷发出去 | ❌ 本机 |
| teach | 跨会话教用户一个概念 | ❌ 需与用户对话，本机 |
| wizard | 生成人类步骤的交互式引导脚本 | ❌ 本机 |
| contract-sediment-cleanup | 清理规则文档的版本沉积 | ⚠️ 可用 |
| skill-package-audit | 第三方 skill 压缩包体检 | ⚠️ 可用 |
| setup-matt-pocock-skills | 配置 issue tracker/triage labels/docs 布局 | ❌ 已配置过，本机 |
