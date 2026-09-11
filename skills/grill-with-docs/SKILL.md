---
name: grill-with-docs
description: "在 working directory 中打磨计划或设计的持续追问式访谈，过程中同步沉淀 CONTEXT.md 词汇表与 ADR。适用于用户想边打磨想法边留文档痕迹、或明确要求访谈产出 ADR/术语表时。"
---

把一次 `/grilling` session 与 `/domain-modeling` 的文档纪律编织成一趟流程：访谈负责清空 frontier，文档在决策敲定的当下落盘。先调用这两个 skill 加载它们的完整规则——本文件只规定二者如何配合，不重复它们各自的规则。所有文档写进当前 working directory。

## Steps

1. **勘测文档现状。** 在 working directory 里找 `CONTEXT.md`、`CONTEXT-MAP.md`、`docs/adr/`；存在则在第一轮提问前读完，让问题建立在既有语言上。没有则按 domain-modeling 的懒创建规则，等第一个 term 解决时再建。完成标准：你能说出本次 session 接续哪份既有文档，或确认从空白开始。

2. **按 rounds 跑访谈。** 完全遵循 grilling：逐轮问完整条 frontier、每题附推荐答案、facts 派 sub-agent 去查而不问用户。完成标准与 grilling 相同：frontier 为空。

3. **每轮回答后即落盘。** 在用户回答之后、下一轮提问之前，按 domain-modeling 处理本轮敲定的内容——term 进 `CONTEXT.md`，满足三项条件的 decision 提议写 ADR。文档是共同理解的实证，随轮次生长。完成标准：本轮每个敲定的 term 和 decision 都处理完毕，才发出下一轮的 frontier。

4. **收尾对齐。** frontier 清空后，请用户确认达成共同理解（grilling 的开工门槛），并列出本次 session 新建与修改的全部文件路径。完成标准：用户确认理解一致，且每个敲定的 decision 都有明确归宿——`CONTEXT.md`、ADR、或被判定不满足 ADR 条件。
