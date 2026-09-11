# longtask-kit

一个最小工具包，让多步骤任务不容易在中间跑偏。

它只做两件事：

1. **把状态从对话搬到文件里。** 对话会被压缩、会被丢掉，文件不会。
2. **把「完成」的判断权从模型手里拿走。** 完成与否由命令的退出码决定，不由模型自己说。

只需要 Python 3，没有别的依赖。

## 文件

| 文件 | 作用 | 谁写 |
|---|---|---|
| `features.json` | 全部要做的功能 + 每条的验收命令 + 通过状态 | 你写一次，`verify.py` 翻转状态 |
| `todo.md` | 本轮做什么、步骤、完成标准 | 每轮**重写**（覆盖，不追加） |
| `progress.md` | 每轮的做了什么、证据、卡点 | 每轮**追加**（不改历史） |
| `warmup.py` | 开场热身：打印当前状态，只读 | 每轮开始跑一次 |
| `verify.py` | 验收闸门：跑 check 命令，通过才翻转 `passes` | 每做完一个功能跑一次 |
| `agent-rules.md` | 给 agent 的常驻规则 | 粘进系统提示或 `AGENTS.md` |

## 每轮的循环

```
1. python warmup.py              看现在在哪，起点干不干净
2. 挑一个 passes 还是 false 的功能，写进 todo.md
3. 只做这一个
4. python verify.py F003         通过 → passes 自动翻成 true
                                 没通过 → 保持 false，去修
5. 在 progress.md 追加一条
6. git commit
```

## 开始用

1. 把 `features.json` 里的示例功能换成你自己的。每条都要有一个 `check` 命令——写不出这条命令，说明验收标准还没想清楚。
2. 把 `baseline_test` 换成一条跑得快的基础测试。每轮开场会跑它，确认起点是干净的。
3. 把 `agent-rules.md` 里的规则粘进你的 agent 配置。
4. 运行 `python warmup.py` 开始第一轮。

## 常用命令

```bash
python verify.py --list          # 看所有功能的状态
python verify.py F003            # 验收 F003
python verify.py F003 --reset    # 退回未通过，重做
python warmup.py --no-test       # 热身但跳过基础测试
```

## 三条容易搞错的

- **`todo.md` 是覆盖，`progress.md` 是追加。** 前者描述「本轮」，后者是历史，不要混。
- **不要手改 `passes`。** 手改一次，这个清单就不再是证据了。
- **失败也要写进 `progress.md`。** 报错原文贴上。删掉失败记录，下一轮还会犯同一个错。
