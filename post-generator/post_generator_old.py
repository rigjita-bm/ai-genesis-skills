#!/usr/bin/env python3
"""
Post Generator — AI-powered content creation for social media
Uses OpenAI GPT-4 for generating platform-optimized posts
"""

import os
import sys
import json
import argparse
from datetime import datetime

# Try to import openai
try:
    from openai import OpenAI
except ImportError:
    print("⚠️  OpenAI не установлен. Установка...")
    print("   pip install openai --break-system-packages")
    sys.exit(1)

# Platform configurations
PLATFORM_CONFIG = {
    "instagram": {
        "max_length": 2200,
        "optimal_length": 150,
        "style": "визуальный, эмоциональный, с эмодзи",
        "hashtag_count": "10-15",
        "cta": "в конце поста"
    },
    "telegram": {
        "max_length": 4096,
        "optimal_length": 500,
        "style": "информативный, полезный, без перегрузки эмодзи",
        "hashtag_count": "3-5",
        "cta": "в середине или конце"
    },
    "facebook": {
        "max_length": 63206,
        "optimal_length": 80,
        "style": "разговорный, вызывающий обсуждение",
        "hashtag_count": "1-2",
        "cta": "вопрос в конце"
    },
    "linkedin": {
        "max_length": 3000,
        "optimal_length": 200,
        "style": "профессиональный, экспертный, с фактами",
        "hashtag_count": "3-5",
        "cta": "призыв к дискуссии"
    }
}

# Tone presets
TONE_PRESETS = {
    "professional": "деловой, уверенный, экспертный тон. Используйте профессиональную терминологию",
    "casual": "неформальный, дружелюбный, как разговор с другом. Лёгкий и доступный язык",
    "storytelling": "нарративный, эмоциональный, через истории и примеры. Захватывающий стиль",
    "educational": "образовательный, структурированный, с bullet points и чёткими выводами",
    "inspirational": "вдохновляющий, мотивирующий, с позитивным посылом и призывом к действию",
    "urgent": "срочный, с акцентом на ограниченное время или возможность. FOMO-эффект"
}

# Business context for AI Genesis
BUSINESS_CONTEXT = """AI Genesis — компания по автоматизации бизнеса для русскоязычных предпринимателей в Нью-Йорке.
Услуги: цифровые администраторы, автоматизация процессов, AI-ассистенты.
Целевая аудитория: владельцы малого бизнеса (салоны красоты, ремонт квартир, доставка, кафе).
Ценности: экономия времени, профессионализм, результат, понятные цены ($100/$350/$700/$1000).
Тон: экспертный но доступный, без занудства, с фокусом на пользу."""


def get_openai_client():
    """Initialize OpenAI client with API key from environment"""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ Ошибка: OPENAI_API_KEY не найден")
        print("   Установите переменную окружения:")
        print("   export OPENAI_API_KEY='sk-...'")
        sys.exit(1)
    return OpenAI(api_key=api_key)


