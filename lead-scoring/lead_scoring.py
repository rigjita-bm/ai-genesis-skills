#!/usr/bin/env python3
"""
Lead Scoring System for AI Genesis CRM
Assigns 0-100 score based on client data for prioritization
Integrates with Notion CRM
"""

import json
import sys
from datetime import datetime, timedelta

# Add path for CRM integration
sys.path.insert(0, '/root/.openclaw/ai_genesis_crew')

try:
    from crm_integration import NotionCRM
    CRM_AVAILABLE = True
except ImportError:
    CRM_AVAILABLE = False

class LeadScorer:
    """Score leads 0-100 for AI Genesis sales prioritization"""
    
    SCORING_CRITERIA = {
        # Pain/Urgency (0-25 points) - Most important
        "pain_urgency": {
            "losing_clients": 25,     # "Теряю клиентов из-за долгих ответов"
            "overwhelmed": 22,        # "Не справляюсь с перепиской"
            "want_scale": 18,         # "Хочу масштабироваться"
            "exploring": 10,          # "Просто интересно"
        },
        
        # Daily Inquiries (0-20 points) - For pricing
        "daily_inquiries": {
            "50+": 20,
            "20-50": 18,
            "10-20": 15,
            "5-10": 12,
            "1-5": 8,
            "unknown": 5
        },
        
        # Clarity of Request (0-15 points) - NEW!
        "clarity": {
            "specific_pain": 15,      # "Теряю 30% заявок, 50 сообщений в день"
            "general_want": 10,       # "Хочу автоматизировать продажи"
            "exploration": 5          # "Расскажите про ваши услуги"
        },
        
        # Budget Readiness (0-15 points)
        "budget_flexibility": {
            "ready_now": 15,
            "need_pilot": 13,
            "considering": 10,
            "price_sensitive": 6
        },
        
        # Business Type (0-10 points)
        "business_type": {
            "services": 10,           # Salons, clinics
            "healthcare": 10,
            "ecommerce": 9,
            "restaurant": 8,
            "construction": 8,
            "saas": 7,
            "realestate": 6,
            "education": 5,
            "other": 5
        },
        
        # AI Experience (0-10 points) - NEW!
        "ai_experience": {
            "used_successfully": 10,  # Knows the value
            "tried_failed": 7,        # Needs reassurance
            "beginner": 5             # Education needed
        },
        
        # Source Warmth (0-5 points)
        "source": {
            "referral": 5,
            "warm_intro": 5,
            "instagram": 3,
            "telegram": 3,
            "website": 2,
            "cold": 1
        }
    }
    
    # Message templates by category
    TEMPLATES = {
        "🔴 HOT": {
            "timing": "В течение 1 часа",
            "channel": "Звонок + Telegram",
            "message": """Привет {name}! 👋

Увидел ваш запрос про {pain_summary}.

Это решается за 2-3 дня — есть готовое решение для {business_type}.

Готов показать как работает на реальном примере. 

Созвонимся сегодня в {time}? 15 минут, покажу быстро.

— AI Genesis""",
            "follow_up": "Если не ответил через 2 часа — второе сообщение",
            "notify_owner": True
        },
        
        "🟡 WARM": {
            "timing": "В течение 24 часов",
            "channel": "Telegram / Email",
            "message": """Привет {name}! 

Понял задачу — {pain_summary}.

Отправлю кейс, как мы решали похожую ситуацию у {case_example}.

Посмотрите, подойдёт ли подход под ваш бизнес? Обсудим детали.

— AI Genesis""",
            "follow_up": "Через 3 дня спросить про кейс",
            "notify_owner": False
        },
        
        "🔵 COLD": {
            "timing": "В течение 48 часов",
            "channel": "Telegram",
            "message": """Привет {name}!

Получил ваш запрос про автоматизацию.

Подготовил подборку материалов — как другие {business_type} экономят 10+ часов в неделю.

Отправить вам? 📎

— AI Genesis""",
            "follow_up": "Добавить в прогревочную email-рассылку",
            "notify_owner": False
        }
    }
    
    def score_lead(self, lead_data):
        """
        Calculate lead score 0-100
        
        lead_data format:
        {
            "business_type": "services",
            "daily_inquiries": "10-20",
            "pain_urgency": "overwhelmed",
            "clarity": "specific_pain",
            "budget_flexibility": "need_pilot",
            "ai_experience": "beginner",
            "source": "referral"
        }
        """
        score = 0
        breakdown = {}
        
        # Pain Urgency (0-25) - Most important
        pain = lead_data.get("pain_urgency", "exploring")
        pain_score = self.SCORING_CRITERIA["pain_urgency"].get(pain, 10)
        score += pain_score
        breakdown["pain_urgency"] = pain_score
        
        # Daily Inquiries (0-20) - For pricing context
        inquiries = lead_data.get("daily_inquiries", "unknown")
        inquiry_score = self.SCORING_CRITERIA["daily_inquiries"].get(inquiries, 5)
        score += inquiry_score
        breakdown["daily_inquiries"] = inquiry_score
        
        # Clarity of Request (0-15) - NEW!
        clarity = lead_data.get("clarity", "exploration")
        clarity_score = self.SCORING_CRITERIA["clarity"].get(clarity, 5)
        score += clarity_score
        breakdown["clarity"] = clarity_score
        
        # Budget (0-15)
        budget = lead_data.get("budget_flexibility", "considering")
        budget_score = self.SCORING_CRITERIA["budget_flexibility"].get(budget, 10)
        score += budget_score
        breakdown["budget_flexibility"] = budget_score
        
        # Business Type (0-10)
        biz_type = lead_data.get("business_type", "other")
        biz_score = self.SCORING_CRITERIA["business_type"].get(biz_type, 5)
        score += biz_score
        breakdown["business_type"] = biz_score
        
        # AI Experience (0-10) - NEW!
        ai_exp = lead_data.get("ai_experience", "beginner")
        ai_score = self.SCORING_CRITERIA["ai_experience"].get(ai_exp, 5)
        score += ai_score
        breakdown["ai_experience"] = ai_score
        
        # Source (0-5)
        source = lead_data.get("source", "cold")
        source_score = self.SCORING_CRITERIA["source"].get(source, 1)
        score += source_score
        breakdown["source"] = source_score
        
        # Cap at 100
        score = min(score, 100)
        
        # Determine category
        category = self._get_category(score)
        
        return {
            "score": score,
            "category": category,
            "breakdown": breakdown,
            "max_possible": 100,
            "recommendation": self._get_recommendation(score, category),
            "template": self._get_template(category, lead_data)
        }

    def _get_category(self, score):
        """Convert score to HOT/WARM/COLD with emojis"""
        if score >= 75:
            return "🔴 HOT"
        elif score >= 50:
            return "🟡 WARM"
        else:
            return "🔵 COLD"

    def _get_template(self, category, lead_data):
        """Get message template for the lead"""
        template_data = self.TEMPLATES.get(category, self.TEMPLATES["COLD"])
        
        # Fill in template variables
        name = lead_data.get("name", "там")
        business_type = lead_data.get("business_type", "бизнес")
        
        # Generate pain summary based on pain_urgency
        pain = lead_data.get("pain_urgency", "")
        pain_map = {
            "losing_clients": "потерю клиентов из-за долгих ответов",
            "overwhelmed": "завал перепиской",
            "want_scale": "масштабирование",
            "exploring": "автоматизацию"
        }
        pain_summary = pain_map.get(pain, "автоматизацию")
        
        # Case example based on business type
        case_map = {
            "services": "салона красоты",
            "healthcare": "клиники",
            "ecommerce": "магазина",
            "restaurant": "ресторана",
            "construction": "строительной фирмы"
        }
        case_example = case_map.get(business_type, "похожего бизнеса")
        
        filled_template = template_data["message"].format(
            name=name,
            pain_summary=pain_summary,
            business_type=business_type,
            case_example=case_example,
            time="14:00 или 18:00"
        )
        
        return {
            "timing": template_data["timing"],
            "channel": template_data["channel"],
            "message": filled_template,
            "follow_up": template_data["follow_up"]
        }

    def _get_recommendation(self, score, category):
        """Get action recommendation based on score"""
        recommendations = {
            "🔴 HOT": {
                "action": "Звонить сегодня",
                "priority": 1,
                "message": "Высокий скоринг — готов к покупке. Предложить созвон в ближайшие 24 часа.",
                "next_step": "Персонализированное предложение",
                "notification": "🔴 ГОРЯЧИЙ ЛИД — требует немедленного контакта!"
            },
            "🟡 WARM": {
                "action": "Нуртуринг",
                "priority": 2,
                "message": "Средний скоринг — нужно прогреть. Отправить кейс/примеры работ.",
                "next_step": "Email sequence + follow-up через 3 дня",
                "notification": None
            },
            "🔵 COLD": {
                "action": "Долгосрочная работа",
                "priority": 3,
                "message": "Низкий скоринг — пока не готов. Добавить в базу для newsletters.",
                "next_step": "Образовательный контент, подписка на updates",
                "notification": None
            }
        }
        return recommendations.get(category)
    
    def score_from_notes(self, notes_text):
        """
        Auto-score from free-form notes using keyword analysis
        """
        notes_lower = notes_text.lower()
        
        lead_data = {
            "business_type": "other",
            "daily_inquiries": "unknown",
            "pain_urgency": "exploring",
            "clarity": "exploration",
            "budget_flexibility": "considering",
            "ai_experience": "beginner",
            "source": "cold"
        }
        
        # Detect business type
        if any(word in notes_lower for word in ["салон", "красота", "услуг", "repair", "сервис"]):
            lead_data["business_type"] = "services"
        elif any(word in notes_lower for word in ["магазин", "shop", "продажа", "ecommerce"]):
            lead_data["business_type"] = "ecommerce"
        elif any(word in notes_lower for word in ["клиника", "врач", "health", "wellness"]):
            lead_data["business_type"] = "healthcare"
        elif any(word in notes_lower for word in ["ресторан", "кафе", "еда", "доставка"]):
            lead_data["business_type"] = "restaurant"
        elif any(word in notes_lower for word in ["курс", "обучение", "school"]):
            lead_data["business_type"] = "education"
        elif any(word in notes_lower for word in ["строительство", "construction", "ремонт"]):
            lead_data["business_type"] = "construction"
        
        # Detect pain urgency
        if any(word in notes_lower for word in ["теряю", "losing", "клиенты уходят", "срочно", "urgent"]):
            lead_data["pain_urgency"] = "losing_clients"
        elif any(word in notes_lower for word in ["не справляюсь", "завал", "overwhelmed", "некогда"]):
            lead_data["pain_urgency"] = "overwhelmed"
        elif any(word in notes_lower for word in ["масштаб", "scale", "рост", "больше клиентов"]):
            lead_data["pain_urgency"] = "want_scale"
        
        # Detect clarity - NEW!
        if any(word in notes_lower for word in ["конкретно", "точно", "цифры", "30%", "50 сообщений", "долгие ответы", "теряю", "%"]):
            lead_data["clarity"] = "specific_pain"
        elif any(word in notes_lower for word in ["хочу автоматизировать", "нужен бот", "помогите", "записаться", "нужна помощь"]):
            lead_data["clarity"] = "general_want"
        
        # Detect AI experience - NEW!
        if any(word in notes_lower for word in ["уже использую", "работал с", "настраивал бота", "опыт с ии", "chatgpt", "знаком с"]):
            lead_data["ai_experience"] = "used_successfully"
        elif any(word in notes_lower for word in ["пробовал", "не получилось", "прошлый раз", "пытался", "не сработало"]):
            lead_data["ai_experience"] = "tried_failed"
        
        # Detect inquiries volume
        if any(word in notes_lower for word in ["50+", "более 50", "куча сообщений", "тонны"]):
            lead_data["daily_inquiries"] = "50+"
        elif any(word in notes_lower for word in ["20-50", "20 сообщений", "30 сообщений", "40 сообщений"]):
            lead_data["daily_inquiries"] = "20-50"
        elif any(word in notes_lower for word in ["10-20", "10 сообщений", "15 сообщений"]):
            lead_data["daily_inquiries"] = "10-20"
        elif any(word in notes_lower for word in ["5-10", "5 сообщений", "несколько", "7-8"]):
            lead_data["daily_inquiries"] = "5-10"
        
        # Detect budget
        if any(word in notes_lower for word in ["готов", "оплачу", "давайте", "ready", "вношу", "отправлю"]):
            lead_data["budget_flexibility"] = "ready_now"
        elif any(word in notes_lower for word in ["пилот", "попробовать", "test", "пробный", "посмотреть"]):
            lead_data["budget_flexibility"] = "need_pilot"
        elif any(word in notes_lower for word in ["дорого", "дешевле", "скидка", "price", "стоимость"]):
            lead_data["budget_flexibility"] = "price_sensitive"
        
        # Detect source warmth
        if any(word in notes_lower for word in ["порекомендовали", "знакомый", "друг сказал", "referral", "партнёр"]):
            lead_data["source"] = "referral"
        elif any(word in notes_lower for word in ["instagram", "инстаграм", "ig", "direct"]):
            lead_data["source"] = "instagram"
        elif any(word in notes_lower for word in ["telegram", "телеграм", "канал"]):
            lead_data["source"] = "telegram"
        
        return self.score_lead(lead_data)

    def score_crm_lead(self, client_name: str) -> dict:
        """
        Score a lead from Notion CRM by name
        Returns score and suggested status update
        """
        if not CRM_AVAILABLE:
            return {
                "error": "CRM integration not available",
                "message": "Install ai_genesis_crew dependencies"
            }
        
        try:
            crm = NotionCRM()
            clients = crm.get_all_clients()
            
            # Find client by name (partial match)
            matching_clients = [
                c for c in clients 
                if client_name.lower() in c.get('name', '').lower()
            ]
            
            if not matching_clients:
                return {
                    "error": f"Client '{client_name}' not found in CRM",
                    "available_clients": [c.get('name') for c in clients[:10]]
                }
            
            client = matching_clients[0]
            notes = client.get('notes', '') + ' ' + client.get('source', '')
            
            # Score based on notes
            result = self.score_from_notes(notes)
            
            # Add CRM context
            result['client_name'] = client.get('name')
            result['client_id'] = client.get('id')
            result['current_status'] = client.get('status')
            result['suggested_status'] = self._suggest_status(result['category'])
            result['crm_update_recommended'] = result['current_status'] != result['suggested_status']
            
            return result
            
        except Exception as e:
            return {
                "error": f"CRM error: {str(e)}",
                "message": "Check Notion API connection"
            }
    
    def _suggest_status(self, category: str) -> str:
        """Suggest CRM status based on score category"""
        status_map = {
            "🔴 HOT": "Контакт установлен",
            "🟡 WARM": "В работе",
            "🔵 COLD": "Новый лид"
        }
        return status_map.get(category, "Новый лид")
    
    def get_hot_leads_report(self, min_score: int = 75) -> list:
        """
        Get all leads from CRM with score >= min_score
        """
        if not CRM_AVAILABLE:
            return []
        
        try:
            crm = NotionCRM()
            clients = crm.get_all_clients()
            
            hot_leads = []
            for client in clients:
                notes = client.get('notes', '') + ' ' + client.get('source', '')
                result = self.score_from_notes(notes)
                
                if result['score'] >= min_score:
                    hot_leads.append({
                        'name': client.get('name'),
                        'score': result['score'],
                        'category': result['category'],
                        'status': client.get('status'),
                        'recommendation': result['recommendation']['action']
                    })
            
            # Sort by score descending
            hot_leads.sort(key=lambda x: x['score'], reverse=True)
            return hot_leads
            
        except Exception as e:
            print(f"Error fetching hot leads: {e}")
            return []

