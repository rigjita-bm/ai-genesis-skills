#!/usr/bin/env python3
"""
Post Generator v2.0 — AI-powered content creation
Uses Kimi API (Moonshot AI) — 4-8x cheaper than GPT-4, better Russian quality
"""

import os
import sys
import json
import argparse
import requests
from datetime import datetime

# Kimi API Configuration
KIMI_API_KEY = os.getenv("KIMI_API_KEY", "")
KIMI_API_URL = "https://api.moonshot.cn/v1/chat/completions"

# Check for API key
if not KIMI_API_KEY:
    # Fallback: try to use without key for demo mode
    DEMO_MODE = True
else:
    DEMO_MODE = False

# Platform configurations
PLATFORM_CONFIG = {
    "instagram": {
        "max_length": 2200,
        "optimal_length": 150,
        "style": "визуальный, эмоциональный, с эмодзи",
        "hashtag_count": "10-15",
        "cta": "в конце поста",
        "features": ["hook в первых 2 строках", "разрыв строк", "эмодзи", "hashtags внизу"]
    },
    "telegram": {
        "max_length": 4096,
        "optimal_length": 500,
        "style": "информативный, полезный, без перегрузки эмодзи",
        "hashtag_count": "3-5",
        "cta": "в середине или конце",
        "features": ["чёткая структура", "подзаголовки", "ссылки"]
    },
    "facebook": {
        "max_length": 63206,
        "optimal_length": 80,
        "style": "разговорный, вызывающий обсуждение",
        "hashtag_count": "1-2",
        "cta": "вопрос в конце",
        "features": ["короткий текст", "вопрос аудитории"]
    },
    "linkedin": {
        "max_length": 3000,
        "optimal_length": 200,
        "style": "профессиональный, экспертный, с фактами",
        "hashtag_count": "3-5",
        "cta": "призыв к дискуссии",
        "features": ["экспертный тон", "факты/данные", "разрывы строк"]
    }
}

# Tone presets
TONE_PRESETS = {
    "professional": "деловой, уверенный, экспертный тон. Профессиональная терминология",
    "casual": "неформальный, дружелюбный, как разговор с другом. Лёгкий язык",
    "storytelling": "нарративный, эмоциональный, через истории. Захватывающий стиль",
    "educational": "образовательный, структурированный, bullet points, чёткие выводы",
    "inspirational": "вдохновляющий, мотивирующий, позитивный посыл, призыв к действию",
    "urgent": "срочный, акцент на ограниченное время. FOMO-эффект"
}

# Business context for AI Genesis
BUSINESS_CONTEXT = """AI Genesis — автоматизация бизнеса для русскоязычных предпринимателей в NYC.
Услуги: цифровые администраторы, AI-ассистенты, автоматизация.
ЦА: владельцы малого бизнеса (салоны, ремонт, кафе, доставка).
Ценности: экономия времени, результат, прозрачные цены ($100/$350/$700/$1000).
Тон: экспертный но доступный, без занудства, фокус на пользу."""

# Template library for DEMO MODE
TEMPLATES = {
    "instagram": {
        "professional": """💼 Автоматизация бизнеса — это не роскошь, а необходимость в 2026.

Три процесса, которые стоит отдать AI прямо сейчас:

✅ Ответы на вопросы клиентов
✅ Запись и напоминания
✅ Сбор обратной связи

Результат: +10-15 часов в неделю для стратегии.

Стоимость пилота: $350
Окупаемость: 1-2 недели

Заинтересовало? Напишите "пилот" в комментариях 👇

#автоматизациябизнеса #аигенезис #предприниматели #бизнесньюйорк #айассистент""",
        "casual": """Ребята, честно — сколько часов в день вы тратите на ответы "а сколько стоит?" 😅

Я тоже так жил, пока не настроил бота.

Теперь:
• Клиенты записываются сами
• Напоминания приходят автоматом
• Я сплю, а бот работает

Лучшие $350, которые я потратил в бизнесе.

Кто ещё хочет так? 👇"""
    },
    "telegram": {
        "professional": """🤖 Автоматизация клиентского сервиса: пошаговый гайд

Большинство предпринимателей теряют 30% лидов из-за медленных ответов.

Вот как это исправить за неделю:

<b>Шаг 1: Аудит (день 1-2)</b>
Запишите все типовые вопросы клиентов за неделю. Обычно их 5-7.

<b>Шаг 2: Сценарии (день 3-4)</b>
Напишите ответы на каждый вопрос. Не идеально — достаточно хорошо.

<b>Шаг 3: Бот (день 5-7)</b>
Настройте Telegram-бота с этими сценариями. Тестируйте на себе.

<b>Результат:</b>
• Время ответа: с часов до секунд
• Конверсия: +20-40%
• Ваше время: +10 часов/неделю

<b>Инвестиции:</b> от $350 (пилот)
<b>Окупаемость:</b> 1-2 недели

Хотите такой же результат? Напишите "хочу пилот" — расскажу детали."""
    }
}


def generate_with_kimi(prompt, model="kimi-k2.5", temperature=0.7):
    """Generate content using Kimi API"""
    if DEMO_MODE:
        return None
    
    headers = {
        "Authorization": f"Bearer {KIMI_API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": temperature,
        "max_tokens": 2000
    }
    
    try:
        response = requests.post(KIMI_API_URL, headers=headers, json=data, timeout=60)
        response.raise_for_status()
        result = response.json()
        return result["choices"][0]["message"][content]
    except Exception as e:
        print(f"⚠️  Kimi API error: {e}")
        return None


