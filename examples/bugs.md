# Bug 记录

## 2026-05-09
- [已修复] 登录页 500 错误 — 空邮箱提交时 Zod 校验未触发，因 form 的 onSubmit 未正确包裹 validate
- [待修复] 仪表盘图表在 Safari 下不渲染 — ECharts 版本兼容问题，影响所有 macOS 用户

## 2026-05-07
- [已修复] 导出 CSV 中文乱码 — 缺少 BOM 头，在 response header 加 `﻿`
