#!/usr/bin/env python3
"""
AI Genesis Content Strategist
Content planning, YouTube→Instagram adaptation, Telegram posts
"""

import json
import random
from datetime import datetime, timedelta
from typing import List, Dict, Optional

class ContentStrategist:
    """
    Content strategy for AI Genesis
    - Weekly content plans
    - YouTube to Instagram adaptation  
    - Telegram posts
    - Multi-platform coordination
    """
    
    # Content themes aligned with AI Genesis business
    THEMES = {
        "automation": {
            "topics": [
                "Сколько часов в день вы тратите на переписку",
                "3 процесса в бизнесе, которые можно отдать ИИ",
                "Как я настроил бота за 2 часа",
                "CRM vs Excel: когда пора переходить",
                "Автоматизация записи: до и после"
            ],
            "formats": ["carousel", "story", "reels"],
            "goal": "education"
        },
        "case_studies": {
            "topics": [
                "Кейс: салон красоты +15 часов свободы",
                "Как магазин чая перестал терять заказы",
                "Консультант: от хаоса к системе за неделю",
                "Строительная фирма: автоматизация смет",
                "Клиника: запись без администратора"
            ],
            "formats": ["carousel", "post"],
            "goal": "social_proof"
        },
        "myths": {
            "topics": [
                "Миф: ИИ заменит человека",
                "Миф: Автоматизация — это дорого",
                "Миф: Боты раздражают клиентов",
                "Миф: Нужен программист для настройки",
                "Миф: Автоматизация не для малого бизнеса"
            ],
            "formats": ["story", "reels", "carousel"],
            "goal": "objection_handling"
        },
        "behind_scenes": {
            "topics": [
                "Как я тестирую ботов перед запуском",
                "Мой рабочий день с 25 клиентами в CRM",
                "Инструменты, которые использую каждый день",
                "Ошибка, которая стоила мне $500",
                "Почему я отказался от Google Sheets"
            ],
            "formats": ["story", "post"],
            "goal": "trust"
        },
        "productivity": {
            "topics": [
                "Система приоритетов MUST/SHOULD/NICE",
                "Как не утонуть в мелких задачах",
                "Мой метод планирования на неделю",
                "Почему я перешёл на Telegram для всего",
                "Мобильный офис: работа с телефона"
            ],
            "formats": ["carousel", "story"],
            "goal": "authority"
        }
    }
    
    # Hooks by goal
    HOOKS = {
        "education": [
            "Перестаньте делать это вручную",
            "Экономия 10 часов в неделю — реально",
            "Честный разбор: стоит ли автоматизация",
            "Ваш конкурент уже использует ИИ",
            "3 ошибки при автоматизации бизнеса"
        ],
        "social_proof": [
            "Реальный результат за 2 недели",
            "Клиент сказал: 'Почему не сделал раньше'",
            "До/после: цифры без воды",
            "Как мы закрыли 40% больше заявок",
            "Он сэкономил $2000 за месяц"
        ],
        "objection_handling": [
            "Все говорят, что это дорого. Вот правда.",
            "Я тоже так думал, пока не попробовал",
            "Миф, который стоит вам клиентов",
            "Почему это не сработает (и когда сработает)",
            "Честно: минусы автоматизации"
        ],
        "trust": [
            "Показываю процесс без купюр",
            "Моя реальная статистика за месяц",
            "Честный пост о том, как я работаю",
            "Инструменты, которые не врут",
            "За кулисами AI Genesis"
        ],
        "authority": [
            "Моя система после 3 лет экспериментов",
            "То, что работает, vs то, что продают",
            "Как я принимаю решения",
            "Фреймворк, который изменил мой бизнес",
            "От $0 до $10k: честная история"
        ]
    }
    
    CTAS = {
        "education": ["Сохраните", "Поделитесь с предпринимателем", "Какой пункт самый важный?"],
        "social_proof": ["Хотите так же?", "Напишите в директ", "Кейс полностью — по ссылке"],
        "objection_handling": ["Согласны?", "Какой миф разрушить следующим?", "Делитесь мнением"],
        "trust": ["Вопросы — в комменты", "Что ещё показать?", "Пишите, если узнали себя"],
        "authority": ["Пробовали такое?", "Ваш метод — в комменты", "Сохраните в закладки"]
    }
    
    HASHTAGS = {
        "automation": ["#автоматизация", "#ии", "#бизнес", "#предпринимательство", "#эффективность"],
        "general": ["#aigenesis", "#digital", "#business", "#automation", "#nycbusiness"]
    }
    
    def generate_weekly_plan(self, focus: str = "mixed", platform_mix: Dict = None) -> Dict:
        """
        Generate weekly content plan
        
        focus: automation | case_studies | myths | mixed
        platform_mix: {"instagram": 4, "telegram": 3, "stories": 7}
        """
        if platform_mix is None:
            platform_mix = {"instagram": 4, "telegram": 3, "stories": 7}
        
        plan = []
        days = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]
        
        # Select themes
        if focus == "mixed":
            theme_keys = list(self.THEMES.keys())
        else:
            theme_keys = [focus] if focus in self.THEMES else list(self.THEMES.keys())
        
        content_index = 0
        
        for day in days:
            day_content = []
            
            # Instagram post (Mon, Wed, Fri, Sun)
            if day in ["Понедельник", "Среда", "Пятница", "Воскресенье"]:
                theme_key = theme_keys[content_index % len(theme_keys)]
                theme = self.THEMES[theme_key]
                topic = theme["topics"][content_index % len(theme["topics"])]
                
                day_content.append({
                    "platform": "Instagram",
                    "topic": topic,
                    "format": "carousel" if day in ["Понедельник", "Четверг"] else "post",
                    "goal": theme["goal"],
                    "time": "10:00"
                })
                content_index += 1
            
            # Telegram post (Tue, Thu, Sat)
            if day in ["Вторник", "Четверг", "Суббота"]:
                theme_key = theme_keys[content_index % len(theme_keys)]
                theme = self.THEMES[theme_key]
                topic = theme["topics"][content_index % len(theme["topics"])]
                
                day_content.append({
                    "platform": "Telegram",
                    "topic": topic,
                    "format": "post",
                    "goal": theme["goal"],
                    "time": "14:00"
                })
                content_index += 1
            
            # Stories (every day)
            day_content.append({
                "platform": "Stories",
                "topic": "Behind the scenes / Daily tip",
                "format": "story",
                "goal": "engagement",
                "time": "18:00"
            })
            
            plan.append({
                "day": day,
                "content": day_content
            })
        
        return {
            "week_start": datetime.now().strftime("%Y-%m-%d"),
            "focus": focus,
            "plan": plan,
            "total_posts": sum(len(d["content"]) for d in plan)
        }
    
    def adapt_youtube_to_instagram(self, youtube_title: str, youtube_description: str, 
                                    key_points: List[str]) -> Dict:
        """
        Adapt YouTube content for Instagram
        """
        # Extract hook from title
        hook = self._create_hook(youtube_title)
        
        # Create carousel structure
        slides = []
        
        # Slide 1: Hook
        slides.append({
            "type": "cover",
            "text": hook,
            "style": "bold_title"
        })
        
        # Slides 2-4: Key points
        for i, point in enumerate(key_points[:3], 2):
            slides.append({
                "type": "content",
                "number": i,
                "text": point[:120],  # Keep it short
                "style": "bullet_point"
            })
        
        # Slide 5: CTA
        slides.append({
            "type": "cta",
            "text": "Полная версия — по ссылке в профиле",
            "style": "minimal"
        })
        
        # Generate caption
        caption = self._generate_caption(hook, key_points, "education")
        
        return {
            "source": "youtube",
            "original_title": youtube_title,
            "adapted_for": "instagram_carousel",
            "slides": slides,
            "caption": caption,
            "hashtags": self.HASHTAGS["automation"][:3] + self.HASHTAGS["general"][:2]
        }
    
    def create_telegram_post(self, topic: str, goal: str = "education", 
                              style: str = "conversational") -> Dict:
        """
        Create Telegram post
        """
        hook = self._create_hook(topic)
        
        if style == "conversational":
            body = self._create_conversational_body(topic, goal)
        else:
            body = self._create_formal_body(topic, goal)
        
        cta = random.choice(self.CTAS.get(goal, self.CTAS["education"]))
        
        full_text = f"{hook}\n\n{body}\n\n{cta}"
        
        return {
            "platform": "telegram",
            "topic": topic,
            "goal": goal,
            "text": full_text,
            "formatting": {
                "bold": [hook.split("\n")[0]],
                "italic": [],
                "links": []
            }
        }
    
    def create_content_batch(self, theme: str, count: int = 5) -> List[Dict]:
        """
        Create batch of content pieces on same theme
        """
        batch = []
        theme_data = self.THEMES.get(theme, self.THEMES["automation"])
        
        for i in range(min(count, len(theme_data["topics"]))):
            topic = theme_data["topics"][i]
            goal = theme_data["goal"]
            
            # Create Instagram version
            insta = self.adapt_youtube_to_instagram(
                youtube_title=topic,
                youtube_description="",
                key_points=[
                    f"Пункт 1: основная мысль о {topic}",
                    f"Пункт 2: практическое применение",
                    f"Пункт 3: результат через 2 недели"
                ]
            )
            
            # Create Telegram version
            telegram = self.create_telegram_post(topic, goal)
            
            batch.append({
                "topic": topic,
                "instagram": insta,
                "telegram": telegram,
                "goal": goal
            })
        
        return batch
    
    def _create_hook(self, topic: str) -> str:
        """Create engaging hook from topic"""
        hooks = [
            f"Перестаньте делать это вручную:\n{topic}",
            f"Честно про {topic}:",
            f"Миф разрушен:\n{topic}",
            f"Реальный кейс:\n{topic}",
            f"Ваш конкурент уже знает:\n{topic}"
        ]
        return random.choice(hooks)
    
    def _generate_caption(self, hook: str, key_points: List[str], goal: str) -> str:
        """Generate Instagram caption"""
        cta = random.choice(self.CTAS.get(goal, self.CTAS["education"]))
        
        caption = f"{hook}\n\n"
        caption += "Свайпайте →\n\n"
        caption += f"{cta}\n\n"
        caption += "—\n"
        caption += "AI Genesis | Автоматизация для предпринимателей\n"
        
        return caption
    
    def _create_conversational_body(self, topic: str, goal: str) -> str:
        """Create conversational body text"""
        templates = {
            "education": [
                f"Рассказываю, как это работает на практике.\n\n"
                f"{topic} — не сложно, если знать пару трюков.\n\n"
                f"Главное — начать с малого и не пытаться автоматизировать всё сразу.",
                
                f"Вчера обсуждал с клиентом именно это.\n\n"
                f"{topic} — вопрос, который задают чаще всего.\n\n"
                f"Вот мой ответ без воды..."
            ],
            "social_proof": [
                f"Точные цифры из реальной работы:\n\n"
                f"{topic}\n\n"
                f"Это не теория — это то, что получилось за 3 недели.",
                
                f"Клиент написал после внедрения:\n\n"
                f"'{topic}'\n\n"
                f"Вот что изменилось..."
            ]
        }
        
        options = templates.get(goal, templates["education"])
        return random.choice(options)
    
    def _create_formal_body(self, topic: str, goal: str) -> str:
        """Create formal body text"""
        return f"{topic}\n\nРазбираем по пунктам:\n\n1. Анализ ситуации\n2. Выбор инструментов\n3. Внедрение\n4. Результат"
    
    def export_plan_to_notion_format(self, plan: Dict) -> str:
        """Export weekly plan to Notion-compatible markdown"""
        output = f"# Контент-план: {plan['week_start']}\n\n"
        output += f"**Фокус:** {plan['focus']}\n"
        output += f"**Всего постов:** {plan['total_posts']}\n\n"
        
        for day_data in plan['plan']:
            output += f"## {day_data['day']}\n\n"
            for content in day_data['content']:
                output += f"### {content['platform']} ({content['time']})\n"
                output += f"- **Тема:** {content['topic']}\n"
                output += f"- **Формат:** {content['format']}\n"
                output += f"- **Цель:** {content['goal']}\n\n"
        
        return output

