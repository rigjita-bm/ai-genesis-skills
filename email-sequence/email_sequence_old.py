#!/usr/bin/env python3
"""
Email Sequence Generator for AI Genesis - Universal Version
Covers all business types: e-commerce, SaaS, services, healthcare, etc.
"""

import json
from datetime import datetime, timedelta

class EmailSequenceGenerator:
    """Generate email drip campaigns for any business type"""
    
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
🎁 WELCOME10 — скидка 10%

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

Осталось мало — успейте выбрать размер!

{brand_name}""",
                    "cta": "Смотреть хиты",
                    "role": "engagement"
                },
                {
                    "day": 7,
                    "subject": "Ваш код WELCOME10 сгорит через 24 часа ⏰",
                    "subject_b": "Последний шанс — скидка 10%",
                    "preview": "Используйте код сейчас",
                    "body": """Здравствуйте!

Ваш персональный код WELCOME10 действует ещё 24 часа.

После этого он сгорит безвозвратно.

Не упустите скидку 10% на первый заказ!

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

Ваш trial доступ активирован на 14 дней.

Быстрый старт:
1️⃣ {quick_start_step_1}
2️⃣ {quick_start_step_2}
3️⃣ {quick_start_step_3}

💡 Совет: пользователи, которые завершают эти 3 шага, получают в 3 раза больше пользы от {product_name}.

Нужна помощь? Просто ответьте на это письмо.

Команда {product_name}""",
                    "cta": "Начать работу",
                    "role": "activation"
                },
                {
                    "day": 2,
                    "subject": "Как {company_name} сэкономили {result_metric}",
                    "subject_b": "Кейс: реальные результаты клиентов",
                    "preview": "История успеха вашей индустрии",
                    "body": """Привет!

Посмотрите, как {company_name} используют {product_name}:

{case_study_summary}

Результаты:
✓ {result_1}
✓ {result_2}
✓ {result_3}

Хотите такие же результаты? 

{cta_link}

Команда {product_name}""",
                    "cta": "Прочитать кейс",
                    "role": "social_proof"
                },
                {
                    "day": 7,
                    "subject": "Половина trial прошла — вот ваш прогресс 📊",
                    "subject_b": "7 дней с {product_name}: итоги",
                    "preview": "Персональная статистика",
                    "body": """Здравствуйте!

Прошла неделя вашего trial. Вот что вы сделали:

{user_progress}

👍 Хороший старт! Но есть куда расти.

Пользователи с похожим прогрессом обычно пробуют {advanced_feature} — это даёт {benefit}.

Попробовать: {feature_link}

Команда {product_name}""",
                    "cta": "Попробовать функцию",
                    "role": "expansion"
                },
                {
                    "day": 12,
                    "subject": "Trial заканчивается через 2 дня — что дальше?",
                    "subject_b": "Сохраните доступ к {product_name}",
                    "preview": "Тарифы и скидка на апгрейд",
                    "body": """Привет!

Ваш trial заканчивается {trial_end_date}.

Что будет дальше?
• Все данные сохранятся
• Доступ ограничится
• Можно апгрейдить в любой момент

Тарифы от ${price_monthly}/мес
🎁 Скидка 20% при оплате за год

Выбрать тариф: {pricing_url}

Вопросы? Ответьте на это письмо — поможем выбрать.

