#!/usr/bin/env python3
"""
Proposal Generator v1.0 for AI Genesis
Generates professional HTML proposals for 3 tiers: $350/$700/$1000
Supports 5 niches: salon, dental, renovation, cafe, fitness
"""

import os
import sys
import json
import argparse
from datetime import datetime, timedelta

# Business configuration
BUSINESS_CONFIG = {
    "company_name": "AI Genesis",
    "company_tagline": "Цифровые администраторы для вашего бизнеса",
    "contact": {
        "telegram": "@Rbmultibot",
        "email": "contact@aigenesis.com",
        "phone": "+1 (XXX) XXX-XXXX"
    },
    "tiers": {
        "audit": {
            "name": "AI Audit",
            "price": 100,
            "duration": "3-5 дней",
            "description": "Аудит процессов и рекомендации по автоматизации",
            "features": [
                "Анализ текущих процессов",
                "Выявление узких мест",
                "План автоматизации",
                "ROI-расчёт",
                "PDF-отчёт"
            ]
        },
        "pilot": {
            "name": "AI Pilot",
            "price": 350,
            "duration": "7-10 дней",
            "description": "Пилотный запуск AI-ассистента для одного процесса",
            "features": [
                "Telegram-бот с базовыми сценариями",
                "До 5 сценариев диалога",
                "Интеграция с вашим календарём",
                "Тестирование и отладка",
                "Обучение команды (1 час)",
                "Поддержка 14 дней"
            ]
        },
        "full": {
            "name": "AI Assistant Pro",
            "price": 700,
            "duration": "14-21 день",
            "description": "Полноценный AI-ассистент для бизнеса",
            "features": [
                "Расширенный Telegram/WhatsApp бот",
                "До 15 сценариев диалога",
                "Интеграция с CRM (Notion/Airtable)",
                "Автоматическая запись клиентов",
                "Напоминания и follow-up",
                "Сбор обратной связи",
                "Аналитика и отчёты",
                "Обучение команды (2 часа)",
                "Поддержка 30 дней"
            ]
        },
        "combo": {
            "name": "AI Business Suite",
            "price": 1000,
            "duration": "21-30 дней",
            "description": "Комплексная автоматизация + контент-система",
            "features": [
                "Всё из AI Assistant Pro",
                "AI-генерация постов для Instagram/Telegram",
                "Контент-календарь на месяц",
                "Email-рассылки (3 шаблона)",
                "Аналитика эффективности контента",
                "Карусели и визуалы (5 шт)",
                "Обучение команды (3 часа)",
                "Поддержка 60 дней",
                "Приоритетная поддержка"
            ]
        }
    }
}

