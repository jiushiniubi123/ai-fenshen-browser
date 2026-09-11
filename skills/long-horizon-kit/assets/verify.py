#!/usr/bin/env python3
"""验收闸门：跑功能清单里那条 check 命令。退出码为 0 才把 passes 翻成 true。

只有这个脚本能翻转 passes。模型自己说「做完了」不算。

用法：
    python verify.py --list             看所有功能的状态
    python verify.py F003               验收 F003
    python verify.py F003 --reset       把 F003 退回未通过
    python verify.py F003 --file a.json 指定清单文件
"""

import argparse
import datetime
import json
import pathlib
import subprocess
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def save(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def find(data, fid):
    for f in data.get("features", []):
        if f.get("id") == fid:
            return f
    return None


def count(data):
    feats = data.get("features", [])
    return sum(1 for f in feats if f.get("passes")), len(feats)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("feature_id", nargs="?")
    ap.add_argument("--file", default="features.json")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--reset", action="store_true")
    args = ap.parse_args()

    path = pathlib.Path(args.file)
    if not path.exists():
        print(f"找不到 {path}。请在项目根目录运行，或用 --file 指定。")
        return 2
    data = load(path)

    if args.list or not args.feature_id:
        done, total = count(data)
        print(f"任务：{data.get('task', '')}    进度：{done}/{total}\n")
        for f in data.get("features", []):
            print(f"  [{'通过' if f.get('passes') else '未通过'}] {f.get('id')}  {f.get('title')}")
            print(f"          验收：{f.get('acceptance')}")
            print(f"          命令：{f.get('check')}")
        return 0

    f = find(data, args.feature_id)
    if not f:
        print(f"清单里没有 {args.feature_id}。用 --list 看有哪些。")
        return 2

    if args.reset:
        f["passes"] = False
        f["verified_at"] = ""
        f["verified_by"] = ""
        save(path, data)
        print(f"{args.feature_id} 已退回未通过。")
        return 0

    cmd = f.get("check") or ""
    print(f"验收 {args.feature_id}：{f.get('title')}")
    print(f"验收标准：{f.get('acceptance')}")
    print(f"执行：{cmd}\n")
    sys.stdout.flush()

    r = subprocess.run(cmd, shell=True)
    print()

    if r.returncode == 0:
        f["passes"] = True
        f["verified_at"] = datetime.datetime.now().isoformat(timespec="seconds")
        f["verified_by"] = cmd
        save(path, data)
        done, total = count(data)
        print(f"通过。{args.feature_id} 的 passes 已翻成 true。进度 {done}/{total}。")
        print("接下来：写 progress.md，然后 git commit。")
        return 0

    print(f"未通过（退出码 {r.returncode}）。passes 保持 false，不翻转。")
    print("接下来：把这次失败写进 progress.md。不要删掉报错。")
    return 1


if __name__ == "__main__":
    sys.exit(main())
