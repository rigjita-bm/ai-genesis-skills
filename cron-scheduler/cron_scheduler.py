#!/usr/bin/env python3
"""
Cron Scheduler + Follow-up System for AI Genesis
Manages scheduled tasks and automated follow-ups
"""

import json
import os
import sys
from datetime import datetime, timedelta
from typing import Dict, List, Optional

class FollowUpScheduler:
    """
    Manages follow-up sequences for leads
    3-touch system: +24h, +72h, +7days
    """
    
    # Follow-up templates
    FOLLOW_UP_TEMPLATES = {
        "24h": {
            "delay_hours": 24,
            "subject": "Проверка",
            "message": """Добрый день!

Если появились вопросы по {topic} — я здесь.

Что уточнить?""",
            "channel": "telegram"
        },
        "72h": {
            "delay_hours": 72,
            "subject": "Полезное",
            "message": """Хочу поделиться полезным:

{fact}

Актуально для вас?""",
            "channel": "telegram"
        },
        "7d": {
            "delay_hours": 168,  # 7 days
            "subject": "Финальное",
            "message": """Если выбрали другого специалиста — желаю успехов!

Если появятся вопросы по AI или здоровью — всегда здесь 🌿""",
            "channel": "telegram"
        }
    }
    
    def __init__(self):
        self.tasks_file = "/root/.openclaw/followup_tasks.json"
        self.leads_file = "/root/.openclaw/crm_cache.json"
        self.tasks = self._load_tasks()
    
    def _load_tasks(self) -> List[Dict]:
        """Load scheduled follow-up tasks"""
        if os.path.exists(self.tasks_file):
            try:
                with open(self.tasks_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def _save_tasks(self):
        """Save follow-up tasks"""
        with open(self.tasks_file, 'w', encoding='utf-8') as f:
            json.dump(self.tasks, f, ensure_ascii=False, indent=2)
    
    def schedule_followup(self, lead_contact: str, topic: str, 
                         fact: str = None, start_time: datetime = None) -> Dict:
        """
        Schedule 3-touch follow-up sequence for a lead
        
        Args:
            lead_contact: Telegram username, email, or phone
            topic: Topic of interest (from conversation)
            fact: Interesting fact to share at 72h (auto-generated if None)
            start_time: When to start (default: now)
        """
        if start_time is None:
            start_time = datetime.now()
        
        # Auto-generate fact if not provided
        if fact is None:
            facts = [
                "73% предпринимателей экономят 15+ часов в неделю с AI-автоматизацией",
                "NMN активирует энергию клеток на молекулярном уровне — исследование 2025",
                "Бот отвечает за 3 секунды vs 3 часа у человека — конверсия растёт на 40%",
                "Ашваганда снижает кортизол на 30% — клиническое исследование",
                "Один пилот за $350 заменяет 20 часов рутины каждую неделю"
            ]
            fact = facts[hash(lead_contact) % len(facts)]
        
        # Create 3 follow-up tasks
        new_tasks = []
        for touch_type, template in self.FOLLOW_UP_TEMPLATES.items():
            scheduled_time = start_time + timedelta(hours=template["delay_hours"])
            
            task = {
                "id": f"{lead_contact}_{touch_type}_{scheduled_time.strftime('%Y%m%d_%H%M')}",
                "lead_contact": lead_contact,
                "topic": topic,
                "fact": fact if touch_type == "72h" else None,
                "touch_type": touch_type,
                "scheduled_time": scheduled_time.isoformat(),
                "message": template["message"].format(topic=topic, fact=fact),
                "channel": template["channel"],
                "status": "pending",  # pending, sent, cancelled
                "created_at": datetime.now().isoformat()
            }
            new_tasks.append(task)
            self.tasks.append(task)
        
        self._save_tasks()
        
        return {
            "status": "scheduled",
            "lead": lead_contact,
            "tasks_count": 3,
            "schedule": [
                {"touch": "24h", "time": (start_time + timedelta(hours=24)).strftime('%d.%m %H:%M')},
                {"touch": "72h", "time": (start_time + timedelta(hours=72)).strftime('%d.%m %H:%M')},
                {"touch": "7d", "time": (start_time + timedelta(hours=168)).strftime('%d.%m %H:%M')}
            ]
        }
    
    def get_pending_tasks(self, hours_ahead: int = 24) -> List[Dict]:
        """
        Get tasks that need to be executed
        
        Args:
            hours_ahead: How many hours ahead to check (default: 24)
        """
        now = datetime.now()
        cutoff = now + timedelta(hours=hours_ahead)
        
        pending = []
        for task in self.tasks:
            if task["status"] != "pending":
                continue
            
            task_time = datetime.fromisoformat(task["scheduled_time"])
            if now <= task_time <= cutoff:
                pending.append(task)
        
        # Sort by scheduled time
        pending.sort(key=lambda x: x["scheduled_time"])
        return pending
    
    def execute_task(self, task_id: str) -> Dict:
        """
        Execute a follow-up task (send message)
        In real implementation, this would send via Telegram API
        """
        for task in self.tasks:
            if task["id"] == task_id:
                # Mark as sent
                task["status"] = "sent"
                task["sent_at"] = datetime.now().isoformat()
                self._save_tasks()
                
                return {
                    "status": "executed",
                    "task": task,
                    "message_sent": task["message"]
                }
        
        return {"status": "error", "message": "Task not found"}
    
    def cancel_followup(self, lead_contact: str) -> Dict:
        """Cancel all pending follow-ups for a lead (if they converted)"""
        cancelled = 0
        for task in self.tasks:
            if task["lead_contact"] == lead_contact and task["status"] == "pending":
                task["status"] = "cancelled"
                task["cancelled_at"] = datetime.now().isoformat()
                cancelled += 1
        
        self._save_tasks()
        
        return {
            "status": "cancelled",
            "lead": lead_contact,
            "tasks_cancelled": cancelled
        }
    
    def list_upcoming(self, days: int = 7) -> List[Dict]:
        """List all upcoming follow-ups for next N days"""
        now = datetime.now()
        cutoff = now + timedelta(days=days)
        
        upcoming = []
        for task in self.tasks:
            if task["status"] != "pending":
                continue
            
            task_time = datetime.fromisoformat(task["scheduled_time"])
            if task_time <= cutoff:
                upcoming.append({
                    "id": task["id"],
                    "lead": task["lead_contact"],
                    "type": task["touch_type"],
                    "when": task_time.strftime('%d.%m %H:%M'),
                    "message_preview": task["message"][:50] + "..."
                })
        
        return sorted(upcoming, key=lambda x: x["when"])
    
    def get_lead_history(self, lead_contact: str) -> List[Dict]:
        """Get full follow-up history for a lead"""
        return [t for t in self.tasks if t["lead_contact"] == lead_contact]
    
    def generate_daily_report(self) -> str:
        """Generate report of today's follow-ups"""
        today = datetime.now().date()
        today_tasks = []
        
        for task in self.tasks:
            task_time = datetime.fromisoformat(task["scheduled_time"])
            if task_time.date() == today and task["status"] == "pending":
                today_tasks.append(task)
        
        if not today_tasks:
            return f"📋 Follow-up report for {today.strftime('%d.%m.%Y')}\n\n✅ Нет запланированных follow-up на сегодня"
        
        report = f"📋 Follow-up report for {today.strftime('%d.%m.%Y')}\n\n"
        report += f"Всего задач на сегодня: {len(today_tasks)}\n\n"
        
        for task in sorted(today_tasks, key=lambda x: x["scheduled_time"]):
            time_str = datetime.fromisoformat(task["scheduled_time"]).strftime('%H:%M')
            report += f"⏰ {time_str} | {task['touch_type']} | {task['lead_contact']}\n"
            report += f"   💬 {task['message'][:60]}...\n\n"
        
        return report

def main():
    import sys
    
    scheduler = FollowUpScheduler()
    
    if len(sys.argv) < 2:
        print("⏰ Cron Scheduler + Follow-up System for AI Genesis")
        print("")
        print("Usage:")
        print('  python3 cron_scheduler.py schedule "@username" "тема"    # Запланировать 3 касания')
        print('  python3 cron_scheduler.py pending                       # Показать предстоящие задачи')
        print('  python3 cron_scheduler.py today                         # Сегодняшние follow-up')
        print('  python3 cron_scheduler.py upcoming [дней]               # На ближайшие N дней')
        print('  python3 cron_scheduler.py cancel "@username"            # Отменить follow-up')
        print('  python3 cron_scheduler.py history "@username"           # История по лиду')
        print('  python3 cron_scheduler.py execute "task_id"             # Выполнить задачу сейчас')
        print("")
        print("Examples:")
        print('  python3 cron_scheduler.py schedule "@anna_salon" "автоматизация салона"')
        print('  python3 cron_scheduler.py today')
        print('  python3 cron_scheduler.py upcoming 3')
        sys.exit(0)
    
    command = sys.argv[1]
    
    if command == "schedule" and len(sys.argv) >= 4:
        contact = sys.argv[2]
        topic = sys.argv[3]
        fact = sys.argv[4] if len(sys.argv) > 4 else None
        
        result = scheduler.schedule_followup(contact, topic, fact)
        print(f"\n✅ Follow-up запланирован!")
        print(f"👤 Лид: {result['lead']}")
        print(f"📊 Задач: {result['tasks_count']}")
        print("\n📅 Расписание:")
        for item in result['schedule']:
            print(f"  {item['touch']:3s} → {item['time']}")
    
    elif command == "pending":
        tasks = scheduler.get_pending_tasks(24)
        if not tasks:
            print("ℹ️ Нет pending задач на ближайшие 24 часа")
        else:
            print(f"\n⏰ Предстоящие задачи ({len(tasks)}):\n")
            for task in tasks[:10]:
                time_str = datetime.fromisoformat(task["scheduled_time"]).strftime('%d.%m %H:%M')
                print(f"  {time_str} | {task['touch_type']:3s} | {task['lead_contact']}")
    
    elif command == "today":
        report = scheduler.generate_daily_report()
        print(report)
    
    elif command == "upcoming":
        days = int(sys.argv[2]) if len(sys.argv) > 2 else 7
        upcoming = scheduler.list_upcoming(days)
        
        if not upcoming:
            print(f"ℹ️ Нет запланированных follow-up на {days} дней")
        else:
            print(f"\n📅 Upcoming follow-ups ({len(upcoming)}):\n")
            for item in upcoming:
                print(f"  {item['when']} | {item['type']:3s} | {item['lead']}")
                print(f"     {item['message_preview']}")
    
    elif command == "cancel" and len(sys.argv) > 2:
        contact = sys.argv[2]
        result = scheduler.cancel_followup(contact)
        print(f"\n🚫 Follow-up отменён для {result['lead']}")
        print(f"   Отменено задач: {result['tasks_cancelled']}")
    
    elif command == "history" and len(sys.argv) > 2:
        contact = sys.argv[2]
        history = scheduler.get_lead_history(contact)
        
        if not history:
            print(f"ℹ️ Нет истории для {contact}")
        else:
            print(f"\n📜 История follow-up для {contact}:\n")
            for task in history:
                time_str = datetime.fromisoformat(task["scheduled_time"]).strftime('%d.%m %H:%M')
                status_emoji = {"pending": "⏳", "sent": "✅", "cancelled": "🚫"}.get(task["status"], "❓")
                print(f"  {status_emoji} {time_str} | {task['touch_type']} | {task['status']}")
    
    elif command == "execute" and len(sys.argv) > 2:
        task_id = sys.argv[2]
        result = scheduler.execute_task(task_id)
        
        if result["status"] == "executed":
            print(f"\n✅ Задача выполнена!")
            print(f"📤 Отправлено сообщение:")
            print(f"   {result['message_sent']}")
        else:
            print(f"❌ Ошибка: {result['message']}")
    
    else:
        print("❌ Unknown command")
        print("Run without arguments for help")

if __name__ == "__main__":
    main()
