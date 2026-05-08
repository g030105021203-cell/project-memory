读取 `MEMORY/` 下的三个文件：

1. **MEMORY/bugs.md** — 全文读取
2. **MEMORY/todo.md** — 全文读取
3. **MEMORY/completed.md** — 使用脚本智能截断，执行以下命令读取：

   ```bash
   python scripts/read_completed.py
   ```

如 `MEMORY/` 不存在则提示用户"这是新项目，暂无 MEMORY"。输出时简要总结每个文件的关键信息。
