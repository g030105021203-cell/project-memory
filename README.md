# Project Memory Skill

> **Persist completed work, bugs, and todos across Claude Code / Cursor sessions.**  
> 跨会话保留已完成工作、Bug 和待办事项，让 AI 记住每个项目的上下文。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## What is this? / 这是什么？

A skill for Claude Code (also works with Cursor) that maintains `MEMORY/` folder in your project root:

```
<project-root>/
  MEMORY/
    completed.md    # Done work (append-only, by date)
    bugs.md         # Bug log (with [fixed]/[pending] tags)
    todo.md         # Todo list (reorganized on each update)
```

**Three conversational commands** — tell your AI assistant these, and it follows the steps in `SKILL.md`:

| Command | When | What it does |
|---------|------|-------------|
| `/create memory` | After first session | Initialize all 3 files |
| `/update memory` | After subsequent sessions | Append completed/bugs, reorganize todo |
| `/read memory` | At session start | Load context from all 3 files |

> **⚠️ These are semantic commands, not built-in slash commands.**  
> When you say `/create memory` to Claude, it reads the instructions in SKILL.md and performs the corresponding file operations. No plugin or extension needed — just tell your AI.

---

## Quick Start / 快速开始

1. Copy this folder to `~/.claude/skills/project-memory/`
2. In a Claude Code session, use the **Skill** tool to load `project-memory`
3. At the end of your first project session, say: **"/create memory"**
4. Next session, start with: **"/read memory"**
5. End each session with: **"/update memory"**

For full command details and file templates → see [SKILL.md](SKILL.md).

---

## Smart Truncation / 智能截断

`scripts/read_completed.py` handles long `completed.md`:
- ≤ 40 lines → full output
- > 40 lines → last 3 sessions in full + summary of older content

Saves tokens while keeping recent context intact.

---

## License

MIT
