# Carousel Mode Router

Интеллектуальный агент для автоматического выбора режима дизайна Carousel на основе анализа темы, аудитории и контекста.

## 🚀 Быстрый старт

```bash
cd /root/.openclaw/skills/skills/carousel-pro

# Анализ темы
python3 carousel_router.py "AI автоматизация для бизнеса"

# С контекстом
python3 carousel_router.py "Йога для начинающих" "аудитория: женщины 25-40"
```

## 🎨 Как работает роутер

### 4 уровня анализа:

| Уровень | Вес | Что анализирует |
|---------|-----|-----------------|
| **Keywords** | 40% | Ключевые слова в теме |
| **Industry** | 25% | Принадлежность к индустрии |
| **Tone** | 20% | Тональность заголовка |
| **Audience** | 15% | Целевая аудитория |

### Пример работы:

```
Тема: "AI автоматизация для бизнеса"

🎨 Рекомендуемый режим: Velocity (66% уверенность)

Почему:
  • Ключевые слова: ai, automation, business
  • Индустрия: technology
  • Тональность: техническая

Характеристики:
• Цвета: gradient, purple, pink
• Шрифты: geometric, space grotesk
• Эмоции: excitement, innovation, speed

🔄 Альтернативы:
  • Executive (15%) — если аудитория enterprise
  • Essence (5%) — если для креативной индустрии
```

## 📊 Режимы и триггеры

### 🏢 Executive (corporate)
**Триггеры:** `финансы`, `юридические`, `консалтинг`, `b2b`, `enterprise`

```bash
python3 carousel_router.py "Юридические услуги для бизнеса"
# → Executive (85%)
```

### 🚀 Velocity (startup)
**Триггеры:** `saas`, `ai`, `app`, `tech`, `automation`, `digital`

```bash
python3 carousel_router.py "Новый AI-продукт"
# → Velocity (92%)
```

### ✨ Essence (lifestyle)
**Триггеры:** `fashion`, `beauty`, `travel`, `food`, `style`, `luxury`

```bash
python3 carousel_router.py "Luxury skincare routine"
# → Essence (78%)
```

### 🌿 Serenity (wellness)
**Триггеры:** `yoga`, `health`, `wellness`, `meditation`, `organic`, `fitness`

```bash
python3 carousel_router.py "Медитация для снятия стресса"
# → Serenity (88%)
```

### 🔥 Bold (creator)
**Триггеры:** `coach`, `creator`, `business coach`, `мотивация`, `success`

```bash
python3 carousel_router.py "Как стать миллионером за 30 дней"
# → Bold (95%)
```

## 🔧 Интеграция с Carousel Pro

### Вариант 1: CLI через роутер

```bash
# Сначала определяем режим
MODE=$(python3 carousel_router.py "Тема" | grep "Рекомендуемый режим" | awk '{print $3}' | tr '[:upper:]' '[:lower:]')

# Потом генерируем карусель
python3 carousel_pro.py "Тема" --mode $MODE --export png
```

### Вариант 2: Python импорт

```python
from carousel_router import CarouselModeRouter
from carousel_pro import CarouselPro

router = CarouselModeRouter()
carousel = CarouselPro()

# Анализируем тему
match = router.analyze("AI для ресторанного бизнеса")
print(f"Рекомендуемый режим: {match.mode} ({int(match.confidence * 100)}%)")

# Генерируем с выбранным режимом
result = carousel.generate_carousel(
    topic="AI для ресторанного бизнеса",
    mode_name=match.mode
)
```

### Вариант 3: Telegram Bot команда

```python
# Добавить в бота:
/carousel_auto "Тема" [контекст]

# Пример:
/carousel_auto "Йога курсы" "для беременных"
# → Бот сам выбирает режим (Serenity) и генерирует карусель
```

## 📈 Точность роутера

| Тип темы | Точность | Примеры |
|----------|----------|---------|
| Технологии | 90%+ | AI, SaaS, Apps |
| Wellness | 85%+ | Yoga, Health, Meditation |
| Coaching | 88%+ | Business coach, Motivation |
| Fashion/Lifestyle | 82%+ | Beauty, Travel, Food |
| B2B Services | 80%+ | Legal, Finance, Consulting |

## 🛠️ API Router

### `analyze(topic, context)`
```python
match = router.analyze(
    topic="AI автоматизация",
    context="для малого бизнеса"
)
# ModeMatch(mode='startup', confidence=0.85, reasons=[...])
```

### `get_recommendation(topic, context)`
Возвращает красивую текстовую рекомендацию.

### `get_alternative_modes(topic, context, top_n=2)`
Возвращает топ-N альтернативных режимов.

## 📁 Файлы

- `carousel_router.py` — главный роутер
- `carousel_pro.py` — генератор каруселей
- `modes/` — режимы дизайна

**Path**: `/root/.openclaw/skills/skills/carousel-pro/`
