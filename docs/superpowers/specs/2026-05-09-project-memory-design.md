# Project Memory Skill — Design Spec

## 概述

一个 Claude Code skill，为每个项目在根目录下创建 `MEMORY/` 文件夹，维护三份长期记忆文档：已完成工作、Bug 记录、待办事项。支持三个 slash 命令：`/create memory`、`/update memory`、`/read memory`。

## 命令定义

### `/create memory`

- **触发时机**：新项目第一次会话结束时
- **行为**：在 CWD 根目录创建 `MEMORY/` 文件夹，生成 `completed.md`、`bugs.md`、`todo.md`，根据本次会话内容填充
- **不应覆盖已有 MEMORY 文件夹**（若存在则提示用户）

### `/update memory`

- **触发时机**：第二次及以后的会话结束时
- **行为**：
  - 读取现有三个文件
  - `completed.md`：追加新完成的工作（按日期分区，不删不改旧内容）
  - `bugs.md`：追加新 bug、更新已有 bug 的状态 tag（`[已修复]` / `[待修复]`）
  - `todo.md`：整体重排——移除已完成项、新增待办、调整优先级

### `/read memory`

- **触发时机**：会话开始时
- **行为**：读取三个文件，合并输出为本次工作上下文
  - `bugs.md`：全文读取
  - `todo.md`：全文读取
  - `completed.md`：通过 Python 脚本智能处理——≤40 行全文输出，>40 行则输出最近 3 次会话的完整条目 + 旧内容摘要

## 文件结构

### 项目目录下的 MEMORY 文件夹

```
<project-root>/
  MEMORY/
    completed.md
    bugs.md
    todo.md
```

### Skill 自身目录

```
E:\memory skill\
  SKILL.md          # 主 skill 文件
  scripts\
    read_completed.py  # 智能读取 completed.md 的脚本
```

## 文件模板

### completed.md

```markdown
# 已完成工作

## 2026-05-09
- [x] 功能/任务描述 — 关键细节
- [x] 另一个完成的任务

## 2026-05-08
- [x] ...
```

- 只追加，按日期分区
- 从不修改或删除已写内容

### bugs.md

```markdown
# Bug 记录

## 2026-05-09
- [已修复] Bug 简述 — 原因 & 解决方案
- [待修复] Bug 简述 — 影响范围

## 2026-05-08
- [已修复] ...
```

- 可追加新 bug
- 可更新已有 bug 的 tag（`[已修复]` / `[待修复]`）
- 保留所有历史记录

### todo.md

```markdown
# 待办事项

## 高优先级
- [ ] 任务描述

## 中优先级
- [ ] ...

## 低优先级 / 将来考虑
- [ ] ...
```

- 每次 `/update memory` 时完整重排
- 已完成的移除（或移至 completed.md）
- 新增待办加入
- 优先级动态调整

## read_completed.py 脚本

```python
# 读取 completed.md
# 按日期块（## YYYY-MM-DD）分割
# 如果总行数 ≤ 40：全文输出
# 如果 > 40：输出最近 3 个日期块的完整条目 + 对旧内容的摘要
```

## 关键技术决策

| 决策 | 选择 | 理由 |
|------|------|------|
| 实现方式 | 纯 SKILL.md + 可选脚本 | 零依赖，AI 擅长读写 Markdown |
| 文件格式 | Markdown | 人类可读，AI 易解析，版本控制友好 |
| 项目识别 | CWD（当前工作目录） | 简单直观，无需额外配置 |
| completed 阅读 | 智能截断（3 会话摘要） | 控制 token 消耗，保留关键上下文 |

## 未纳入范围

- 跨项目记忆聚合
- 自动触发（需用户手动调用命令）
- 图形界面或 web 展示
- 与 git 版本历史的自动关联：`completed.md` 的描述已足够 AI 理解上下文；查 git log 产生额外 token 开销，收益不足以抵消成本
