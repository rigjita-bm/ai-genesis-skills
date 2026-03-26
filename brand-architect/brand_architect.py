#!/usr/bin/env python3
"""
Personal Brand Architect for AI Genesis
Expert positioning strategy for Риджита / AI Genesis
Niche: AI + Business for Russian-speaking entrepreneurs in USA
"""

import json
import random
from typing import Dict, List, Optional
from datetime import datetime

class PersonalBrandArchitect:
    """
    Builds personal brand strategy for AI Genesis
    - Brand identity & positioning
    - Content archetypes & balance
    - Platform-specific tone
    - Signature content formats
    - Bio generation for all platforms
    """
    
    # AI Genesis Brand Foundation
    BRAND_IDENTITY = {
        "expert_position": "AI-архитектор для русскоязычных предпринимателей в NYC",
        "origin_story": {
            "before": "Биолог, 12-часовые смены в лаборатории, рутина",
            "pivot": "Понял, что бизнес можно автоматизировать так же, как лабораторные процессы",
            "discovery": "3 года изучал AI-инструменты, тестировал на своих проектах",
            "transformation": "Создал систему, которая экономит 15+ часов в неделю",
            "mission": "Теперь помогаю предпринимателям делегировать рутину AI"
        },
        "core_values": [
            "Mobile-first — весь бизнес с телефона",
            "Done-for-you, не just courses — реальные результаты за дни",
            "Честность насчёт ограничений AI — не волшебная палочка",
        ],
        "anti_positioning": [
            "❌ Не продаю 'get rich quick' — только реальная автоматизация",
            "❌ Не работаю с enterprise — только малый бизнес",
            "❌ Не делаю 'курсы для всех' — только русскоязычные иммигранты в США",
            "❌ Не обещаю заменить людей — освобождаю время для важного"
        ],
        "unique_angles": [
            "Единственный, кто фокусируется на русскоязычных в NYC",
            "Реальные кейсы из нью-йоркского бизнеса (салоны, стройка, рестораны)",
            "Мобильная настройка — можно всё сделать с телефона",
            "Скорость: рабочий бот за 2-3 дня, не месяцы"
        ]
    }
    
    # Content Archetype Balance
    CONTENT_ARCHETYPES = {
        "expert": {
            "percentage": 40,
            "goal": "Доверие и авторитет",
            "formats": ["Разборы ошибок", "Кейсы клиентов", "Инсайты рынка", "Сравнения инструментов"],
            "examples": [
                "3 ошибки при настройке бота, которые убивают конверсию",
                "Как салон на Брайтоне сэкономил 20 часов в неделю",
                "Что изменилось в Telegram-ботах в 2026"
            ]
        },
        "personal": {
            "percentage": 25,
            "goal": "Близость и доверие",
            "formats": ["Истории", "За кулисами", "Ценности", "Провалы"],
            "examples": [
                "Как я чуть не бросил всё в первый месяц",
                "Мой рабочий день: от MUST-к задач до вечера",
                "Почему я отказался от клиента на $10k"
            ]
        },
        "educational": {
            "percentage": 25,
            "goal": "Польза и ретеншн",
            "formats": ["Туториалы", "Чек-листы", "Фреймворки", "Шаблоны"],
            "examples": [
                "Чек-лист: готов ли ваш бизнес к автоматизации",
                "Фреймворк MUST/SHOULD/NICE для приоритетов",
                "5 шаблонов ответов для салона красоты"
            ]
        },
        "selling": {
            "percentage": 10,
            "goal": "Конверсия",
            "formats": ["Офферы", "Кейсы студентов", "Результаты", "FAQ по ценам"],
            "examples": [
                "Осталось 2 места на пилот за $350",
                "Отзыв: 'Окупился за первую неделю'",
                "Сколько реально стоит автоматизация"
            ]
        }
    }
    
    # Platform-Specific Tone
    PLATFORM_TONE = {
        "telegram": {
            "style": "Глубокий эксперт, длинные мысли, закулисье",
            "length": "Длинные посты (1000-2000 символов)",
            "frequency": "3-4 раза в неделю",
            "best_archetypes": ["expert", "personal"],
            "signature_elements": ["Разборы в деталях", "Личные истории", "Честные цифры"],
            "examples": [
                "Вчера закрыл очередной пилот. Честно — клиент был сложный...",
                "3 вещи, которые я понял после 25 настроенных ботов..."
            ]
        },
        "instagram": {
            "style": "Визуальный эксперт, эстетика + польза",
            "length": "Карусели 5-7 слайдов, Reels 15-30 сек",
            "frequency": "Ежедневно (сторис) + 3-4 поста в неделю",
            "best_archetypes": ["educational", "expert"],
            "signature_elements": ["Карусели с чек-листами", "Reels с быстрыми tips", "Сторис 'день из жизни'"],
            "examples": [
                "5 признаков, что ваш бот настроен неправильно [карусель]",
                "POV: ты настроил автоматизацию и спишь спокойно [Reels]"
            ]
        },
        "youtube": {
            "style": "Обучающий авторитет, структурированный контент",
            "length": "10-20 минут",
            "frequency": "1-2 видео в неделю",
            "best_archetypes": ["educational", "expert"],
            "signature_elements": ["Пошаговые туториалы", "Кейс-стади", "Обзоры инструментов"],
            "examples": [
                "Полный гайд по настройке Telegram-бота с нуля",
                "Как я автоматизировал 3 бизнеса за месяц"
            ]
        },
        "tiktok": {
            "style": "Trendy, viral hooks, быстрые insights",
            "length": "15-60 секунд",
            "frequency": "1-2 в день",
            "best_archetypes": ["educational", "personal"],
            "signature_elements": ["Быстрые лайфхаки", "Мифы vs реальность", "До/после"],
            "examples": [
                "3 признака, что пора автоматизироваться",
                "Миф: боты дорогие. Реальность:"
            ]
        }
    }
    
    # Signature Content Formats (unique to AI Genesis)
    SIGNATURE_FORMATS = {
        "format_1": {
            "name": "🔍 'Честный разбор'",
            "description": "Показываю реальные цифры, ошибки и ограничения — не только успехи",
            "example": "Честный разбор: почему бот не сработал у клиента (и что мы изменили)",
            "platform": "Telegram, YouTube",
            "frequency": "Раз в 2 недели"
        },
        "format_2": {
            "name": "⚡ '3 дня до результата'",
            "description": "Таймлапс настройки бота: день 1, 2, 3",
            "example": "День 1: аудит. День 2: настройка. День 3: тестирование.",
            "platform": "Instagram Stories, TikTok",
            "frequency": "Ежемесячно"
        },
        "format_3": {
            "name": "🎯 'Сколько стоит'",
            "description": "Разбор реальной стоимости автоматизации с цифрами",
            "example": "Сколько я трачу на свою автоматизацию (честные цифры за месяц)",
            "platform": "Telegram, Instagram",
            "frequency": "Раз в месяц"
        }
    }
    
    # Bio Templates
    BIO_TEMPLATES = {
        "short": {
            "max_chars": 150,
            "structure": "Кто + Для кого + Результат + CTA",
            "template": "🤖 AI-архитектор для бизнеса\n📍 NYC | Русскоязычные предприниматели\n⚡ Боты, автоматизация, свободное время\n👇 Пилот от $350",
            "example": "🤖 Создаю AI-ассистентов для бизнеса\n📍 NYC → русскоязычные предприниматели\n⚡ Освобождаю 15+ часов в неделю\n👇 Узнай, сколько сэкономишь ты"
        },
        "medium": {
            "max_chars": 500,
            "structure": "Позиция + Origin Story (кратко) + Результат + Отличие + CTA",
            "template": """🤖 AI-архитектор для русскоязычных предпринимателей в NYC

Был биологом → понял, что бизнес тоже можно автоматизировать → 3 года изучал AI → теперь настраиваю ботов

⚡ Реальные результаты за 2-3 дня (не месяцы)
⚡ Всё с телефона — не нужен компьютер
⚡ 25+ настроенных бизнесов

❌ Не курсы — реальная настройка под тебя

👇 Напиши "АУДИТ" — бесплатно оценю, что можно автоматизировать""",
            "example": """🤖 Помогаю предпринимателям делегировать рутину AI

📍 Работаю с русскоязычными в NYC
💡 Бывший биолог → 3 года в AI-автоматизации
✅ 25+ бизнесов с работающими ботами

Что отличает:
→ Мобильная настройка (всё с телефона)
→ Результат за дни, не месяцы
→ Честно про ограничения AI

👇 Напиши "ПИЛОТ" — начнём с $350"""
        },
        "full": {
            "max_chars": 1500,
            "structure": "Full story + Credibility + Process + Anti-positioning + CTA",
            "template": """🤖 AI Genesis — автоматизация бизнеса для русскоязычных предпринимателей в NYC

КТО Я:
Бывший биолог, который понял: бизнес-процессы можно автоматизировать так же, как лабораторные. 3 года тестировал AI-инструменты на своих проектах. Создал систему, которая экономит 15+ часов в неделю.

ЧТО ДЕЛАЮ:
Настраиваю AI-ассистентов для малого бизнеса. Не продаю курсы — делаю настройку под ключ. Салоны, магазины, консультанты, строители — любой бизнес с повторяющимися задачами.

РЕЗУЛЬТАТЫ:
✅ 25+ настроенных бизнесов
✅ Средняя экономия: 15 часов в неделю
✅ Скорость: рабочий бот за 2-3 дня
✅ Всё с телефона — не нужен компьютер

ЧТО ОТЛИЧАЕТ:
→ Mobile-first: настраиваю всё с телефона, ты тоже управляешь с телефона
→ Скорость: не месяцы обучения — дни до результата  
→ Честность: скажу, если AI не решит твою проблему
→ Фокус: только русскоязычные иммигранты в США

ЧЕГО НЕ ДЕЛАЮ:
❌ Не работаю с enterprise (только малый бизнес)
❌ Не продаю "волшебные" курсы (только реальная настройка)
❌ Не обещаю заменить людей (освобождаю время для важного)

ГОТОВ НАЧАТЬ?
Напиши "АУДИТ" — бесплатно оценю, что можно автоматизировать в твоём бизнесе."""
        }
    }
    
    def generate_brand_identity(self) -> Dict:
        """Generate complete brand identity"""
        return {
            "expert_position": self.BRAND_IDENTITY["expert_position"],
            "origin_story": self._format_origin_story(),
            "core_values": self.BRAND_IDENTITY["core_values"],
            "anti_positioning": self.BRAND_IDENTITY["anti_positioning"],
            "unique_angles": self.BRAND_IDENTITY["unique_angles"]
        }
    
    def _format_origin_story(self) -> str:
        """Format origin story as narrative"""
        story = self.BRAND_IDENTITY["origin_story"]
        return f"""{story['before']}.
{story['pivot']}.
{story['discovery']}.
{story['transformation']}.
{story['mission']}."""
    
    def generate_content_plan(self, month: str = None) -> Dict:
        """Generate monthly content plan with archetype balance"""
        month = month or datetime.now().strftime("%B %Y")
        
        plan = {
            "month": month,
            "archetype_balance": {},
            "weekly_breakdown": []
        }
        
        # Calculate content pieces per archetype (assuming 20 posts/month)
        total_posts = 20
        for archetype, config in self.CONTENT_ARCHETYPES.items():
            count = int(total_posts * config["percentage"] / 100)
            plan["archetype_balance"][archetype] = {
                "percentage": config["percentage"],
                "posts_count": count,
                "goal": config["goal"],
                "formats": config["formats"]
            }
        
        # Generate 4 weeks
        for week in range(1, 5):
            week_plan = {
                "week": week,
                "focus": random.choice(["automation", "case_study", "myth", "behind_scenes", "productivity"]),
                "posts": []
            }
            
            # Mix of archetypes for the week
            for archetype in ["expert", "educational", "personal", "selling"]:
                if random.random() > 0.3:  # 70% chance to include
                    example = random.choice(self.CONTENT_ARCHETYPES[archetype]["examples"])
                    week_plan["posts"].append({
                        "archetype": archetype,
                        "topic": example,
                        "platform": random.choice(["telegram", "instagram", "tiktok"])
                    })
            
            plan["weekly_breakdown"].append(week_plan)
        
        return plan
    
    def generate_platform_guide(self, platform: str) -> Dict:
        """Generate platform-specific strategy"""
        if platform not in self.PLATFORM_TONE:
            return {"error": f"Unknown platform. Available: {list(self.PLATFORM_TONE.keys())}"}
        
        config = self.PLATFORM_TONE[platform]
        return {
            "platform": platform,
            "strategy": config,
            "content_ideas": self._generate_platform_ideas(platform),
            "best_posting_times": self._get_posting_times(platform)
        }
    
    def _generate_platform_ideas(self, platform: str) -> List[str]:
        """Generate content ideas for platform"""
        ideas = {
            "telegram": [
                "Честный разбор: почему бот не сработал",
                "3 инсайта после 25 настроенных CRM",
                "Мой рабочий день: от MUST к NICE",
                "Сколько я трачу на свою автоматизацию",
                "Ответы на вопросы подписчиков"
            ],
            "instagram": [
                "Карусель: 5 ошибок при настройке бота",
                "Reels: POV ты настроил автоматизацию",
                "Stories: день из жизни AI-архитектора",
                "Карусель: до/после автоматизации",
                "Reels: 3 признака пора автоматизироваться"
            ],
            "youtube": [
                "Полный гайд по Telegram-ботам 2026",
                "Кейс: салон красоты +20 часов свободы",
                "Сравнение: 5 платформ для автоматизации",
                "Туториал: настройка бота с нуля",
                "Честный разбор: ограничения AI"
            ],
            "tiktok": [
                "Миф: боты дорогие",
                "3 признака пора автоматизироваться",
                "Сколько стоит моя автоматизация",
                "До/после: 3 часа → 20 минут",
                "POV: клиент пишет ночью"
            ]
        }
        return ideas.get(platform, [])
    
    def _get_posting_times(self, platform: str) -> List[str]:
        """Get optimal posting times"""
        times = {
            "telegram": ["09:00", "13:00", "19:00"],
            "instagram": ["08:00", "12:00", "18:00", "21:00"],
            "youtube": ["14:00", "17:00"],
            "tiktok": ["11:00", "15:00", "19:00", "21:00"]
        }
        return times.get(platform, ["12:00"])
    
    def generate_bio(self, version: str = "all") -> Dict:
        """Generate bio for specified version or all"""
        if version == "all":
            return {
                "short": self.BIO_TEMPLATES["short"],
                "medium": self.BIO_TEMPLATES["medium"],
                "full": self.BIO_TEMPLATES["full"]
            }
        elif version in self.BIO_TEMPLATES:
            return {version: self.BIO_TEMPLATES[version]}
        else:
            return {"error": f"Unknown version. Use: short, medium, full, or all"}
    
    def generate_full_strategy(self) -> Dict:
        """Generate complete brand strategy"""
        return {
            "generated_at": datetime.now().isoformat(),
            "brand_identity": self.generate_brand_identity(),
            "content_archetypes": self.CONTENT_ARCHETYPES,
            "platform_strategy": {
                platform: self.generate_platform_guide(platform)
                for platform in self.PLATFORM_TONE.keys()
            },
            "signature_formats": self.SIGNATURE_FORMATS,
            "bio_versions": self.generate_bio("all"),
            "monthly_plan": self.generate_content_plan()
        }
    
    def generate_report(self) -> str:
        """Generate human-readable brand strategy report"""
        strategy = self.generate_full_strategy()
        
        report = f"""
╔══════════════════════════════════════════════════════════════════╗
║  🌟 AI GENESIS PERSONAL BRAND STRATEGY                            ║
║  Generated: {datetime.now().strftime('%Y-%m-%d')}                                          ║
╚══════════════════════════════════════════════════════════════════╝

═══════════════════════════════════════════════════════════════════
  🎯 BRAND IDENTITY
═══════════════════════════════════════════════════════════════════

📍 Эксперт-позиция:
   {strategy['brand_identity']['expert_position']}

📖 Origin Story:
{strategy['brand_identity']['origin_story']}

💎 Core Values:
"""
        for value in strategy['brand_identity']['core_values']:
            report += f"   • {value}\n"
        
        report += "\n🚫 Anti-Positioning (чего НЕ делаю):\n"
        for anti in strategy['brand_identity']['anti_positioning']:
            report += f"   {anti}\n"
        
        report += "\n✨ Unique Angles:\n"
        for angle in strategy['brand_identity']['unique_angles']:
            report += f"   • {angle}\n"
        
        report += """
═══════════════════════════════════════════════════════════════════
  📊 CONTENT ARCHETYPES (Monthly Balance)
═══════════════════════════════════════════════════════════════════
"""
        for archetype, config in strategy['content_archetypes'].items():
            report += f"""
{archetype.upper()} ({config['percentage']}%):
   Goal: {config['goal']}
   Formats: {', '.join(config['formats'])}
   Example: {config['examples'][0]}
"""
        
        report += """
═══════════════════════════════════════════════════════════════════
  📱 PLATFORM STRATEGY
═══════════════════════════════════════════════════════════════════
"""
        for platform, guide in strategy['platform_strategy'].items():
            report += f"""
{platform.upper()}:
   Style: {guide['strategy']['style']}
   Length: {guide['strategy']['length']}
   Frequency: {guide['strategy']['frequency']}
   Best Times: {', '.join(guide['best_posting_times'])}
"""
        
        report += """
═══════════════════════════════════════════════════════════════════
  🎨 SIGNATURE CONTENT FORMATS
═══════════════════════════════════════════════════════════════════
"""
        for key, format_info in strategy['signature_formats'].items():
            report += f"""
{format_info['name']}:
   {format_info['description']}
   Platform: {format_info['platform']}
   Frequency: {format_info['frequency']}
   Example: {format_info['example']}
"""
        
        report += """
═══════════════════════════════════════════════════════════════════
  📝 BIO VERSIONS
═══════════════════════════════════════════════════════════════════

SHORT (Instagram):
"""
        report += strategy['bio_versions']['short']['example']
        
        report += """

MEDIUM (Telegram/YouTube):
"""
        report += strategy['bio_versions']['medium']['example']
        
        report += """

═══════════════════════════════════════════════════════════════════
  ✅ NEXT STEPS
═══════════════════════════════════════════════════════════════════
   1. Обновить bio на всех платформах
   2. Создать контент-план на месяц
   3. Записать 3 signature формата
   4. Настроить частоту публикаций

═══════════════════════════════════════════════════════════════════
"""
        return report

