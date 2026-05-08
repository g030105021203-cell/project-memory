# Project Memory Skill

一个 Claude Code skill，在每个项目根目录下维护 `MEMORY/` 文件夹，实现跨会话的项目长期记忆。

## 文件结构

```
<project-root>/
  MEMORY/
    completed.md    # 已完成工作概览（只追加，按日期分区）
    bugs.md         # Bug 记录（可追加，可更新状态 tag）
    todo.md         # 待办事项（每次更新时完整重排）
```

## 安装

将 `project-memory/` 放入 `~/.claude/skills/`，或通过 Skill 工具直接加载 `SKILL.md`。

## 命令

| 命令 | 时机 | 行为 |
|------|------|------|
| `/create memory` | 新项目第一次会话结束时 | 创建 MEMORY 文件夹及三个文件 |
| `/update memory` | 后续会话结束时 | 追加 completed/bugs，重排 todo |
| `/read memory` | 会话开始时 | 读取三个文件作为工作上下文 |

## 使用流程

1. 新项目第一次会话结束 → `/create memory`
2. 下次会话开始 → `/read memory`（加载上下文）
3. 会话结束 → `/update memory`（更新记录）
4. 重复步骤 2-3

## 辅助脚本

`scripts/read_completed.py` — 智能读取 `completed.md`：
- 全文 ≤ 40 行 → 直接输出
- 全文 > 40 行 → 旧内容摘要 + 最近 3 次会话完整条目
