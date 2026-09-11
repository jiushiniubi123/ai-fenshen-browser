#!/usr/bin/env python3
"""每轮开场热身：打印当前状态。只读，不改任何东西。

先跑这个，再动手。它替你回答一个问题：我现在在哪。

用法：
    python warmup.py
    python warmup.py --no-test
    python warmup.py --file features.json
"""

import argparse
import json
import os
import pathlib
import subprocess
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass


def run(cmd):
    try:
        r = subprocess.run(
            cmd, shell=True, capture_output=True, text=True,
            encoding="utf-8", errors="replace", timeout=300,
        )
        out = ((r.stdout or "") + (r.stderr or "")).strip()
        return out, r.returncode
    except Exception as e:
        return f"（没能执行：{e}）", -1


def tail(path, n):
    p = pathlib.Path(path)
    if not p.exists():
        return f"（没有 {path}）"
    lines = p.read_text(encoding="utf-8").splitlines()
    return "\n".join(lines[-n:]) or "（空文件）"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", default="features.json")
    ap.add_argument("--no-test", action="store_true")
    args = ap.parse_args()

    print("=" * 62)
    print("1. 当前目录")
    print(os.getcwd())

    print("\n2. 最近 5 次提交")
    out, _ = run("git log --oneline -5")
    print(out or "（没有提交记录）")

    print("\n3. 工作区状态（有输出 = 有未提交的改动）")
    out, _ = run("git status --short")
    print(out or "（干净）")

    print("\n4. progress.md 末尾")
    print(tail("progress.md", 25))

    print("\n5. todo.md")
    print(tail("todo.md", 40))

    print("\n6. 功能清单")
    path = pathlib.Path(args.file)
    baseline = ""
    if not path.exists():
        print(f"（找不到 {path}）")
    else:
        data = json.loads(path.read_text(encoding="utf-8"))
        feats = data.get("features", [])
        done = sum(1 for f in feats if f.get("passes"))
        print(f"任务：{data.get('task', '')}    进度：{done}/{len(feats)}")
        for f in feats:
            mark = "通过" if f.get("passes") else "未通过"
            print(f"  [{mark}] {f.get('id')}  {f.get('title')}")
        nxt = next((f for f in feats if not f.get("passes")), None)
        print("\n   下一个要做：" + (f"{nxt['id']}  {nxt['title']}" if nxt else "全部通过"))
        baseline = data.get("baseline_test", "")

    print("\n7. 基础测试")
    if args.no_test or not baseline:
        print("（跳过）")
    else:
        print(f"执行：{baseline}")
        out, code = run(baseline)
        print(out or "（没有输出）")
        print("结论：起点干净" if code == 0 else f"结论：起点不干净（退出码 {code}）。先修好再动手。")

    print("\n提醒：一次只做一个功能。做完跑 verify.py，通过才翻转 passes。")
    print("=" * 62)


if __name__ == "__main__":
    main()