def main():
    import sys
    import random
    
    architect = PersonalBrandArchitect()
    
    if len(sys.argv) < 2:
        print("🌟 Personal Brand Architect for AI Genesis")
        print("")
        print("Usage:")
        print("  python3 brand_architect.py identity          # Brand identity")
        print("  python3 brand_architect.py plan [month]      # Content plan")
        print("  python3 brand_architect.py platform [name]   # Platform strategy")
        print("  python3 brand_architect.py bio [version]     # Bio generator")
        print("  python3 brand_architect.py full              # Full strategy")
        print("  python3 brand_architect.py report            # Human-readable report")
        print("")
        print("Platforms: telegram, instagram, youtube, tiktok")
        print("Bio versions: short, medium, full, all")
        sys.exit(0)
    
    command = sys.argv[1]
    
    if command == "identity":
        result = architect.generate_brand_identity()
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    elif command == "plan":
        month = sys.argv[2] if len(sys.argv) > 2 else None
        result = architect.generate_content_plan(month)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    elif command == "platform":
        platform = sys.argv[2] if len(sys.argv) > 2 else "instagram"
        result = architect.generate_platform_guide(platform)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    elif command == "bio":
        version = sys.argv[2] if len(sys.argv) > 2 else "all"
        result = architect.generate_bio(version)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    elif command == "full":
        result = architect.generate_full_strategy()
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    elif command == "report":
        print(architect.generate_report())
        
        # Save to file
        output_file = f"/root/.openclaw/output/brand_strategy_{datetime.now().strftime('%Y%m%d')}.md"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(architect.generate_report())
        print(f"\n💾 Saved to: {output_file}")
    
    else:
        print(f"❌ Unknown command: {command}")
        print("Run without arguments for help")

if __name__ == "__main__":
    main()
