请在当前项目创建 MEMORY 文件夹及其三个文件。

## 规则

- 如 `MEMORY/` 已存在则跳过，提示用户"MEMORY 已存在"
- 根据本次会话内容填充文件
- 使用以下模板：

### MEMORY/completed.md

```markdown
# 已完成工作

## YYYY-MM-DD
- [x] 功能描述 — 关键细节
```

### MEMORY/bugs.md

```markdown
# Bug 记录

## YYYY-MM-DD
- [待修复] 问题 — 影响范围
```

### MEMORY/todo.md

```markdown
# 待办事项

## 高优先级
- [ ] 任务

## 中优先级
- [ ] 任务
```

## 输出格式

```
[已创建] MEMORY/completed.md (N 项已完成工作)
[已创建] MEMORY/bugs.md (N 个 bug 记录)
[已创建] MEMORY/todo.md (N 项待办)
```
