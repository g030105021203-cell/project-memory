---
name: project-memory
description: Use when starting a new Claude Code session in an existing project, when wrapping up work that should be preserved across sessions, or when you see a MEMORY folder in the project root
commands:
  create-memory: 创建 MEMORY/completed.md bugs.md todo.md
  update-memory: 更新 MEMORY 三个文件（completed 追加、bugs 追加、todo 重排）
  read-memory: 读取 MEMORY 三个文件作为工作上下文
---

# Project Memory Skill

跨会话保留已完成工作、Bug 和待办事项，避免每个新会话都从零开始。

**两种使用方式：**
- **CLI 命令：** 直接输入 `/create-memory`、`/update-memory`、`/read-memory`
- **语义指令：** 对 AI 说"帮我运行 /create memory"，AI 也能理解并执行相同步骤

## When to Use

- 进入已有项目的新会话，需要上次工作的上下文
- 会话结束前，需要记录本次完成的工作和新发现的 Bug
- 项目根目录存在 `MEMORY/` 文件夹时

**不要用在：** 一次性脚本或探索性任务，不需要跨会话上下文

## Quick Reference

| 命令 | 时机 | 产出 |
|------|------|------|
| `/create-memory` | 新项目第一次会话结束时 | 创建 `MEMORY/completed.md` + `bugs.md` + `todo.md` |
| `/update-memory` | 后续会话结束时 | 追加 completed/bugs，重排 todo |
| `/read-memory` | 会话开始时 | 读取三个文件作为工作上下文 |

## Commands

### /create-memory

第一次会话结束时创建 MEMORY。在 `CWD/MEMORY/` 下生成三个文件，根据本次会话内容填充。如 `MEMORY/` 已存在则不覆盖。

```
[已创建] MEMORY/completed.md (3 项已完成工作)
[已创建] MEMORY/bugs.md (1 个 bug 记录)
[已创建] MEMORY/todo.md (5 项待办)
```

你也可以对 AI 说"帮我运行 /create memory"，效果相同。

### /update-memory

读取现有三个文件，追加本次会话新内容。`completed.md` 和 `bugs.md` 只追加不删改旧内容；**`todo.md` 完整重排**（移除已完成、新增、调优先级）。如 MEMORY 不存在则提示先运行 `/create-memory`。

### /read-memory

读取 `CWD/MEMORY/` 下三个文件：
- `bugs.md` / `todo.md` — 全文读取
- `completed.md` — 通过 `scripts/read_completed.py` 智能截断：≤40 行全文输出，>40 行保留最近 3 次会话的完整条目 + 旧内容摘要

如 MEMORY 不存在则提示用户这是新项目。

## File Templates

### completed.md（只追加）

```markdown
# 已完成工作

## 2026-05-09
- [x] 功能描述 — 关键细节
```

永不修改或删除旧内容。

> `⚠️` 日期标题必须为 `## YYYY-MM-DD` 格式（如 `## 2026-05-09`）。`read_completed.py` 依赖此格式做会话分割，改格式会导致截断错位。文件开头可有一段非日期说明文字，不会影响分割。

### bugs.md（追加 + 状态 tag）

```markdown
# Bug 记录

## 2026-05-09
- [已修复] 问题 — 原因 & 方案
- [待修复] 问题 — 影响范围
```

可追加新 Bug，可更新已有 Bug 的 `[已修复]` / `[待修复]` tag。

> `💡` 标记为 `[待修复]` 的 Bug 建议同时在 `todo.md` 中有一条对应任务，避免遗漏。

### todo.md（完整重排）

```markdown
# 待办事项

## 高优先级
- [ ] 任务
```

每次 `/update-memory` 时整份重排，优先级动态调整。

## Common Mistakes

- **在会话中间用 /create-memory 覆盖已有 MEMORY** — 只应在第一次会话结束时使用。之后始终用 `/update-memory`
- **手动编辑 todo.md** — AI 每次 `/update-memory` 时会完整重排 todo.md，手动编辑会被覆盖
- **completed.md 太长不处理** — 脚本会自动截断，确保拿到最近 3 次会话的完整条目 + 旧内容摘要
- **忘了 /read-memory 就开工** — 先在项目根目录运行 `/read-memory` 加载上下文再开始工作