# Niche-specific content
NICHE_CONTENT = {
    "salon": {
        "name": "Салон красоты / Барбершоп",
        "pain_points": [
            "Клиенты пишут в WhatsApp/Telegram в любое время",
            "Мастера отвлекаются на переписку во время работы",
            "Забывают о записях → no-shows (20-30%)",
            "Не собирают обратную связь после визита",
            "Теряют лиды из-за медленных ответов"
        ],
        "solutions": {
            "pilot": [
                "Бот отвечает на вопросы о услугах и ценах 24/7",
                "Автозапись в свободные слоты мастеров",
                "Напоминания за день и за 2 часа до визита"
            ],
            "full": [
                "Персонализированные сценарии для каждого мастера",
                "Автоматический сбор отзывов после визита",
                "Рассылка акций и спецпредложений",
                "Статистика по записям и отменам в Notion CRM"
            ]
        },
        "roi_example": {
            "time_saved": "15 часов/неделю",
            "no_show_reduction": "с 25% до 8%",
            "conversion_increase": "+35%",
            "monthly_value": "$1,200-2,000"
        }
    },
    "dental": {
        "name": "Стоматологическая клиника",
        "pain_points": [
            "Администратор перегружен звонками и сообщениями",
            "Пациенты отменяют в последний момент",
            "Сложно отследить историю лечения",
            "Нет системы напоминаний о профосмотрах",
            "Теряются потенциальные пациенты из-за долгих ответов"
        ],
        "solutions": {
            "pilot": [
                "Бот отвечает на вопросы о услугах и ценах",
                "Запись на консультацию с учётом расписания врачей",
                "Автоматические напоминания о приёме"
            ],
            "full": [
                "Интеграция с медицинской CRM",
                "Напоминания о плановых осмотрах (каждые 6 месяцев)",
                "Сбор анамнеза перед визитом",
                "Автоответы на частые вопросы (имплантация, брекеты, отбеливание)"
            ]
        },
        "roi_example": {
            "time_saved": "20 часов/неделю",
            "no_show_reduction": "с 30% до 10%",
            "conversion_increase": "+40%",
            "monthly_value": "$2,500-4,000"
        }
    },
    "renovation": {
        "name": "Ремонт квартир / Строительные услуги",
        "pain_points": [
            "Много однотипных вопросов о цене и сроках",
            "Замеры назначаются вручную, частые переносы",
            "Сметы готовятся долго — клиенты уходят к конкурентам",
            "Нет системы отслеживания этапов ремонта",
            "Сложно собирать фотоотчёты с бригад"
        ],
        "solutions": {
            "pilot": [
                "Бот квалифицирует лиды (площадь, тип ремонта, бюджет)",
                "Автозапись на замер в календарь",
                "Быстрые ответы на типовые вопросы о ценах"
            ],
            "full": [
                "Автоматическая отправка примерных смет",
                "Напоминания о замерах и начале работ",
                "Еженедельные отчёты о прогрессе для клиента",
                "Сбор фотоотчётов от бригад",
                "База материалов с ценами"
            ]
        },
        "roi_example": {
            "time_saved": "25 часов/неделю",
            "lead_conversion": "с 15% до 35%",
            "response_time": "с часов до минут",
            "monthly_value": "$3,000-5,000"
        }
    },
    "cafe": {
        "name": "Кафе / Доставка еды",
        "pain_points": [
            "Заказы по телефону во время пиковых часов",
            "Ошибки в принятии заказов (шум, спешка)",
            "Нет системы лояльности и повторных продаж",
            "Сложно собирать отзывы",
            "Меню не обновляется оперативно"
        ],
        "solutions": {
            "pilot": [
                "Telegram-бот для приёма заказов",
                "Автоматический расчёт стоимости и времени доставки",
                "Подтверждение заказа и уведомление о статусе"
            ],
            "full": [
                "Интеграция с кухней — заказ сразу в работу",
                "Система лояльности (бонусы, скидки)",
                "Автосбор отзывов после доставки",
                "Рассылка новинок и акций",
                "Аналитика популярных блюд"
            ]
        },
        "roi_example": {
            "time_saved": "10 часов/неделю",
            "order_accuracy": "+95%",
            "repeat_customers": "+30%",
            "monthly_value": "$1,500-2,500"
        }
    },
    "fitness": {
        "name": "Фитнес-клуб / Персональный тренер",
        "pain_points": [
            "Клиенты спрашивают расписание и свободные слоты",
            "Частые переносы и отмены тренировок",
            "Нет напоминаний о продлении абонементов",
            "Сложно отслеживать прогресс клиентов",
            "Теряются потенциальные клиенты на этапе консультации"
        ],
        "solutions": {
            "pilot": [
                "Бот с расписанием и ценами 24/7",
                "Запись на пробную тренировку",
                "Напоминания о тренировках"
            ],
            "full": [
                "Интеграция с CRM клиентов",
                "Напоминания об окончании абонемента (за 7 дней)",
                "Сбор фидбека после тренировок",
                "Рассылка мотивационного контента",
                "Отслеживание прогресса (вес, замеры)"
            ]
        },
        "roi_example": {
            "time_saved": "12 часов/неделю",
            "retention_increase": "+25%",
            "conversion_increase": "+45%",
            "monthly_value": "$2,000-3,500"
        }
    }
}