Команда {product_name}""",
                    "cta": "Выбрать тариф",
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
Код: BACK10

До встречи!
{business_name}""",
                    "cta": "Оставить отзыв",
                    "role": "feedback"
                }
            ]
        },
        
        # === HEALTHCARE/WELLNESS ===
        "healthcare_onboarding": {
            "name": "Healthcare & Wellness Onboarding",
            "description": "Для клиник, wellness-центров, фитнеса",
            "emails": [
                {
                    "day": 0,
                    "subject": "Добро пожаловать в {clinic_name}! Ваш план лечения",
                    "subject_b": "Первые шаги к здоровью",
                    "preview": "Персональные рекомендации",
                    "body": """Здравствуйте, {patient_name}!

Спасибо за доверие к {clinic_name}.

Ваш персональный план:
{treatment_plan}

Ближайший приём:
📅 {next_appointment}
⏰ {appointment_time}
👨‍⚕️ {doctor_name}

Подготовка к визиту:
{preparation_notes}

Вопросы? Звоните: {phone}

С заботой о вашем здоровье,
{clinic_name}""",
                    "cta": "Подтвердить приём",
                    "role": "onboarding"
                },
                {
                    "day": 3,
                    "subject": "Как вы себя чувствуете? 🌿",
                    "subject_b": "Проверка самочувствия",
                    "preview": "Важно знать ваш прогресс",
                    "body": """{patient_name}, здравствуйте!

Прошло 3 дня с начала лечения.

Как вы себя чувствуете?

Если появились:
• Новые симптомы
• Вопросы по приёму препаратов
• Необходимость корректировки плана

Свяжитесь с нами: {contact_link}

Также полезно:
{health_tips}

{clinic_name}""",
                    "cta": "Сообщить о самочувствии",
                    "role": "check_in"
                },
                {
                    "day": 14,
                    "subject": "Пора на повторный приём? 📅",
                    "subject_b": "Контрольный осмотр",
                    "preview": "Запишитесь на следующий визит",
                    "body": """Здравствуйте, {patient_name}!

Прошло 2 недели с вашего последнего визита.

Для контроля динамики рекомендуем повторный приём.

Свободные даты:
{available_slots}

Записаться: {booking_link}

Или позвоните: {phone}

{clinic_name}""",
                    "cta": "Записаться",
                    "role": "retention"
                }
            ]
        },
        
        # === REAL ESTATE ===
        "realestate_buyer": {
            "name": "Real Estate Buyer Journey",
            "description": "Для риелторов и агентств недвижимости",
            "emails": [
                {
                    "day": 0,
                    "subject": "Ваш запрос на {property_type} получен 🏠",
                    "subject_b": "Начинаем поиск недвижимости",
                    "preview": "Следующие шаги и гайд",
                    "body": """Здравствуйте, {client_name}!

Спасибо за обращение в {agency_name}.

Параметры поиска:
📍 Район: {area}
🏠 Тип: {property_type}
💰 Бюджет: {budget}

Что дальше:
1️⃣ Подберём варианты (1-2 дня)
2️⃣ Согласуем удобное время для просмотров
3️⃣ Организуем показы

Пока скачайте гайд:
"Как купить {property_type} безопасно"
{guide_link}

Вопросы? Пишите или звоните: {phone}

{agent_name}
{agency_name}""",
                    "cta": "Скачать гайд",
                    "role": "acknowledgment"
                },
                {
                    "day": 2,
                    "subject": "5 вариантов по вашим критериям 🏘️",
                    "subject_b": "Новые объекты в {area}",
                    "preview": "Эксклюзивные предложения",
                    "body": """{client_name}, здравствуйте!

Подобрали варианты под ваш запрос:

{property_listings}

Хотите посмотреть?
Ответьте на письмо или позвоните {phone}

Также есть 2 объекта, которые пока не на сайте — спрашивайте 😉

{agent_name}
{agency_name}""",
                    "cta": "Записаться на просмотр",
                    "role": "nurture"
                },
                {
                    "day": 7,
                    "subject": "Рынок {area}: цены и тренды 📊",
                    "subject_b": "Аналитика района",
                    "preview": "Поможет принять решение",
                    "body": """Здравствуйте, {client_name}!

Краткий анализ рынка {area}:

💰 Средняя цена: {avg_price}
📈 Динамика: {price_trend}
⏱️ Среднее время продажи: {avg_days} дней
🏗️ Новостройки: {new_developments}

{market_insights}

Это поможет вам ориентироваться в ценах при выборе.

Свежие объекты: {listings_url}

{agent_name}
{agency_name}""",
                    "cta": "Смотреть все варианты",
                    "role": "education"
                }
            ]
        },
        
        # === EDUCATION ===
        "education_course": {
            "name": "Online Course Enrollment",
            "description": "Для онлайн-курсов и образовательных платформ",
            "emails": [
                {
                    "day": 0,
                    "subject": "Вы записаны на курс! Вот ваш доступ 📚",
                    "subject_b": "Добро пожаловать в {course_name}",
                    "preview": "Старт обучения и материалы",
                    "body": """Здравствуйте, {student_name}!

Поздравляем с записью на курс "{course_name}"!

🎯 Что вы получите:
{learning_outcomes}

📅 Старт: {start_date}
⏱️ Длительность: {duration}
📱 Формат: {format}

Ваш личный кабинет:
{dashboard_link}

Логин: {login}
Пароль: {password}

Совет: пройдите вводный модуль сегодня — это займёт 15 минут и задаст темп.

Вопросы? {support_link}

С наилучшими пожеланиями,
Команда {school_name}""",
                    "cta": "Начать обучение",
                    "role": "enrollment"
                },
                {
                    "day": 1,
                    "subject": "День 1: ваша первая маленькая победа 🏆",
                    "subject_b": "Пройдите первый урок сегодня",
                    "preview": "15 минут — и первый шаг сделан",
                    "body": """{student_name}, привет!

Вчера вы начали курс. Как ощущения?

Секрет успешного обучения — маленькие шаги каждый день.

Ваша цель на сегодня:
✓ Пройти Урок 1 (15 минут)
✓ Сделать первое задание

Начать: {lesson_1_link}

💡 Те, кто проходит первый урок в день старта, заканчивают курс в 3 раза чаще.

Вперёд!

Команда {school_name}""",
                    "cta": "Урок 1",
                    "role": "engagement"
                },
                {
                    "day": 7,
                    "subject": "Неделя 1: ваш прогресс и следующие шаги 📊",
                    "subject_b": "Проверьте свою статистику",
                    "preview": "Вы на {progress_percent}%",
                    "body": """{student_name}, здравствуйте!

Прошла первая неделя. Ваши результаты:

✓ Пройдено уроков: {completed_lessons}/{total_lessons}
✓ Выполнено заданий: {completed_assignments}
✓ Средняя оценка: {avg_score}
✓ Общий прогресс: {progress_percent}%

{progress_feedback}

Следующая цель: {next_milestone}

Продолжить: {continue_link}

Команда {school_name}""",
                    "cta": "Продолжить обучение",
                    "role": "progress"
                },
                {
                    "day": 21,
                    "subject": "{student_name}, вы близки к цели! 🎯",
                    "subject_b": "Осталось {lessons_left} уроков",
                    "preview": "Не сбавляйте темп",
                    "body": """{student_name}, привет!

Вы прошли {progress_percent}% курса — осталось совсем немного!

Осталось:
• {lessons_left} уроков
• {assignments_left} заданий
• Итоговый проект

Финиш уже видно 🏁

{motivational_message}

Завершить курс: {continue_link}

Команда {school_name}""",
                    "cta": "Дойти до конца",
                    "role": "retention"
                }
            ]
        },
        
        # === RESTAURANT/FOOD ===
        "restaurant_loyalty": {
            "name": "Restaurant Loyalty Program",
            "description": "Для ресторанов, кафе, доставки еды",
            "emails": [
                {
                    "day": 0,
                    "subject": "Добро пожаловать в клуб {restaurant_name}! 🍽️",
                    "subject_b": "Ваш столик ждёт",
                    "preview": "Бонусы и привилегии",
                    "body": """{customer_name}, здравствуйте!

Спасибо, что выбрали {restaurant_name}!

Вы в клубе постоянных гостей.

🎁 Ваши бонусы:
• Скидка 10% на каждый заказ
• Праздничный десерт в день рождения
• Ранний доступ к новому меню
• Бронирование без предоплаты

Попробуйте наши фирменные блюда:
{signature_dishes}

Забронировать столик:
{booking_link} или {phone}

{restaurant_name}""",
                    "cta": "Забронировать стол",
                    "role": "welcome"
                },
                {
                    "day": 14,
                    "subject": "Скучаем по вам! Возвращайтесь со скидкой 🎉",
                    "subject_b": "Мы приготовили ваше любимое",
                    "preview": "Скидка 15% на следующий визит",
                    "body": """{customer_name}, привет!

Давно не виделись!

Последний раз вы были у нас {last_visit_date}.

За это время:
• Обновили меню — {new_dishes_count} новых блюд
• Появилось сезонное предложение
• Приготовили ваш фаворит — {favorite_dish}

Возвращайтесь со скидкой 15%:
Код: MISSYOU15
Действует до: {expiry_date}

Забронировать: {booking_link}

{restaurant_name}""",
                    "cta": "Забронировать со скидкой",
                    "role": "win_back"
                }
            ]
        },
        
        # === SUBSCRIPTION ===
        "subscription_retention": {
            "name": "Subscription Retention",
            "description": "Для подписочных сервисов: box, membership, SaaS",
            "emails": [
                {
                    "day": 0,
                    "subject": "Подписка оформлена! Вот что будет дальше 📦",
                    "subject_b": "Добро пожаловать в {subscription_name}",
                    "preview": "Дата первой доставки",
                    "body": """{subscriber_name}, здравствуйте!

Спасибо за подписку на {subscription_name}!

Ваш план: {plan_name}
💰 {price}/{billing_period}

Первая доставка:
📅 {first_delivery_date}
📍 {delivery_address}

Что внутри:
{box_contents}

Управлять подпиской: {account_link}
Изменить дату доставки: {reschedule_link}

Вопросы? {support_link}

{subscription_name}""",
                    "cta": "Посмотреть детали подписки",
                    "role": "confirmation"
                },
                {
                    "day": 30,
                    "subject": "Месяц с вами! Что получилось 🎁",
                    "subject_b": "Итоги первого месяца",
                    "preview": "Персональная статистика",
                    "body": """{subscriber_name}, привет!

Прошёл первый месяц вашей подписки.

Ваши результаты:
📦 Получено: {boxes_received}
💰 Сэкономлено: {savings_amount}
⭐ Оценка: {average_rating}

Что дальше?
Следующая доставка: {next_delivery_date}

Эксклюзивно для подписчиков:
{exclusive_offer}

{subscription_name}""",
                    "cta": "Продлить подписку",
                    "role": "retention"
                },
                {
                    "day": -3,
                    "subject": "Подписка заканчивается через 3 дня",
                    "subject_b": "Продлите до {expiry_date}",
                    "preview": "Не прерывайте получение боксов",
                    "body": """{subscriber_name}, здравствуйте!

Ваша подписка заканчивается {expiry_date}.

Чтобы не пропустить следующую доставку, продлите сейчас.

🎁 Бонус при продлении:
{renewal_bonus}

Продлить: {renewal_link}

Или измените план: {change_plan_link}

{subscription_name}""",
                    "cta": "Продлить подписку",
                    "role": "renewal"
                }
            ]
        },
        
        # === CONSULTING/COACHING ===
        "consulting_nurture": {
            "name": "Consulting & Coaching Nurture",
            "description": "Для консультантов, коучей, менторов",
            "emails": [
                {
                    "day": 0,
                    "subject": "Ваша заявка на консультацию получена",
                    "subject_b": "Что будет дальше?",
                    "preview": "Следующие шаги",
                    "body": """{client_name}, здравствуйте!

Спасибо за интерес к моей консультации.

Вы запросили помощь с: {client_goal}

Что дальше:
1️⃣ Я свяжусь с вами в течение 24 часов
2️⃣ Уточним детали и задачи
3️⃣ Согласуем время первой сессии

Пока можете подготовить:
{preparation_list}

Также полезно:
{free_resource}

{consultant_name}
{consultant_title}""",
                    "cta": "Скачать бесплатный материал",
                    "role": "acknowledgment"
                },
                {
                    "day": 1,
                    "subject": "Как другие достигли {result_type}",
                    "subject_b": "История клиента {testimonial_client}",
                    "preview": "Реальный кейс",
                    "body": """{client_name}, привет!

Пока вы готовитесь к консультации, посмотрите историю {testimonial_client}.

Запрос:
"{client_original_problem}"

Результат за {timeframe}:
"{testimonial_result}"

Полная история: {case_study_link}

Это похоже на вашу ситуацию?

{consultant_name}""",
                    "cta": "Прочитать кейс",
                    "role": "social_proof"
                },
                {
                    "day": 7,
                    "subject": "После консультации: ваш план действий 📋",
                    "subject_b": "Следуйте шагам для результата",
                    "preview": "Персональные рекомендации",
                    "body": """{client_name}, здравствуйте!

Спасибо за продуктивную сессию.

Ваш план действий:

{action_plan}

Сроки:
• Быстрые победы (неделя 1): {quick_wins}
• Среднесрочные (месяц 1): {medium_goals}
• Стратегические (3 месяца): {long_term_goals}

Материалы и шаблоны: {resources_link}

Следующая сессия: {next_session_date}

На связи!
{consultant_name}""",
                    "cta": "Задать вопрос",
                    "role": "follow_up"
                }
            ]
        },
        
        # === EXISTING TEMPLATES (kept from original) ===
        "tea_onboarding": {
            "name": "Добро пожаловать в мир чая",
            "description": "Onboarding для новых клиентов чайного бизнеса",
            "emails": [
                {
                    "day": 0,
                    "subject": "Ваш чай уже в пути! 🍵",
                    "subject_b": "Спасибо за заказ — бонус внутри",
                    "preview": "Как правильно заваривать ваш сорт",
                    "body": """Привет!

Ваш заказ уже собирается и скоро отправится.

А пока — подарок: гайд "Как заваривать {tea_type}"

✓ Температура воды: {temp}
✓ Время заваривания: {time}
✓ Количество: {amount}

Сохраните это письмо — пригодится!

С любовью к чаю,
AI Genesis Tea""",
                    "cta": "Скачать гайд",
                    "role": "education"
                },
                {
                    "day": 3,
                    "subject": "Первый глоток? Вот что почувствуете",
                    "subject_b": "Эффект от вашего чая через 20 минут",
                    "preview": "Что происходит с организмом",
                    "body": """Здравствуйте!

Прошло 3 дня с момента получения.

Как ваши ощущения после первых чашек?

{tea_type} обычно даёт эффект через 20-30 минут:
• Мягкий подъём энергии
• Фокус без тревожности
• Стабильное состояние 4-6 часов

Если что-то не так — просто ответьте на это письмо. Лично разберёмся.

С уважением,
AI Genesis Tea""",
                    "cta": "Поделиться впечатлениями",
                    "role": "engagement"
                },
                {
                    "day": 14,
                    "subject": "Ваш чай заканчивается? 📦",
                    "subject_b": "Скидка 15% на повторный заказ",
                    "preview": "Пора пополнить запасы",
                    "body": """Привет!

Прошло 2 недели — ваш чай, наверное, подходит к концу?

Ваш любимый {tea_type} ждёт скидку 15%:

Код: TEA15
Действует: 7 дней

Или попробуйте что-то новое:
• Похожий эффект: {similar_tea_1}
• Другой вкус: {similar_tea_2}

Заказать: {website_url}

С наилучшими пожеланиями,
AI Genesis Tea""",
                    "cta": "Заказать со скидкой",
                    "role": "conversion"
                }
            ]
        },
        
        "ai_service_nurture": {
            "name": "Автоматизация бизнеса — Education",
            "description": "Sequence для лидов, интересующихся ИИ-ассистентами",
            "emails": [
                {
                    "day": 0,
                    "subject": "Ваша заявка получена — что дальше?",
                    "subject_b": "3 шага до автоматизации",
                    "preview": "План внедрения ИИ-ассистента",
                    "body": """Здравствуйте!

Спасибо за интерес к AI Genesis.

Вы запросили автоматизацию для {business_type}.

Вот как обычно проходит внедрение:

1️⃣ День 1-2: Анализ ваших процессов
   • Что отнимает больше времени
   • Какие вопросы повторяются
   • Где теряются лиды

2️⃣ День 3-7: Настройка бота
   • Сценарии диалогов
   • Интеграция с вашими системами
   • Тестирование

3️⃣ День 8+: Запуск и оптимизация
   • Мониторинг первых диалогов
   • Корректировка ответов
   • Обучение команды

Хотите обсудить детали? Ответьте на это письмо.

С уважением,
AI Genesis Team""",
                    "cta": "Записаться на созвон",
                    "role": "education"
                },
                {
                    "day": 3,
                    "subject": "Кейс: как салон сэкономил 15 часов в неделю",
                    "subject_b": "Реальный пример автоматизации",
                    "preview": "До и после внедрения ИИ",
                    "body": """Привет!

Делюсь реальным кейсом.

Салон красоты "Лаванда" (Бруклин):

ДО автоматизации:
• 30-40 сообщений в день в Instagram
• Запись на встречи вручную
• 2 часа в день на переписку

ПОСЛЕ внедрения бота:
• Бот отвечает 24/7
• Автозапись в календарь
• Только квалифицированные лиды передаются менеджеру
• Экономия: 15 часов в неделю

Инвестиция окупилась за 3 недели.

Полный кейс: {case_study_url}

Хотите так же для {business_type}?

AI Genesis Team""",
                    "cta": "Узнать стоимость для моего бизнеса",
                    "role": "social_proof"
                },
                {
                    "day": 7,
                    "subject": "Вопросы, которые задают перед покупкой",
                    "subject_b": "Частые сомнения — честные ответы",
                    "preview": "Про цену, сроки и результат",
                    "body": """Здравствуйте!

Прошла неделя с вашей заявки. 

Знаю, выбор ИИ-ассистента — ответственное решение.

Вот что обычно спрашивают:

❓ "Слишком дорого"
💬 Пилот $350 — это 5-10 часов вашего времени по $35-70/час. Бот работает 24/7 бесконечно.

❓ "А если не сработает?"
💬 Пилот — это 2 недели теста. Не понравится — не продолжаем. Риск минимальный.

❓ "Мне нечего автоматизировать"
💬 Посчитайте: сколько часов в день вы тратите на переписку? Умножьте на $50. Это ваша цифра.

❓ "Сложно настраивать?"
💬 Вы только отвечаете на вопросы. Вся техническая работа — на нас.

Есть другие вопросы? Пишите — отвечу лично.

С уважением,
AI Genesis Team""",
                    "cta": "Задать свой вопрос",
                    "role": "objection_handling"
                },
                {
                    "day": 14,
                    "subject": "Последнее письмо — решение за вами",
                    "subject_b": "Закрываю вашу заявку",
                    "preview": "Без давления, честно",
                    "body": """Привет!

Прошло 2 недели с вашей заявки.

Не хочу надоедать, поэтому это последнее письмо по этой теме.

Автоматизация — не для всех.

✓ Подходит, если у вас 5+ клиентских обращений в день
✓ Подходит, если вы теряете лиды из-за медленных ответов  
✓ Подходит, если хотите масштабироваться без найма

✗ Не подходит, если вам нравится отвечать вручную
✗ Не подходит, если клиентов пока мало

Если сейчас не время — окей, возможно, встретимся через полгода.

Если готовы обсудить — просто ответьте "ДА".

Без шаблонных писем дальше. Только живое общение.

С уважением,
AI Genesis Team

P.S. Если точно нет — тоже ответьте, уберу из рассылки.""",
                    "cta": "Да, готов обсудить",
                    "role": "conversion"
                }
            ]
        },
        
        "abandoned_cart": {
            "name": "Брошенная корзина",
            "description": "Recovery sequence для незавершённых заказов",
            "emails": [
                {
                    "day": 0,
                    "hour": 1,
                    "subject": "Забыли что-то? 🛒",
                    "subject_b": "Ваш чай ждёт",
                    "preview": "Завершите заказ за 2 минуты",
                    "body": """Привет!

Вы выбрали отличные сорта, но не завершили заказ.

В корзине:
{cart_items}

Сумма: {cart_total}

Завершить: {checkout_url}

Если есть вопросы — просто ответьте на это письмо.

AI Genesis Tea""",
                    "cta": "Завершить заказ",
                    "role": "recovery"
                },
                {
                    "day": 1,
                    "subject": "Скидка 10% на ваш заказ",
                    "subject_b": "Чуть не ушло — ловите бонус",
                    "preview": "Код действует 24 часа",
                    "body": """Здравствуйте!

Ваш заказ всё ещё ждёт.

Дарим скидку 10%, чтобы помочь с решением:

Код: COMEBACK10
Действует: 24 часа

{checkout_url}

После оформления — доставка в течение 2 дней.

AI Genesis Tea""",
                    "cta": "Оформить со скидкой",
                    "role": "incentive"
                }
            ]
        }
    }
    
    def generate_sequence(self, template_name, variables=None):
        """Generate email sequence with variables"""
        template = self.TEMPLATES.get(template_name)
        if not template:
            return None
        
        variables = variables or {}
        
        emails = []
        for email in template["emails"]:
            # Replace variables in content
            try:
                subject = email["subject"].format(**variables)
                subject_b = email["subject_b"].format(**variables)
                preview = email["preview"].format(**variables)
                body = email["body"].format(**variables)
                cta = email["cta"].format(**variables)
            except KeyError as e:
                # If variable missing, use placeholder
                print(f"⚠️ Missing variable: {e}, using defaults")
                subject = email["subject"]
                subject_b = email["subject_b"]
                preview = email["preview"]
                body = email["body"]
                cta = email["cta"]
            
            emails.append({
                "day": email.get("day", 0),
                "hour": email.get("hour", 9),
                "subject_a": subject,
                "subject_b": subject_b,
                "preview_text": preview,
                "body": body,
                "cta": cta,
                "role": email["role"],
                "send_time": self._calculate_send_time(email.get("day", 0), email.get("hour", 9))
            })
        
        return {
            "name": template["name"],
            "description": template["description"],
            "created_at": datetime.now().isoformat(),
            "total_emails": len(emails),
            "emails": emails
        }
    
    def _calculate_send_time(self, day, hour=9):
        """Calculate send datetime"""
        send_date = datetime.now() + timedelta(days=day)
        return send_date.replace(hour=hour, minute=0, second=0).isoformat()
    
    def export_to_json(self, sequence, output_path):
        """Export sequence to JSON"""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(sequence, f, ensure_ascii=False, indent=2)
        return output_path
    
    def list_templates(self, category=None):
        """List available templates by category"""
        categories = {
            "e-commerce": ["ecommerce_welcome", "abandoned_cart"],
            "saas": ["saas_trial"],
            "services": ["service_booking"],
            "healthcare": ["healthcare_onboarding"],
            "realestate": ["realestate_buyer"],
            "education": ["education_course"],
            "restaurant": ["restaurant_loyalty"],
            "subscription": ["subscription_retention"],
            "consulting": ["consulting_nurture"],
            "specialty": ["tea_onboarding", "ai_service_nurture"]
        }
        
        if category:
            return {k: self.TEMPLATES[k]["description"] for k in categories.get(category, [])}
        
        return {k: v["description"] for k, v in self.TEMPLATES.items()}

