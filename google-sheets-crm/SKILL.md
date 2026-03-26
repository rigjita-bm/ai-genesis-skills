# Google Sheets CRM

CRM система на Google Sheets с дедупликацией лидов и автоматическими follow-up.

## Возможности

- ✅ **Дедупликация** — проверка по телефону/email перед добавлением
- ✅ **Приоритеты** — 🔴 HOT / 🟡 WARM / 🔵 COLD авто-определение
- ✅ **Follow-up серии** — автоматические напоминания 24ч/72ч/7дн
- ✅ **Горячие лиды** — фильтрация и уведомления владельцу
- ✅ **Извлечение данных** — авто-парсинг из текста сообщения
- ✅ **Fallback** — локальное хранилище при проблемах с Google

## Установка

```bash
pip install gspread google-auth --break-system-packages
```

## Настройка Google Sheets API

1. Перейдите в [Google Cloud Console](https://console.cloud.google.com/)
2. Создайте проект → APIs & Services → Credentials
3. Create Credentials → Service Account
4. Создайте ключ JSON → скачайте файл
5. Переименуйте в `google-sheets-credentials.json`
6. Поместите в `/root/.openclaw/config/`
7. Поделитесь Google Sheet с email сервисного аккаунта

## Переменные окружения

```bash
export GOOGLE_SHEETS_CREDENTIALS=/root/.openclaw/config/google-sheets-credentials.json
export CRM_SPREADSHEET_ID=your_spreadsheet_id_here  # Опционально
```

## Использование

### CLI

```bash
# Добавить лид
python google_sheets_crm.py add "Анна, +7 999 123-45-67, anna@email.com, интересна автоматизация"

# Проверить дубликат
python google_sheets_crm.py check +79991234567
python google_sheets_crm.py check anna@email.com

# Показать горячие лиды
python google_sheets_crm.py hot

# Показать ожидающие follow-up
python google_sheets_crm.py pending

# Обновить лид
python google_sheets_crm.py update LD202403231234 status=CONVERTED priority=🔴 HOT
```

### Python API

```python
from google_sheets_crm import GoogleSheetsCRM, extract_lead_info

# Инициализация
crm = GoogleSheetsCRM()

# Извлечь данные из текста
lead_data = extract_lead_info("Иван, +7 999 123-45-67, хочу автоматизацию")

# Добавить лид (с автоматической проверкой дубликатов)
result = crm.add_lead(lead_data)
print(result['message'])

# Получить горячие лиды
hot_leads = crm.get_hot_leads()

# Обновить лид
crm.update_lead('LD202403231234', {'status': 'CONVERTED'})
```

## Структура данных

### Leads Sheet

| Колонка | Описание |
|---------|----------|
| ID | Уникальный ID (LD + timestamp) |
| Date Added | Дата добавления |
| Source | Источник (telegram, email, etc) |
| Name | Имя контакта |
| Phone | Телефон |
| Email | Email |
| Company | Компания |
| Status | Статус (NEW, CONTACTED, CONVERTED, LOST) |
| Priority | Приоритет (🔴 HOT, 🟡 WARM, 🔵 COLD) |
| Last Contact | Последний контакт |
| Notes | Заметки |
| Follow-up 24h | Дата follow-up через 24ч |
| Follow-up 72h | Дата follow-up через 72ч |
| Follow-up 7d | Дата follow-up через 7 дней |
| Owner Notified | Уведомлён ли владелец |

## Авто-определение приоритета

| Приоритет | Ключевые слова |
|-----------|----------------|
| 🔴 HOT | горячий, hot, срочно, urgent, куплю сейчас |
| 🟡 WARM | заинтересован, interested, хочу, цена |
| 🔵 COLD | остальные |

## Follow-up серия

При добавлении лида автоматически планируются:

1. **+24 часа** — проверка вопросов
   > "Привет! Остались вопросы по AI-ассистенту?"

2. **+72 часа** — полезный факт
   > "Кстати: наши клиенты экономят 15+ часов в неделю"

3. **+7 дней** — финальное сообщение
   > "Последний шанс получить скидку 20% на пилот"

## Интеграция с ботом

```python
# В обработчике сообщений бота
if "сохранить лид" in text.lower():
    from google_sheets_crm import GoogleSheetsCRM, extract_lead_info
    
    crm = GoogleSheetsCRM()
    lead_data = extract_lead_info(text)
    result = crm.add_lead(lead_data)
    
    if result['success']:
        send_message(chat_id, f"✅ Лид сохранён!\nID: {result['lead']['id']}")
        
        # Если горячий лид — уведомить владельца
        if result['lead']['priority'] == '🔴 HOT':
            notify_owner(result['lead'])
    else:
        send_message(chat_id, result['message'])
```

## Архитектура

```
google-sheets-crm/
├── google_sheets_crm.py    # Основной модуль
├── SKILL.md               # Документация
└── config/
    └── google-sheets-credentials.json  # API ключ
```

## Fallback Mode

Если Google Sheets недоступен:
- Данные сохраняются в `/tmp/crm_local_backup.json`
- При восстановлении соединения — миграция в Sheets
- Нет потери данных

## Безопасность

- API ключ хранится вне репозитория
- Доступ только к нужным scopes (sheets + drive)
- Service Account с ограниченными правами