def generate_post(topic, platform="instagram", tone="professional", variants=3, language="ru"):
    """Generate social media post using OpenAI"""
    
    client = get_openai_client()
    
    platform_config = PLATFORM_CONFIG.get(platform, PLATFORM_CONFIG["instagram"])
    tone_config = TONE_PRESETS.get(tone, TONE_PRESETS["professional"])
    
    lang_instruction = "русский" if language == "ru" else "english"
    
    system_prompt = f"""Ты — эксперт по контент-маркетингу для AI Genesis.
    
{BUSINESS_CONTEXT}

Задача: Создать пост для {platform.upper()}.

Характеристики платформы:
- Стиль: {platform_config['style']}
- Оптимальная длина: {platform_config['optimal_length']} символов
- Хештеги: {platform_config['hashtag_count']}
- CTA: {platform_config['cta']}

Тон поста: {tone_config}

Язык: {lang_instruction}

Требования:
1. Захватывающее начало (hook) в первых 2 строках
2. Структура: Hook → Раскрытие темы → Ценность → CTA
3. Естественное использование эмодзи (не перегружать)
4. Релевантные хештеги в конце
5. Человечный, не "продающий" напрямую тон"""

    user_prompt = f"""Тема поста: {topic}

Создай {variants} варианта поста. Для каждого варианта:
1. Придумай цепляющий заголовок
2. Напиши полный текст поста
3. Добавь подходящие хештеги
4. Укажи рекомендуемое время публикации (утро/день/вечер)

Формат вывода — JSON:
{{
  "posts": [
    {{
      "title": "...",
      "content": "...",
      "hashtags": ["..."],
      "best_time": "...",
      "char_count": 123
    }}
  ]
}}"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.8,
            max_tokens=2000
        )
        
        content = response.choices[0].message.content
        
        # Try to parse JSON
        try:
            # Clean up markdown code blocks if present
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0]
            elif "```" in content:
                content = content.split("```")[1].split("```")[0]
            
            result = json.loads(content.strip())
            return result
        except json.JSONDecodeError:
            # Return raw content if JSON parsing fails
            return {"raw_content": content}
            
    except Exception as e:
        return {"error": str(e)}


def generate_caption_for_image(image_description, platform="instagram"):
    """Generate caption for existing image/carousel"""
    
    client = get_openai_client()
    
    system_prompt = f"""Ты создаёшь подписи для {platform.upper()}.
    
{BUSINESS_CONTEXT}

Подпись должна:
1. Дополнять визуал, не дублировать
2. Рассказывать историю или давать контекст
3. Включать призыв к действию
4. Быть в тоне AI Genesis — профессиональном но дружелюбном"""

    user_prompt = f"""Описание изображения/карусели: {image_description}

Создай подпись для этого контента."""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
            max_tokens=500
        )
        
        return {"caption": response.choices[0].message.content}
        
    except Exception as e:
        return {"error": str(e)}


def generate_content_calendar(days=7, focus="automation"):
    """Generate weekly content calendar"""
    
    client = get_openai_client()
    
    system_prompt = f"""Ты — контент-стратег AI Genesis.
    
{BUSINESS_CONTEXT}

Создай контент-план на {days} дней.
Тематика: {focus}

Разнообразие форматов:
- Образовательные (как/почему)
- Истории клиентов
- За кулисами
- Мифы vs реальность
- Вдохновляющие
- Практические советы"""

    user_prompt = """Создай контент-календарь в формате JSON:
{
  "calendar": [
    {
      "day": 1,
      "date": "2026-03-23",
      "type": "educational",
      "topic": "...",
      "format": "single post",
      "platform": "instagram",
      "goal": "..."
    }
  ]
}"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.8,
            max_tokens=2500
        )
        
        content = response.choices[0].message.content
        
        # Clean up markdown code blocks
        if "```json" in content:
            content = content.split("```json")[1].split("```")[0]
        elif "```" in content:
            content = content.split("```")[1].split("```")[0]
        
        return json.loads(content.strip())
        
    except Exception as e:
        return {"error": str(e)}


