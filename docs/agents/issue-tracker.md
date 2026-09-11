# Issue tracker: GitHub

这个 repo 的 issues 和 specs 存放在 GitHub issues 中。所有操作都使用 `gh` CLI。

**Repo: `jiushiniubi123/ai-fenshen-browser`**（<https://github.com/jiushiniubi123/ai-fenshen-browser>，私有仓库，2026-09-12 创建）。

## 运行环境注意事项

- 本目录自 2026-09-12 起 **是 git clone**（origin = jiushiniubi123/ai-fenshen-browser，MinGit 推送）。保险起见 `gh` 命令仍统一显式带 `-R jiushiniubi123/ai-fenshen-browser`。
- `gh` 已登录账号 `jiushiniubi123`。若 `gh` 不在 PATH，完整路径为 `%LOCALAPPDATA%\Programs\GitHub CLI\bin\gh.exe`。

## Conventions

- **Create an issue**: `gh issue create -R jiushiniubi123/ai-fenshen-browser --title "..." --body "..."`。多行 body 使用 heredoc。
- **Read an issue**: `gh issue view <number> -R jiushiniubi123/ai-fenshen-browser --comments`，用 `jq` 过滤 comments，并同时获取 labels。
- **List issues**: `gh issue list -R jiushiniubi123/ai-fenshen-browser --state open --json number,title,body,labels,comments --jq '[.[] | {number, title, body, labels: [.labels[].name], comments: [.comments[].body]}]'`，按需加上 `--label` 和 `--state` filters。
- **Comment on an issue**: `gh issue comment <number> -R jiushiniubi123/ai-fenshen-browser --body "..."`
- **Apply / remove labels**: `gh issue edit <number> -R jiushiniubi123/ai-fenshen-browser --add-label "..."` / `--remove-label "..."`
- **Close**: `gh issue close <number> -R jiushiniubi123/ai-fenshen-browser --comment "..."`

## Pull requests as a triage surface

**PRs as a request surface: no.** _（如果这个 repo 把 external PRs 当作 feature requests，则设为 `yes`；`/triage` 会读取这个 flag。）_

设为 `yes` 时，PRs 走与 issues 相同的 labels 和 states，使用 `gh pr` 对应命令：

- **Read a PR**: `gh pr view <number> -R jiushiniubi123/ai-fenshen-browser --comments`，以及 `gh pr diff <number> -R jiushiniubi123/ai-fenshen-browser` 获取 diff。
- **List external PRs for triage**: `gh pr list -R jiushiniubi123/ai-fenshen-browser --state open --json number,title,body,labels,author,authorAssociation,comments`，然后只保留 `authorAssociation` 为 `CONTRIBUTOR`、`FIRST_TIME_CONTRIBUTOR` 或 `NONE` 的（丢弃 `OWNER`/`MEMBER`/`COLLABORATOR`）。
- **Comment / label / close**: `gh pr comment`、`gh pr edit --add-label`/`--remove-label`、`gh pr close`。

GitHub 在 issues 和 PRs 之间共享一个 number space，因此裸 `#42` 可能是两者之一——用 `gh pr view 42` 解析，失败则回退到 `gh issue view 42`。

## When a skill says "publish to the issue tracker"

创建一个 GitHub issue。

## When a skill says "fetch the relevant ticket"

运行 `gh issue view <number> -R jiushiniubi123/ai-fenshen-browser --comments`。

## Wayfinding operations

供 `/wayfinder` 使用。**map** 是单个 issue，以 **child** issues 作为 tickets。

- **Map**: 单个带 `wayfinder:map` label 的 issue，保存 Notes / Decisions-so-far / Fog body。`gh issue create -R jiushiniubi123/ai-fenshen-browser --label wayfinder:map`。
- **Child ticket**: 作为 GitHub sub-issue 链接到 map 的 issue（通过 sub-issues endpoint 使用 `gh api`）。未启用 sub-issues 时，把 child 加入 map body 中的 task list，并在 child body 顶部写 `Part of #<map>`。Labels：`wayfinder:<type>`（`research`/`prototype`/`grilling`/`task`）。一旦被 claim，ticket 被 assign 给 driving dev。
- **Blocking**: GitHub 的 **native issue dependencies**——canonical、UI 可见的表达。用 `gh api --method POST repos/jiushiniubi123/ai-fenshen-browser/issues/<child>/dependencies/blocked_by -F issue_id=<blocker-db-id>` 添加 edge，其中 `<blocker-db-id>` 是 blocker 的数字 **database id**（`gh api repos/jiushiniubi123/ai-fenshen-browser/issues/<n> --jq .id`，_不是_ `#number` 或 `node_id`）。GitHub 报告 `issue_dependencies_summary.blocked_by`（仅 open blockers——即 live gate）。依赖不可用时，回退到 child body 顶部的 `Blocked by: #<n>, #<n>` 行。当所有 blockers 都关闭时，ticket 即为 unblocked。
- **Frontier query**: 列出 map 的 open children（`gh issue list -R jiushiniubi123/ai-fenshen-browser --state open`，限定在 map 的 sub-issues / task list），丢弃任何带有 open blocker 的（`issue_dependencies_summary.blocked_by > 0`，或 `Blocked by` 行中的 open issue）或带有 assignee 的；按 map 顺序第一个胜出。
- **Claim**: `gh issue edit <n> -R jiushiniubi123/ai-fenshen-browser --add-assignee @me`——session 的第一次写入。
- **Resolve**: `gh issue comment <n> -R jiushiniubi123/ai-fenshen-browser --body "<answer>"`，然后 `gh issue close <n>`，再向 map 的 Decisions-so-far 追加 context pointer（gist + link）。