def generate_html_proposal(niche, tier, client_name="", client_business=""):
    """Generate professional HTML proposal"""
    
    if niche not in NICHE_CONTENT:
        available = ", ".join(NICHE_CONTENT.keys())
        raise ValueError(f"Unknown niche: {niche}. Available: {available}")
    
    if tier not in BUSINESS_CONFIG["tiers"]:
        available = ", ".join(BUSINESS_CONFIG["tiers"].keys())
        raise ValueError(f"Unknown tier: {tier}. Available: {available}")
    
    niche_data = NICHE_CONTENT[niche]
    tier_data = BUSINESS_CONFIG["tiers"][tier]
    today = datetime.now().strftime("%d.%m.%Y")
    valid_until = (datetime.now() + timedelta(days=14)).strftime("%d.%m.%Y")
    
    # Generate features list
    features_html = "\n".join([f"<li>✅ {feature}</li>" for feature in tier_data["features"]])
    
    # Generate pain points
    pain_points_html = "\n".join([f"<li>❌ {point}</li>" for point in niche_data["pain_points"]])
    
    # Generate solutions based on tier
    if tier == "pilot":
        solutions = niche_data["solutions"]["pilot"]
    elif tier in ["full", "combo"]:
        solutions = niche_data["solutions"]["pilot"] + niche_data["solutions"]["full"]
    else:  # audit
        solutions = ["Проведём полный аудит ваших процессов и подготовим план автоматизации"]
    
    solutions_html = "\n".join([f"<li>✓ {solution}</li>" for solution in solutions])
    
    # ROI block
    roi = niche_data.get("roi_example", {})
    roi_html = ""
    if roi:
        roi_items = []
        if "time_saved" in roi:
            roi_items.append(f'<div class="roi-item"><span class="roi-number">{roi["time_saved"]}</span><span class="roi-label">экономия времени</span></div>')
        if "no_show_reduction" in roi:
            roi_items.append(f'<div class="roi-item"><span class="roi-number">{roi["no_show_reduction"]}</span><span class="roi-label">снижение no-shows</span></div>')
        if "conversion_increase" in roi:
            roi_items.append(f'<div class="roi-item"><span class="roi-number">{roi["conversion_increase"]}</span><span class="roi-label">рост конверсии</span></div>')
        if "monthly_value" in roi:
            roi_items.append(f'<div class="roi-item"><span class="roi-number">{roi["monthly_value"]}</span><span class="roi-label">ценность/месяц</span></div>')
        roi_html = "\n".join(roi_items)
    
    html = f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Коммерческое предложение — {BUSINESS_CONFIG['company_name']}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
        }}
        .container {{
            max-width: 800px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}
        .header h1 {{ font-size: 2.5em; margin-bottom: 10px; }}
        .header p {{ font-size: 1.2em; opacity: 0.9; }}
        .content {{ padding: 40px; }}
        .section {{ margin-bottom: 30px; }}
        .section h2 {{
            color: #667eea;
            border-bottom: 3px solid #667eea;
            padding-bottom: 10px;
            margin-bottom: 20px;
        }}
        .client-info {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 30px;
        }}
        .client-info p {{ margin: 5px 0; }}
        .pain-points {{
            background: #fff5f5;
            border-left: 4px solid #e53e3e;
            padding: 20px;
            border-radius: 0 10px 10px 0;
        }}
        .pain-points li {{
            margin: 10px 0;
            list-style: none;
        }}
        .solutions {{
            background: #f0fff4;
            border-left: 4px solid #38a169;
            padding: 20px;
            border-radius: 0 10px 10px 0;
        }}
        .solutions li {{
            margin: 10px 0;
            list-style: none;
            font-weight: 500;
        }}
        .tier-box {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 15px;
            text-align: center;
            margin: 30px 0;
        }}
        .tier-name {{ font-size: 1.5em; font-weight: bold; margin-bottom: 10px; }}
        .tier-price {{
            font-size: 3em;
            font-weight: bold;
            margin: 20px 0;
        }}
        .tier-price span {{ font-size: 0.4em; opacity: 0.8; }}
        .tier-duration {{
            background: rgba(255,255,255,0.2);
            display: inline-block;
            padding: 8px 20px;
            border-radius: 20px;
            margin-bottom: 20px;
        }}
        .features {{
            background: white;
            color: #333;
            padding: 20px;
            border-radius: 10px;
            text-align: left;
        }}
        .features li {{
            margin: 10px 0;
            list-style: none;
            padding-left: 25px;
            position: relative;
        }}
        .roi-section {{
            background: linear-gradient(135deg, #38a169 0%, #2f855a 100%);
            color: white;
            padding: 30px;
            border-radius: 15px;
            margin: 30px 0;
        }}
        .roi-section h2 {{
            color: white;
            border-bottom-color: rgba(255,255,255,0.3);
            text-align: center;
        }}
        .roi-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }}
        .roi-item {{
            text-align: center;
            padding: 15px;
            background: rgba(255,255,255,0.1);
            border-radius: 10px;
        }}
        .roi-number {{
            display: block;
            font-size: 1.5em;
            font-weight: bold;
            margin-bottom: 5px;
        }}
        .roi-label {{ font-size: 0.9em; opacity: 0.9; }}
        .cta {{
            background: #38a169;
            color: white;
            padding: 40px;
            text-align: center;
            border-radius: 15px;
            margin: 30px 0;
        }}
        .cta h2 {{ color: white; border: none; }}
        .cta-button {{
            display: inline-block;
            background: white;
            color: #38a169;
            padding: 15px 40px;
            border-radius: 30px;
            font-size: 1.2em;
            font-weight: bold;
            text-decoration: none;
            margin-top: 20px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        }}
        .footer {{
            background: #2d3748;
            color: white;
            padding: 30px;
            text-align: center;
        }}
        .footer p {{ margin: 5px 0; opacity: 0.8; }}
        .validity {{
            background: #fed7d7;
            color: #c53030;
            padding: 15px;
            border-radius: 10px;
            text-align: center;
            font-weight: bold;
            margin: 20px 0;
        }}
        @media print {{
            body {{ background: white; padding: 0; }}
            .container {{ box-shadow: none; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 {BUSINESS_CONFIG['company_name']}</h1>
            <p>{BUSINESS_CONFIG['company_tagline']}</p>
        </div>
        
        <div class="content">
            <div class="client-info">
                <p><strong>КП №:</strong> AG-{datetime.now().strftime('%Y%m%d')}-001</p>
                <p><strong>Дата:</strong> {today}</p>
                <p><strong>Клиент:</strong> {client_name or "_____________________"}</p>
                <p><strong>Бизнес:</strong> {client_business or niche_data['name']}</p>
            </div>
            
            <div class="validity">
                ⏰ Предложение действительно до: {valid_until}
            </div>
            
            <div class="section">
                <h2>📋 Ваши текущие вызовы</h2>
                <ul class="pain-points">
                    {pain_points_html}
                </ul>
            </div>
            
            <div class="section">
                <h2>✓ Как мы решаем эти проблемы</h2>
                <ul class="solutions">
                    {solutions_html}
                </ul>
            </div>
            
            <div class="tier-box">
                <div class="tier-name">{tier_data['name']}</div>
                <div class="tier-duration">⏱ Срок: {tier_data['duration']}</div>
                <div class="tier-price">${tier_data['price']}<span>USD</span></div>
                <div class="features">
                    <ul>
                        {features_html}
                    </ul>
                </div>
            </div>
            
            {f'''<div class="roi-section">
                <h2>📈 Ожидаемый результат</h2>
                <div class="roi-grid">
                    {roi_html}
                </div>
            </div>''' if roi_html else ''}
            
            <div class="cta">
                <h2>🚀 Готовы автоматизировать свой бизнес?</h2>
                <p>Свяжитесь с нами для старта проекта:</p>
                <a href="https://t.me/Rbmultibot" class="cta-button">Начать в Telegram →</a>
                <p style="margin-top: 20px; opacity: 0.9;">
                    📧 {BUSINESS_CONFIG['contact']['email']}<br>
                    💬 Telegram: {BUSINESS_CONFIG['contact']['telegram']}
                </p>
            </div>
        </div>
        
        <div class="footer">
            <p><strong>{BUSINESS_CONFIG['company_name']}</strong></p>
            <p>Цифровые администраторы для вашего бизнеса</p>
            <p style="margin-top: 15px; font-size: 0.9em;">
                Это коммерческое предложение не является публичной офертой.
            </p>
        </div>
    </div>
</body>
</html>"""
    
    return html


def list_niches():
    """List all available niches"""
    print("\n🎯 Доступные ниши:\n")
    for key, data in NICHE_CONTENT.items():
        print(f"  {key:12} — {data['name']}")
    print()


def list_tiers():
    """List all available tiers"""
    print("\n💎 Доступные тарифы:\n")
    for key, data in BUSINESS_CONFIG["tiers"].items():
        print(f"  {key:12} — ${data['price']:4} — {data['name']}")
        print(f"               {data['description']}")
        print()


def save_proposal(html_content, filename=None):
    """Save proposal to file"""
    output_dir = "/root/.openclaw/output/proposals"
    os.makedirs(output_dir, exist_ok=True)
    
    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"proposal_{timestamp}.html"
    
    filepath = os.path.join(output_dir, filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    return filepath


def generate_comparison_table(niche):
    """Generate comparison table of all tiers"""
    if niche not in NICHE_CONTENT:
        raise ValueError(f"Unknown niche: {niche}")
    
    niche_data = NICHE_CONTENT[niche]
    
    html = """<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <title>Сравнение тарифов — AI Genesis</title>
    <style>
        body { font-family: 'Segoe UI', sans-serif; padding: 20px; background: #f5f5f5; }
        table { width: 100%; background: white; border-radius: 10px; overflow: hidden; box-shadow: 0 4px 20px rgba(0,0,0,0.1); }
        th { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; }
        td { padding: 15px; border-bottom: 1px solid #eee; text-align: center; }
        tr:hover { background: #f8f9fa; }
        .price { font-size: 1.5em; font-weight: bold; color: #667eea; }
        .check { color: #38a169; font-size: 1.2em; }
        .cross { color: #e53e3e; }
    </style>
</head>
<body>
    <h2 style="text-align: center; color: #333;">Сравнение тарифов — """ + niche_data['name'] + """</h2>
    <table>
        <tr>
            <th>Функция</th>
            <th>Audit<br><span style="font-size: 0.8em; opacity: 0.8;">$100</span></th>
            <th>Pilot<br><span style="font-size: 0.8em; opacity: 0.8;">$350</span></th>
            <th>Full<br><span style="font-size: 0.8em; opacity: 0.8;">$700</span></th>
            <th>Combo<br><span style="font-size: 0.8em; opacity: 0.8;">$1000</span></th>
        </tr>
"""
    
    # Features comparison
    features = [
        ("Аудит процессов", "✓", "✓", "✓", "✓"),
        ("Telegram-бот", "—", "✓", "✓", "✓"),
        ("WhatsApp интеграция", "—", "—", "✓", "✓"),
        ("CRM интеграция", "—", "—", "✓", "✓"),
        ("Email-рассылки", "—", "—", "—", "✓"),
        ("Контент-генерация", "—", "—", "—", "✓"),
        ("Поддержка", "—", "14 дней", "30 дней", "60 дней"),
    ]
    
    for feature, audit, pilot, full, combo in features:
        html += f"""        <tr>
            <td style="text-align: left; font-weight: 500;">{feature}</td>
            <td>{audit}</td>
            <td>{pilot}</td>
            <td>{full}</td>
            <td>{combo}</td>
        </tr>
"""
    
    html += """    </table>
    <p style="text-align: center; margin-top: 30px; color: #666;">
        AI Genesis — Цифровые администраторы для вашего бизнеса<br>
        📧 contact@aigenesis.com | 💬 @Rbmultibot
    </p>
</body>
</html>"""
    
    return html


def main():
    parser = argparse.ArgumentParser(description='Proposal Generator — AI Genesis')
    parser.add_argument('niche', nargs='?', help='Business niche (salon, dental, renovation, cafe, fitness)')
    parser.add_argument('tier', nargs='?', help='Service tier (audit, pilot, full, combo)')
    parser.add_argument('--client', '-c', default='', help='Client name')
    parser.add_argument('--business', '-b', default='', help='Business name')
    parser.add_argument('--compare', action='store_true', help='Generate comparison table')
    parser.add_argument('--list', '-l', action='store_true', help='List available niches and tiers')
    parser.add_argument('--save', '-s', action='store_true', help='Save to file')
    
    args = parser.parse_args()
    
    if args.list:
        list_niches()
        list_tiers()
        return
    
    if args.compare:
        if not args.niche:
            print("❌ Укажите нишу для сравнения")
            list_niches()
            sys.exit(1)
        
        html = generate_comparison_table(args.niche)
        filepath = save_proposal(html, f"comparison_{args.niche}.html")
        print(f"✅ Таблица сравнения создана: {filepath}")
        return
    
    if not args.niche or not args.tier:
        print("\n🚀 AI Genesis Proposal Generator\n")
        print("Использование:")
        print("  genesis proposal [ниша] [тариф] [опции]")
        print("\nПримеры:")
        print('  genesis proposal salon pilot                    # КП для салона, пилот $350')
        print('  genesis proposal dental full --client "Иван"    # КП со именем клиента')
        print('  genesis proposal renovation combo --save        # Сохранить в файл')
        print('  genesis proposal salon --compare                # Таблица сравнения')
        print('  genesis proposal --list                         # Список ниш и тарифов')
        print()
        list_niches()
        list_tiers()
        return
    
    try:
        print(f"\n📝 Генерирую коммерческое предложение...")
        print(f"   Ниша: {args.niche}")
        print(f"   Тариф: {args.tier}")
        if args.client:
            print(f"   Клиент: {args.client}")
        print()
        
        html = generate_html_proposal(args.niche, args.tier, args.client, args.business)
        
        if args.save:
            filename = f"proposal_{args.niche}_{args.tier}_{datetime.now().strftime('%Y%m%d')}.html"
            filepath = save_proposal(html, filename)
            print(f"✅ КП сохранено: {filepath}")
            print(f"   Откройте в браузере для просмотра/печати")
        else:
            # Print summary
            niche_data = NICHE_CONTENT[args.niche]
            tier_data = BUSINESS_CONFIG["tiers"][args.tier]
            print(f"✅ КП сгенерировано!")
            print(f"\n📋 Детали:")
            print(f"   Ниша: {niche_data['name']}")
            print(f"   Тариф: {tier_data['name']} — ${tier_data['price']}")
            print(f"   Срок: {tier_data['duration']}")
            print(f"\n💾 Для сохранения добавьте флаг --save")
            print(f"   genesis proposal {args.niche} {args.tier} --save")
        
    except ValueError as e:
        print(f"❌ Ошибка: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
