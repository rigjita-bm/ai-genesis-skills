#!/usr/bin/env python3
"""
Course Launch Automation for AI Genesis
Complete launch system: pre-launch → sales → onboarding → analytics
Version: 1.0
"""

import json
from datetime import datetime, timedelta
from typing import List, Dict, Optional

class CourseLaunchAutomation:
    """
    Automates entire course launch cycle:
    - Phase 1: Pre-launch warming (5 posts over 7 days)
    - Phase 2: Sales post (AIDA + Social Proof)
    - Phase 3: Onboarding sequence (4 automated messages)
    - Phase 4: Launch report (analytics)
    """
    
    # Templates for different niches
    NICHE_TEMPLATES = {
        "ai_automation": {
            "pain": "теряют клиентов из-за медленных ответов",
            "transformation": "от 50 сообщений в день ручных → бот отвечает за 2 секунды",
            "benefit": "экономия 15+ часов в неделю",
            "objection_time": "настройка занимает 2-3 дня, не месяцы",
            "objection_price": "окупается за первую неделю за счёт непотерянных клиентов",
            "objection_tech": "настраиваем всё сами, вам только польза"
        },
        "sales": {
            "pain": "упускают сделки на этапе переговоров",
            "transformation": "от холодных звонков → система прогрева автоматически",
            "benefit": "рост конверсии на 30-50%",
            "objection_time": "первые результаты через 1 неделю",
            "objection_price": "одна дополнительная сделка окупает вложение",
            "objection_tech": "пошаговые инструкции, поддержка 24/7"
        },
        "marketing": {
            "pain": "контент создаётся вручную, нет системы",
            "transformation": "от хаоса → автоматизированный контент-календарь",
            "benefit": "3x больше контента за то же время",
            "objection_time": "1 день настройки = месяц автоматизации",
            "objection_price": "дешевле штатного SMM-менеджера",
            "objection_tech": "интерфейс проще, чем кажется"
        },
        "general": {
            "pain": "теряют время на рутину вместо роста бизнеса",
            "transformation": "от ручной работы → система работает сама",
            "benefit": "освобождение 10+ часов в неделю",
            "objection_time": "быстрый старт без долгого обучения",
            "objection_price": "инвестиция окупается за неделю",
            "objection_tech": "всё настраивается под вас"
        }
    }
    
    def __init__(self, niche: str = "ai_automation", course_price: int = 350):
        self.niche = niche
        self.course_price = course_price
        self.templates = self.NICHE_TEMPLATES.get(niche, self.NICHE_TEMPLATES["general"])
        self.launch_date = None
    
    def set_launch_date(self, date_str: str):
        """Set course launch date (YYYY-MM-DD)"""
        self.launch_date = datetime.strptime(date_str, "%Y-%m-%d")
    
    def generate_prelaunch_sequence(self) -> List[Dict]:
        """
        Phase 1: 5 warming posts over 7 days
        """
        if not self.launch_date:
            self.launch_date = datetime.now() + timedelta(days=7)
        
        posts = []
        
        # Day -7: Pain point
        day_minus_7 = self.launch_date - timedelta(days=7)
        posts.append({
            "day": -7,
            "date": day_minus_7.strftime("%Y-%m-%d"),
            "type": "pain_point",
            "title": "Почему 90% предпринимателей {pain}?".format(pain=self.templates["pain"]),
            "content": self._generate_pain_post(),
            "platforms": ["Telegram", "Instagram"],
            "goal": "Привлечь внимание к проблеме"
        })
        
        # Day -5: Transformation story
        day_minus_5 = self.launch_date - timedelta(days=5)
        posts.append({
            "day": -5,
            "date": day_minus_5.strftime("%Y-%m-%d"),
            "type": "transformation",
            "title": "История успеха: {transformation}".format(transformation=self.templates["transformation"]),
            "content": self._generate_transformation_post(),
            "platforms": ["Telegram", "Instagram", "Stories"],
            "goal": "Показать возможный результат"
        })
        
        # Day -3: Program reveal
        day_minus_3 = self.launch_date - timedelta(days=3)
        posts.append({
            "day": -3,
            "date": day_minus_3.strftime("%Y-%m-%d"),
            "type": "program_reveal",
            "title": "Что внутри курса — полная программа",
            "content": self._generate_program_post(),
            "platforms": ["Telegram", "Instagram Carousel"],
            "goal": "Раскрыть ценность программы"
        })
        
        # Day -2: Scarcity
        day_minus_2 = self.launch_date - timedelta(days=2)
        posts.append({
            "day": -2,
            "date": day_minus_2.strftime("%Y-%m-%d"),
            "type": "scarcity",
            "title": "Осталось мало мест / цена повышается",
            "content": self._generate_scarcity_post(),
            "platforms": ["Telegram", "Instagram Stories"],
            "goal": "Создать срочность"
        })
        
        # Day -1: Final call
        day_minus_1 = self.launch_date - timedelta(days=1)
        posts.append({
            "day": -1,
            "date": day_minus_1.strftime("%Y-%m-%d"),
            "type": "final_call",
            "title": "Последний день регистрации",
            "content": self._generate_final_call_post(),
            "platforms": ["Telegram", "Instagram", "Stories"],
            "goal": "Закрыть продажи"
        })
        
        return posts
    
    def _generate_pain_post(self) -> str:
        return f"""
😤 Знакомо: {self.templates['pain'].capitalize()}?

Каждый день теряете потенциальных клиентов. Не потому что плохой продукт — а потому что не успеваете отвечать.

Вот что происходит:
• Сообщение приходит в 23:00 → вы спите → клиент ушёл к конкуренту
• 50 сообщений в день → 3 часа на ответы → нет времени на развитие
• Постоянные "а сколько стоит?" → одни и те же вопросы

Я тоже так жил. Пока не настроил систему.

Через 3 дня расскажу, как {self.templates['transformation']}.

Следите за обновлениями 👇

#предпринимательство #автоматизация #AI
""".strip()
    
    def _generate_transformation_post(self) -> str:
        return f"""
✨ История без фильтров

Месяц назад ко мне пришёл Иван. Салон красоты, 40+ сообщений в день, работает с 8:00 до 23:00.

"Уже не знаю, как успевать отвечать. Постоянно теряю клиентов."

Что сделали:
✅ Настроили бота для первичных ответов
✅ Автоматизировали запись на услуги
✅ Создали FAQ для типовых вопросов

Результат через 2 недели:
📉 Время на переписку: 3 часа → 20 минут
📈 Ответ клиенту: 2-3 часа → 2 секунды
💰 Не потеряли ни одного клиента из-за долгого ответа

{self.templates['transformation'].capitalize()}.

В пятницу открываю регистрацию на курс, где показываю пошагово, как настроить такую же систему.

Кто хочет знать первым — ставьте 🔥 в комментариях.

#кейс #результат #автоматизация
""".strip()
    
    def _generate_program_post(self) -> str:
        return f"""
📚 Всё, что внутри курса

Регистрация открывается послезавтра. Вот что получите:

🔹 МОДУЛЬ 1: Аудит текущих процессов
• Где теряете больше всего времени
• Точки автоматизации в вашем бизнесе
• Приоритизация: что автоматизировать первым

🔹 МОДУЛЬ 2: Настройка AI-ассистента
• Создание персонализированного бота
• Интеграция с Telegram/WhatsApp
• FAQ и обработка возражений

🔹 МОДУЛЬ 3: Автоматизация продаж
• Воронка от первого контакта до оплаты
• Follow-up система
• Upselling и повторные продажи

🔹 МОДУЛЬ 4: Масштабирование
• Аналитика и метрики
• Оптимизация на основе данных
• Делегирование и рост

🎁 БОНУСЫ:
• Готовые шаблоны сообщений (цена $200)
• Чек-лист внедрения за 3 дня
• Доступ к закрытому чату выпускников

💰 Инвестиция: ${self.course_price}
📅 Старт: {self.launch_date.strftime('%d.%m.%Y')}

Кто готов? Пишите "ГОТОВ" — напомню, когда откроется регистрация.

#программа #обучение #AI
""".strip()
    
    def _generate_scarcity_post(self) -> str:
        return f"""
⏰ Важное обновление

Регистрация открывается завтра. Но есть нюансы:

🔸 Первый поток — только 15 мест
Лично провожу каждого через настройку. Больше не потяну.

🔸 Цена для первого потока: ${self.course_price}
Следующий поток — ${self.course_price + 150}+ (проверили спрос)

🔸 Старт {self.launch_date.strftime('%d.%m.%Y')}
Уже через 2 дня начинаем.

Почему ограничения? 
Хочу реальных результатов, а не массового потока. Каждый студент должен настроить работающую систему.

Если читаете это — вы в группе риска 😄

Кто точно ворвётся завтра — поставьте 💪

#запуск #курс #ограниченно
""".strip()
    
    def _generate_final_call_post(self) -> str:
        return f"""
🚨 Последний день

Регистрация закрывается сегодня в 23:59.

Что будет, если не зайти сейчас:
❌ Продолжите терять клиентов из-за медленных ответов
❌ Потратите 10+ часов в неделю на рутину
❌ Следующий поток дороже на $150+

Что будет, если зайдёте:
✅ Работающая система через 3 дня
✅ {self.templates['benefit'].capitalize()}
✅ Поддержка и чат единомышленников

Ссылка на регистрацию в шапке профиля 👆

Или напишите мне "КУРС" — вышлю напрямую.

⏰ До закрытия: 8 часов

---
P.S. Если сомневаетесь — напишите вопрос. Честно скажу, подойдёт ли вам курс.

#последнийшанс #регистрация #AI
""".strip()
    
    def generate_sales_post(self, bonuses: List[str] = None) -> str:
        """
        Phase 2: Sales post with AIDA + Social Proof + FAQ
        """
        bonuses = bonuses or ["Шаблоны сообщений", "Чек-лист внедрения", "Закрытый чат"]
        
        return f"""
╔════════════════════════════════════════════════════════╗
║  🚀 КУРС ОТКРЫТ: Автоматизация бизнеса с AI            ║
║  {self.launch_date.strftime('%d.%m.%Y') if self.launch_date else 'Старт сегодня'}                                              ║
╚════════════════════════════════════════════════════════╝

😤 ATTENTION
За последний месяц 3 клиента ушли к конкурентам. Не из-за цены — из-за того, что я ответил через 4 часа.

Вы тоже теряете клиентов из-за медленных ответов?

💡 INTEREST
Представьте: бот отвечает мгновенно 24/7. Вы спите — клиент получает информацию. Вы заняты — запись на услугу происходит автоматически.

{self.templates['transformation'].capitalize()}.

🔥 DESIRE
Что внутри:
• 4 модуля по настройке автоматизации
• Готовые шаблоны (экономия 20+ часов)
• Поддержка лично от меня
• Закрытый чат выпускников

🎁 Бонусы:
""" + "\n".join([f"• {b}" for b in bonuses]) + f"""

💰 Инвестиция: ${self.course_price} (следующий поток +${self.course_price + 150})

✅ ACTION
Регистрация: [ССЫЛКА]
Или напишите "КУРС" в личные сообщения

---

📊 SOCIAL PROOF
"За 2 недели сэкономил 15 часов в неделю. Бот закрыл 70% рутины." — Иван, салон красоты

"Окупился за первую неделю. Не потеряли ни одного клиента из-за ответов." — Анна, магазин чая

---

❓ FAQ

Q: {self.templates['objection_time']}
A: Курс рассчитан на 1 неделю интенсива. Первые результаты — через 2-3 дня.

Q: {self.templates['objection_price']}
A: {self.templates['objection_price'].capitalize()}. Средний студент экономит 10+ часов в неделю × $50/час = $500/неделя.

Q: {self.templates['objection_tech']}
A: {self.templates['objection_tech'].capitalize()}. Без программирования, через визуальные интерфейсы.

---

⏰ Регистрация открыта до {self.launch_date.strftime('%d.%m.%Y') if self.launch_date else 'конца дня'} 23:59

#запуск #курс #автоматизация #AI
"""
    
    def generate_onboarding_sequence(self, student_name: str = "Студент") -> List[Dict]:
        """
        Phase 3: Onboarding messages after payment
        """
        return [
            {
                "order": 1,
                "delay": "0 минут",
                "trigger": "Сразу после оплаты",
                "subject": "Добро пожаловать!",
                "content": f"""
🎉 {student_name}, добро пожаловать на курс!

Ваш доступ активирован.

👇 Первые шаги:
1. Вступите в закрытый чат: [ССЫЛКА]
2. Скачайте материалы: [ССЫЛКА]
3. Заполните анкету для персонализации: [ССЫЛКА]

Старт — {self.launch_date.strftime('%d.%m.%Y') if self.launch_date else 'завтра'}.

Вопросы? Пишите в чат или мне лично.

— AI Genesis
""".strip()
            },
            {
                "order": 2,
                "delay": "1 час",
                "trigger": "Через 1 час",
                "subject": "Как не потеряться в материалах",
                "content": f"""
📚 {student_name}, инструкция по старту

Вот ваш план на ближайшие 24 часа:

✅ Час 1-2: Модуль 1 (Аудит)
→ Определите, что автоматизировать первым

✅ Час 3-4: Практика
→ Сделайте упражнение из модуля

✅ Завтра: Модуль 2
→ Начнём настройку бота

💡 Совет: Не пытайтесь всё сделать за один день. Лучше 1 час качественно, чем 3 часа в спешке.

Вопросы? Задавайте в чате — там уже {self.launch_date.strftime('%d') if self.launch_date else '10'} участников.

— AI Genesis
""".strip()
            },
            {
                "order": 3,
                "delay": "24 часа",
                "trigger": "На следующий день",
                "subject": "Время начинать Модуль 2",
                "content": f"""
🚀 {student_name}, пора к действию

Вы прошли Модуль 1? Отлично!

Сегодня начинаем главное — настройку вашего AI-ассистента.

🔹 Модуль 2: Настройка бота
• Создание персонализированных ответов
• Интеграция с вашими каналами
• Тестирование

⏱️ Время: ~2 часа
🎯 Результат: Работающий бот для первых ответов

Начните сейчас → [ССЫЛКА]

Застряли? Не стесняйтесь спрашивать в чате.

— AI Genesis
""".strip()
            },
            {
                "order": 4,
                "delay": "3 дня",
                "trigger": "Check-in через 3 дня",
                "subject": "Как продвигается?",
                "content": f"""
👋 {student_name}, чек-ин

Прошло 3 дня с начала курса. Как вы?

Быстрый опрос (ответьте цифрой):
1️⃣ Уже настроил бота и вижу результаты
2️⃣ В процессе, есть вопросы
3️⃣ Отстаю, нужна помощь

Важно: если выбираете 2 или 3 — напишите мне. Помогу разобраться.

💡 Напоминаю: в чате уже несколько человек с рабочими ботами. Можете задать им вопросы.

Продолжайте в том же духе!

— AI Genesis
""".strip()
            }
        ]
    
    def generate_launch_report(
        self,
        registrations: int = 0,
        sales: int = 0,
        revenue: int = 0,
        refunds: int = 0,
        nps: int = 0
    ) -> Dict:
        """
        Phase 4: Launch analytics report
        """
        conversion = round(sales / max(registrations, 1) * 100, 1)
        avg_check = round(revenue / max(sales, 1))
        refund_rate = round(refunds / max(sales, 1) * 100, 1)
        
        report = {
            "launch_date": self.launch_date.strftime("%Y-%m-%d") if self.launch_date else "N/A",
            "course_price": self.course_price,
            "metrics": {
                "registrations": registrations,
                "sales": sales,
                "revenue": revenue,
                "conversion_rate": f"{conversion}%",
                "avg_check": f"${avg_check}",
                "refunds": refunds,
                "refund_rate": f"{refund_rate}%",
                "nps": nps
            },
            "interpretation": self._interpret_metrics(conversion, refund_rate, nps),
            "recommendations": self._generate_recommendations(conversion, refund_rate)
        }
        
        return report
    
    def _interpret_metrics(self, conversion: float, refund_rate: float, nps: int) -> Dict:
        """Interpret launch metrics"""
        interpretation = {}
        
        # Conversion
        if conversion >= 5:
            interpretation["conversion"] = "✅ Отличная конверсия (>5%)"
        elif conversion >= 2:
            interpretation["conversion"] = "⚠️ Нормальная конверсия (2-5%)"
        else:
            interpretation["conversion"] = "❌ Низкая конверсия (<2%) — проверьте воронку"
        
        # Refund rate
        if refund_rate <= 5:
            interpretation["refunds"] = "✅ Низкий уровень возвратов"
        elif refund_rate <= 10:
            interpretation["refunds"] = "⚠️ Средний уровень возвратов"
        else:
            interpretation["refunds"] = "❌ Высокий уровень возвратов — проверьте ожидания"
        
        # NPS
        if nps >= 50:
            interpretation["nps"] = "✅ Отличная удовлетворённость"
        elif nps >= 30:
            interpretation["nps"] = "⚠️ Хорошая удовлетворённость"
        else:
            interpretation["nps"] = "❌ Нужно улучшать продукт"
        
        return interpretation
    
    def _generate_recommendations(self, conversion: float, refund_rate: float) -> List[str]:
        """Generate recommendations based on metrics"""
        recs = []
        
        if conversion < 2:
            recs.append("Добавить больше социальных доказательств в прогрев")
            recs.append("Упростить процесс регистрации")
        
        if refund_rate > 10:
            recs.append("Уточнить ожидания в прогревочных постах")
            recs.append("Добавить пробный модуль перед покупкой")
        
        if not recs:
            recs.append("Масштабировать: увеличить рекламный бюджет")
            recs.append("Запустить партнёрскую программу")
        
        return recs
    
    def generate_full_launch_package(self) -> Dict:
        """Generate complete launch package"""
        return {
            "meta": {
                "generated_at": datetime.now().isoformat(),
                "niche": self.niche,
                "course_price": self.course_price,
                "launch_date": self.launch_date.strftime("%Y-%m-%d") if self.launch_date else "TBD"
            },
            "phase_1_prelaunch": self.generate_prelaunch_sequence(),
            "phase_2_sales_post": self.generate_sales_post(),
            "phase_3_onboarding": self.generate_onboarding_sequence(),
            "phase_4_report_template": "Use generate_launch_report() after launch"
        }

