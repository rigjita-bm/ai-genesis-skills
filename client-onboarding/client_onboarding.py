#!/usr/bin/env python3
"""
AI Client Onboarding for AI Genesis
Automates new consulting client intake:
- Brief, AI audit, personalized roadmap
- ROI forecast, welcome package, progress tracker
"""

import json
import random
from typing import Dict, List, Optional
from datetime import datetime, timedelta

class ClientOnboarding:
    """
    Complete client onboarding automation
    From first contact to working relationship
    """
    
    # Onboarding Stages
    STAGES = {
        "discovery": {
            "name": "🔍 Discovery Call Brief",
            "duration": "30-45 мин",
            "goal": "Understand pain points, AI-readiness and qualify fit",
            "questions": {
                "business_context": [
                    "Ниша и тип бизнеса?",
                    "Текущий месячный оборот (диапазон)?",
                    "Команда — сколько человек и структура?",
                    "Основные процессы, занимающие >5 часов/неделю?"
                ],
                "ai_readiness": [
                    "Какие AI-инструменты уже используете?",
                    "Уровень технической грамотности команды (1-10)?",
                    "Бюджет на AI-внедрение (месяц/проект)?",
                    "Есть ли технический специалист в команде?"
                ],
                "goals_pain": [
                    "Что хотите автоматизировать в первую очередь?",
                    "Какой KPI определит успех внедрения?",
                    "Какие сроки ожидания первых результатов?",
                    "Что мешает масштабировать сейчас?"
                ]
            },
            "deliverables": ["Discovery notes", "AI-readiness assessment", "Next steps recommendation"]
        },
        
        "brief": {
            "name": "📝 Smart Brief",
            "duration": "15 мин (async)",
            "goal": "Collect structured business data",
            "sections": {
                "business_info": {
                    "title": "О бизнесе",
                    "fields": ["Ниша", "Годовой оборот", "Количество клиентов/мес", "Текущие инструменты"]
                },
                "pain_points": {
                    "title": "Болевые точки",
                    "fields": ["Топ-3 задачи, отнимающие время", "Что бесит больше всего", "Последствия не решения проблемы"]
                },
                "current_workflow": {
                    "title": "Текущий процесс",
                    "fields": ["Как клиенты находят вас", "Как происходит первая коммуникация", "Где теряете клиентов", "Сколько времени на ручные задачи"]
                },
                "goals": {
                    "title": "Цели",
                    "fields": ["Что хотите получить через 3 месяца", "Идеальный результат автоматизации", "Как измерите успех"]
                },
                "constraints": {
                    "title": "Ограничения",
                    "fields": ["Бюджет", "Сроки", "Технические ограничения", "Чего точно не хотите"]
                }
            },
            "deliverables": ["Completed brief", "Process map draft", "Automation opportunities list"]
        },
        
        "ai_audit": {
            "name": "🤖 AI Business Audit",
            "duration": "2-4 часа (моя работа)",
            "goal": "Analyze automation potential, identify Quick Wins and Big Moves",
            "analysis_areas": [
                "Customer journey mapping",
                "Current AI tools audit",
                "Quick Wins identification (1-2 weeks implementation)",
                "Big Moves planning (1-3 months)",
                "AI Stack recommendation based on budget/tech level"
            ],
            "outputs": {
                "quick_wins": [
                    "Что можно автоматизировать за 1-2 недели",
                    "Инструменты с минимальным learning curve",
                    "Ожидаемый результат и KPI"
                ],
                "big_moves": [
                    "Стратегические изменения за 1-3 месяца",
                    "Сложные AI-интеграции",
                    "Долгосрочный ROI"
                ],
                "ai_stack": {
                    "low_budget_low_tech": ["ChatGPT", "Zapier", "Google Sheets"],
                    "low_budget_high_tech": ["OpenAI API", "n8n", "Supabase"],
                    "high_budget_low_tech": ["Clay", "Make", "Airtable"],
                    "high_budget_high_tech": ["Custom AI agents", "LangChain", "Vector DBs"]
                }
            },
            "deliverables": ["AI Audit report", "Quick Wins list", "Big Moves roadmap", "AI Stack recommendation"]
        },
        
        "roadmap": {
            "name": "🗺️ AI Implementation Roadmap",
            "duration": "1 час (presentation)",
            "goal": "Present personalized AI implementation plan with Quick Wins and Big Moves",
            "structure": {
                "quick_win_1": {
                    "timeline": "Неделя 1-2",
                    "focus": "Быстрый результат с минимальными затратами",
                    "example": "Telegram-бот для приёма заявок",
                    "tool": "ChatGPT + Telegram Bot API",
                    "kpi": "Время ответа сокращено с 2 часов до 2 минут",
                    "expected_result": "5-10 часов экономии/неделю"
                },
                "quick_win_2": {
                    "timeline": "Неделя 3-4",
                    "focus": "Автоматизация рутинных процессов",
                    "example": "Автоответы на частые вопросы + CRM интеграция",
                    "tool": "Make + Notion",
                    "kpi": "80% запросов закрываются без человека",
                    "expected_result": "10-15 часов экономии/неделю"
                },
                "big_move_1": {
                    "timeline": "Месяц 2",
                    "focus": "Стратегическая автоматизация",
                    "example": "AI-ассистент для квалификации лидов",
                    "tool": "Custom AI agent (CrewAI)",
                    "kpi": "Конверсия лидов +20%",
                    "expected_result": "+15% к выручке"
                },
                "big_move_2": {
                    "timeline": "Месяц 3",
                    "focus": "Полная интеграция AI в workflow",
                    "example": "Автоматизированная воронка продаж с AI-аналитикой",
                    "tool": "LangChain + Vector DB + Analytics",
                    "kpi": "ROI >300%",
                    "expected_result": "Масштабирование без найма"
                }
            },
            "format_template": """
📋 AI IMPLEMENTATION ROADMAP
Клиент: [Имя/Компания]
━━━━━━━━━━━━━━━━━━━━━━━━━━
НЕДЕЛЯ 1-2: [Quick Win #1]
Инструмент: [конкретный AI-инструмент]
Результат: [измеримый KPI]

НЕДЕЛЯ 3-4: [Quick Win #2]
Инструмент: [инструмент]
Результат: [KPI]

МЕСЯЦ 2: [Big Move #1]
Инструмент: [инструмент]
Результат: [KPI]

МЕСЯЦ 3: [Big Move #2]
Инструмент: [инструмент]
Результат: [KPI]
━━━━━━━━━━━━━━━━━━━━━━━━━━
💰 ПРОГНОЗ ROI: [расчёт экономии времени / денег]
📊 МЕТРИКИ УСПЕХА: [список 3-5 KPI]
""",
            "deliverables": ["Visual roadmap", "Timeline with milestones", "Investment breakdown", "AI Stack list"]
        },
        
        "proposal": {
            "name": "📄 Proposal & Contract",
            "duration": "30 мин",
            "goal": "Formalize engagement",
            "elements": {
                "scope": "Detailed list of deliverables",
                "timeline": "Specific dates and milestones",
                "investment": "Breakdown: setup, tools, support",
                "guarantees": "ROI guarantee, revision policy",
                "terms": "Payment schedule, intellectual property"
            },
            "deliverables": ["Signed proposal", "Contract", "Invoice"]
        },
        
        "welcome": {
            "name": "🎉 Welcome Package",
            "duration": "Immediate upon signing",
            "goal": "Set expectations, provide resources and schedule checkpoints",
            "package_contents": [
                "Welcome video (personal, 3-5 min)",
                "Project timeline with your start date",
                "Access to shared workspace (Notion)",
                "Communication protocol (Telegram, response times)",
                "Preparation checklist",
                "Learning materials matched to your tech level",
                "FAQ document",
                "Emergency contact"
            ],
            "learning_materials": {
                "low_tech": [
                    "AI для бизнеса: базовые понятия (видео 15 мин)",
                    "Как общаться с AI-ассистентом (чеклист)",
                    "10 примеров use-case для вашей ниши"
                ],
                "high_tech": [
                    "API documentation и интеграции",
                    "Prompt engineering best practices",
                    "Custom agent architecture overview"
                ]
            },
            "checkpoint_schedule": [
                "Week 1: Quick Win #1 review",
                "Week 2: Quick Win #2 planning",
                "Week 4: Big Move #1 kickoff",
                "Week 6: Mid-project review",
                "Week 8: Big Move #2 planning",
                "Week 12: Final review and handoff"
            ],
            "feedback_form": "Еженедельная форма обратной связи (3 вопроса: что работает, что нет, что нужно)",
            "deliverables": ["Welcome email", "Resource access", "Kickoff meeting scheduled", "Checkpoint calendar"]
        },
        
        "kickoff": {
            "name": "🚀 Kickoff Meeting",
            "duration": "45 мин",
            "goal": "Align and begin execution",
            "agenda": [
                "Quick introductions",
                "Roadmap review and any adjustments",
                "Immediate next steps (this week)",
                "Communication rhythm setup",
                "Q&A",
                "Celebrate the start!"
            ],
            "deliverables": ["Meeting recording", "Action items list", "Week 1 schedule"]
        }
    }
    
    # ROI Calculator
    ROI_TEMPLATES = {
        "time_savings": {
            "metric": "Часов в неделю",
            "typical_range": "10-20 часов",
            "calculation": "(Текущие часы - Автоматизированные часы) × 52 недели × Ставка/час",
            "example": "15 часов/неделю × $50/час × 52 = $39,000/год"
        },
        "conversion_improvement": {
            "metric": "Процент конверсии",
            "typical_range": "+15-30%",
            "calculation": "Текущие лиды × Улучшение конверсии × Средний чек",
            "example": "50 лидов/мес × 20% улучшение × $200 = +$2,000/мес"
        },
        "customer_retention": {
            "metric": "Удержание клиентов",
            "typical_range": "+10-25%",
            "calculation": "Уменьшение оттока × LTV клиента",
            "example": "10 клиентов сохранено × $1,200 LTV = $12,000/год"
        },
        "error_reduction": {
            "metric": "Снижение ошибок",
            "typical_range": "-40-60%",
            "calculation": "Текущие потери от ошибок × Процент снижения",
            "example": "$500/мес потерь × 50% = $250/мес экономии"
        }
    }
    
    # Progress Tracker
    TRACKER_TEMPLATE = {
        "week_1": {
            "focus": "Quick wins setup",
            "deliverables": ["Welcome bot", "FAQ automation", "Calendar integration"],
            "check_in": "Day 3 and Day 7",
            "metrics": ["Response time", "First contact resolution"]
        },
        "week_2": {
            "focus": "Core automation",
            "deliverables": ["Lead qualification", "CRM sync", "Follow-up sequences"],
            "check_in": "Day 10 and Day 14",
            "metrics": ["Qualified leads", "Conversion rate"]
        },
        "week_3": {
            "focus": "Advanced features",
            "deliverables": ["Personalization", "Analytics setup", "Team training"],
            "check_in": "Day 17 and Day 21",
            "metrics": ["User satisfaction", "Automation rate"]
        },
        "week_4": {
            "focus": "Optimization & handoff",
            "deliverables": ["Performance report", "Optimization plan", "Documentation"],
            "check_in": "Day 24 and Day 28 (final review)",
            "metrics": ["ROI achieved", "Time saved", "Revenue impact"]
        }
    }
    
    def generate_brief(self, client_name: str, business_type: str = "general") -> Dict:
        """Generate smart brief template"""
        brief = {
            "client_name": client_name,
            "business_type": business_type,
            "created_at": datetime.now().isoformat(),
            "sections": self.STAGES["brief"]["sections"],
            "instructions": """
Заполните разделы выше. Чем детальнее — тем точнее будет аудит.

Время заполнения: 10-15 минут
Формат: короткие ответы, можно bullet points
"""
        }
        return brief
    
    def calculate_roi(self, current_hours: int, hourly_rate: int, 
                     leads_per_month: int, avg_deal: int,
                     improvement_pct: float = 20) -> Dict:
        """Calculate ROI forecast"""
        
        # Time savings
        hours_saved = current_hours * 0.6  # Typical 60% automation
        annual_time_value = hours_saved * 52 * hourly_rate
        
        # Conversion improvement
        additional_leads = leads_per_month * (improvement_pct / 100)
        monthly_revenue_increase = additional_leads * avg_deal
        annual_conversion_value = monthly_revenue_increase * 12
        
        # Total ROI
        total_annual_value = annual_time_value + annual_conversion_value
        investment = 700  # Full package price
        roi_percentage = ((total_annual_value - investment) / investment) * 100
        payback_months = investment / (total_annual_value / 12)
        
        return {
            "assumptions": {
                "current_weekly_hours": current_hours,
                "hourly_rate": hourly_rate,
                "monthly_leads": leads_per_month,
                "average_deal": avg_deal,
                "conversion_improvement": f"{improvement_pct}%"
            },
            "time_savings": {
                "hours_per_week": round(hours_saved, 1),
                "annual_value": round(annual_time_value, 0)
            },
            "conversion_improvement": {
                "additional_leads_per_month": round(additional_leads, 0),
                "monthly_revenue_increase": round(monthly_revenue_increase, 0),
                "annual_value": round(annual_conversion_value, 0)
            },
            "total_roi": {
                "annual_value": round(total_annual_value, 0),
                "investment": investment,
                "roi_percentage": round(roi_percentage, 0),
                "payback_period_months": round(payback_months, 1)
            },
            "conservative_estimate": round(total_annual_value * 0.7, 0),
            "optimistic_estimate": round(total_annual_value * 1.3, 0)
        }
    
    def generate_ai_stack_recommendation(self, budget_level: str = "medium", tech_level: str = "medium") -> Dict:
        """Generate AI tool stack recommendation based on budget and tech level"""
        
        # Determine stack category
        budget_cat = "high" if budget_level in ["high", "large", "premium", ">$2000"] else "low"
        tech_cat = "high" if tech_level in ["high", "advanced", "expert", ">7"] else "low"
        
        stack_key = f"{budget_cat}_budget_{tech_cat}_tech"
        
        stacks = {
            "low_budget_low_tech": {
                "name": "Starter Stack (Низкий бюджет, базовый уровень)",
                "tools": ["ChatGPT Plus ($20/мес)", "Zapier (бесплатный план)", "Google Sheets", "Telegram Bot (бесплатно)", "Notion (бесплатно)"],
                "best_for": "Соло-предприниматели, первые шаги в AI",
                "monthly_cost": "$20-50",
                "setup_time": "1-2 недели",
                "quick_win_example": "Telegram-бот для приёма заявок с автоответами"
            },
            "low_budget_high_tech": {
                "name": "Builder Stack (Низкий бюджет, высокий уровень)",
                "tools": ["OpenAI API", "n8n (self-hosted)", "Supabase (бесплатный)", "Telegram Bot API", "GitHub"],
                "best_for": "Технические основатели, стартапы с разработчиком",
                "monthly_cost": "$50-100",
                "setup_time": "2-3 недели",
                "quick_win_example": "Custom AI-агент с RAG на собственных данных"
            },
            "high_budget_low_tech": {
                "name": "Enterprise No-Code (Высокий бюджет, базовый уровень)",
                "tools": ["Clay", "Make (Business)", "Airtable", "ChatGPT Team", "Zapier (Professional)"],
                "best_for": "Растущие компании без технической команды",
                "monthly_cost": "$300-800",
                "setup_time": "1-2 недели",
                "quick_win_example": "Автоматизированная CRM с AI-аналитикой"
            },
            "high_budget_high_tech": {
                "name": "Custom AI Stack (Высокий бюджет, высокий уровень)",
                "tools": ["Custom AI agents (CrewAI)", "LangChain", "Pinecone/Weaviate", "AWS/GCP", "Custom frontend"],
                "best_for": "Компании с технической командой, сложные интеграции",
                "monthly_cost": "$1000-5000+",
                "setup_time": "1-3 месяца",
                "quick_win_example": "Полностью кастомная AI-система с ML-моделями"
            }
        }
        
        return {
            "stack_key": stack_key,
            "recommendation": stacks.get(stack_key, stacks["low_budget_low_tech"]),
            "alternative_stacks": [k for k in stacks.keys() if k != stack_key][:2]
        }
    
    def generate_roadmap(self, client_name: str, business_type: str,
                        budget_level: str = "medium", tech_level: str = "medium") -> Dict:
        """Generate personalized AI implementation roadmap with Quick Wins and Big Moves"""
        
        # Get AI stack recommendation
        ai_stack = self.generate_ai_stack_recommendation(budget_level, tech_level)
        
        # Build roadmap structure
        roadmap = {
            "client": client_name,
            "business_type": business_type,
            "ai_stack": ai_stack["recommendation"]["name"],
            "generated_at": datetime.now().isoformat(),
            "quick_wins": [],
            "big_moves": [],
            "format_template": self.STAGES["roadmap"]["structure"]
        }
        
        start_date = datetime.now()
        
        # Quick Wins (Weeks 1-4)
        quick_wins_structure = self.STAGES["roadmap"]["structure"]
        for key in ["quick_win_1", "quick_win_2"]:
            if key in quick_wins_structure:
                qw = quick_wins_structure[key]
                roadmap["quick_wins"].append({
                    "phase": qw["timeline"],
                    "focus": qw["focus"],
                    "deliverable": qw["example"],
                    "tool": qw["tool"],
                    "kpi": qw["kpi"],
                    "expected_result": qw["expected_result"],
                    "start": (start_date + timedelta(weeks=int(qw["timeline"].split()[1].split("-")[0]) - 1)).strftime("%Y-%m-%d")
                })
        
        # Big Moves (Months 2-3)
        for key in ["big_move_1", "big_move_2"]:
            if key in quick_wins_structure:
                bm = quick_wins_structure[key]
                roadmap["big_moves"].append({
                    "phase": bm["timeline"],
                    "focus": bm["focus"],
                    "deliverable": bm["example"],
                    "tool": bm["tool"],
                    "kpi": bm["kpi"],
                    "expected_result": bm["expected_result"]
                })
        
        return roadmap
        
        return roadmap
    
    def generate_welcome_package(self, client_name: str, start_date: str) -> Dict:
        """Generate welcome package content"""
        return {
            "client": client_name,
            "start_date": start_date,
            "welcome_video_script": f"""
Привет, {client_name}!

Спасибо, что выбрали AI Genesis. Я лично буду работать над вашим проектом.

В этом видео:
• Что будет происходить следующие 4 недели
• Как мы будем коммуницировать
• Что вам нужно подготовить
• Как измерим успех

Начинаем {start_date}. До встречи на kickoff!
""",
            "resources": {
                "workspace_url": f"https://notion.so/aigenesis-{client_name.lower().replace(' ', '-')}",
                "communication": "Telegram: @rigjita | Email: rigjita@aigenesis.ai",
                "emergency": "Telegram: @rigjita (помечайте #срочно)"
            },
            "preparation_checklist": [
                "☐ Доступ к текущему Telegram/WhatsApp бизнес-аккаунту",
                "☐ Логины от CRM (если есть)",
                "☐ Примеры частых вопросов клиентов (10-20 штук)",
                "☐ Описание текущего процесса (можно голосовым)",
                "☐ Доступ к календарю для интеграции"
            ],
            "faq": [
                {"q": "Как быстро увижу результат?", "a": "Первые изменения — через 3-5 дней, полный эффект — через 3-4 недели."},
                {"q": "Что если не сработает?", "a": "2 недели бесплатных доработок после запуска. Если не поможет — возврат."},
                {"q": "Нужно ли мне разбираться в технологиях?", "a": "Нет. Я настраиваю всё сам, объясняю просто. Вам только пользоваться."},
                {"q": "Как часто будем общаться?", "a": "Ежедневные короткие апдейты в Telegram + звонки по milestone'ам."}
            ]
        }
    
    def generate_progress_tracker(self, client_name: str, start_date: str) -> Dict:
        """Generate weekly progress tracker"""
        tracker = {
            "client": client_name,
            "start_date": start_date,
            "weeks": []
        }
        
        start = datetime.strptime(start_date, "%Y-%m-%d")
        
        for week_num, (week_key, week_data) in enumerate(self.TRACKER_TEMPLATE.items(), 1):
            week_start = start + timedelta(weeks=week_num-1)
            tracker["weeks"].append({
                "week": week_num,
                "dates": f"{week_start.strftime('%d.%m')} - {(week_start + timedelta(days=6)).strftime('%d.%m')}",
                "focus": week_data["focus"],
                "deliverables": week_data["deliverables"],
                "check_ins": week_data["check_in"],
                "metrics": week_data["metrics"],
                "status": "planned"
            })
        
        return tracker
    
    def generate_full_onboarding(self, client_name: str, business_type: str,
                                 current_hours: int, hourly_rate: int,
                                 leads_per_month: int, avg_deal: int) -> Dict:
        """Generate complete onboarding package"""
        
        start_date = (datetime.now() + timedelta(days=3)).strftime("%Y-%m-%d")
        
        return {
            "client": client_name,
            "generated_at": datetime.now().isoformat(),
            "onboarding_stages": {k: v for k, v in self.STAGES.items()},
            "brief": self.generate_brief(client_name, business_type),
            "roi_forecast": self.calculate_roi(current_hours, hourly_rate, 
                                               leads_per_month, avg_deal),
            "roadmap": self.generate_roadmap(client_name, business_type),
            "welcome_package": self.generate_welcome_package(client_name, start_date),
            "progress_tracker": self.generate_progress_tracker(client_name, start_date),
            "next_steps": [
                "1. Fill out the brief (15 min)",
                "2. Schedule discovery call",
                "3. Review ROI forecast together",
                "4. Sign proposal",
                "5. Receive welcome package",
                "6. Kickoff meeting"
            ]
        }
    
    def generate_report(self, client_name: str, business_type: str,
                       current_hours: int, hourly_rate: int,
                       leads_per_month: int, avg_deal: int,
                       budget_level: str = "medium", tech_level: str = "medium") -> str:
        """Generate human-readable onboarding report with Quick Wins / Big Moves format"""
        
        package = self.generate_full_onboarding(client_name, business_type,
                                               current_hours, hourly_rate,
                                               leads_per_month, avg_deal)
        
        # Get AI stack recommendation
        ai_stack = self.generate_ai_stack_recommendation(budget_level, tech_level)
        
        report = f"""
╔══════════════════════════════════════════════════════════════════╗
║  🤖 AI CONSULTING CLIENT ONBOARDING                               ║
║  Client: {client_name[:35]:<35} ║
║  Generated: {datetime.now().strftime('%Y-%m-%d'):<35} ║
╚══════════════════════════════════════════════════════════════════╝

═══════════════════════════════════════════════════════════════════
  📊 ROI FORECAST
═══════════════════════════════════════════════════════════════════

Исходные данные:
   • Текущие часы рутины: {current_hours}/неделю
   • Ваша ставка: ${hourly_rate}/час
   • Лидов в месяц: {leads_per_month}
   • Средний чек: ${avg_deal}

Расчёт экономии времени:
   • Часов сэкономлено: {package['roi_forecast']['time_savings']['hours_per_week']}/неделю
   • Годовая ценность: ${package['roi_forecast']['time_savings']['annual_value']:,.0f}

Расчёт улучшения конверсии:
   • Дополнительные лиды: {package['roi_forecast']['conversion_improvement']['additional_leads_per_month']:.0f}/мес
   • Прирост выручки: ${package['roi_forecast']['conversion_improvement']['monthly_revenue_increase']:,.0f}/мес
   • Годовая ценность: ${package['roi_forecast']['conversion_improvement']['annual_value']:,.0f}

💰 ИТОГОВЫЙ ROI:
   • Инвестиция: ${package['roi_forecast']['total_roi']['investment']}
   • Годовая ценность: ${package['roi_forecast']['total_roi']['annual_value']:,.0f}
   • ROI: {package['roi_forecast']['total_roi']['roi_percentage']:.0f}%
   • Окупаемость: {package['roi_forecast']['total_roi']['payback_period_months']:.1f} месяцев

   Консервативная оценка: ${package['roi_forecast']['conservative_estimate']:,.0f}
   Оптимистичная оценка: ${package['roi_forecast']['optimistic_estimate']:,.0f}

═══════════════════════════════════════════════════════════════════
  🗺️ AI IMPLEMENTATION ROADMAP
═══════════════════════════════════════════════════════════════════

Клиент: {client_name}
AI Stack: {ai_stack['recommendation']['name']}
━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        
        # Quick Wins
        for qw in package['roadmap']['quick_wins']:
            report += f"""
{qw['phase']}: QUICK WIN
Фокус: {qw['focus']}
Инструмент: {qw['tool']}
Результат: {qw['kpi']}
Ожидаемый эффект: {qw['expected_result']}
"""
        
        # Big Moves
        for bm in package['roadmap']['big_moves']:
            report += f"""
{bm['phase']}: BIG MOVE
Фокус: {bm['focus']}
Инструмент: {bm['tool']}
Результат: {bm['kpi']}
Ожидаемый эффект: {bm['expected_result']}
"""
        
        # AI Stack details
        report += f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━
💰 ПРОГНОЗ ROI: ${package['roi_forecast']['total_roi']['annual_value']:,.0f} годовой ценности
📊 МЕТРИКИ УСПЕХА:
   • Время ответа: с 2 часов до 2 минут
   • Автоматизация запросов: 80% без человека
   • Конверсия лидов: +20%
   • ROI: >300%

═══════════════════════════════════════════════════════════════════
  🤖 RECOMMENDED AI STACK
═══════════════════════════════════════════════════════════════════

{ai_stack['recommendation']['name']}

Инструменты:
"""
        for tool in ai_stack['recommendation']['tools']:
            report += f"   • {tool}\n"
        
        report += f"""
Лучше всего подходит для: {ai_stack['recommendation']['best_for']}
Месячная стоимость: {ai_stack['recommendation']['monthly_cost']}
Время настройки: {ai_stack['recommendation']['setup_time']}

Пример Quick Win: {ai_stack['recommendation']['quick_win_example']}

═══════════════════════════════════════════════════════════════════
  📋 DISCOVERY CALL BRIEF (заполнить перед встречей)
═══════════════════════════════════════════════════════════════════

Бизнес-контекст:
"""
        for question in package['onboarding_stages']['discovery']['questions']['business_context']:
            report += f"   • {question}\n"
        
        report += "\nAI-готовность:\n"
        for question in package['onboarding_stages']['discovery']['questions']['ai_readiness']:
            report += f"   • {question}\n"
        
        report += "\nЦели и боли:\n"
        for question in package['onboarding_stages']['discovery']['questions']['goals_pain']:
            report += f"   • {question}\n"
        
        report += f"""
═══════════════════════════════════════════════════════════════════
  🎉 WELCOME PACKAGE PREVIEW
═══════════════════════════════════════════════════════════════════

Старт проекта: {package['welcome_package']['start_date']}

Ресурсы:
   • Workspace: {package['welcome_package']['resources']['workspace_url']}
   • Коммуникация: {package['welcome_package']['resources']['communication']}
   • Экстренный контакт: {package['welcome_package']['resources']['emergency']}

Обучающие материалы (под уровень):
   Для базового уровня:
"""
        for material in package['onboarding_stages']['welcome']['learning_materials']['low_tech']:
            report += f"      • {material}\n"
        
        report += "\n   Для продвинутого уровня:\n"
        for material in package['onboarding_stages']['welcome']['learning_materials']['high_tech']:
            report += f"      • {material}\n"
        
        report += f"""
Расписание checkpoint-встреч:
"""
        for checkpoint in package['onboarding_stages']['welcome']['checkpoint_schedule']:
            report += f"   • {checkpoint}\n"
        
        report += f"""
Чек-лист подготовки:
"""
        for item in package['welcome_package']['preparation_checklist']:
            report += f"   {item}\n"
        
        report += f"""

═══════════════════════════════════════════════════════════════════
  📈 PROGRESS TRACKER (еженедельно)
═══════════════════════════════════════════════════════════════════
"""
        for week in package['progress_tracker']['weeks']:
            report += f"""
Неделя {week['week']} ({week['dates']})
   Фокус: {week['focus']}
   Доставляем: {', '.join(week['deliverables'])}
   Чек-ины: {week['check_ins']}
   Метрики: {', '.join(week['metrics'])}
"""
        
        report += """
═══════════════════════════════════════════════════════════════════
  ✅ NEXT STEPS
═══════════════════════════════════════════════════════════════════
   1. Заполнить Discovery Call Brief (15 мин)
   2. Провести Discovery Call (30-45 мин)
   3. Получить AI Business Audit с Quick Wins
   4. Согласовать Roadmap и AI Stack
   5. Подписать Proposal и оплатить
   6. Получить Welcome Package
   7. Провести Kickoff Meeting

═══════════════════════════════════════════════════════════════════
"""
        return report