def generate_post(topic, platform="instagram", tone="professional", variants=3):
    """Generate social media post"""
    config = PLATFORM_CONFIG[platform]
    tone_desc = TONE_PRESETS[tone]
    
    # Try API first
    if not DEMO_MODE:
        prompt = f"""Создай {variants} варианта поста для {platform} на тему: "{topic}"

Контекст бизнеса: {BUSINESS_CONTEXT}

Требования:
- Платформа: {platform}
- Стиль: {config['style']}
- Тон: {tone_desc}
- Оптимальная длина: {config['optimal_length']} символов
- CTA: {config['cta']}
- {', '.join(config['features'])}

Формат: раздели варианты маркером "---VARIANT---"
"""
        result = generate_with_kimi(prompt)
        if result:
            return result
    
    # Fallback to templates
    return get_template_post(platform, tone, topic)


def get_template_post(platform, tone, topic):
    """Get template-based post when API unavailable"""
    if platform in TEMPLATES and tone in TEMPLATES[platform]:
        template = TEMPLATES[platform][tone]
        # Simple topic substitution
        return template.replace("автоматизация", topic).replace("бизнеса", topic)
    
    # Generic fallback
    return f"""📝 {topic}

Интересует подробности? Напишите в комментариях 👇

#{topic.replace(' ', '')} #аигенезис #бизнес"""


def generate_content_calendar(days=7, focus="mixed"):
    """Generate content calendar"""
    calendar = []
    
    themes = {
        "automation": ["AI инструменты", "Автоматизация процессов", "Боты для бизнеса"],
        "case_studies": ["Кейс клиента", "До/После", "Отзыв"],
        "myths": ["Миф об AI", "Правда vs Ложь", "Что AI не может"],
        "mixed": ["AI инструменты", "Кейс клиента", "Миф об AI", "Совет дня", "Познавательное"]
    }
    
    selected_themes = themes.get(focus, themes["mixed"])
    
    for i in range(days):
        theme = selected_themes[i % len(selected_themes)]
        calendar.append({
            "day": i + 1,
            "theme": theme,
            "platform": "Instagram" if i % 2 == 0 else "Telegram",
            "format": "Carousel" if i % 3 == 0 else "Single post"
        })
    
    return calendar


def generate_caption(image_description, platform="instagram", tone="professional"):
    """Generate caption for image"""
    prompt = f"""Напиши подпись к изображению: "{image_description}"

Платформа: {platform}
Тон: {TONE_PRESETS[tone]}
Контекст: {BUSINESS_CONTEXT}

Требования:
- Хук в первой строке
- 2-3 абзаца максимум
- CTA в конце
- Подходящие хэштеги
"""
    
    if not DEMO_MODE:
        result = generate_with_kimi(prompt)
        if result:
            return result
    
    return f"✨ {image_description}\n\nЧто думаете? Делитесь в комментариях 👇\n\n#аигенезис #бизнес #автоматизация"


def save_output(content, filename=None):
    """Save output to file"""
    output_dir = "/root/.openclaw/output/posts"
    os.makedirs(output_dir, exist_ok=True)
    
    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"post_{timestamp}.txt"
    
    filepath = os.path.join(output_dir, filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return filepath


def main():
    parser = argparse.ArgumentParser(description='Post Generator — AI content creation')
    parser.add_argument('topic', nargs='?', help='Topic for the post')
    parser.add_argument('-p', '--platform', default='instagram', choices=PLATFORM_CONFIG.keys())
    parser.add_argument('-t', '--tone', default='professional', choices=TONE_PRESETS.keys())
    parser.add_argument('-v', '--variants', type=int, default=3)
    parser.add_argument('-l', '--language', default='ru', choices=['ru', 'en'])
    parser.add_argument('-s', '--save', action='store_true')
    parser.add_argument('-c', '--calendar', type=int, metavar='DAYS')
    parser.add_argument('--caption', action='store_true', help='Generate image caption')
    
    args = parser.parse_args()
    
    if DEMO_MODE:
        print("🎨 POST GENERATOR v2.0 (DEMO MODE)")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print("⚠️  KIMI_API_KEY не установлен")
        print("   Работаю в режиме шаблонов")
        print("   Для полной функциональности:")
        print("   export KIMI_API_KEY='your_key'")
        print()
    else:
        print("🎨 POST GENERATOR v2.0 (Kimi API)")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    
    if args.calendar:
        print(f"📅 Контент-календарь на {args.calendar} дней")
        calendar = generate_content_calendar(args.calendar)
        for item in calendar:
            print(f"\nДень {item['day']}: {item['theme']}")
            print(f"   Платформа: {item['platform']} | Формат: {item['format']}")
        return
    
    if args.caption:
        if not args.topic:
            print("❌ Укажите описание изображения")
            sys.exit(1)
        print(f"🖼️  Подпись для: {args.topic[:50]}...")
        caption = generate_caption(args.topic, args.platform, args.tone)
        print("\n" + caption)
        if args.save:
            filepath = save_output(caption, f"caption_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
            print(f"\n💾 Сохранено: {filepath}")
        return
    
    if not args.topic:
        parser.print_help()
        sys.exit(1)
    
    print(f"📝 Генерирую {args.variants} варианта для {args.platform}")
    print(f"   Тема: {args.topic}")
    print(f"   Тон: {args.tone}")
    print()
    
    result = generate_post(args.topic, args.platform, args.tone, args.variants)
    
    if "---VARIANT---" in result:
        variants = result.split("---VARIANT---")
        for i, variant in enumerate(variants[:args.variants], 1):
            print(f"\n{'='*50}")
            print(f"ВАРИАНТ {i}")
            print('='*50)
            print(variant.strip())
    else:
        print(result)
    
    if args.save:
        filepath = save_output(result, f"post_{args.platform}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
        print(f"\n💾 Сохранено: {filepath}")


if __name__ == "__main__":
    main()
