---
name: project-memory
description: Use when managing long-term project memory across Claude Code sessions — create/update/read MEMORY folder with completed work, bugs, and todo items for project continuity
---

# Project Memory Skill

在项目根目录下维护 `MEMORY/` 文件夹，记录已完成工作、Bug 和待办事项，实现跨会话的项目记忆。

## 文件模板

以下三个文件统一放在项目根目录的 `MEMORY/` 文件夹中。

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
- 永不修改或删除已写内容

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
- 可更新已有 bug 的状态 tag（`[已修复]` / `[待修复]`）
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

- 每次更新时完整重排
- 已完成的移除（或移至 completed.md）
- 新增待办加入
- 优先级动态调整

---

## /create memory — 创建项目记忆

**触发时机：** 新项目第一次会话结束时

**行为：**
1. 在 `CWD/MEMORY/` 创建三个文件
2. 根据本次会话内容填充：
   - `completed.md` — 本次完成的所有工作
   - `bugs.md` — 本次遇到的 bug
   - `todo.md` — 下一步需要做的事
3. 如 `MEMORY/` 已存在则提示用户，不覆盖

**示例输出：**
```
[已创建] MEMORY/completed.md (3 项已完成工作)
[已创建] MEMORY/bugs.md (1 个 bug 记录)
[已创建] MEMORY/todo.md (5 项待办)
```

---

## /update memory — 更新项目记忆

**触发时机：** 第二次及以后的会话结束时

**行为：**
1. 读取 `CWD/MEMORY/` 下现有三个文件
2. 追加本次会话的新内容：
   - `completed.md` — 在末尾追加新的日期块，不删不改旧内容
   - `bugs.md` — 追加新 bug，更新已有 bug 的 tag 状态
   - `todo.md` — **完整重排**：移除已完成、新增待办、调整优先级
3. 如果 `MEMORY/` 不存在，提示先运行 `/create memory`

---

## /read memory — 读取项目记忆

**触发时机：** 会话开始时（首次或后续）

**行为：**
1. 检查 `CWD/MEMORY/` 是否存在
2. 如不存在 → 提示用户是新项目，建议运行 `/create memory`
3. 如存在 → 读取三个文件：
   - `bugs.md` — 全文直接读取
   - `todo.md` — 全文直接读取
   - `completed.md` — 调用脚本智能读取：
     - 如果 `E:\memory skill\scripts\read_completed.py` 存在，用脚本处理
     - 如果脚本不存在或出错，全文直接读取
4. 将合并结果作为本次工作的上下文

---

## 注意事项

- 所有文件使用 Markdown 格式，UTF-8 编码
- 日期格式统一为 `YYYY-MM-DD`
- `read_completed.py` 脚本位于 `E:\memory skill\scripts\read_completed.py`，无需安装额外依赖