def main():
    import sys
    
    onboarding = ClientOnboarding()
    
    if len(sys.argv) < 2:
        print("🤖 AI Consulting Client Onboarding for AI Genesis")
        print("")
        print("Usage:")
        print("  python3 client_onboarding.py stages              # List onboarding stages")
        print("  python3 client_onboarding.py brief 'Name'        # Generate smart brief")
        print("  python3 client_onboarding.py roi HOURS RATE LEADS DEAL  # Calculate ROI")
        print("  python3 client_onboarding.py stack [budget] [tech]  # AI Stack recommendation")
        print("  python3 client_onboarding.py roadmap 'Name' [business] [budget] [tech]")
        print("  python3 client_onboarding.py welcome 'Name'      # Generate welcome package")
        print("  python3 client_onboarding.py tracker 'Name'      # Generate progress tracker")
        print("  python3 client_onboarding.py full [params...]    # Full onboarding package")
        print("  python3 client_onboarding.py report [params...]  # Human-readable report")
        print("")
        print("Examples:")
        print('  python3 client_onboarding.py roi 15 50 30 200')
        print('  python3 client_onboarding.py stack low high      # Низкий бюджет, высокий техуровень')
        print('  python3 client_onboarding.py roadmap "Иван" salon medium medium')
        sys.exit(0)
    
    command = sys.argv[1]
    
    if command == "stages":
        print("🤖 Onboarding Stages:\n")
        for key, stage in onboarding.STAGES.items():
            print(f"  {stage['name']}")
            print(f"    Duration: {stage['duration']}")
            print(f"    Goal: {stage['goal']}")
            print()
    
    elif command == "brief":
        name = sys.argv[2] if len(sys.argv) > 2 else "Client"
        business = sys.argv[3] if len(sys.argv) > 3 else "general"
        result = onboarding.generate_brief(name, business)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    elif command == "roi":
        if len(sys.argv) < 6:
            print("❌ Need: hours rate leads deal")
            print("Example: python3 client_onboarding.py roi 15 50 30 200")
            sys.exit(1)
        hours, rate, leads, deal = map(int, sys.argv[2:6])
        result = onboarding.calculate_roi(hours, rate, leads, deal)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    elif command == "stack":
        budget = sys.argv[2] if len(sys.argv) > 2 else "medium"
        tech = sys.argv[3] if len(sys.argv) > 3 else "medium"
        print(f"🤖 Подбираю AI Stack (бюджет: {budget}, уровень: {tech})...")
        result = onboarding.generate_ai_stack_recommendation(budget, tech)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    elif command == "roadmap":
        name = sys.argv[2] if len(sys.argv) > 2 else "Client"
        business = sys.argv[3] if len(sys.argv) > 3 else "general"
        budget = sys.argv[4] if len(sys.argv) > 4 else "medium"
        tech = sys.argv[5] if len(sys.argv) > 5 else "medium"
        print(f"🗺️ Генерирую roadmap для {name}...")
        result = onboarding.generate_roadmap(name, business, budget, tech)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    elif command == "welcome":
        name = sys.argv[2] if len(sys.argv) > 2 else "Client"
        start = sys.argv[3] if len(sys.argv) > 3 else datetime.now().strftime("%Y-%m-%d")
        result = onboarding.generate_welcome_package(name, start)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    elif command == "tracker":
        name = sys.argv[2] if len(sys.argv) > 2 else "Client"
        start = sys.argv[3] if len(sys.argv) > 3 else datetime.now().strftime("%Y-%m-%d")
        result = onboarding.generate_progress_tracker(name, start)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    elif command == "full":
        if len(sys.argv) < 7:
            print("❌ Need: name business hours rate leads deal")
            print('Example: python3 client_onboarding.py full "Иван" salon 15 50 30 200')
            sys.exit(1)
        name, business, hours, rate, leads, deal = sys.argv[2], sys.argv[3], int(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6]), int(sys.argv[7])
        result = onboarding.generate_full_onboarding(name, business, hours, rate, leads, deal)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    elif command == "report":
        if len(sys.argv) < 8:
            print("❌ Need: name business hours rate leads deal budget tech")
            print('Example: python3 client_onboarding.py report "Иван" salon 15 50 30 200 medium medium')
            sys.exit(1)
        name, business, hours, rate, leads, deal, budget, tech = sys.argv[2], sys.argv[3], int(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6]), int(sys.argv[7]), sys.argv[8], sys.argv[9]
        print(f"📊 Генерирую отчёт онбординга для {name}...")
        report = onboarding.generate_report(name, business, hours, rate, leads, deal, budget, tech)
        print(report)
        
        output_file = f"/root/.openclaw/output/onboarding_{name.lower().replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.md"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"\n💾 Saved to: {output_file}")
    
    else:
        print(f"❌ Unknown command: {command}")
        print("Run without arguments for help")

if __name__ == "__main__":
    main()
