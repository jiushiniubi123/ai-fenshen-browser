# 0004 - 分身隔离采用 GeckoView 会话 contextId

日期：2026-09-12 ｜ 状态：已接受

每个分身对应一个 GeckoSession 的独立 contextId。官方源码注释明确："设置 context ID 会按 ID 分隔 cookie 罐子，隔离 cookie 与 localStorage 等浏览器存储，存储数据按 context 持久收集"（GeckoSessionSettings.java；Mozilla 工程师在 geckoview#129 的答复同此）。分身登录状态因此跨 App 重启持久保留；删除分身时用 `StorageController.clearDataForSessionContext` 清数据。

## Considered Options

- **Firefox 容器（Multi-Account Containers）**：Android 端不可用，被否（见 ADR 0001）。
- **多 Runtime / 多 Profile**：面向整个浏览器实例的重量级方案，不是账号粒度，被否。