def main():
    import sys
    
    if len(sys.argv) < 2:
        print("🚀 Course Launch Automation for AI Genesis")
        print("")
        print("Usage:")
        print("  python3 course_launch.py prelaunch [niche] [date]     # 5 warming posts")
        print("  python3 course_launch.py sales [niche] [price]        # Sales post")
        print("  python3 course_launch.py onboarding [name]            # Onboarding sequence")
        print("  python3 course_launch.py full [niche] [date] [price]  # Complete package")
        print("  python3 course_launch.py report [reg] [sales] [rev]   # Launch report")
        print("")
        print("Niches: ai_automation, sales, marketing, general")
        print("Date format: YYYY-MM-DD")
        print("")
        print("Examples:")
        print('  python3 course_launch.py prelaunch ai_automation 2026-04-01')
        print('  python3 course_launch.py sales ai_automation 350')
        print('  python3 course_launch.py full ai_automation 2026-04-01 350')
        sys.exit(0)
    
    command = sys.argv[1]
    
    if command == "prelaunch":
        niche = sys.argv[2] if len(sys.argv) > 2 else "ai_automation"
        date = sys.argv[3] if len(sys.argv) > 3 else None
        
        launcher = CourseLaunchAutomation(niche)
        if date:
            launcher.set_launch_date(date)
        
        posts = launcher.generate_prelaunch_sequence()
        
        print(f"\n🚀 Pre-launch Sequence for {niche}")
        print(f"Launch date: {launcher.launch_date.strftime('%Y-%m-%d') if launcher.launch_date else 'TBD'}")
        print("="*60)
        
        for post in posts:
            print(f"\n📅 Day {post['day']} ({post['date']}) - {post['type']}")
            print(f"Title: {post['title']}")
            print(f"Platforms: {', '.join(post['platforms'])}")
            print(f"Goal: {post['goal']}")
            print(f"\n{post['content']}")
            print("-"*60)
    
    elif command == "sales":
        niche = sys.argv[2] if len(sys.argv) > 2 else "ai_automation"
        price = int(sys.argv[3]) if len(sys.argv) > 3 else 350
        
        launcher = CourseLaunchAutomation(niche, price)
        
        print(f"\n💰 Sales Post for {niche} (${price})")
        print("="*60)
        print(launcher.generate_sales_post())
    
    elif command == "onboarding":
        name = sys.argv[2] if len(sys.argv) > 2 else "Студент"
        
        launcher = CourseLaunchAutomation()
        sequence = launcher.generate_onboarding_sequence(name)
        
        print(f"\n📚 Onboarding Sequence for {name}")
        print("="*60)
        
        for msg in sequence:
            print(f"\n📧 Message {msg['order']} ({msg['delay']})")
            print(f"Subject: {msg['subject']}")
            print(f"\n{msg['content']}")
            print("-"*60)
    
    elif command == "full":
        niche = sys.argv[2] if len(sys.argv) > 2 else "ai_automation"
        date = sys.argv[3] if len(sys.argv) > 3 else None
        price = int(sys.argv[4]) if len(sys.argv) > 4 else 350
        
        launcher = CourseLaunchAutomation(niche, price)
        if date:
            launcher.set_launch_date(date)
        
        package = launcher.generate_full_launch_package()
        
        # Save to file
        output_file = f"/root/.openclaw/output/course_launch_{niche}_{datetime.now().strftime('%Y%m%d')}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(package, f, indent=2, ensure_ascii=False)
        
        print(f"\n📦 Full Launch Package Generated")
        print(f"Niche: {niche}")
        print(f"Price: ${price}")
        print(f"Launch date: {date or 'TBD'}")
        print(f"\nSaved to: {output_file}")
        print(f"\nContents:")
        print(f"  • 5 pre-launch posts")
        print(f"  • 1 sales post (AIDA)")
        print(f"  • 4 onboarding messages")
        print(f"  • Report template")
    
    elif command == "report":
        registrations = int(sys.argv[2]) if len(sys.argv) > 2 else 100
        sales = int(sys.argv[3]) if len(sys.argv) > 3 else 5
        revenue = int(sys.argv[4]) if len(sys.argv) > 4 else 1750
        refunds = int(sys.argv[5]) if len(sys.argv) > 5 else 0
        nps = int(sys.argv[6]) if len(sys.argv) > 6 else 45
        
        launcher = CourseLaunchAutomation()
        report = launcher.generate_launch_report(registrations, sales, revenue, refunds, nps)
        
        print("\n📊 LAUNCH REPORT")
        print("="*60)
        print(json.dumps(report, indent=2, ensure_ascii=False))
    
    else:
        print(f"❌ Unknown command: {command}")
        print("Run without arguments for help")

if __name__ == "__main__":
    main()
