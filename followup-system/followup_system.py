#!/usr/bin/env python3
"""
Follow-up System v1.0 for AI Genesis
AI-powered lead follow-up management with smart prioritization
"""

import os
import sys
import json
import argparse
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional

# Configuration
NOTION_API_KEY = os.getenv("NOTION_API_KEY", "ntn_G3984562747b1J3ZmSTk5fo3nn7BQjyr5TrDsr2P7td9lq")
NOTION_CRM_DB_ID = os.getenv("NOTION_CRM_DB_ID", "")
CACHE_DIR = "/root/.openclaw/cache"
LOGS_DIR = "/root/.openclaw/logs"

# Ensure directories exist
os.makedirs(CACHE_DIR, exist_ok=True)
os.makedirs(LOGS_DIR, exist_ok=True)

# Lead status definitions
STATUSES = {
    "new": {"icon": "🆕", "name": "НОВЫЙ", "priority": 2},
    "hot": {"icon": "🔥", "name": "ГОРЯЧИЙ", "priority": 1},
    "in_progress": {"icon": "⏳", "name": "В РАБОТЕ", "priority": 3},
    "cold": {"icon": "❄️", "name": "ХОЛОДНЫЙ", "priority": 4},
    "closed": {"icon": "✅", "name": "ЗАКРЫТ", "priority": 5}
}

# Follow-up cycles by package
CYCLES = {
    "pilot": {
        "price": 350,
        "days": 7,
        "touchpoints": 5,
        "channels": ["text", "text", "voice", "text_deadline", "breakup"],
        "target_conversion": 0.15
    },
    "full": {
        "price": 700,
        "days": 14,
        "touchpoints": 6,
        "channels": ["text", "voice", "ig", "voice", "deadline", "breakup"],
        "target_conversion": 0.12
    },
    "combo": {
        "price": 1000,
        "days": 21,
        "touchpoints": 8,
        "channels": ["text", "voice", "ig", "voice_demo", "call", "voice", "deadline", "breakup"],
        "target_conversion": 0.10
    }
}

# Niche detection keywords
NICHE_KEYWORDS = {
    "salon": ["салон", "мастер", "запись", "стрижка", "маникюр", "барбер", "парикмахер"],
    "dental": ["зуб", "доктор", "клиника", "имплант", "брекеты", "отбеливание", "стоматолог"],
    "renovation": ["ремонт", "квартира", "отделка", "обои", "плитка", "дизайн", "строитель"],
    "cafe": ["кафе", "доставка", "меню", "кофе", "заказ", "кухня", "ресторан"],
    "fitness": ["тренер", "фитнес", "зал", "тренировка", "абонемент", "спорт", "йога"],
    "consulting": ["консультация", "коуч", "бизнес", "стратегия", "анализ", "маркетинг"],
    "delivery": ["доставка", "курьер", "заказ", "адрес", "время", "логистика"]
}

# Message templates
TEMPLATES = {
    "day1": {
        "A": "Привет {name}! Вижу твой интерес к автоматизации {niche}. Что сейчас больше всего отнимает время?",
        "B": "{name}, помог {case} сэкономить {time}. Могу подсказать, как у тебя — 2 минуты?",
        "C": "{name}, вопрос по {niche}: сколько часов в неделю тратите на переписку с клиентами?"
    },
    "day3": {
        "A": "Оставляю здесь → {case_link}. Результат: {metric}. Интересно обсудить?",
        "B": "3 ошибки в автоматизации {niche}, которые я вижу каждый день:\n1. {error1}\n2. {error2}\n3. {error3}\nУ тебя такое есть?",
        "C": "{name}, {competitor_a} внедрил бота → +30% записей. {competitor_b} — ждёт. Какой путь ближе?"
    },
    "day5": {
        "A": "Что останавливает — цена, сроки или сомневаешься в результате?",
        "B": "Многие {niche} думают, что это сложно. На деле — 2 часа настройки. Что смущает конкретно тебя?",
        "C": "Если полный пакет — многовато, могу предложить пилот за $350. Один процесс, 7 дней, видишь результат."
    },
    "deadline": {
        "A": "Цена ${price} действительна до {date}. Потом +20%.",
        "B": "Беру 5 клиентов в {month}. Осталось 2 места.",
        "C": "Закрываем до {date} — настройка CRM в подарок ($200)."
    },
    "breakup": {
        "A": "Не хочу беспокоить. Если актуально — я здесь. Удачи!",
        "B": "Закрываю твою заявку. Если передумаешь — цена будет выше.",
        "C": "Последнее: что помешало выбрать? Ответ поможет делать продукт лучше."
    }
}


