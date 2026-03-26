---
name: notion-sync
description: Sync AI Genesis skills inventory with Notion CRM database
version: 1.0.0
---

# Notion Sync

Синхронизация инвентаря скиллов AI Genesis с базой данных Notion.

## Features

- Автоматическая синхронизация всех скиллов в Notion
- Отслеживание статуса, рейтинга и категорий
- Документирование автоматизаций для клиентов
- Метаданные: пути, описания, цены

## Usage

```bash
# Full sync all skills
./sync_skills.sh

# Or use genesis CLI
genesis sync skills
```

## Database Schema

**AI Genesis Skills** (Notion Database)

| Property | Type | Options |
|----------|------|---------|
| Name | Title | - |
| Category | Select | Автоматизация, Контент, Аналитика, CRM, Утилиты |
| Status | Select | Активен, В разработке, Архив |
| Tier | Select | Базовый, Пилот, Полный |
| Price | Number | $USD |
| Rating | Number | 1-10 |
| File Path | Rich Text | /skills/{name}/ |
| Description | Rich Text | - |

## Database Info

- **Database ID**: `6469b63d-5e4f-4429-966d-3b0f94fe6df4`
- **URL**: https://www.notion.so/6469b63d5e4f4429966d3b0f94fe6df4
- **Location**: AI Genesis page

## Current Skills (12 total)

| Skill | Category | Tier | Rating |
|-------|----------|------|--------|
| Proposal Generator | Автоматизация | Полный | 10 |
| Post Generator | Контент | Полный | 10 |
| Email Sequence | Автоматизация | Пилот | 10 |
| Carousel Pro | Контент | Пилот | 9 |
| Competitive Intel | Аналитика | Полный | 10 |
| Client Onboarding | CRM | Базовый | 9 |
| Lead Scoring | CRM | Пилот | 9 |
| Content Strategist | Контент | Полный | 9 |
| Objection Handler | CRM | Базовый | 8 |
| Followup System | Автоматизация | Пилот | 9 |
| Notion Sync | Утилиты | Полный | 10 |
| Cron Scheduler | Утилиты | Базовый | 9 |

## API

```bash
NOTION_KEY=$(cat ~/.config/notion/api_key)
DB_ID="6469b63d-5e4f-4429-966d-3b0f94fe6df4"

# Query all skills
curl -X POST "https://api.notion.com/v1/databases/$DB_ID/query" \
  -H "Authorization: Bearer $NOTION_KEY" \
  -H "Notion-Version: 2025-09-03"
```

## Files

- `sync_skills.sh` — Main sync script
- `SKILL.md` — This documentation