def main():
    import sys
    
    scorer = LeadScorer()
    
    if len(sys.argv) < 2:
        print("🎯 Lead Scoring System for AI Genesis")
        print("")
        print("Usage:")
        print("  python3 lead_scoring.py demo                    # Show scoring examples")
        print("  python3 lead_scoring.py score 'text'            # Score from notes text")
        print("  python3 lead_scoring.py crm 'Client Name'       # Score CRM lead by name")
        print("  python3 lead_scoring.py hot [min_score]         # Get all HOT leads")
        print("")
        print("Score ranges:")
        print("  75-100: HOT   → Звонить сегодня")
        print("  50-74:  WARM  → Нуртуринг, кейсы")
        print("  0-49:   COLD  → Долгосрочная работа")
        sys.exit(0)
    
    command = sys.argv[1]
    
    if command == "demo":
        examples = [
            {
                "name": "Салон красоты — HOT",
                "data": {
                    "business_type": "services",
                    "daily_inquiries": "20-50",
                    "pain_urgency": "losing_clients",
                    "budget_flexibility": "ready_now",
                    "decision_speed": "this_week"
                }
            },
            {
                "name": "Магазин чая — WARM",
                "data": {
                    "business_type": "ecommerce",
                    "daily_inquiries": "5-10",
                    "pain_urgency": "want_scale",
                    "budget_flexibility": "need_pilot",
                    "decision_speed": "this_month"
                }
            },
            {
                "name": "Курс по рисованию — COLD",
                "data": {
                    "business_type": "education",
                    "daily_inquiries": "1-5",
                    "pain_urgency": "exploring",
                    "budget_flexibility": "price_sensitive",
                    "decision_speed": "no_timeline"
                }
            }
        ]
        
        print("\n🎯 Lead Scoring Examples:\n")
        for ex in examples:
            result = scorer.score_lead(ex["data"])
            print(f"{ex['name']}")
            print(f"  Score: {result['score']}/100 [{result['category']}]")
            print(f"  Action: {result['recommendation']['action']}")
            print(f"  Priority: #{result['recommendation']['priority']}")
            print("")
    
    elif command == "score" and len(sys.argv) > 2:
        notes = " ".join(sys.argv[2:])
        result = scorer.score_from_notes(notes)
        
        print(f"\n🎯 Lead Score: {result['score']}/100")
        print(f"Category: {result['category']}")
        print("")
        print("Breakdown:")
        for key, value in result['breakdown'].items():
            print(f"  {key}: +{value}")
        print("")
        print(f"Recommendation: {result['recommendation']['action']}")
        print(f"Next step: {result['recommendation']['next_step']}")
        print("")
        print("📨 Готовое сообщение:")
        print("-" * 50)
        print(result['template']['message'])
        print("-" * 50)
        print(f"⏰ Когда: {result['template']['timing']}")
        print(f"📱 Канал: {result['template']['channel']}")
        print(f"🔄 Follow-up: {result['template']['follow_up']}")

    elif command == "template" and len(sys.argv) > 3:
        # Generate template for specific category with data
        category = sys.argv[2].upper()
        name = sys.argv[3]
        
        lead_data = {"name": name, "business_type": "services", "pain_urgency": "losing_clients"}
        if len(sys.argv) > 4:
            lead_data["business_type"] = sys.argv[4]
        
        template = scorer._get_template(category, lead_data)
        
        print(f"\n📨 Шаблон для {category} лида ({name}):")
        print("-" * 50)
        print(template['message'])
        print("-" * 50)
        print(f"⏰ Когда: {template['timing']}")
        print(f"📱 Канал: {template['channel']}")
        print(f"🔄 Follow-up: {template['follow_up']}")
    
    elif command == "crm" and len(sys.argv) > 2:
        client_name = " ".join(sys.argv[2:])
        result = scorer.score_crm_lead(client_name)
        
        if "error" in result:
            print(f"❌ {result['error']}")
            if "available_clients" in result:
                print("\nДоступные клиенты:")
                for name in result["available_clients"]:
                    print(f"  • {name}")
        else:
            print(f"\n🎯 CRM Lead Score: {result['score']}/100")
            print(f"Клиент: {result['client_name']}")
            print(f"Category: {result['category']}")
            print(f"Текущий статус: {result['current_status']}")
            print(f"Рекомендуемый статус: {result['suggested_status']}")
            if result['crm_update_recommended']:
                print("⚠️  Рекомендуется обновить статус в CRM!")
            print("")
            print(f"Recommendation: {result['recommendation']['action']}")
            print(f"Next step: {result['recommendation']['next_step']}")
    
    elif command == "hot":
        min_score = int(sys.argv[2]) if len(sys.argv) > 2 else 75
        leads = scorer.get_hot_leads_report(min_score)
        
        if not leads:
            print(f"ℹ️ Нет leads с score >= {min_score}")
            if not CRM_AVAILABLE:
                print("⚠️ CRM integration not available")
        else:
            print(f"\n🔥 HOT Leads (score >= {min_score}):\n")
            for lead in leads:
                print(f"  {lead['name']}")
                print(f"    Score: {lead['score']}/100 [{lead['category']}]")
                print(f"    Status: {lead['status']}")
                print(f"    Action: {lead['recommendation']}")
                print("")
    
    else:
        print("❌ Unknown command")
        print("Run without arguments for help")

if __name__ == "__main__":
    main()
