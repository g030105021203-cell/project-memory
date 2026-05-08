"""智能读取 completed.md：短文件全文输出，长文件保留最近3次会话 + 旧内容摘要。

按 ## YYYY-MM-DD 分割会话块。文件开头的非标题文字视为前言，始终保留。
"""
import sys
from pathlib import Path

MAX_LINES = 40
KEEP_SESSIONS = 3

def read_completed(path):
    content = Path(path).read_text(encoding="utf-8").rstrip()
    lines = content.split("\n")

    if len(lines) <= MAX_LINES:
        return content

    # 按 ## 标题分割
    blocks = []
    current = []
    for line in lines:
        if line.startswith("## ") and current:
            blocks.append(current)
            current = [line]
        else:
            current.append(line)
    if current:
        blocks.append(current)

    # 没有 ## 标题，无法分块 → 全文输出
    if not any(b[0].startswith("## ") for b in blocks):
        return content

    # 第一块如果不是 ## 开头，说明是前言 → 拆出来
    preamble = []
    if blocks and not blocks[0][0].startswith("## "):
        preamble = blocks.pop(0)

    if len(blocks) <= KEEP_SESSIONS:
        return content

    old_blocks = blocks[:-KEEP_SESSIONS]
    recent_blocks = blocks[-KEEP_SESSIONS:]

    summary_sessions = len(old_blocks)
    total_items = sum(
        1 for b in old_blocks for l in b if l.strip().startswith("- [")
    )

    result = []
    if preamble:
        result.append("\n".join(preamble) + "\n")

    result.append(f"""# completed.md（智能摘要模式）

## 较早记录摘要（共 {summary_sessions} 个会话，{total_items} 项已完成工作）

_详细内容已归档。如需查看较早记录，请直接打开 completed.md。_

---
""")

    for block in recent_blocks:
        result.append("\n".join(block))

    return "\n\n".join(result).strip()

if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "MEMORY/completed.md"
    print(read_completed(path))
