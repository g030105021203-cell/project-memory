更新 `MEMORY/` 下的三个文件，追加本次会话的新内容。

## 规则

1. **MEMORY/completed.md** — 只追加不删改：在文件末尾追加 `## YYYY-MM-DD` 标题和本次会话完成的条目
2. **MEMORY/bugs.md** — 追加新 Bug（`[待修复]`），可更新已有 Bug 的 `[已修复]`/`[待修复]` 状态 tag
3. **MEMORY/todo.md** — 完整重排：移除已完成的，新增待办的，按高/中/低优先级排序

如 `MEMORY/` 不存在则提示"请先运行 /create-memory"。

## 输出格式

```
[已更新] MEMORY/completed.md (+N 项)
[已更新] MEMORY/bugs.md (+N 个)
[已更新] MEMORY/todo.md (重排后共 N 项)
```