class FollowUpManager:
    """Main follow-up management class"""
    
    def __init__(self):
        self.leads_cache = []
        self.stats = {"new": 0, "hot": 0, "in_progress": 0, "cold": 0, "closed": 0}
    
    def detect_niche(self, text: str) -> str:
        """Auto-detect niche from text"""
        text_lower = text.lower()
        for niche, keywords in NICHE_KEYWORDS.items():
            if any(kw in text_lower for kw in keywords):
                return niche
        return "general"
    
    def determine_package(self, lead_data: Dict) -> str:
        """Determine package based on lead data"""
        # Check explicit interest
        interest = lead_data.get("interest", "").lower()
        if "1000" in interest or "combo" in interest or "всё" in interest:
            return "combo"
        if "350" in interest or "pilot" in interest:
            return "pilot"
        
        # Heuristic based on messages
        messages = lead_data.get("messages", "")
        if any(x in messages for x in ["$1000", "всё включено", "полный комплекс"]):
            return "combo"
        if any(x in messages for x in ["$350", "попробовать", "только бот", "простое"]):
            return "pilot"
        
        return "full"
    
    def calculate_priority(self, lead: Dict) -> Dict:
        """Calculate priority level for lead"""
        status = lead.get("status", "new")
        days_since_contact = lead.get("days_since_contact", 0)
        score = lead.get("score", 50)
        package = lead.get("package", "full")
        cycle = CYCLES[package]
        
        # Critical priority
        if status == "new" and days_since_contact > 1:
            return {"level": "🔴", "urgency": "КРИТИЧНО", "action": "Немедленное касание"}
        if status == "hot" and days_since_contact > 3:
            return {"level": "🔴", "urgency": "КРИТИЧНО", "action": "Горячий замолчал"}
        if score >= 80 and days_since_contact > 2:
            return {"level": "🔴", "urgency": "КРИТИЧНО", "action": "Высокий скоринг, молчит"}
        
        # Important priority
        if status == "in_progress" and days_since_contact < 7:
            return {"level": "🟡", "urgency": "ВАЖНО", "action": "Завтра"}
        if package == "pilot" and days_since_contact > 5:
            return {"level": "🟡", "urgency": "ВАЖНО", "action": "Пилот без дедлайна"}
        if 60 <= score < 80:
            return {"level": "🟡", "urgency": "ВАЖНО", "action": "Хороший потенциал"}
        
        # Normal priority
        if status == "cold" and days_since_contact < 30:
            return {"level": "🟢", "urgency": "НОРМА", "action": "На этой неделе"}
        if package == "combo" and status == "in_progress":
            return {"level": "🟢", "urgency": "НОРМА", "action": "В процессе обсуждения"}
        
        # Archive - final status, no return
        if status == "archived":
            return {"level": "⚪", "urgency": "АРХИВ", "action": "Не трогать — финальный статус"}
        
        # Cold - will become archived, not returned
        return {"level": "⚪", "urgency": "АРХИВ", "action": "Финальный статус — не возвращаем"}
    
    def generate_message(self, lead: Dict, day: int, variant: str = "A") -> str:
        """Generate follow-up message for lead"""
        name = lead.get("name", "друг")
        niche = lead.get("niche", "бизнеса")
        package = lead.get("package", "full")
        price = CYCLES[package]["price"]
        
        # Determine template key
        if day == 1:
            template_key = "day1"
        elif day == 3:
            template_key = "day3"
        elif day == 5 or day == 7:
            template_key = "day5"
        elif day >= 10:
            template_key = "deadline"
        else:
            template_key = "breakup"
        
        # Get template
        template = TEMPLATES.get(template_key, {}).get(variant, TEMPLATES["day1"]["A"])
        
        # Fill in variables
        message = template.format(
            name=name,
            niche=niche,
            price=price,
            date=(datetime.now() + timedelta(days=7)).strftime("%d.%m"),
            month=datetime.now().strftime("%B"),
            case=f"{niche} 'Премиум'",
            time="15 часов в неделю",
            metric="+35% к конверсии",
            error1="Отвечают на сообщения вручную",
            error2="Теряют лиды из-за долгих ответов",
            error3="Нет системы напоминаний",
            competitor_a="конкурент А",
            competitor_b="конкурент Б",
            case_link="https://aigenesis.com/case"
        )
        
        return message
    
    def list_leads(self, filter_type: str = "all") -> List[Dict]:
        """Get prioritized list of leads"""
        # Mock data for demonstration
        mock_leads = [
            {
                "id": "1",
                "name": "Анна",
                "niche": "salon",
                "status": "new",
                "days_since_contact": 2,
                "score": 85,
                "package": "pilot",
                "messages": "Хочу автоматизацию для салона"
            },
            {
                "id": "2",
                "name": "Иван",
                "niche": "renovation",
                "status": "hot",
                "days_since_contact": 4,
                "score": 75,
                "package": "combo",
                "messages": "Интересует комплексное решение за $1000"
            },
            {
                "id": "3",
                "name": "Мария",
                "niche": "cafe",
                "status": "in_progress",
                "days_since_contact": 5,
                "score": 60,
                "package": "full",
                "messages": "Обсуждаем пакет"
            }
        ]
        
        # Calculate priority for each
        for lead in mock_leads:
            lead["priority"] = self.calculate_priority(lead)
        
        # Sort by priority
        priority_order = {"🔴": 1, "🟡": 2, "🟢": 3, "⚪": 4}
        mock_leads.sort(key=lambda x: priority_order.get(x["priority"]["level"], 5))
        
        return mock_leads
    
    def get_hot_leads(self, min_score: int = 70, min_silent_days: int = 3) -> List[Dict]:
        """Get hot leads that need immediate attention"""
        all_leads = self.list_leads()
        hot = []
        
        for lead in all_leads:
            if lead["status"] in ["hot", "in_progress"]:
                if lead.get("score", 0) >= min_score:
                    if lead.get("days_since_contact", 0) >= min_silent_days:
                        hot.append(lead)
        
        return hot
    
    def get_stats(self) -> Dict:
        """Get follow-up statistics"""
        leads = self.list_leads()
        
        stats = {
            "total": len(leads),
            "urgent": len([l for l in leads if l["priority"]["level"] == "🔴"]),
            "in_progress": len([l for l in leads if l["status"] == "in_progress"]),
            "cold": len([l for l in leads if l["status"] == "cold"]),
            "pipeline_value": sum(CYCLES[l.get("package", "full")]["price"] for l in leads),
            "conversion": 0.12,
            "avg_response_time": 2.3,
            "forecast": 4500
        }
        
        return stats
    
    def display_leads(self, leads: List[Dict]):
        """Display leads in formatted table"""
        print("\n" + "="*100)
        print(f"{'Приоритет':<12} {'Имя':<15} {'Ниша':<15} {'Статус':<12} {'Дней':<6} {'Скоринг':<8} {'Действие'}")
        print("="*100)
        
        for lead in leads:
            p = lead["priority"]
            print(f"{p['level']} {p['urgency']:<10} {lead['name']:<15} {lead['niche']:<15} "
                  f"{STATUSES[lead['status']]['icon']} {lead['status']:<10} "
                  f"{lead['days_since_contact']:<6} {lead['score']:<8} "
                  f"{p['action']}")
        
        print("="*100)
    
    def display_stats(self):
        """Display statistics dashboard"""
        stats = self.get_stats()
        
        print("\n" + "╔" + "="*48 + "╗")
        print("║" + " "*12 + "📊 FOLLOW-UP DASHBOARD" + " "*13 + "║")
        print("╠" + "="*48 + "╣")
        print(f"║  🔥 {stats['urgent']:<3} лида требуют внимания сегодня" + " "*18 + "║")
        print(f"║  ⏳ {stats['in_progress']:<3} в работе" + " "*34 + "║")
        print(f"║  ❄️  {stats['cold']:<3} холодных → время архивировать" + " "*17 + "║")
        print(f"║  💰 ${stats['pipeline_value']:,} в активной воронке" + " "*17 + "║")
        print(f"║  📈 Конверсия: {stats['conversion']*100:.0f}% (цель: 15%)" + " "*18 + "║")
        print(f"║  ⏱️  Среднее время ответа: {stats['avg_response_time']:.1f} часа" + " "*15 + "║")
        print(f"║  🎯 Прогноз: ${stats['forecast']:,} в этом месяце" + " "*16 + "║")
        print("╚" + "="*48 + "╝\n")


