"""智能读取 completed.md：短文件全文输出，长文件保留最近3次会话 + 旧内容摘要。"""
import sys
from pathlib import Path

def read_completed(path, max_lines=40, keep_sessions=3):
    content = Path(path).read_text(encoding="utf-8").rstrip()
    lines = content.split("\n")

    if len(lines) <= max_lines:
        return content

    # 按日期块分割（## YYYY-MM-DD）
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

    if len(blocks) <= keep_sessions:
        return content

    old_blocks = blocks[:-keep_sessions]
    recent_blocks = blocks[-keep_sessions:]

    summary_sessions = len(old_blocks)
    total_items = sum(1 for b in old_blocks for l in b if l.strip().startswith("- ["))

    result = f"""# completed.md（智能摘要模式）

## 较早记录摘要（共 {summary_sessions} 个会话，{total_items} 项已完成工作）

_详细内容已归档。如需查看较早记录，请直接打开 completed.md。_

---

"""
    for block in recent_blocks:
        result += "\n".join(block) + "\n\n"

    return result.strip()

if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "MEMORY/completed.md"
    print(read_completed(path))
