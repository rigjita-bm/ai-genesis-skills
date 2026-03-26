# 🔄 Adaptive Carousel — Контекстное переключение

Система автоматически определяет бизнес-нишу и переключает дизайн + структуру слайдов.

## Как это работает

```
Пользователь пишет → Определяем нишу → Выбираем режим → Генерируем слайды
     ↓                      ↓                    ↓                   ↓
"У меня салон"      →    salon        →    lifestyle    →    Beauty-структура
"AI платформа"      →    tech_saas    →    startup     →    Tech-структура
"Веду блог"         →    creator      →    bold        →    Creator-структура
```

## Режимы и ниши

| Ниша | Ключевые слова | Режим | Цвет |
|------|----------------|-------|------|
| Салон красоты | салон, красота, маникюр, spa | **Essence** | `#D4A373` |
| Ресторан | ресторан, кафе, доставка, кухня | **Serenity** | `#7C9A92` |
| SaaS/AI | ai, saas, автоматизация, бот | **Velocity** | `#6366F1` |
| Консалтинг | консалтинг, бизнес, аудит | **Corporate** | `#1E3A5F` |
| Блогер | блог, контент, тикток, youtube | **Bold** | `#FF006E` |

## Использование в боте

```python
from carousel_switcher import handle_carousel_request

# В обработчике сообщений
result = handle_carousel_request(
    user_message="У меня салон красоты", 
    user_id=message.from_user.id
)

# Отправляем результат
await message.reply(f"""
🎯 Определена ниша: {result['niche']['name']}
🎨 Выбран режим: {result['design_mode']['name']}
📊 Сгенерировано слайдов: {len(result['slides'])}
""")
```

## Структуры слайдов по нишам

### Салон красоты (Essence)
1. **Hero** — "Ваша красота — наш приоритет"
2. **Problem** — Боль клиента
3. **Solution** — Онлайн-запись 24/7
4. **Benefits** — Экономия времени
5. **Social Proof** — 500+ клиентов
6. **CTA** — Записаться сейчас

### SaaS (Velocity)
1. **Hero** — "Масштабируйтесь без границ"
2. **Problem** — Ручные процессы тормозят
3. **Solution** — AI-автоматизация
4. **Stats** — 10x быстрее
5. **Integration** — 100+ интеграций
6. **CTA** — Запустить пилот

### Блогер (Bold)
1. **Hero** — "Выходи на новый уровень"
2. **Myth** — Разрушение мифа
3. **Truth** — Правда о росте
4. **Strategy** — Формула контента
5. **Transformation** — До/После
6. **CTA** — Присоединиться

## API

### `AdaptiveCarousel`

```python
from adaptive_carousel import AdaptiveCarousel

carousel = AdaptiveCarousel()

# Генерация с адаптацией
result = carousel.generate_adaptive_carousel(
    business_description="У меня салон красоты"
)

# Результат
{
    'niche': {
        'key': 'salon',
        'name': 'Салон красоты',
        'confidence': 1
    },
    'design_mode': {
        'key': 'lifestyle',
        'name': 'Essence',
        'palette': {...},
        'fonts': {...}
    },
    'slides': [
        {'number': 1, 'type': 'hero', 'title': '...', ...},
        ...
    ]
}
```

### `CarouselContextSwitcher`

```python
from carousel_switcher import carousel_switcher

# Определить и переключить
result = carousel_switcher.detect_and_switch(
    user_message="У меня салон",
    user_id=123456
)

# Получить сводку
summary = carousel_switcher.get_carousel_summary(user_id=123456)
```

## Тестирование

```bash
cd /root/.openclaw/skills/skills/carousel-pro

# Тест адаптивной карусели
python3 adaptive_carousel.py

# Тест переключателя
python3 carousel_switcher.py
```

## Файлы

- `adaptive_carousel.py` — Движок адаптации
- `carousel_switcher.py` — Интеграция с ботом
- `ADAPTIVE.md` — Эта документация