def save_post_to_file(content, platform, topic):
    """Save generated post to file"""
    
    output_dir = "/root/.openclaw/output/posts"
    os.makedirs(output_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_topic = topic.replace(" ", "_")[:30]
    filename = f"{platform}_{safe_topic}_{timestamp}.txt"
    filepath = os.path.join(output_dir, filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        if isinstance(content, dict) and "posts" in content:
            for i, post in enumerate(content["posts"], 1):
                f.write(f"=== ВАРИАНТ {i} ===\n\n")
                f.write(f"📌 {post.get('title', 'Без названия')}\n\n")
                f.write(post.get('content', ''))
                f.write("\n\n")
                if 'hashtags' in post:
                    f.write(" ".join(post['hashtags']))
                    f.write("\n\n")
                if 'best_time' in post:
                    f.write(f"⏰ Лучшее время: {post['best_time']}\n")
                f.write(f"📊 Символов: {post.get('char_count', 'N/A')}\n")
                f.write("\n" + "="*50 + "\n\n")
        else:
            f.write(str(content))
    
    return filepath


def main():
    parser = argparse.ArgumentParser(description="Post Generator — AI content for social media")
    parser.add_argument("topic", nargs="?", help="Тема поста")
    parser.add_argument("--platform", "-p", default="instagram", 
                       choices=["instagram", "telegram", "facebook", "linkedin"],
                       help="Платформа (default: instagram)")
    parser.add_argument("--tone", "-t", default="professional",
                       choices=["professional", "casual", "storytelling", "educational", "inspirational", "urgent"],
                       help="Тон поста (default: professional)")
    parser.add_argument("--variants", "-v", type=int, default=3,
                       help="Количество вариантов (default: 3)")
    parser.add_argument("--language", "-l", default="ru",
                       choices=["ru", "en"],
                       help="Язык (default: ru)")
    parser.add_argument("--save", "-s", action="store_true",
                       help="Сохранить в файл")
    parser.add_argument("--calendar", "-c", type=int, metavar="DAYS",
                       help="Создать контент-календарь на N дней")
    parser.add_argument("--caption", action="store_true",
                       help="Создать подпись для изображения (topic = описание)")
    
    args = parser.parse_args()
    
    # Content calendar mode
    if args.calendar:
        print(f"📅 Создаю контент-календарь на {args.calendar} дней...")
        result = generate_content_calendar(args.calendar)
        
        if "error" in result:
            print(f"❌ Ошибка: {result['error']}")
            return
        
        print("\n📅 КОНТЕНТ-КАЛЕНДАРЬ:\n")
        for item in result.get("calendar", []):
            print(f"День {item['day']} ({item['date']})")
            print(f"   Тип: {item['type']}")
            print(f"   Тема: {item['topic']}")
            print(f"   Формат: {item['format']}")
            print(f"   Цель: {item['goal']}")
            print()
        return
    
    # Caption mode
    if args.caption:
        if not args.topic:
            print("❌ Укажите описание изображения")
            return
        
        print(f"🖼️ Создаю подпись для {args.platform}...")
        result = generate_caption_for_image(args.topic, args.platform)
        
        if "error" in result:
            print(f"❌ Ошибка: {result['error']}")
            return
        
        print("\n📝 ПОДПИСЬ:\n")
        print(result['caption'])
        return
    
    # Regular post generation
    if not args.topic:
        print("📝 Post Generator — AI для социальных сетей")
        print()
        print("Использование:")
        print('  genesis post "Тема поста"')
        print('  genesis post "Тема" -p telegram -t casual')
        print('  genesis post "Тема" -v 5 --save')
        print('  genesis post -c 7  # контент-календарь')
        print('  genesis post "Описание картинки" --caption')
        print()
        print("Платформы: instagram, telegram, facebook, linkedin")
        print("Тоны: professional, casual, storytelling, educational, inspirational, urgent")
        return
    
    print(f"📝 Генерирую пост для {args.platform.upper()}...")
    print(f"   Тема: {args.topic}")
    print(f"   Тон: {args.tone}")
    print(f"   Вариантов: {args.variants}")
    print()
    
    result = generate_post(args.topic, args.platform, args.tone, args.variants, args.language)
    
    if "error" in result:
        print(f"❌ Ошибка: {result['error']}")
        return
    
    if "raw_content" in result:
        print(result['raw_content'])
    else:
        posts = result.get("posts", [])
        for i, post in enumerate(posts, 1):
            print(f"\n{'='*60}")
            print(f"📌 ВАРИАНТ {i}: {post.get('title', 'Без названия')}")
            print('='*60)
            print()
            print(post.get('content', ''))
            print()
            if 'hashtags' in post:
                print(" ".join(post['hashtags']))
            print()
            print(f"⏰ Лучшее время: {post.get('best_time', 'N/A')}")
            print(f"📊 Символов: {post.get('char_count', 'N/A')}")
    
    # Save to file
    if args.save:
        filepath = save_post_to_file(result, args.platform, args.topic)
        print(f"\n💾 Сохранено: {filepath}")


if __name__ == "__main__":
    main()
