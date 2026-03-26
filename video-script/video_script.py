"""
Video Script Generator
A/B variants for Reels, TikTok, Shorts
Formats: emotional vs rational
"""

import json
import argparse
from datetime import datetime
from typing import Dict, List, Optional


class VideoScriptGenerator:
    """Generate video scripts for short-form content"""
    
    TEMPLATES = {
        "reels": {
            "duration": 60,
            "hook_time": 3,
            "cta_time": 5
        },
        "tiktok": {
            "duration": 45,
            "hook_time": 2,
            "cta_time": 3
        },
        "shorts": {
            "duration": 60,
            "hook_time": 3,
            "cta_time": 5
        }
    }
    
    def __init__(self, topic: str, platform: str = "reels", category: str = "business"):
        self.topic = topic
        self.platform = platform.lower()
        self.category = category.lower()
        self.template = self.TEMPLATES.get(self.platform, self.TEMPLATES["reels"])
        
    def generate_hook(self, variant: str = "emotional") -> str:
        """Generate opening hook"""
        hooks = {
            "business": {
                "emotional": [
                    "Я потратил 5 лет на это, а вы можете сделать за 5 минут...",
                    "Вчера мой клиент сказал: 'Почему я не узнал это раньше?'",
                    "Это изменило мою жизнь, и я знаю — изменит и вашу...",
                    f"3 ошибки в {self.topic}, которые стоят вам денег",
                    "Мой секрет, которым я не хотел делиться..."
                ],
                "rational": [
                    f"Как {self.topic} работает на самом деле",
                    f"3 факта о {self.topic}, которые вы не знали",
                    f"Почему {self.topic} важен для бизнеса",
                    f"Разбор {self.topic}: мифы и реальность",
                    f"{self.topic}: полное руководство за 60 секунд"
                ]
            },
            "wellness": {
                "emotional": [
                    "Мое утро начинается с этого... и я чувствую себя на 10 лет моложе",
                    "Врач сказал: 'Продолжайте делать то, что делаете'",
                    "Я искала решение 3 года. Нашла за 3 недели...",
                    "Этот ритуал изменил мою энергию к обеду",
                    "Моя история: от постоянной усталости к полной энергии"
                ],
                "rational": [
                    "3 ингредиента для здоровья, подтверждённые наукой",
                    "Почему большинство добавок не работают",
                    "Разбор состава: что действительно важно",
                    "5 минут в день = 10 часов энергии",
                    "Научный подход к wellness"
                ]
            }
        }
        
        category_hooks = hooks.get(self.category, hooks["business"])
        variant_hooks = category_hooks.get(variant, category_hooks["emotional"])
        
        # Select based on topic hash for consistency
        import hashlib
        topic_hash = int(hashlib.md5(self.topic.encode()).hexdigest(), 16)
        return variant_hooks[topic_hash % len(variant_hooks)]
    
    def generate_body(self, variant: str = "emotional") -> List[Dict]:
        """Generate main content points with timestamps"""
        
        if self.category == "wellness":
            if variant == "emotional":
                return [
                    {"time": "0:05", "text": "Моя история началась 2 года назад...", "visual": "фото 'до'"},
                    {"time": "0:15", "text": "Я пробовала всё. Ничего не работало.", "visual": "b-roll разных продуктов"},
                    {"time": "0:25", "text": "Пока не нашла ЭТО", "visual": "продукт крупным планом"},
                    {"time": "0:35", "text": "Результат через 30 дней", "visual": "фото 'после' / отзыв"}
                ]
            else:  # rational
                return [
                    {"time": "0:05", "text": "Проблема: 80% добавок — плацебо", "visual": "график исследования"},
                    {"time": "0:15", "text": "Причина: плохая биодоступность", "visual": "схема усвоения"},
                    {"time": "0:30", "text": "Решение: правильная формула", "visual": "структура молекулы"},
                    {"time": "0:45", "text": "Результат: 95% усвоение", "visual": "график эффективности"}
                ]
        
        else:  # business
            if variant == "emotional":
                return [
                    {"time": "0:05", "text": "Я работал 12 часов в сутки...", "visual": "таймлапс работы"},
                    {"time": "0:15", "text": "Пропускал семейные ужины", "visual": "сентиментальный кадр"},
                    {"time": "0:25", "text": "Пока не автоматизировал процессы", "visual": "скриншот дашборда"},
                    {"time": "0:40", "text": "Теперь я свободен", "visual": "кадр с семьёй / отдых"}
                ]
            else:  # rational
                return [
                    {"time": "0:05", "text": f"Что такое {self.topic}?", "visual": "определение на экране"},
                    {"time": "0:15", "text": "Проблема: ручная работа = ошибки", "visual": "статистика ошибок"},
                    {"time": "0:30", "text": "Решение: автоматизация процессов", "visual": "схема workflow"},
                    {"time": "0:45", "text": "Результат: +40% эффективности", "visual": "график роста"}
                ]
    
    def generate_cta(self, variant: str = "emotional") -> str:
        """Generate call-to-action"""
        ctas = {
            "emotional": [
                "Начните свой путь сегодня. Ссылка в профиле.",
                "Вы заслуживаете этого. Начните сейчас.",
                "Не откладывайте. Ваше будущее начинается сегодня.",
                "Присоединяйтесь к тысячам, кто уже изменил свою жизнь.",
                "Ваш момент — сейчас. Ссылка в шапке профиля."
            ],
            "rational": [
                "Получите бесплатную консультацию. Ссылка в профиле.",
                "Попробуйте 7 дней бесплатно. Оформите заявку.",
                "Скачайте чек-лист. Бесплатно, без регистрации.",
                "Забронируйте звонок. Подберём решение под вас.",
                "Узнайте стоимость. Калькулятор по ссылке."
            ]
        }
        
        variant_ctas = ctas.get(variant, ctas["emotional"])
        import hashlib
        topic_hash = int(hashlib.md5(self.topic.encode()).hexdigest(), 16)
        return variant_ctas[topic_hash % len(variant_ctas)]
    
    def generate_script(self, variant: str = "emotional") -> Dict:
        """Generate complete script for one variant"""
        return {
            "variant": variant,
            "platform": self.platform,
            "topic": self.topic,
            "duration": self.template["duration"],
            "hook": {
                "time": f"0:00-{self.template['hook_time']}",
                "text": self.generate_hook(variant),
                "visual": "текст на экране / крупный план"
            },
            "body": self.generate_body(variant),
            "cta": {
                "time": f"0:{self.template['duration'] - self.template['cta_time']}-{self.template['duration']}",
                "text": self.generate_cta(variant),
                "visual": "кнопка / ссылка / QR"
            },
            "captions": self._generate_captions(variant)
        }
    
    def _generate_captions(self, variant: str) -> str:
        """Generate post caption"""
        base_caption = f"{self.topic} — сохраните, чтобы не потерять 📌\n\n"
        
        if variant == "emotional":
            base_caption += "💭 Поделитесь в комментариях — узнаёте себя?\n\n"
        else:
            base_caption += "💡 Какой факт был для вас новым?\n\n"
        
        hashtags = {
            "business": "#бизнес #автоматизация #предпринимательство #лайфхак #продуктивность",
            "wellness": "#здоровье #велнес #красота #зож #здоровоепитание"
        }
        
        base_caption += f"\n{hashtags.get(self.category, hashtags['business'])}"
        base_caption += f" #{self.platform}"
        
        return base_caption
    
    def generate_ab_variants(self) -> Dict:
        """Generate both A/B variants"""
        return {
            "topic": self.topic,
            "platform": self.platform,
            "category": self.category,
            "created_at": datetime.now().isoformat(),
            "variant_a": self.generate_script("emotional"),
            "variant_b": self.generate_script("rational"),
            "recommendations": self._get_recommendations()
        }
    
    def _get_recommendations(self) -> List[str]:
        """Get platform-specific recommendations"""
        recs = {
            "reels": [
                "Используйте trending audio",
                "Добавьте 3-5 хештегов в описании",
                "Оптимальное время публикации: 11:00-13:00, 19:00-21:00"
            ],
            "tiktok": [
                "Зацепка в первые 2 секунды критична",
                "Используйте популярные звуки из библиотеки",
                "Добавьте субтитры — 80% смотрят без звука"
            ],
            "shorts": [
                "Вертикальный формат обязателен",
                "Добавьте end screen с подпиской",
                "Ссылки в описании работают для монетизации"
            ]
        }
        return recs.get(self.platform, recs["reels"])
    
    def export(self, output_path: Optional[str] = None) -> str:
        """Export script to JSON file"""
        script = self.generate_ab_variants()
        
        if output_path is None:
            output_path = f"/tmp/video_scripts/{self.topic.replace(' ', '_')}_{self.platform}.json"
        
        import os
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(script, f, ensure_ascii=False, indent=2)
        
        return output_path
    
    def format_for_display(self) -> str:
        """Format script for display in chat"""
        script = self.generate_ab_variants()
        
        output = f"🎬 Сценарий для {self.platform.upper()}\n"
        output += f"Тема: {self.topic}\n"
        output += f"Длительность: {self.template['duration']} сек\n"
        output += "=" * 40 + "\n\n"
        
        # Variant A
        output += "🔴 ВАРИАНТ A (Эмоциональный)\n\n"
        va = script["variant_a"]
        output += f"⏱️ {va['hook']['time']} — HOOK\n"
        output += f"💬 {va['hook']['text']}\n"
        output += f"🎥 Визуал: {va['hook']['visual']}\n\n"
        
        for point in va['body']:
            output += f"⏱️ {point['time']}\n"
            output += f"💬 {point['text']}\n"
            output += f"🎥 {point['visual']}\n\n"
        
        output += f"⏱️ {va['cta']['time']} — CTA\n"
        output += f"💬 {va['cta']['text']}\n\n"
        
        output += "-" * 40 + "\n\n"
        
        # Variant B
        output += "🔵 ВАРИАНТ B (Рациональный)\n\n"
        vb = script["variant_b"]
        output += f"⏱️ {vb['hook']['time']} — HOOK\n"
        output += f"💬 {vb['hook']['text']}\n"
        output += f"🎥 Визуал: {vb['hook']['visual']}\n\n"
        
        for point in vb['body']:
            output += f"⏱️ {point['time']}\n"
            output += f"💬 {point['text']}\n"
            output += f"🎥 {point['visual']}\n\n"
        
        output += f"⏱️ {vb['cta']['time']} — CTA\n"
        output += f"💬 {vb['cta']['text']}\n\n"
        
        output += "=" * 40 + "\n\n"
        output += "💡 Рекомендации:\n"
        for rec in script["recommendations"]:
            output += f"   • {rec}\n"
        
        return output


def main():
    """CLI interface"""
    parser = argparse.ArgumentParser(description='Generate video scripts')
    parser.add_argument('topic', help='Video topic')
    parser.add_argument('--platform', '-p', default='reels',
                       choices=['reels', 'tiktok', 'shorts'],
                       help='Platform (default: reels)')
    parser.add_argument('--category', '-c', default='business',
                       choices=['business', 'wellness'],
                       help='Content category (default: business)')
    parser.add_argument('--output', '-o', help='Output JSON file path')
    parser.add_argument('--format', '-f', default='display',
                       choices=['display', 'json'],
                       help='Output format')
    
    args = parser.parse_args()
    
    generator = VideoScriptGenerator(args.topic, args.platform, args.category)
    
    if args.format == 'json':
        path = generator.export(args.output)
        print(f"✅ Сценарий сохранён: {path}")
    else:
        print(generator.format_for_display())


if __name__ == '__main__':
    main()
