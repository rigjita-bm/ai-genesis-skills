# Cron Scheduler + Follow-up System

Manage scheduled tasks and automated follow-ups for AI Genesis leads.

## Modules

### 1. `cron_scheduler.py` — Core Scheduler
Legacy scheduler for basic task management.

### 2. `followup_scheduler.py` — 3-Touch Follow-up System ⭐ NEW
Dedicated module for CRM follow-up automation.

---

## 3-Touch Follow-up System

### Touch 1: +24 hours (Value)
**Business:**
```
Привет! Остались вопросы по AI-ассистенту?

Я могу:
• Уточнить детали под вашу ситуацию
• Рассчитать конкретную экономию времени
• Показать пример из вашей ниши

Что приоритетнее?
```

**Wellness:**
```
Привет! Как ваше самочувствие?

Есть вопросы по протоколу?
• Подбор под ваши цели
• Совместимость с добавками
• Оптимальный график приёма

Напишите — подскажу.
```

### Touch 2: +72 hours (Social Proof)
**Business:**
```
Кстати, интересный факт:

Наши клиенты экономят 15+ часов в неделю на рутине.
Это 720 часов в год = 18 рабочих недель!

Хотите такой же результат?
```

**Wellness:**
```
Кстати, факт дня:

73% людей чувствуют прирост энергии на 3-й день
правильного протокола.

У вас уже есть опыт с добавками или только начинаете?
```

### Touch 3: +7 days (Close/Urgency)
**Business:**
```
Финальное сообщение:

Предложение недели: скидка 20% на пилот ($350 → $280)
• Действует до [date]
• Включает полную настройку
• Работает 30 дней

Начнём на этой неделе или пока рано?
```

**Wellness:**
```
Последний шанс этого месяца:

Протокол со скидкой 20%
• Чай Долголетие: $100 → $80
• Anti-Age Pro: $150 → $120

Предложение до [date]. Забронировать?
```

---

## Commands

### Follow-up Scheduler CLI

```bash
# Schedule 3-touch follow-up for a lead
python3 followup_scheduler.py schedule <lead_id> <contact> [category] [product]

# View pending follow-ups (due now)
python3 followup_scheduler.py pending

# Process and send all due follow-ups
python3 followup_scheduler.py process

# Cancel follow-up series (lead converted)
python3 followup_scheduler.py cancel <lead_id>

# View statistics
python3 followup_scheduler.py stats
```

### Legacy Cron Commands

```bash
# View today's tasks
genesis cron today

# View upcoming tasks (next N days)
genesis cron upcoming 3

# View pending tasks (next 24h)
genesis cron pending

# Execute task manually
genesis cron execute "task_id"
```

---

## Integration

### With google-sheets-crm

```python
from google_sheets_crm import GoogleSheetsCRM
from followup_scheduler import FollowUpScheduler

# When adding a lead
crm = GoogleSheetsCRM()
result = crm.add_lead(lead_data)

if result['success']:
    # Auto-schedule follow-up
    scheduler = FollowUpScheduler()
    scheduler.schedule_followup(
        lead_id=result['lead']['id'],
        contact=result['lead']['phone'] or result['lead']['email'],
        category='business',  # or 'wellness'
        product='AI Automation'  # optional
    )
```

### Python API

```python
from followup_scheduler import FollowUpScheduler

scheduler = FollowUpScheduler()

# Schedule 3-touch series
result = scheduler.schedule_followup(
    lead_id="LD20240323123456",
    contact="+79991234567",
    category="business",  # or "wellness"
    product="AI Automation"
)

# Get pending follow-ups
pending = scheduler.get_pending()

# Process due follow-ups
def send_message(item):
    # Your send logic here
    print(f"Sending {item['stage']} to {item['contact']}")

processed = scheduler.process_due(send_callback=send_message)

# Cancel if lead converted
scheduler.cancel_followup("LD20240323123456")

# Get stats
stats = scheduler.get_stats()
```

---

## Files

| File | Purpose |
|------|---------|
| `cron_scheduler.py` | Legacy task scheduler |
| `followup_scheduler.py` | 3-touch follow-up system |
| `/tmp/followup_queue.json` | Follow-up queue storage |
| `/tmp/crm_local_backup.json` | Lead data (CRM fallback) |

---

## Automation

### Crontab (every hour)

```bash
# Check and send follow-ups every hour
0 * * * * python3 /root/.openclaw/skills/skills/cron-scheduler/followup_scheduler.py process >> /var/log/followup.log 2>&1
```

### OpenClaw Cron (recommended)

```python
# Add hourly follow-up check
cron.add(
    name="followup-processor",
    schedule="0 * * * *",
    command="python3 /root/.openclaw/skills/skills/cron-scheduler/followup_scheduler.py process"
)
```

---

## Data Structure

```json
{
  "lead_id": "LD20240323123456",
  "contact": "+79991234567",
  "category": "business",
  "product": "AI Automation",
  "created_at": "2024-03-23T10:30:00",
  "status": "active",
  "touches": [
    {
      "stage": "24h",
      "scheduled_at": "2024-03-24T10:30:00",
      "sent": true,
      "sent_at": "2024-03-24T10:35:00",
      "template": "Привет! Остались вопросы..."
    },
    {
      "stage": "72h",
      "scheduled_at": "2024-03-26T10:30:00",
      "sent": false,
      "sent_at": null,
      "template": "Кстати, интересный факт..."
    },
    {
      "stage": "7d",
      "scheduled_at": "2024-04-01T10:30:00",
      "sent": false,
      "sent_at": null,
      "template": "Финальное сообщение..."
    }
  ]
}
```

---

## Statistics

```
📊 Follow-up статистика:
   Всего серий: 45
   Активных: 12
   Отменено: 8
   Завершено: 25
   Ожидает отправки: 3
```

---

## Best Practices

1. **Auto-schedule on lead creation** — Don't forget to schedule
2. **Cancel on conversion** — Stop follow-up when lead buys
3. **Personalize templates** — Use {name}, {product} variables
4. **Track responses** — Mark replied leads for human handoff
5. **Review stats weekly** — Optimize timing and content
