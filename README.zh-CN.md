# Hermes Durable Skills

让 Codex、Claude Code、Cursor、Hermes Agent 等编码 Agent 的长任务在**上下文丢失、中断、切换模型或换人接手后仍然可恢复、可验收**。

> Chat 只是工作缓存。任务状态写入仓库。Agent 的“完成了”不是验收证据。

## 解决三个问题

1. **任务跑偏**：`durable-task` 在执行前固定目标、范围、非目标、约束和验收标准。
2. **中断后重来**：`checkpoint-resume` 保存当前阶段、已完成步骤和唯一下一步。
3. **假完成**：`evidence-gate` 要求把每条验收标准映射到测试、命令、Diff、文件或人工检查证据。

## 快速开始

```bash
git clone https://github.com/wookzzz57-beep/hermes-skills.git
cd hermes-skills
python -m pip install .
```

初始化一个任务：

```bash
hermes-durable init feature-42 \
  --objective "修复结账回归并保持现有 API 行为" \
  --scope "src/checkout" \
  --non-goal "重构支付模块" \
  --accept "相关单元测试通过" \
  --accept "结账 smoke test 通过"
```

记录证据并检查：

```bash
hermes-durable evidence feature-42 \
  --kind test \
  --summary "checkout tests passed" \
  --command "pytest tests/checkout -q" \
  --result "exit 0"

hermes-durable verify feature-42
```

状态默认保存在：

```text
.agent/tasks/<task_id>/
├── task.json
├── checkpoint.json
└── evidence.jsonl
```

## 安装 Skills

把需要的目录复制到你的 Agent skills 路径：

```bash
cp -R skills/durable-task ~/.codex/skills/
cp -R skills/checkpoint-resume ~/.codex/skills/
cp -R skills/evidence-gate ~/.codex/skills/
```

Hermes Agent 可复制到 `~/.hermes/skills/`。其他支持 `SKILL.md` 的客户端使用其对应 skills 目录。

## 设计原则

- Capability before complexity
- Durable state before long-chat memory
- Evidence before completion
- Resume instead of replay
- Provider-neutral core
- 不把 secrets 写入持久状态

## License

MIT
