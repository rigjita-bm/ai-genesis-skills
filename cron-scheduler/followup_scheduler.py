"""
Follow-up Scheduler for CRM
Automated 3-touch follow-up series: 24h / 72h / 7d
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional


class FollowUpScheduler:
    """Manage automated follow-up sequences"""
    
    # Follow-up templates by stage
    TEMPLATES = {
        "24h": {
            "business": """Привет! Остались вопросы по AI-ассистенту?

Я могу:
• Уточнить детали под вашу ситуацию
• Рассчитать конкретную экономию времени
• Показать пример из вашей ниши

Что приоритетнее?""",
            "wellness": """Привет! Как ваше самочувствие?

Есть вопросы по протоколу?
• Подбор под ваши цели
• Совместимость с текущими добавками
• Оптимальный график приёма

Напишите — подскажу."""
        },
        "72h": {
            "business": """Кстати, интересный факт:

Наши клиенты в среднем экономят 15+ часов в неделю на рутине.

Это:
• 60 часов в месяц
• 720 часов в год
• ≈ 18 рабочих недель

Представьте, что можно сделать с этим временем?

Хотите такой же результат?""",
            "wellness": """Кстати, факт дня:

По данным исследований, 73% людей чувствуют прирост энергии
уже на 3-й день правильного протокола.

Главное — правильная комбинация и дозировка.

У вас уже есть опыт с добавками или только начинаете?"""
        },
        "7d": {
            "business": """Финальное сообщение:

Мы обсуждали автоматизацию для вашего бизнеса.

Предложение недели: скидка 20% на пилот ($350 → $280)
• Действует до [date]
• Включает полную настройку
• Работает 30 дней

Начнём на этой неделе или пока рано?""",
            "wellness": """Последний шанс этого месяца:

Протокол «{product}» со скидкой 20%
• Чай Долголетие: $100 → $80
• Anti-Age Pro: $150 → $120
• Deep Sleep: $300 → $240

Предложение до [date] или пока есть stock.

Забронировать комплект?"""
        }
    }
    
    def __init__(self, storage_path: str = "/tmp/followup_queue.json"):
        self.storage_path = storage_path
        self._ensure_storage()
    
    def _ensure_storage(self):
        """Ensure storage file exists"""
        if not os.path.exists(self.storage_path):
            with open(self.storage_path, 'w') as f:
                json.dump([], f)
    
    def _load_queue(self) -> List[Dict]:
        """Load follow-up queue"""
        with open(self.storage_path, 'r') as f:
            return json.load(f)
    
    def _save_queue(self, queue: List[Dict]):
        """Save follow-up queue"""
        with open(self.storage_path, 'w') as f:
            json.dump(queue, f, indent=2)
    
    def schedule_followup(self, lead_id: str, contact: str, 
                         category: str = "business", product: str = "") -> Dict:
        """Schedule 3-touch follow-up series for a lead"""
        
        now = datetime.now()
        
        schedule = {
            "lead_id": lead_id,
            "contact": contact,
            "category": category,
            "product": product,
            "created_at": now.isoformat(),
            "status": "active",
            "touches": [
                {
                    "stage": "24h",
                    "scheduled_at": (now + timedelta(hours=24)).isoformat(),
                    "sent": False,
                    "sent_at": None,
                    "template": self.TEMPLATES["24h"].get(category, self.TEMPLATES["24h"]["business"])
                },
                {
                    "stage": "72h",
                    "scheduled_at": (now + timedelta(hours=72)).isoformat(),
                    "sent": False,
                    "sent_at": None,
                    "template": self.TEMPLATES["72h"].get(category, self.TEMPLATES["72h"]["business"])
                },
                {
                    "stage": "7d",
                    "scheduled_at": (now + timedelta(days=7)).isoformat(),
                    "sent": False,
                    "sent_at": None,
                    "template": self.TEMPLATES["7d"].get(category, self.TEMPLATES["7d"]["business"]).replace("{product}", product or "Долголетие")
                }
            ]
        }
        
        # Add to queue
        queue = self._load_queue()
        queue.append(schedule)
        self._save_queue(queue)
        
        return {
            "success": True,
            "lead_id": lead_id,
            "scheduled": [
                f"24h: {(now + timedelta(hours=24)).strftime('%Y-%m-%d %H:%M')}",
                f"72h: {(now + timedelta(hours=72)).strftime('%Y-%m-%d %H:%M')}",
                f"7d: {(now + timedelta(days=7)).strftime('%Y-%m-%d %H:%M')}"
            ]
        }
    
    def get_pending(self) -> List[Dict]:
        """Get all pending follow-ups that are due"""
        now = datetime.now()
        queue = self._load_queue()
        pending = []
        
        for item in queue:
            if item["status"] != "active":
                continue
            
            for touch in item["touches"]:
                if not touch["sent"]:
                    scheduled = datetime.fromisoformat(touch["scheduled_at"])
                    if scheduled <= now:
                        pending.append({
                            "lead_id": item["lead_id"],
                            "contact": item["contact"],
                            "category": item["category"],
                            "stage": touch["stage"],
                            "message": touch["template"],
                            "scheduled_at": touch["scheduled_at"]
                        })
        
        return pending
    
    def mark_sent(self, lead_id: str, stage: str):
        """Mark a follow-up as sent"""
        queue = self._load_queue()
        
        for item in queue:
            if item["lead_id"] == lead_id:
                for touch in item["touches"]:
                    if touch["stage"] == stage:
                        touch["sent"] = True
                        touch["sent_at"] = datetime.now().isoformat()
                        break
        
        self._save_queue(queue)
    
    def cancel_followup(self, lead_id: str) -> bool:
        """Cancel all follow-ups for a lead (e.g., if converted)"""
        queue = self._load_queue()
        
        for item in queue:
            if item["lead_id"] == lead_id:
                item["status"] = "cancelled"
                self._save_queue(queue)
                return True
        
        return False
    
    def process_due(self, send_callback=None) -> List[Dict]:
        """Process all due follow-ups"""
        pending = self.get_pending()
        processed = []
        
        for item in pending:
            # Mark as sent
            self.mark_sent(item["lead_id"], item["stage"])
            
            processed.append(item)
            
            # Call send callback if provided
            if send_callback:
                send_callback(item)
        
        return processed
    
    def get_stats(self) -> Dict:
        """Get follow-up statistics"""
        queue = self._load_queue()
        
        stats = {
            "total_series": len(queue),
            "active": sum(1 for q in queue if q["status"] == "active"),
            "cancelled": sum(1 for q in queue if q["status"] == "cancelled"),
            "completed": sum(1 for q in queue if q["status"] == "completed"),
            "pending_sends": 0
        }
        
        now = datetime.now()
        for item in queue:
            if item["status"] == "active":
                for touch in item["touches"]:
                    if not touch["sent"]:
                        scheduled = datetime.fromisoformat(touch["scheduled_at"])
                        if scheduled <= now:
                            stats["pending_sends"] += 1
        
        return stats


def main():
    """CLI for follow-up management"""
    import sys
    
    if len(sys.argv) < 2:
        print("""Follow-up Scheduler

