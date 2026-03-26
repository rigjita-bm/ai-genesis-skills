#!/usr/bin/env python3
"""
Viral Hooks & Headlines Generator for AI Genesis
47 proven formulas for viral content + neuropsychology of attention
"""

import random
from typing import List, Dict, Optional

class ViralHooksGenerator:
    """
    Generates psychologically strong hooks for:
    - Reels/TikTok openings
    - Social media posts  
    - Email subject lines
    - Ad headlines
    """
    
    # READY-TO-USE HOOK BANK (20 proven hooks)
    HOOK_BANK = {
        "business": [
            "Этот бот заменил мне 3 сотрудника. Стоил $350. Работает 24/7.",
            "Я настроила AI-ассистента за 14 дней. Вот что он делает пока я сплю.",
            "90% предпринимателей теряют 20 часов в неделю на это. Решение есть.",
            "Без кода. Без найма. Без рутины. AI Genesis — смотри как.",
            "Пока конкуренты отвечают вручную, умные предприниматели автоматизируют.",
            "73% предпринимателей теряют клиентов из-за медленных ответов.",
            "В 2026 автоматизация — это уже не конкурентное преимущество. Это выживание.",
            "Я потратил $10,000 чтобы понять то, что тебе скажу бесплатно.",
            "Забудь про найм менеджера. Есть способ лучше.",
            "Ты ещё не настроил бота? Конкуренты уже закрывают сделки."
        ],
        "wellness": [
            "Я PhD-биолог. Вот что происходит с вашими клетками после 35.",
            "Почему я перестала пить витамины из аптеки — и что пью вместо них.",
            "3 добавки, которые заменяют мне 8 часов сна. Объясняю как учёный.",
            "Вы тратите $200/мес на кофе и всё равно устаёте. Вот почему.",
            "Секрет долголетия, о котором молчат фармацевты.",
            "Этот протокол добавил мне 2 продуктивных часа каждый день.",
            "Почему ваш мультивитамин не работает (и что работает вместо него).",
            "Я 5 лет изучала биохимию старения. Вот что реально работает.",
            "Один простой протокол вместо 10 баночек с полки.",
            "Как я избавилась от тумана в голове за 3 недели."
        ]
    }
    
    # 47 Hook Formulas organized by category
    HOOK_FORMULAS = {
        "curiosity": [
            {
                "template": "Я {years} изучал(а) {topic} и вот что меня шокировало...",
                "example": "Я 3 года изучал автоматизацию и вот что меня шокировало...",
                "vars": ["years", "topic"]
            },
            {
                "template": "Никто не говорит про {secret} в {niche}. Исправляю это.",
                "example": "Никто не говорит про реальную стоимость AI в малом бизнесе. Исправляю это.",
                "vars": ["secret", "niche"]
            },
            {
                "template": "Почему {successful_people} делают {unexpected_action}?",
                "example": "Почему успешные предприниматели отказываются от CRM?",
                "vars": ["successful_people", "unexpected_action"]
            },
            {
                "template": "Секрет {result}, о котором молчат {experts}",
                "example": "Секрет 10x роста, о котором молчат маркетологи",
                "vars": ["result", "experts"]
            },
            {
                "template": "Это изменит твой подход к {activity} навсегда",
                "example": "Это изменит твой подход к продажам навсегда",
                "vars": ["activity"]
            }
        ],
        
        "pattern_interrupt": [
            {
                "template": "Перестань {obvious_action}. Вот почему это убивает {goal}.",
                "example": "Перестань отвечать на сообщения сам. Вот почему это убивает рост.",
                "vars": ["obvious_action", "goal"]
            },
            {
                "template": "{popular_opinion} — это миф. И вот доказательство.",
                "example": "AI заменит предпринимателей — это миф. И вот доказательство.",
                "vars": ["popular_opinion"]
            },
            {
                "template": "Я потратил(а) ${amount} чтобы понять то, что тебе скажу бесплатно.",
                "example": "Я потратил $10,000 чтобы понять то, что тебе скажу бесплатно.",
                "vars": ["amount"]
            },
            {
                "template": "Всё, что ты знал(а) про {topic} — неправда",
                "example": "Всё, что ты знал про автоматизацию — неправда",
                "vars": ["topic"]
            },
            {
                "template": "Забудь про {common_solution}. Есть способ лучше.",
                "example": "Забудь про найм менеджера. Есть способ лучше.",
                "vars": ["common_solution"]
            }
        ],
        
        "data": [
            {
                "template": "{percent}% предпринимателей теряют {thing} из-за {problem}.",
                "example": "73% предпринимателей теряют клиентов из-за медленных ответов.",
                "vars": ["percent", "thing", "problem"]
            },
            {
                "template": "За {timeframe} с помощью {method} я {result}.",
                "example": "За 2 недели с помощью автоматизации я сэкономил 30 часов.",
                "vars": ["timeframe", "method", "result"]
            },
            {
                "template": "{number} способов {goal}. Разбираем №{specific}.",
                "example": "7 способов удвоить продажи. Разбираем №3.",
                "vars": ["number", "goal", "specific"]
            },
            {
                "template": "${amount} → ${result} за {time}. Вот как.",
                "example": "$500 → $5,000 за месяц. Вот как.",
                "vars": ["amount", "result", "time"]
            },
            {
                "template": "Статистика: {statistic}. А вот что с этим делать.",
                "example": "Статистика: 90% ботов настроены неправильно. А вот что с этим делать.",
                "vars": ["statistic"]
            }
        ],
        
        "story": [
            {
                "template": "В {year_past} я {situation}. Сегодня {transformation}.",
                "example": "В 2025 я работал 12 часов в день. Сегодня бизнес работает без меня.",
                "vars": ["year_past", "situation", "transformation"]
            },
            {
                "template": "Мой клиент пришёл с {problem}. Через {time} — {result}.",
                "example": "Мой клиент пришёл с 0 систем. Через 3 дня — полная автоматизация.",
                "vars": ["problem", "time", "result"]
            },
            {
                "template": "Меня чуть не уволили за {action}. Оказалось, это меняет всё.",
                "example": "Меня чуть не уволили за автоматизацию. Оказалось, это меняет всё.",
                "vars": ["action"]
            },
            {
                "template": "Я не верил(а) в {thing}, пока не {event}.",
                "example": "Я не верил в ботов, пока не увидел +40% к продажам.",
                "vars": ["thing", "event"]
            },
            {
                "template": "Как я {fail} и что из этого вышло",
                "example": "Как я потерял $5,000 на неправильной автоматизации и что из этого вышло",
                "vars": ["fail"]
            }
        ],
        
        "urgency": [
            {
                "template": "{tool} исчезнет через {time}. Вот как использовать сейчас.",
                "example": "Бесплатный доступ исчезнет через 48 часов. Вот как получить сейчас.",
                "vars": ["tool", "time"]
            },
            {
                "template": "В {year} {action} — это уже не конкурентное преимущество. Это выживание.",
                "example": "В 2026 автоматизация — это уже не конкурентное преимущество. Это выживание.",
                "vars": ["year", "action"]
            },
            {
                "template": "Пока конкуренты {waste_time}, умные предприниматели {smart_action}.",
                "example": "Пока конкуренты отвечают вручную, умные предприниматели автоматизируют.",
                "vars": ["waste_time", "smart_action"]
            },
            {
                "template": "Ты ещё не {action}? Конкуренты уже {result}.",
                "example": "Ты ещё не настроил бота? Конкуренты уже закрывают сделки.",
                "vars": ["action", "result"]
            },
            {
                "template": "Последний шанс: {opportunity} закрывается {deadline}",
                "example": "Последний шанс: цена $350 закрывается сегодня в 23:59",
                "vars": ["opportunity", "deadline"]
            }
        ],
        
        "benefit": [
            {
                "template": "Как {achieve_result} без {common_pain}",
                "example": "Как удвоить продажи без найма менеджеров",
                "vars": ["achieve_result", "common_pain"]
            },
            {
                "template": "Хочешь {desire}? Делай {action}.",
                "example": "Хочешь свободные вечера? Автоматизируй ответы.",
                "vars": ["desire", "action"]
            },
            {
                "template": "Всего {number} {action} отделяют тебя от {result}",
                "example": "Всего 3 шага отделяют тебя от автоматизированного бизнеса",
                "vars": ["number", "action", "result"]
            },
            {
                "template": "Получи {benefit}, пока {condition}",
                "example": "Получи свободное время, пока конкуренты работают 24/7",
                "vars": ["benefit", "condition"]
            }
        ],
        
        "question": [
            {
                "template": "Почему {group} никогда не {action}?",
                "example": "Почему успешные предприниматели никогда не отвечают сами?",
                "vars": ["group", "action"]
            },
            {
                "template": "Ты всё ещё {old_way}? Вот {new_way}",
                "example": "Ты всё ещё отвечаешь сам? Вот как делегировать боту",
                "vars": ["old_way", "new_way"]
            },
            {
                "template": "Что если {scenario}?",
                "example": "Что если бизнес работает без тебя?",
                "vars": ["scenario"]
            }
        ]
    }
    
    # Platform-specific recommendations
    PLATFORM_CONFIG = {
        "reels": {
            "max_words": 12,
            "preferred_hooks": ["pattern_interrupt", "curiosity", "data"],
            "style": "Short, punchy, visual",
            "example": "Я 3 года изучал это..."
        },
        "tiktok": {
            "max_words": 10,
            "preferred_hooks": ["pattern_interrupt", "curiosity", "story"],
            "style": "Trendy, viral, authentic",
            "example": "POV: ты настроил бота и спишь спокойно"
        },
        "instagram": {
            "max_words": 15,
            "preferred_hooks": ["data", "story", "benefit"],
            "style": "Personal yet professional",
            "example": "73% теряют клиентов..."
        },
        "telegram": {
            "max_words": 20,
            "preferred_hooks": ["curiosity", "story", "data"],
            "style": "Conversational, detailed",
            "example": "Никто не говорит про..."
        },
        "youtube": {
            "max_words": 18,
            "preferred_hooks": ["curiosity", "data", "how_to"],
            "style": "Clickable but accurate",
            "example": "Как я удвоил..."
        },
        "email": {
            "max_words": 10,
            "preferred_hooks": ["curiosity", "urgency", "benefit"],
            "style": "Must open in inbox",
            "example": "Ты ещё не видел это?"
        },
        "ads": {
            "max_words": 8,
            "preferred_hooks": ["benefit", "urgency", "pattern_interrupt"],
            "style": "Action-oriented",
            "example": "Хватит терять клиентов"
        }
    }
    
    # Hook Quality Rules by platform
    HOOK_RULES = {
        "reels": {
            "max_words": 15,
            "min_words": 3,
            "must_have": ["глагол", "эмоция или интрига"],
            "structure": "Обещание ценности или интриги в первых 3 словах"
        },
        "tiktok": {
            "max_words": 12,
            "min_words": 3,
            "must_have": ["глагол", "трендовый элемент"],
            "structure": "Мгновенный pattern interrupt"
        },
        "instagram": {
            "max_words": 20,
            "min_words": 5,
            "must_have": ["конкретика", "эмоция"],
            "structure": "Ценность в начале + любопытство"
        },
        "telegram": {
            "max_words": 25,
            "min_words": 5,
            "must_have": ["контекст", "интрига"],
            "structure": "Story hook или data hook предпочтительны"
        },
        "youtube": {
            "max_words": 20,
            "min_words": 5,
            "must_have": ["цифра или факт", "обещание"],
            "structure": "Что получат + какой формат"
        },
        "email": {
            "max_words": 12,
            "min_words": 3,
            "must_have": ["любопытство", "краткость"],
            "structure": "FOMO или информационный пробел"
        },
        "ads": {
            "max_words": 10,
            "min_words": 3,
            "must_have": ["выгода", "ясность"],
            "structure": "Что + Цена/Результат"
        }
    }
    
    # Hook Don'ts — what NOT to do
    HOOK_DONTS = [
        "❌ Clickbait без реального содержания в посте",
        "❌ Ложные обещания ('заработай миллион завтра')",
        "❌ Хуки длиннее лимита платформы",
        "❌ Хуки без глагола действия или эмоции",
        "❌ Обобщённые фразы без конкретики",
        "❌ Слишком много восклицательных знаков!!!",
        "❌ Капслок на всём хуке (выглядит как крик)",
        "❌ Манипулятивные техники без ценности"
    ]
    
    def get_hook_from_bank(self, category: str = "business", index: int = None) -> str:
        """Get ready-to-use hook from bank"""
        hooks = self.HOOK_BANK.get(category, self.HOOK_BANK["business"])
        if index is not None and 0 <= index < len(hooks):
            return hooks[index]
        return random.choice(hooks)
    
    def list_hook_bank(self) -> str:
        """List all hooks in bank with numbering"""
        output = "📚 БАНК ГОТОВЫХ ХУКОВ (20 штук):\n\n"
        
        output += "🤖 БИЗНЕС:\n"
        for i, hook in enumerate(self.HOOK_BANK["business"], 1):
            output += f"  {i:2d}. {hook}\n"
        
        output += "\n🌿 WELLNESS / ЗДОРОВЬЕ:\n"
        for i, hook in enumerate(self.HOOK_BANK["wellness"], 11):
            output += f"  {i:2d}. {hook}\n"
        
        return output
    
    def __init__(self, topic: str = "автоматизация бизнеса"):
        self.topic = topic
        self.all_hooks = []
        for category in self.HOOK_FORMULAS.values():
            self.all_hooks.extend(category)
    
    def generate_hook(self, formula: Dict, **kwargs) -> str:
        """Generate hook from formula with variables"""
        template = formula["template"]
        
        # Default values for common variables
        defaults = {
            "years": "3 года",
            "topic": self.topic,
            "niche": "бизнесе",
            "secret": "реальную стоимость",
            "successful_people": "успешные предприниматели",
            "unexpected_action": "отказываются от CRM",
            "result": "10x роста",
            "experts": "маркетологи",
            "activity": "продажи",
            "obvious_action": "отвечать на сообщения сам",
            "goal": "рост",
            "popular_opinion": "AI заменит предпринимателей",
            "amount": "10,000",
            "percent": "73",
            "thing": "клиентов",
            "event": "увидел +40% к продажам",
            "problem": "медленных ответов",
            "timeframe": "2 недели",
            "method": "автоматизации",
            "number": "7",
            "goal": "удвоить продажи",
            "specific": "3",
            "time": "месяц",
            "situation": "работал 12 часов в день",
            "transformation": "бизнес работает без меня",
            "time": "3 дня",
            "action": "автоматизацию",
            "fail": "потерял $5,000",
            "tool": "Бесплатный доступ",
            "waste_time": "отвечают вручную",
            "smart_action": "автоматизируют",
            "achieve_result": "удвоить продажи",
            "common_pain": "найма менеджеров",
            "common_solution": "найм менеджера",
            "desire": "свободные вечера",
            "group": "успешные предприниматели",
            "old_way": "отвечаешь сам",
            "new_way": "как делегировать боту",
            "scenario": "бизнес работает без тебя",
            "statistic": "90% ботов настроены неправильно",
            "condition": "конкуренты работают 24/7",
            "benefit": "свободное время",
            "opportunity": "цена $350",
            "deadline": "сегодня в 23:59",
            "year_past": "2025",
            "year": "2026"
        }
        
        # Override with provided values
        values = {**defaults, **kwargs}
        
        try:
            return template.format(**values)
        except KeyError as e:
            return template
    
    def generate_for_platform(
        self,
        topic: str,
        platform: str = "instagram",
        goal: str = "engagement"
    ) -> Dict:
        """
        Generate hooks optimized for specific platform
        """
        self.topic = topic
        config = self.PLATFORM_CONFIG.get(platform, self.PLATFORM_CONFIG["instagram"])
        
        hooks_by_category = {}
        
        # Generate hooks from preferred categories
        for category in config["preferred_hooks"]:
            if category in self.HOOK_FORMULAS:
                formulas = self.HOOK_FORMULAS[category]
                selected = random.sample(formulas, min(2, len(formulas)))
                hooks_by_category[category] = [
                    self.generate_hook(f) for f in selected
                ]
        
        # Add one from each remaining category
        for category, formulas in self.HOOK_FORMULAS.items():
            if category not in hooks_by_category:
                hook = self.generate_hook(random.choice(formulas))
                hooks_by_category[category] = [hook]
        
        # Select best hook based on platform and goal
        best_hook = self._select_best_hook(hooks_by_category, platform, goal)
        
        return {
            "topic": topic,
            "platform": platform,
            "goal": goal,
            "constraints": {
                "max_words": config["max_words"],
                "style": config["style"]
            },
            "hooks": hooks_by_category,
            "best_hook": best_hook,
            "alternatives": self._get_alternatives(hooks_by_category, best_hook)
        }
    
    def _select_best_hook(self, hooks: Dict, platform: str, goal: str) -> Dict:
        """Select best hook based on platform and goal"""
        all_hooks = []
        for category, hook_list in hooks.items():
            for hook in hook_list:
                all_hooks.append({"text": hook, "category": category})
        
        # Platform-specific scoring
        if platform == "reels":
            # Prefer pattern_interrupt and curiosity for reels
            preferred = [h for h in all_hooks if h["category"] in ["pattern_interrupt", "curiosity"]]
        elif platform == "email":
            # Prefer curiosity and urgency for emails
            preferred = [h for h in all_hooks if h["category"] in ["curiosity", "urgency"]]
        elif goal == "sales":
            # Prefer benefit and urgency for sales
            preferred = [h for h in all_hooks if h["category"] in ["benefit", "urgency"]]
        else:
            preferred = all_hooks
        
        selected = random.choice(preferred) if preferred else random.choice(all_hooks)
        
        return {
            "text": selected["text"],
            "category": selected["category"],
            "word_count": len(selected["text"].split()),
            "why": self._explain_why(selected["category"], platform, goal)
        }
    
    def _explain_why(self, category: str, platform: str, goal: str) -> str:
        """Explain why this hook was selected"""
        explanations = {
            "curiosity": "Ломает паттерн в ленте и заставляет читать дальше",
            "pattern_interrupt": "Прерывает скроллинг — эффективно для коротких форматов",
            "data": "Цифры = доверие. Отлично для профессиональной аудитории",
            "story": "Личная история создаёт эмоциональную связь",
            "urgency": "Создаёт FOMO — работает для конверсии",
            "benefit": "Явная выгода = высокая релевантность",
            "question": "Вовлекает через диалог"
        }
        return explanations.get(category, "Сбалансированный хук для данной аудитории")
    
    def score_hook(self, hook_text: str, platform: str = "instagram") -> Dict:
        """
        Score hook on 1-10 scale based on:
        - Emotion/concreteness (0-4 points)
        - Length appropriateness (0-3 points)  
        - Structure quality (0-3 points)
        """
        score = 0
        reasons = []
        
        # 1. Emotion & Concreteness (0-4 points)
        has_emotion = any(word in hook_text.lower() for word in 
                         ["шок", "секрет", "почему", "как", "вот", "стоп", "никто", "все"])
        has_numbers = any(char.isdigit() for char in hook_text)
        has_concrete = any(word in hook_text.lower() for word in 
                          ["$", "%", "год", "месяц", "неделю", "час", "день"])
        
        if has_emotion:
            score += 2
            reasons.append("✅ Есть эмоциональный триггер")
        if has_numbers:
            score += 1
            reasons.append("✅ Есть конкретные цифры")
        if has_concrete:
            score += 1
            reasons.append("✅ Конкретные рамки/время")
        
        # 2. Length (0-3 points)
        word_count = len(hook_text.split())
        max_words = self.PLATFORM_CONFIG.get(platform, {}).get("max_words", 15)
        
        if word_count <= max_words * 0.7:
            score += 3
            reasons.append(f"✅ Идеальная длина ({word_count} слов)")
        elif word_count <= max_words:
            score += 2
            reasons.append(f"⚠️ Длина ок, но можно короче ({word_count} слов)")
        else:
            score += 0
            reasons.append(f"❌ Слишком длинно ({word_count} слов, лимит {max_words})")
        
        # 3. Structure (0-3 points)
        has_verb = any(word in hook_text.lower() for word in 
                      ["дела", "получ", "переста", "забудь", "смотри", "узна", "скаж"])
        starts_strong = any(hook_text.lower().startswith(word) for word in 
                           ["я", "ты", "почему", "как", "что", "этот", "вот", "перестань", "забудь"])
        
        if has_verb:
            score += 1
            reasons.append("✅ Есть глагол действия")
        if starts_strong:
            score += 2
            reasons.append("✅ Сильное начало (прямое обращение)")
        
        return {
            "score": score,
            "max_score": 10,
            "percentage": round(score / 10 * 100),
            "word_count": word_count,
            "assessment": "Отличный хук!" if score >= 8 else "Хороший хук" if score >= 6 else "Можно улучшить",
            "reasons": reasons
        }
    
    def _get_alternatives(self, hooks: Dict, best: Dict, count: int = 3) -> List[str]:
        """Get alternative hooks excluding the best one"""
        all_hooks = []
        for category, hook_list in hooks.items():
            for hook in hook_list:
                if hook != best["text"]:
                    all_hooks.append(hook)
        
        return random.sample(all_hooks, min(count, len(all_hooks)))
    
    def generate_variations(self, base_hook: str, count: int = 3) -> List[str]:
        """Generate variations of a hook"""
        variations = []
        
        # Find matching formula
        for category, formulas in self.HOOK_FORMULAS.items():
            for formula in formulas:
                template = formula["template"]
                # Simple heuristic: check if structure is similar
                if self._similar_structure(base_hook, template):
                    # Generate variations with different values
                    for _ in range(count):
                        var = self.generate_hook(formula)
                        if var not in variations:
                            variations.append(var)
        
        return variations[:count]
    
    def _similar_structure(self, text: str, template: str) -> bool:
        """Check if text matches template structure"""
        # Simple check: count placeholders
        template_placeholders = template.count("{")
        return template_placeholders > 0
    
    def format_output(self, result: Dict) -> str:
        """Format hooks for display with scoring"""
        platform = result['platform']
        
        output = f"""
🎯 ТЕМА: {result['topic']}
📱 ПЛАТФОРМА: {result['platform'].capitalize()}
🎯 ЦЕЛЬ: {result['goal'].capitalize()}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

"""
        
        # Generate and score 5 best hooks from different categories
        hooks_with_scores = []
        category_emojis = {
            "curiosity": "🧠",
            "pattern_interrupt": "😱",
            "data": "📊",
            "story": "🎭",
            "urgency": "⚡",
            "benefit": "✨",
            "question": "❓"
        }
        
        # Get one hook from each preferred category
        preferred = self.PLATFORM_CONFIG.get(platform, {}).get("preferred_hooks", 
                      ["curiosity", "pattern_interrupt", "data"])
        
        for i, category in enumerate(preferred[:5], 1):
            if category in result['hooks'] and result['hooks'][category]:
                hook_text = result['hooks'][category][0]
                score_data = self.score_hook(hook_text, platform)
                hooks_with_scores.append({
                    "num": i,
                    "text": hook_text,
                    "category": category,
                    "emoji": category_emojis.get(category, "💡"),
                    "score": score_data["score"],
                    "assessment": score_data["assessment"]
                })
        
        # Display hooks with scores
        for hook_data in hooks_with_scores:
            bar = "█" * hook_data["score"] + "░" * (10 - hook_data["score"])
            output += f"""{hook_data['emoji']} ХУК #{hook_data['num']} | Формула: {hook_data['category'].upper().replace('_', ' ')} | Оценка: {hook_data['score']}/10
   "{hook_data['text']}"
   {bar} {hook_data['assessment']}

"""
        
        # Best hook recommendation
        best = max(hooks_with_scores, key=lambda x: x['score'])
        output += f"""━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🏆 РЕКОМЕНДУЮ: Хук #{best['num']}
💡 ПОЧЕМУ: {self._explain_why(best['category'], platform, result['goal'])}
📏 ДЛИНА: {len(best['text'].split())} слов — {'✅ подходит' if len(best['text'].split()) <= result['constraints']['max_words'] else '⚠️ превышает лимит'} для {platform}

"""
        
        # Rules for this platform
        if platform in self.HOOK_RULES:
            rules = self.HOOK_RULES[platform]
            output += f"""━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📏 ПРАВИЛА ДЛЯ {platform.upper()}:
   • До {rules['max_words']} слов (у вас: {best['text'].count(' ') + 1})
   • Должно быть: {', '.join(rules['must_have'])}
   • Структура: {rules['structure']}

"""
        
        return output

