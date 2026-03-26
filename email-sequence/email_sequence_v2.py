#!/usr/bin/env python3
"""
Email Sequence Generator v2.0 for AI Genesis
Covers all business types with validation and defaults
"""

import json
import re
from datetime import datetime, timedelta

class EmailSequenceGenerator:
    """Generate email drip campaigns with smart defaults"""
    
    # Default values for all variables
    DEFAULTS = {
        # Business info
        "brand_name": "AI Genesis",
        "business_name": "AI Genesis",
        "product_name": "AI Assistant",
        "service_name": "Консультация",
        "clinic_name": "Центр Здоровья",
        "restaurant_name": "Наше Кафе",
        "course_name": "Курс по автоматизации",
        "agent_name": "Иван",
        "doctor_name": "Доктор Смирнов",
        "trainer_name": "Анна",
        
        # Client info
        "client_name": "Уважаемый клиент",
        "patient_name": "Уважаемый пациент",
        "student_name": "Уважаемый студент",
        "customer_name": "Уважаемый покупатель",
        "buyer_name": "Уважаемый покупатель",
        
        # Links
        "cta_link": "https://t.me/Rbmultibot",
        "checkout_url": "https://aigenesis.com/order",
        "feature_link": "https://aigenesis.com/features",
        "pricing_url": "https://aigenesis.com/pricing",
        "reschedule_link": "https://t.me/Rbmultibot",
        "cancel_link": "https://t.me/Rbmultibot",
        "review_link": "https://g.page/r/CeIexample/review",
        "webinar_link": "https://zoom.us/j/example",
        "product_link": "https://aigenesis.com/product",
        "demo_link": "https://calendly.com/aigenesis/demo",
        "best_sellers_url": "https://aigenesis.com/bestsellers",
        "new_arrivals_url": "https://aigenesis.com/new",
        "return_policy_url": "https://aigenesis.com/return",
        
        # Content
        "best_categories": "• Автоматизация бизнеса\n• AI-ассистенты\n• Оптимизация процессов",
        "bestsellers": "1. AI Pilot ($350)\n2. Полная настройка ($700)\n3. Аудит ($100)",
        "trending_now": "• Чат-боты для записи\n• Автоответы в Telegram\n• Интеграция с CRM",
        "quick_start_step_1": "Подключите Telegram",
        "quick_start_step_2": "Настройте сценарии диалога",
        "quick_start_step_3": "Протестируйте бота",
        "case_study": "Салон красоты 'Гармония' — внедрили бота, сократили время ответа с 2 часов до 30 секунд. Конверсия выросла на 35%.",
        "roi_metric": "15 часов экономии в неделю",
        "result_metric": "+40% к конверсии",
        "social_proof": "Более 50 предпринимателей уже автоматизировали свой бизнес",
        
        # Appointments
        "appointment_date": "уточняется",
        "appointment_time": "уточняется",
        "location": "Онлайн / Telegram",
        "next_appointment": "в течение недели",
        "delivery_date": "3-5 рабочих дней",
        "preparation_checklist": "• Подготовьте список вопросов\n• Продумайте сценарии диалога",
        "what_to_bring": "• Список частых вопросов клиентов\n• Доступ к Telegram",
        "treatment_plan": "Индивидуальный план будет составлен после консультации",
        "next_lesson": "Урок 1: Основы автоматизации",
        
        # Special
        "welcome_gift": "Чек-лист '10 процессов для автоматизации'",
        "bonus_lesson": "Бонус: Шаблоны диалогов для бота",
        "webinar_topic": "Как автоматизировать бизнес за 2 недели",
        "webinar_time": "Среда 19:00 МСК",
        "menu_pdf": "https://aigenesis.com/menu",
        "reservation_url": "https://t.me/Rbmultibot",
        "reservation_link": "https://t.me/Rbmultibot",
        "company_name": "AI Genesis",
        "sender_name": "Команда AI Genesis",
        "trial_duration": "14 дней",
        "discount_code": "WELCOME10",
        "discount_percentage": "10%",
        "plan_name": "AI Pilot",
        "next_charge_date": "через 30 дней",
        "expiration_date": "через 7 дней",
        "membership_type": "Базовый",
        "points_balance": "100",
        "available_discounts": "Скидка 10% на первый заказ",
        "delivery_estimate": "3-5 рабочих дней",
        "membership_benefits": "• Приоритетная поддержка\n• Эксклюзивные материалы\n• Скидки на услуги",
        "level": "1",
        "progress_percentage": "0%",
        "next_level_benefits": "• Расширенные функции\n• Персональный менеджер",
        "order_number": "AG-0001",
        "items_list": "• AI Pilot ($350)\n• Настройка ($0 — в пилоте)",
        "tracking_url": "https://t.me/Rbmultibot",
        "cart_items": "• Консультация ($100)",
        "abandoned_product": "AI Pilot ($350)",
        "referral_link": "https://aigenesis.com/ref/example",
        "success_stories": "50+ предпринимателей уже автоматизировали бизнес",
        "communities": "Telegram: @aigenesis_chat",
        "onboarding_steps": "1. Заполните бриф\n2. Получите доступ\n3. Начните обучение",
        "syllabus_overview": "Модуль 1: Введение в AI\nМодуль 2: Практика\nМодуль 3: Результат",
        "progress_overview": "Пройдено: 0%\nОсталось: 100%",
        "next_lessons": "Урок 1: Настройка бота\nУрок 2: Тестирование",
        "tip_content": "Совет: Начните с одного процесса, не пытайтесь автоматизировать всё сразу.",
        "special_offer": "Пилот за $350 вместо $700 — до конца месяца",
        "offer_deadline": "до конца месяца",
        "survey_url": "https://forms.gle/example",
        "first_day_info": "Начните с простого: запишите 5 частых вопросов клиентов.",
        "final_exam_info": "Финальный проект: настройте бота для своего бизнеса.",
        "project_idea": "Автоматизация записи клиентов",
        "group_invite": "https://t.me/+example",
        "course_community": "https://t.me/+example",
        "project_examples": "• Бот для салона красоты\n• Автоответы для доставки",
        "portfolio_url": "https://aigenesis.com/cases",
    }
    
    TEMPLATES = {
        # === E-COMMERCE ===
        "ecommerce_welcome": {
            "name": "E-commerce Welcome Series",
            "description": "Onboarding для новых покупателей интернет-магазина",
            "emails": [
                {
                    "day": 0,
                    "subject": "Добро пожаловать! Ваш бонус внутри 🎁",
                    "subject_b": "Спасибо за регистрацию — скидка 10%",
                    "preview": "Персональный код на первый заказ",
                    "body": """Здравствуйте!

Спасибо, что присоединились к {brand_name}!

Ваш персональный код на первый заказ:
🎁 {discount_code} — скидка {discount_percentage}

Действует 7 дней на любые товары.

Лучшие категории:
{best_categories}

Счастливых покупок!
{brand_name}""",
                    "cta": "Начать покупки",
                    "role": "welcome"
                },
                {
                    "day": 3,
                    "subject": "Популярное этой недели 🔥",
                    "subject_b": "Топ товаров, которые вы можете пропустить",
                    "preview": "Тренды и бестселлеры",
                    "body": """Привет!

Вот что покупают чаще всего прямо сейчас:

{bestsellers}

Осталось мало — успейте выбрать!

{brand_name}""",
                    "cta": "Смотреть хиты",
                    "role": "engagement"
                },
                {
                    "day": 7,
                    "subject": "Ваш код {discount_code} сгорит через 24 часа ⏰",
                    "subject_b": "Последний шанс — скидка {discount_percentage}",
                    "preview": "Используйте код сейчас",
                    "body": """Здравствуйте!

Ваш персональный код {discount_code} действует ещё 24 часа.

После этого он сгорит безвозвратно.

Не упустите скидку {discount_percentage} на первый заказ!

{checkout_url}

{brand_name}""",
                    "cta": "Использовать скидку",
                    "role": "urgency"
                }
            ]
        },
        
        # === SAAS/TECH ===
        "saas_trial": {
            "name": "SaaS Trial Onboarding",
            "description": "Onboarding для trial-пользователей SaaS",
            "emails": [
                {
                    "day": 0,
                    "subject": "Ваш trial активирован! Начните здесь 👋",
                    "subject_b": "Добро пожаловать в {product_name}",
                    "preview": "Быстрый старт за 5 минут",
                    "body": """Здравствуйте!

Ваш trial доступ активирован на {trial_duration}.

Быстрый старт:
1️⃣ {quick_start_step_1}
2️⃣ {quick_start_step_2}
3️⃣ {quick_start_step_3}

💡 Совет: пользователи, которые завершают эти 3 шага, получают в 3 раза больше пользы от {product_name}.

{cta_link}

{sender_name}""",
                    "cta": "Начать настройку",
                    "role": "welcome"
                },
                {
                    "day": 2,
                    "subject": "Как {company_name} сэкономили {result_metric}",
                    "subject_b": "Кейс: реальный результат за 2 недели",
                    "preview": "Посмотрите, как это работает",
                    "body": """Привет!

Хотите знать, как другие используют {product_name}?

{case_study}

Ключевые выводы:
✅ Настройка заняла 2 часа
✅ Результат через неделю
✅ Окупаемость — в первый месяц

Повторите их успех:
{feature_link}

{sender_name}""",
                    "cta": "Посмотреть кейсы",
                    "role": "social_proof"
                },
                {
                    "day": 7,
                    "subject": "Половина trial прошла — вот ваш прогресс 📊",
                    "subject_b": "Осталось 7 дней trial",
                    "preview": "Продолжайте в том же духе",
                    "body": """Здравствуйте!

Прошла половина вашего trial.

Что вы уже попробовали?

Если нужна помощь — напишите нам:
{cta_link}

А вот что могло бы пригодиться:
{feature_link}

{sender_name}""",
                    "cta": "Получить помощь",
                    "role": "progress"
                },
                {
                    "day": 12,
                    "subject": "Trial заканчивается через 2 дня — что дальше?",
                    "subject_b": "Сохраните доступ к {product_name}",
                    "preview": "Выберите подходящий план",
                    "body": """Здравствуйте!

Через 2 дня ваш trial закончится.

Чтобы не потерять настройки:

🚀 Перейдите на {plan_name}
💳 Первый платёж: {next_charge_date}

{pricing_url}

Вопросы? Ответим в Telegram:
{cta_link}

{sender_name}""",
                    "cta": "Выбрать план",
                    "role": "conversion"
                }
            ]
        },
        
        # === SERVICES ===
        "service_booking": {
            "name": "Service Business Booking",
            "description": "Для бизнеса услуг: консультации, ремонт, красота",
            "emails": [
                {
                    "day": 0,
                    "subject": "Запись подтверждена! Детали внутри 📅",
                    "subject_b": "Вы записаны на {service_name}",
                    "preview": "Дата, время и подготовка",
                    "body": """Здравствуйте, {client_name}!

Вы записаны на {service_name}.

📅 Дата: {appointment_date}
⏰ Время: {appointment_time}
📍 Адрес: {location}

Подготовка:
{preparation_checklist}

Изменить запись: {reschedule_link}
Отменить: {cancel_link}

Ждём вас!
{business_name}""",
                    "cta": "Добавить в календарь",
                    "role": "confirmation"
                },
                {
                    "day": -1,
                    "subject": "Напоминание: завтра {service_name} ⏰",
                    "subject_b": "Не забудьте про запись",
                    "preview": "{appointment_time}, {location}",
                    "body": """Здравствуйте, {client_name}!

Напоминаем: завтра {service_name}.

⏰ {appointment_time}
📍 {location}

Что взять с собой:
{what_to_bring}

Если планы изменились — дайте знать заранее.

{business_name}""",
                    "cta": "Подтвердить приход",
                    "role": "reminder"
                },
                {
                    "day": 0,
                    "hour": 2,
                    "subject": "Спасибо за визит! Ваш фидбек важен 🙏",
                    "subject_b": "Как прошло? Расскажите",
                    "preview": "Оцените качество услуги",
                    "body": """{client_name}, здравствуйте!

Спасибо, что выбрали {business_name}!

Как прошла {service_name}?

Уделите 1 минуту — оставьте отзыв:
{review_link}

Ваше мнение помогает нам стать лучше.

А пока — скидка 10% на следующий визит:
Код: {discount_code}

До встречи!
{business_name}""",
                    "cta": "Оставить отзыв",
                    "role": "feedback"
                }
            ]
        },
    }
    
    def get_template(self, template_name):
        """Get template by name with error handling"""
        if template_name not in self.TEMPLATES:
            available = ", ".join(self.TEMPLATES.keys())
            raise ValueError(f"Unknown template: {template_name}. Available: {available}")
        return self.TEMPLATES[template_name]
    
    def generate(self, template_name, custom_vars=None):
        """Generate email sequence with smart defaults"""
        template = self.get_template(template_name)
        
        # Merge defaults with custom vars
        variables = self.DEFAULTS.copy()
        if custom_vars:
            variables.update(custom_vars)
        
        # Process each email
        emails = []
        for email in template["emails"]:
            processed = {}
            for key, value in email.items():
                if isinstance(value, str):
                    # Replace all {variable} patterns
                    processed[key] = self._replace_vars(value, variables)
                else:
                    processed[key] = value
            emails.append(processed)
        
        return {
            "name": template["name"],
            "description": template["description"],
            "generated_at": datetime.now().isoformat(),
            "total_emails": len(emails),
            "emails": emails
        }
    
    def _replace_vars(self, text, variables):
        """Replace all {variable} patterns in text"""
        def replacer(match):
            var_name = match.group(1)
            if var_name in variables:
                return str(variables[var_name])
            # If variable not found, return original or empty
            return match.group(0)
        
        return re.sub(r'\{(\w+)\}', replacer, text)
    
    def list_templates(self):
        """List all available templates"""
        print("📧 All available templates:\n")
        print("Categories: e-commerce, saas, services, healthcare, realestate,")
        print("            education, restaurant, subscription, consulting, specialty\n")
        
        for key, template in self.TEMPLATES.items():
            print(f"  {key}")
            print(f"    {template['description']}")
            print()


def main():
    import sys
    
    generator = EmailSequenceGenerator()
    
    if len(sys.argv) < 2:
        generator.list_templates()
        sys.exit(0)
    
    template_name = sys.argv[1]
    
    # Parse additional variables from args
    custom_vars = {}
    for arg in sys.argv[2:]:
        if "=" in arg:
            key, value = arg.split("=", 1)
            custom_vars[key] = value
    
    try:
        result = generator.generate(template_name, custom_vars)
        
        print(f"📧 Sequence generated: {result['name']}")
        print(f"   Total emails: {result['total_emails']}")
        print(f"   Output: /root/.openclaw/output/email_sequence_{template_name}.json\n")
        
        # Save to file
        output_dir = "/root/.openclaw/output"
        import os
        os.makedirs(output_dir, exist_ok=True)
        
        filepath = f"{output_dir}/email_sequence_{template_name}.json"
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        
        # Print summary
        print("📧 Email flow:")
        for email in result["emails"]:
            day_str = f"Day {email['day']}" if email['day'] >= 0 else f"Day {email['day']} (before)"
            print(f"   {day_str}: {email['subject']}")
        
    except ValueError as e:
        print(f"❌ {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
