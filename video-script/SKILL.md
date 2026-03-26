# Video Script Generator

Генератор сценариев для коротких видео (Reels, TikTok, Shorts) с A/B вариантами.

## Возможности

- ✅ **A/B тестирование** — эмоциональный vs рациональный подход
- ✅ **Мульти-платформа** — Reels (60с), TikTok (45с), Shorts (60с)
- ✅ **Хронометраж** — разбивка по времени с визуальными подсказками
- ✅ **Авто-хуки** — цепляющие начала под тему
- ✅ **CTA варианты** — разные призывы к действию
- ✅ **Хештеги** — автоподбор под категорию

## Использование

### CLI

```bash
# Базовый сценарий
python video_script.py "AI Automation"

# Для конкретной платформы
python video_script.py "AI Automation" --platform tiktok
python video_script.py "AI Automation" --platform shorts

# Wellness категория
python video_script.py "Здоровый сон" --category wellness

# Сохранить в JSON
python video_script.py "AI Automation" --format json --output my_script.json
```

### Python API

```python
from video_script import VideoScriptGenerator

# Создать генератор
gen = VideoScriptGenerator(
    topic="AI Automation",
    platform="reels",      # reels | tiktok | shorts
    category="business"    # business | wellness
)

# Получить оба варианта
script = gen.generate_ab_variants()

# Только эмоциональный
emotional = gen.generate_script("emotional")

# Только рациональный
rational = gen.generate_script("rational")

# Сохранить в файл
path = gen.export("/path/to/output.json")
```

## Структура сценария

### Вариант A (Emotional)

```
HOOK (0-3 сек)
💬 Личная история / эмоциональный вызов
🎥 Крупный план / эмоциональный кадр

BODY
⏱️ 0:05 — Моя история началась...
⏱️ 0:15 — Я пробовала всё...
⏱️ 0:25 — Пока не нашла ЭТО
⏱️ 0:35 — Результат через 30 дней

CTA (55-60 сек)
💬 Начните свой путь сегодня...
```

### Вариант B (Rational)

```
HOOK (0-3 сек)
💬 Факт / статистика / вопрос
🎥 График / схема / текст

BODY
⏱️ 0:05 — Проблема: 80%...
⏱️ 0:15 — Причина: плохая...
⏱️ 0:30 — Решение: правильная...
⏱️ 0:45 — Результат: 95%...

CTA (55-60 сек)
💬 Получите бесплатную консультацию...
```

## Форматы контента

| Формат | Длительность | Особенности |
|--------|--------------|-------------|
| **Reels** | 60 сек | Trending audio, 3-5 хештегов |
| **TikTok** | 45 сек | Зацепка за 2 сек, субтитры |
| **Shorts** | 60 сек | End screen, ссылки в описании |

## Категории

### Business
- Автоматизация
- Предпринимательство
- Продуктивность
- Маркетинг

### Wellness
- Здоровье
- Добавки
- Питание
- Фитнес

## Интеграция с ботом

```python
if "видео" in text or "сценарий" in text:
    from video_script import VideoScriptGenerator
    
    # Определить платформу
    platform = "reels"
    if "тикток" in text or "tiktok" in text:
        platform = "tiktok"
    elif "шортс" in text or "shorts" in text:
        platform = "shorts"
    
    # Определить категорию
    category = "business"
    if any(w in text for w in ["здоровье", "wellness"]):
        category = "wellness"
    
    # Генерация
    gen = VideoScriptGenerator(topic, platform, category)
    output = gen.format_for_display()
    
    send_message(chat_id, output)
```

## JSON Output Structure

```json
{
  "topic": "AI Automation",
  "platform": "reels",
  "category": "business",
  "created_at": "2024-03-23T10:30:00",
  "variant_a": {
    "variant": "emotional",
    "duration": 60,
    "hook": {...},
    "body": [...],
    "cta": {...},
    "captions": "..."
  },
  "variant_b": {
    "variant": "rational",
    ...
  },
  "recommendations": [...]
}
```

## A/B Testing Tips

### Когда использовать Emotional?
- Личные бренды
- Wellness продукты
- Премиум услуги
- Истории трансформации

### Когда использовать Rational?
- B2B продукты
- Технические решения
- Цена/качество
- Образовательный контент

### Метрики для сравнения
- Watch time (удержание)
- CTR (клики по ссылке)
- Saves (сохранения)
- Shares (поделились)