def main():
    import sys
    
    strategist = ContentStrategist()
    
    if len(sys.argv) < 2:
        print("🎯 AI Genesis Content Strategist")
        print("")
        print("Usage:")
        print("  python3 content_strategist.py plan [focus]      # Weekly content plan")
        print("  python3 content_strategist.py adapt 'title'     # YouTube→Instagram")
        print("  python3 content_strategist.py telegram 'topic'  # Telegram post")
        print("  python3 content_strategist.py batch [theme] [n] # Batch content")
        print("")
        print("Themes: automation, case_studies, myths, behind_scenes, productivity")
        print("")
        print("Examples:")
        print('  python3 content_strategist.py plan automation')
        print('  python3 content_strategist.py adapt "10 советов по продуктивности"')
        print('  python3 content_strategist.py telegram "Автоматизация салона"')
        sys.exit(0)
    
    command = sys.argv[1]
    
    if command == "plan":
        focus = sys.argv[2] if len(sys.argv) > 2 else "mixed"
        plan = strategist.generate_weekly_plan(focus)
        
        print(f"\n📅 Контент-план на неделю ({plan['week_start']})")
        print(f"Фокус: {focus}")
        print(f"Всего постов: {plan['total_posts']}\n")
        print("-" * 60)
        
        for day_data in plan['plan']:
            print(f"\n{day_data['day']}:")
            for content in day_data['content']:
                print(f"  [{content['time']}] {content['platform']}: {content['topic'][:40]}...")
        
        # Save to file
        output_file = f"/root/.openclaw/output/content_plan_{plan['week_start']}.md"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(strategist.export_plan_to_notion_format(plan))
        print(f"\n✅ Сохранено: {output_file}")
    
    elif command == "adapt":
        if len(sys.argv) < 3:
            print("❌ Укажите название YouTube видео")
            sys.exit(1)
        
        title = sys.argv[2]
        key_points = sys.argv[3:] if len(sys.argv) > 3 else ["Пункт 1", "Пункт 2", "Пункт 3"]
        
        result = strategist.adapt_youtube_to_instagram(title, "", key_points)
        
        print(f"\n📱 YouTube → Instagram адаптация")
        print(f"Оригинал: {result['original_title']}\n")
        print("Карусель:")
        for slide in result['slides']:
            print(f"  Слайд {slide.get('number', 'обложка')}: {slide['text'][:50]}...")
        print(f"\nПодпись:\n{result['caption']}")
        print(f"\nХэштеги: {' '.join(result['hashtags'])}")
    
    elif command == "telegram":
        if len(sys.argv) < 3:
            print("❌ Укажите тему")
            sys.exit(1)
        
        topic = " ".join(sys.argv[2:])
        post = strategist.create_telegram_post(topic)
        
        print(f"\n📱 Telegram пост:\n")
        print(post['text'])
    
    elif command == "batch":
        theme = sys.argv[2] if len(sys.argv) > 2 else "automation"
        count = int(sys.argv[3]) if len(sys.argv) > 3 else 3
        
        batch = strategist.create_content_batch(theme, count)
        
        print(f"\n📦 Батч контента ({theme}): {len(batch)} тем\n")
        for item in batch:
            print(f"• {item['topic']}")
            print(f"  Instagram: {len(item['instagram']['slides'])} слайдов")
            print(f"  Telegram: {len(item['telegram']['text'])} символов")
            print()
    
    else:
        print(f"❌ Unknown command: {command}")
        print("Run without arguments for help")

if __name__ == "__main__":
    main()