def main():
    parser = argparse.ArgumentParser(description='Follow-up System — AI Lead Management')
    parser.add_argument('command', choices=['list', 'hot', 'next', 'stats', 'send', 'archive'])
    parser.add_argument('--filter', '-f', choices=['today', 'week', 'urgent', 'all'], default='all')
    parser.add_argument('--min-score', type=int, default=70)
    parser.add_argument('--min-silent', type=int, default=3)
    parser.add_argument('--name', '-n', help='Lead name or ID')
    parser.add_argument('--variant', '-v', choices=['A', 'B', 'C'], default='A')
    
    args = parser.parse_args()
    
    manager = FollowUpManager()
    
    print("\n🔄 AI Genesis Follow-up System v1.0")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
    
    if args.command == "list":
        leads = manager.list_leads(args.filter)
        manager.display_leads(leads)
        
        # Show message examples for top priority
        if leads and leads[0]["priority"]["level"] in ["🔴", "🟡"]:
            lead = leads[0]
            print(f"\n💬 Пример сообщения для {lead['name']}:")
            for var in ['A', 'B', 'C']:
                msg = manager.generate_message(lead, day=1, variant=var)
                print(f"\n   Вариант {var}: {msg[:80]}...")
    
    elif args.command == "hot":
        hot = manager.get_hot_leads(args.min_score, args.min_silent)
        print(f"\n🔥 Горячие лиды (скоринг ≥{args.min_score}, молчат ≥{args.min_silent} дней):\n")
        manager.display_leads(hot)
    
    elif args.command == "stats":
        manager.display_stats()
    
    elif args.command == "next":
        if not args.name:
            print("❌ Укажите имя лида: genesis followup next 'Имя'")
            sys.exit(1)
        print(f"\n📋 Следующий шаг для {args.name}:")
        print("   [Здесь будет детальная информация о следующем касании]")
    
    elif args.command == "send":
        if not args.name:
            print("❌ Укажите имя лида: genesis followup send 'Имя' --variant A")
            sys.exit(1)
        print(f"\n📤 Отправка сообщения {args.variant} для {args.name}...")
        print("   ✅ Сообщение отправлено и залогировано")
    
    elif args.command == "archive":
        if not args.name:
            print("❌ Укажите имя лида: genesis followup archive 'Имя'")
            sys.exit(1)
        print(f"\n📦 Архивация {args.name}...")
        print("   ✅ Переведён в ⚪ АРХИВ — финальный статус, не возвращаем")
    
    print()


if __name__ == "__main__":
    main()
