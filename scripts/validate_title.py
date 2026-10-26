#!/usr/bin/env python3
"""校验豆包工作对话标题是否符合「类别 emoji 对象｜目标」规范。

用法：
  python3 validate_title.py "🧩 待办清单App｜修复"
  python3 validate_title.py --json "📝 团队周报｜2026-10-26"
  printf '%s\n' "标题1" "标题2" | python3 validate_title.py

退出码：全部合法 0，存在非法 1。
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata

# 顺序重要：带 variation selector 的 ⚙️ 需在其基字符前优先匹配。
CATEGORIES = [
    ("🎬", "内容制作"),
    ("🧩", "工具开发"),
    ("🔎", "对比调研"),
    ("🎨", "页面设计"),
    ("📝", "方法整理"),
    ("📅", "日程安排"),
    ("⚙️", "环境配置"),
    ("💬", "一般讨论"),
]
EMOJIS = [e for e, _ in CATEGORIES]

MIN_LEN, MAX_LEN = 4, 48
FORBIDDEN = ("\n", "\r", "`", "https://", "http://", "@", "/Users/", "sk-")


def _has_extra_emoji(text: str) -> bool:
    for ch in text:
        cp = ord(ch)
        if 0x1F000 <= cp <= 0x1FAFF or 0x2600 <= cp <= 0x27BF:
            return True
        if cp in (0xFE0F, 0x200D):  # variation selector / ZWJ，仅随 emoji 出现
            return True
    return False


def validate(title: str):
    """返回 (ok, error)。"""
    if not isinstance(title, str) or not title:
        return False, "标题为空"
    if title != title.strip():
        return False, "标题首尾不能有空白"
    if not (MIN_LEN <= len(title) <= MAX_LEN):
        return False, "标题长度需在 %d～%d 个字符（当前 %d）" % (MIN_LEN, MAX_LEN, len(title))

    emoji = next((e for e in EMOJIS if title.startswith(e + " ")), None)
    if emoji is None:
        return False, "缺少合法的类别 emoji 前缀（%s）" % "".join(EMOJIS)

    body = title[len(emoji) + 1:]
    if not body:
        return False, "标题正文为空"
    if body.count("｜") != 1:
        return False, "必须恰好包含一个全角分隔符「｜」"
    if "|" in body:
        return False, "不能用半角「|」代替全角「｜」"
    left, right = body.split("｜")
    if not left or not right or left != left.strip() or right != right.strip():
        return False, "「｜」两侧的对象与目标不能为空或带边缘空格"
    if _has_extra_emoji(body):
        return False, "正文只能在开头出现一个类别 emoji"
    if any(unicodedata.category(c).startswith("C") for c in title):
        return False, "标题含控制字符"
    if re.search(r"[A-Za-z]:[\\/]|\\\\", title):
        return False, "标题含绝对路径"
    hit = next((x for x in FORBIDDEN if x in title), None)
    if hit is not None:
        return False, "标题含不允许的格式或私人信息：%s" % (hit.strip() or repr(hit))
    return True, None


def main() -> int:
    ap = argparse.ArgumentParser(description="校验对话标题规范")
    ap.add_argument("titles", nargs="*", help="待校验标题；省略则从 stdin 逐行读取")
    ap.add_argument("--json", action="store_true", help="以 JSON 输出结果")
    args = ap.parse_args()

    if args.titles:
        titles = args.titles
    else:
        titles = [line.rstrip("\n") for line in sys.stdin if line.strip()]

    results = []
    for t in titles:
        ok, err = validate(t)
        results.append({"title": t, "ok": ok, "error": err})

    if args.json:
        if len(results) == 1 and args.titles:
            print(json.dumps(results[0], ensure_ascii=False))
        else:
            print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        for r in results:
            if r["ok"]:
                print("OK   " + r["title"])
            else:
                print("ERR  " + r["title"] + "\n     " + r["error"])

    return 0 if all(r["ok"] for r in results) else 1


if __name__ == "__main__":
    sys.exit(main())