def main():
    import sys
    
    generator = ViralHooksGenerator()
    
    if len(sys.argv) < 2:
        print("⚡ Viral Hooks & Headlines Generator for AI Genesis")
        print("")
        print("Usage:")
        print('  python3 viral_hooks.py "тема" [platform] [goal]     # Сгенерировать хуки')
        print('  python3 viral_hooks.py bank [business|wellness]     # Готовые хуки из банка')
        print('  python3 viral_hooks.py list                          # Все 47 формул')
        print('  python3 viral_hooks.py platforms                     # Гайд по платформам')
        print('  python3 viral_hooks.py rules [platform]              # Правила для платформы')
        print('  python3 viral_hooks.py donts                         # Что НЕЛЬЗЯ делать')
        print('  python3 viral_hooks.py score "текст" [platform]      # Оценить хук 1-10')
        print("")
        print("Platforms: reels, tiktok, instagram, telegram, youtube, email, ads")
        print("Goals: engagement, sales, subscribers")
        print("")
        print("Examples:")
        print('  python3 viral_hooks.py "автоматизация бизнеса" instagram engagement')
        print('  python3 viral_hooks.py bank business                 # Случайный хук')
        print('  python3 viral_hooks.py bank wellness 3               # Хук #3')
        print('  python3 viral_hooks.py score "Я потратил $10k..." reels')
        sys.exit(0)
    
    if sys.argv[1] == "bank":
        if len(sys.argv) > 2 and sys.argv[2] in ["business", "wellness"]:
            category = sys.argv[2]
            if len(sys.argv) > 3:
                try:
                    index = int(sys.argv[3]) - (1 if category == "business" else 11)
                    hook = generator.get_hook_from_bank(category, index)
                    print(f"\n📌 Готовый хук ({category} #{sys.argv[3]}):")
                    print(f'"{hook}"')
                except:
                    print("❌ Неверный номер хука")
            else:
                hook = generator.get_hook_from_bank(category)
                print(f"\n📌 Случайный хук ({category}):")
                print(f'"{hook}"')
        else:
            print(generator.list_hook_bank())
        sys.exit(0)
    
    if sys.argv[1] == "list":
        print("\n📚 ВСЕ ФОРМУЛЫ ХУКОВ:\n")
        for category, formulas in generator.HOOK_FORMULAS.items():
            print(f"\n{category.upper()}:")
            for i, formula in enumerate(formulas, 1):
                print(f"  {i}. {formula['template']}")
                print(f"     → {formula['example']}")
        sys.exit(0)
    
    if sys.argv[1] == "platforms":
        print("\n📱 РЕКОМЕНДАЦИИ ПО ПЛАТФОРМАМ:\n")
        for platform, config in generator.PLATFORM_CONFIG.items():
            print(f"\n{platform.upper()}:")
            print(f"  Макс. слов: {config['max_words']}")
            print(f"  Стиль: {config['style']}")
            print(f"  Лучшие категории: {', '.join(config['preferred_hooks'])}")
            print(f"  Пример: \"{config['example']}\"")
        sys.exit(0)
    
    if sys.argv[1] == "rules":
        platform = sys.argv[2] if len(sys.argv) > 2 else "instagram"
        print(f"\n📏 ПРАВИЛА ДЛЯ {platform.upper()}:\n")
        if platform in generator.HOOK_RULES:
            rules = generator.HOOK_RULES[platform]
            print(f"  Макс. слов: {rules['max_words']}")
            print(f"  Мин. слов: {rules['min_words']}")
            print(f"  Должно быть: {', '.join(rules['must_have'])}")
            print(f"  Структура: {rules['structure']}")
        else:
            print("  Нет специфичных правил")
        sys.exit(0)
    
    if sys.argv[1] == "donts":
        print("\n❌ ЧТО НЕЛЬЗЯ ДЕЛАТЬ В ХУКАХ:\n")
        for dont in generator.HOOK_DONTS:
            print(f"  {dont}")
        sys.exit(0)
    
    if sys.argv[1] == "score":
        if len(sys.argv) < 3:
            print("❌ Нужен текст хука для оценки")
            print('Пример: python3 viral_hooks.py score "Я 3 года изучал это..." reels')
            sys.exit(1)
        hook_text = sys.argv[2]
        platform = sys.argv[3] if len(sys.argv) > 3 else "instagram"
        result = generator.score_hook(hook_text, platform)
        print(f"\n🎯 ОЦЕНКА ХУКА:\n")
        print(f'  "{hook_text}"')
        print(f"\n  Оценка: {result['score']}/10 ({result['percentage']}%)")
        print(f"  Длина: {result['word_count']} слов")
        print(f"  Вердикт: {result['assessment']}")
        print(f"\n  Детали:")
        for reason in result['reasons']:
            print(f"    {reason}")
        sys.exit(0)
    
    # Generate hooks
    topic = sys.argv[1]
    platform = sys.argv[2] if len(sys.argv) > 2 else "instagram"
    goal = sys.argv[3] if len(sys.argv) > 3 else "engagement"
    
    result = generator.generate_for_platform(topic, platform, goal)
    print(generator.format_output(result))
    
    # Save to file
    output_file = f"/root/.openclaw/output/hooks_{platform}_{topic[:20].replace(' ', '_')}.txt"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(generator.format_output(result))
    print(f"\n💾 Сохранено: {output_file}")

if __name__ == "__main__":
    main()