def main():
    import sys
    
    generator = EmailSequenceGenerator()
    
    if len(sys.argv) < 2:
        print("📧 Email Sequence Generator for AI Genesis")
        print("")
        print("Usage:")
        print("  python3 email_sequence.py list                    # All templates")
        print("  python3 email_sequence.py list [category]         # By category")
        print("  python3 email_sequence.py [template_name]         # Generate sequence")
        print("")
        print("Categories: e-commerce, saas, services, healthcare, realestate,")
        print("            education, restaurant, subscription, consulting, specialty")
        print("")
        print("Examples:")
        print("  python3 email_sequence.py list e-commerce")
        print("  python3 email_sequence.py saas_trial")
        print("  python3 email_sequence.py healthcare_onboarding")
        sys.exit(0)
    
    command = sys.argv[1]
    
    if command == "list":
        category = sys.argv[2] if len(sys.argv) > 2 else None
        templates = generator.list_templates(category)
        
        if category:
            print(f"\n📧 {category.upper()} templates:\n")
        else:
            print("\n📧 All available templates:\n")
            print("Categories: e-commerce, saas, services, healthcare, realestate,")
            print("            education, restaurant, subscription, consulting, specialty\n")
        
        for key, desc in templates.items():
            print(f"  {key}")
            print(f"    {desc}\n")
    
    elif command in generator.TEMPLATES:
        # Default variables for demo
        variables = {
            # E-commerce
            "brand_name": "AI Genesis Store",
            "best_categories": "• Чай премиум\n• Витамины\n• Суперфуды",
            
            # SaaS
            "product_name": "AI Genesis Bot",
            "company_name": "Beauty Studio",
            "result_metric": "40% времени",
            "business_type": "салона красоты",
            "quick_start_step_1": "Подключите Telegram",
            "quick_start_step_2": "Загрузите FAQ",
            "quick_start_step_3": "Настройте приветствие",
            "case_study_summary": "Автоматизация записи и ответов на вопросы",
            "result_1": "Экономия 15 часов в неделю",
            "result_2": "Рост конверсии на 25%",
            "result_3": "Нет потерянных заявок",
            "trial_end_date": "31 марта",
            "price_monthly": "49",
            "user_progress": "✓ Подключили Telegram\n✓ Загрузили 5 ответов",
            "advanced_feature": "Интеграцию с календарём",
            "benefit": "автоматическую запись",
            
            # Services
            "service_name": "Консультация",
            "client_name": "Анна",
            "business_name": "AI Genesis",
            "appointment_date": "25 марта",
            "appointment_time": "14:00",
            "location": "Онлайн, Zoom",
            "preparation_checklist": "• Подготовьте список вопросов\n• Проверьте связь",
            "what_to_bring": "• Блокнот\n• Вопросы",
            
            # Healthcare
            "clinic_name": "Wellness Center",
            "patient_name": "Мария",
            "doctor_name": "Др. Иванов",
            "treatment_plan": "Курс витаминов и корректировка питания",
            "next_appointment": "1 апреля",
            "preparation_notes": "• Пройти анализы\n• Вести дневник питания",
            "contact_link": "t.me/doctor_clinic",
            "health_tips": "• Пить 2 литра воды\n• Спать 7-8 часов",
            "available_slots": "• Пн, 10:00\n• Ср, 15:00\n• Пт, 11:00",
            "phone": "+1 (555) 123-45-67",
            "booking_link": "t.me/clinic_booking",
            
            # Real Estate
            "agency_name": "AI Genesis Realty",
            "client_name": "Сергей",
            "agent_name": "Алекс",
            "property_type": "2-комнатную квартиру",
            "area": "Бруклин",
            "budget": "$500,000 - $700,000",
            "guide_link": "#",
            "property_listings": "1. 123 Main St, $650,000\n2. 456 Oak Ave, $580,000",
            "avg_price": "$620,000",
            "price_trend": "+5% за год",
            "avg_days": "45",
            "new_developments": "3 новых ЖК",
            "market_insights": "Спрос превышает предложение",
            "listings_url": "#",
            
            # Education
            "student_name": "Дмитрий",
            "course_name": "Автоматизация бизнеса",
            "school_name": "AI Genesis Academy",
            "learning_outcomes": "• Настроить Telegram бота\n• Автоматизировать продажи\n• Создать CRM",
            "start_date": "25 марта",
            "duration": "4 недели",
            "format": "Видеоуроки + практика",
            "dashboard_link": "#",
            "login": "dmitry@email.com",
            "password": "TempPass123",
            "support_link": "t.me/support",
            "lesson_1_link": "#",
            "completed_lessons": "5",
            "total_lessons": "20",
            "completed_assignments": "3",
            "avg_score": "85",
            "progress_percent": "25",
            "progress_feedback": "Отличный старт! Продолжайте в том же духе.",
            "next_milestone": "Завершить модуль 2",
            "continue_link": "#",
            "lessons_left": "15",
            "assignments_left": "7",
            "motivational_message": "Вы уже знаете больше, чем 60% начинающих!",
            
            # Restaurant
            "customer_name": "Ольга",
            "restaurant_name": "Chai & Co",
            "signature_dishes": "• Матча латте\n• Тайский чай\n• Десерт с чаем",
            "booking_link": "t.me/restaurant_booking",
            "last_visit_date": "1 марта",
            "new_dishes_count": "5",
            "favorite_dish": "Матча латте",
            "expiry_date": "31 марта",
            
            # Subscription
            "subscriber_name": "Елена",
            "subscription_name": "Tea Box Monthly",
            "plan_name": "Премиум",
            "price": "$39",
            "billing_period": "месяц",
            "first_delivery_date": "25 марта",
            "delivery_address": "123 Main St, Brooklyn",
            "box_contents": "• 3 редких сорта чая\n• Гайд по завариванию\n• Печенье к чаю",
            "account_link": "#",
            "reschedule_link": "#",
            "support_link": "t.me/teabox_support",
            "boxes_received": "3",
            "savings_amount": "$45",
            "average_rating": "4.8",
            "next_delivery_date": "25 апреля",
            "exclusive_offer": "Бесплатный чайник при продлении",
            "expiry_date": "31 марта 2026",
            "renewal_bonus": "Бесплатная доставка на 3 месяца",
            "renewal_link": "#",
            "change_plan_link": "#",
            
            # Consulting
            "consultant_name": "Анна",
            "consultant_title": "Бизнес-консультант AI Genesis",
            "client_goal": "автоматизацией продаж",
            "preparation_list": "• Описание текущих процессов\n• Список частых вопросов клиентов",
            "free_resource": "Чек-лист '20 процессов для автоматизации'",
            "testimonial_client": "Иван, владелец кафе",
            "client_original_problem": "Терял 30% заказов из-за долгих ответов",
            "timeframe": "2 месяца",
            "testimonial_result": "Восстановил все потери, теперь обрабатываю в 2 раза больше заказов",
            "case_study_link": "#",
            "action_plan": "1. Настроить бота для FAQ\n2. Подключить автозапись\n3. Создать базу знаний",
            "quick_wins": "Настройка приветствия",
            "medium_goals": "Интеграция с CRM",
            "long_term_goals": "Полная автоматизация первой линии",
            "resources_link": "#",
            "next_session_date": "1 апреля",
            
            # Tea specific
            "tea_type": "Матча Премиум",
            "temp": "80°C",
            "time": "2-3 минуты",
            "amount": "2 г на 200 мл воды",
            "similar_tea_1": "Сенча",
            "similar_tea_2": "Ганпаудер",
            "website_url": "t.me/Rbmultibot",
            
            # Cart
            "cart_items": "• Матча — $35\n• Ганпаудер — $25",
            "cart_total": "$60",
            "checkout_url": "t.me/Rbmultibot",
            "case_study_url": "#"
        }
        
        sequence = generator.generate_sequence(command, variables)
        
        output_path = f"/root/.openclaw/output/email_sequence_{command}.json"
        generator.export_to_json(sequence, output_path)
        
        print(f"✅ Sequence generated: {sequence['name']}")
        print(f"   Total emails: {sequence['total_emails']}")
        print(f"   Output: {output_path}")
        print("")
        print("📧 Email flow:")
        for email in sequence['emails']:
            day_str = f"Day {email['day']}" if email['day'] >= 0 else f"Day {email['day']} (before)"
            print(f"   {day_str}: {email['subject_a']}")
    
    else:
        print(f"❌ Unknown template: {command}")
        print("Run 'python3 email_sequence.py list' to see available templates")

if __name__ == "__main__":
    main()
