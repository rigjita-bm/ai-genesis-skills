# Coding Agent — Claude Code Integration

AI-powered coding assistant for AI Genesis with reliability, quality gates, and cost control.

## What It Does

- **Phase 1: Reliability** — 10-min timeout, auto-restart, auto-save every 60 sec
- **Phase 2: Quality Gates** — flake8 lint, mypy types, syntax check
- **Phase 3: Smart Routing** — Complex → Claude, Simple → Kimi API
- **Phase 4: Cost Control** — $20 budget, alerts at 75%, usage tracking

## Commands

```bash
# Execute coding task
genesis code "Напиши парсер CSV в JSON"
genesis code "Исправь баг в bot_v10.py"

# Check system health
genesis code health

# Check budget
genesis code budget

# View cost report
genesis code report 7

# Assess task complexity (dry run)
genesis code route "Создай API endpoint"

# Check code quality
genesis code quality /path/to/file.py
```

## Approval Levels

| Level | Lines | Complexity | Action |
|-------|-------|------------|--------|
| **auto** | < 50 | Low | ✅ Auto-approve |
| **medium** | 50-200 | Moderate | ⏸️ Review recommended |
| **complex** | > 200 | High | 🛑 Mandatory review |

## Cost Tracking

- **Limit:** $20/day
- **Alert:** At $15 (75%)
- **Auto-switch:** To Kimi API when budget exhausted
- **Rate:** ~$0.008 per 1K tokens (Claude 3.5 Sonnet)

## Smart Routing Logic

Routes to **Claude** if:
- Complexity score > 0.6
- Keywords: architecture, API, database, integration, async
- Estimated lines > 100

Routes to **Kimi** if:
- Simple fixes (< 50 lines)
- Typos, renames, comments
- Low complexity (< 0.4)

## Files

- `coding_agent.py` — Main controller (all 4 phases)
- `/tmp/claude_sandbox/` — Sandbox for code execution
- `/root/.openclaw/coding_sessions/` — Session logs
- `/root/.openclaw/coding_costs.json` — Cost tracking

## Integration

Works with:
- `tmux` skill — For background sessions
- `cron-scheduler` — Health checks every 5 min
- `file-writer` — Save generated code

## Auto-health Check

Add to crontab for automatic monitoring:

```bash
*/5 * * * * python3 /root/.openclaw/skills/skills/coding-agent/coding_agent.py health > /dev/null 2>&1
```

## Example Output

```
🚀 Запускаю Claude Code...
📋 Задача: Напиши функцию для парсинга email...
⏱️ Таймаут: 10 минут

[Generated code here...]

✅ Quality Gate: PASSED (Simple: 45 lines, low complexity)

============================================================
⏱️ Длительность: 45.2 сек
💰 Стоимость: $0.0123
💳 Бюджет сегодня: $3.45/$20
🛡️ Уровень одобрения: AUTO
```