Usage:
  python followup_scheduler.py schedule <lead_id> <contact> [category] [product]
  python followup_scheduler.py pending
  python followup_scheduler.py process
  python followup_scheduler.py cancel <lead_id>
  python followup_scheduler.py stats
""")
        return
    
    command = sys.argv[1]
    scheduler = FollowUpScheduler()
    
    if command == "schedule":
        if len(sys.argv) < 4:
            print("❌ Укажите lead_id и contact")
            return
        
        lead_id = sys.argv[2]
        contact = sys.argv[3]
        category = sys.argv[4] if len(sys.argv) > 4 else "business"
        product = sys.argv[5] if len(sys.argv) > 5 else ""
        
        result = scheduler.schedule_followup(lead_id, contact, category, product)
        if result["success"]:
            print(f"✅ Follow-up запланирован для {lead_id}")
            for s in result["scheduled"]:
                print(f"   • {s}")
    
    elif command == "pending":
        pending = scheduler.get_pending()
        if pending:
            print(f"⏰ Ожидают отправки ({len(pending)}):")
            for p in pending:
                print(f"   • {p['lead_id']} | {p['stage']} | {p['contact']}")
        else:
            print("⏰ Нет ожидающих follow-up")
    
    elif command == "process":
        processed = scheduler.process_due()
        if processed:
            print(f"✅ Обработано ({len(processed)}):")
            for p in processed:
                print(f"   • {p['lead_id']} | {p['stage']}")
        else:
            print("✅ Нет due follow-ups")
    
    elif command == "cancel":
        if len(sys.argv) < 3:
            print("❌ Укажите lead_id")
            return
        
        lead_id = sys.argv[2]
        if scheduler.cancel_followup(lead_id):
            print(f"✅ Follow-up отменён для {lead_id}")
        else:
            print(f"⚠️ Lead {lead_id} не найден")
    
    elif command == "stats":
        stats = scheduler.get_stats()
        print("📊 Follow-up статистика:")
        print(f"   Всего серий: {stats['total_series']}")
        print(f"   Активных: {stats['active']}")
        print(f"   Отменено: {stats['cancelled']}")
        print(f"   Завершено: {stats['completed']}")
        print(f"   Ожидает отправки: {stats['pending_sends']}")
    
    else:
        print(f"❌ Неизвестная команда: {command}")


if __name__ == '__main__':
    main()
