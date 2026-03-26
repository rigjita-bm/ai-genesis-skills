#!/usr/bin/env python3
"""
Weekly Business Command Center for AI Genesis
Comprehensive week review, analysis, and planning
Version: 2.0 (enhanced per skill template)
"""

import json
import os
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple

class WeeklyCommandCenter:
    """
    AI Genesis Weekly Business Command Center
    - Week summary and analysis
    - Metrics dashboard with trends
    - Priority-based planning (MUST/SHOULD/NICE)
    - AI advice generation
    """
    
    def __init__(self):
        self.runway_months = 1.5
        self.daily_burn_rate = 220
        self.debt = 10000
        self.memory_file = "/root/.openclaw/workspace/memory/weekly_state.json"
        self.last_week_data = self._load_last_week()
    
    def _load_last_week(self) -> Dict:
        """Load previous week's data for trend comparison"""
        if os.path.exists(self.memory_file):
            try:
                with open(self.memory_file, 'r') as f:
                    return json.load(f)
            except:
                return self._default_week_data()
        return self._default_week_data()
    
    def _save_current_week(self, data: Dict):
        """Save current week data for next comparison"""
        try:
            os.makedirs(os.path.dirname(self.memory_file), exist_ok=True)
            with open(self.memory_file, 'w') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"⚠️ Could not save week data: {e}")
    
    def _default_week_data(self) -> Dict:
        """Default data structure"""
        return {
            "week_ending": (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d"),
            "metrics": {
                "new_leads": 0,
                "sales": 0,
                "revenue_usd": 0,
                "posts_published": 0,
                "posts_planned": 0,
                "tasks_completed": 0,
                "tasks_planned": 0,
                "followers": 0
            }
        }
    
    def generate_weekly_review(
        self,
        new_leads: int = 0,
        sales_count: int = 0,
        revenue_usd: int = 0,
        posts_published: int = 0,
        posts_planned: int = 0,
        tasks_completed: int = 0,
        tasks_planned: int = 0,
        followers: int = 0
    ) -> Dict:
        """
        Generate complete weekly review
        """
        current_metrics = {
            "new_leads": new_leads,
            "sales": sales_count,
            "revenue_usd": revenue_usd,
            "posts_published": posts_published,
            "posts_planned": posts_planned,
            "tasks_completed": tasks_completed,
            "tasks_planned": tasks_planned,
            "followers": followers
        }
        
        # Calculate trends vs last week
        trends = self._calculate_trends(current_metrics)
        
        # Analysis blocks
        what_worked = self._analyze_what_worked(current_metrics)
        what_failed = self._analyze_what_failed(current_metrics)
        key_insight = self._generate_insight(current_metrics, trends)
        
        # Next week plan
        next_week_plan = self._generate_next_week_plan(current_metrics, trends)
        
        # AI advice
        ai_advice = self._generate_ai_advice(current_metrics, trends)
        
        review = {
            "week_start": (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d"),
            "week_end": datetime.now().strftime("%Y-%m-%d"),
            "financial_context": {
                "runway_months": self.runway_months,
                "debt": self.debt,
                "weekly_burn": self.daily_burn_rate * 7,
                "revenue_needed_next_week": self._revenue_needed()
            },
            "block_1_results": {
                "metrics": current_metrics,
                "vs_plan": {
                    "posts_completion": round(posts_published / max(posts_planned, 1) * 100, 1),
                    "tasks_completion": round(tasks_completed / max(tasks_planned, 1) * 100, 1)
                }
            },
            "block_2_analysis": {
                "what_worked": what_worked,
                "what_failed": what_failed,
                "key_insight": key_insight
            },
            "block_3_next_week": next_week_plan,
            "block_4_dashboard": {
                "current": current_metrics,
                "previous": self.last_week_data.get("metrics", {}),
                "trends": trends
            },
            "block_5_ai_advice": ai_advice
        }
        
        # Save for next week comparison
        self._save_current_week({
            "week_ending": datetime.now().strftime("%Y-%m-%d"),
            "metrics": current_metrics
        })
        
        return review
    
    def _calculate_trends(self, current: Dict) -> Dict:
        """Calculate trends vs previous week"""
        prev = self.last_week_data.get("metrics", {})
        
        trends = {}
        for key in current:
            curr_val = current.get(key, 0)
            prev_val = prev.get(key, 0)
            
            if prev_val == 0:
                trend = "→" if curr_val == 0 else "↑ NEW"
                change = 100 if curr_val > 0 else 0
            else:
                change = round((curr_val - prev_val) / prev_val * 100, 1)
                if change > 5:
                    trend = "↑"
                elif change < -5:
                    trend = "↓"
                else:
                    trend = "→"
            
            trends[key] = {
                "trend": trend,
                "change_percent": change,
                "diff": current.get(key, 0) - prev.get(key, 0)
            }
        
        return trends
    
    def _analyze_what_worked(self, metrics: Dict) -> List[str]:
        """Analyze top 3 things that worked well"""
        worked = []
        
        if metrics["revenue_usd"] > 500:
            worked.append(f"💰 Revenue ${metrics['revenue_usd']} — продажи идут хорошо")
        
        if metrics["new_leads"] >= 5:
            worked.append(f"📞 {metrics['new_leads']} новых лидов — привлечение работает")
        
        posts_rate = metrics["posts_published"] / max(metrics["posts_planned"], 1)
        if posts_rate >= 0.8:
            worked.append(f"📱 {metrics['posts_published']}/{metrics['posts_planned']} постов — контент-план выполнен")
        
        tasks_rate = metrics["tasks_completed"] / max(metrics["tasks_planned"], 1)
        if tasks_rate >= 0.7:
            worked.append(f"✅ {metrics['tasks_completed']}/{metrics['tasks_planned']} задач — продуктивная неделя")
        
        if metrics["sales"] >= 2:
            worked.append(f"🎯 {metrics['sales']} продаж — конверсия на уровне")
        
        return worked[:3] if worked else ["Начало отслеживания — устанавливаем базовые метрики"]
    
    def _analyze_what_failed(self, metrics: Dict) -> List[str]:
        """Analyze top 3 things that didn't work"""
        failed = []
        
        if metrics["revenue_usd"] < 500:
            failed.append(f"💸 Revenue ${metrics['revenue_usd']} ниже целевого ($1000+/неделя)")
        
        if metrics["new_leads"] < 3:
            failed.append(f"📉 Только {metrics['new_leads']} лидов — нужно больше outreach")
        
        posts_rate = metrics["posts_published"] / max(metrics["posts_planned"], 1)
        if posts_rate < 0.6 and metrics["posts_planned"] > 0:
            failed.append(f"📝 Выполнено {metrics['posts_published']}/{metrics['posts_planned']} постов — контент отстаёт")
        
        tasks_rate = metrics["tasks_completed"] / max(metrics["tasks_planned"], 1)
        if tasks_rate < 0.5 and metrics["tasks_planned"] > 0:
            failed.append(f"⏰ Выполнено {metrics['tasks_completed']}/{metrics['tasks_planned']} задач — переоценка планов")
        
        if metrics["sales"] == 0 and metrics["new_leads"] > 0:
            failed.append("🚫 Нет продаж при наличии лидов — проблема в воронке")
        
        return failed[:3] if failed else ["Пока нет критических проблем — отличная неделя!"]
    
    def _generate_insight(self, metrics: Dict, trends: Dict) -> str:
        """Generate key insight for the week"""
        revenue_trend = trends.get("revenue_usd", {}).get("trend", "→")
        leads_trend = trends.get("new_leads", {}).get("trend", "→")
        
        if revenue_trend == "↑" and leads_trend == "↑":
            return "📈 Рост по всем направлениям — текущая стратегия работает, масштабируем"
        elif revenue_trend == "↓" and leads_trend == "↑":
            return "🎯 Много лидов, но мало продаж — фокус на закрытие, не на привлечение"
        elif revenue_trend == "↑" and leads_trend == "↓":
            return "💎 Высокая конверсция — качество > количества, так держать"
        elif metrics["revenue_usd"] < 300:
            return "🚨 Критический revenue — emergency mode, только MUST задачи"
        else:
            return "⚖️ Стабильная неделя — фокус на MUST задачах для runway"
    
    def _generate_next_week_plan(self, metrics: Dict, trends: Dict) -> Dict:
        """Generate MUST/SHOULD/NICE plan for next week"""
        
        # MUST — critical for runway
        must_tasks = []
        
        revenue_gap = self._revenue_needed() - metrics["revenue_usd"]
        if revenue_gap > 0:
            must_tasks.append(f"🔥 Закрыть revenue gap ${revenue_gap} — outreach + follow-ups")
        
        if metrics["new_leads"] < 5:
            must_tasks.append("📞 Найти минимум 5 новых лидов — активный outreach")
        
        if metrics["sales"] == 0:
            must_tasks.append("💰 Провести минимум 2 sales call")
        
        # Add default MUST if list is short
        if len(must_tasks) < 2:
            must_tasks.append("🎯 Follow-up с существующими лидами")
        
        # SHOULD — important but not blocking
        should_tasks = [
            "📝 Создать контент-план и опубликовать 4+ поста",
            "🤖 Завершить настройку текущих ботов",
            "📊 Обновить CRM и проскорить новых лидов",
            "🔍 Competitive intelligence отчёт",
            "💡 Подготовить кейс-стади для продаж"
        ]
        
        # NICE — when time permits
        nice_tasks = [
            "🎨 Обновить визуалы Instagram",
            "📚 Изучить новые фичи CrewAI",
            "🌐 Исследовать новые каналы привлечения"
        ]
        
        return {
            "MUST": must_tasks[:3],
            "SHOULD": should_tasks[:5],
            "NICE": nice_tasks[:3]
        }
    
    def _generate_ai_advice(self, metrics: Dict, trends: Dict) -> str:
        """Generate AI advice for scaling/automation"""
        
        if metrics["new_leads"] > 10 and metrics["sales"] < 2:
            return """
💡 AI СОВЕТ НЕДЕЛИ: Автоматизируйте квалификацию лидов

У вас много лидов ({leads}) но низкая конверсия ({sales} продаж).
Настройте Lead Scoring bot для автоматической квалификации:
- HOT лиды (75+) → немедленный звонок
- WARM (50-74) → nurturing sequence
- COLD (<50) → дайджест 1 раз в неделю

Это освободит время для работы с реально горячими лидами.
""".format(leads=metrics["new_leads"], sales=metrics["sales"])
        
        if metrics["posts_published"] < metrics["posts_planned"]:
            return """
💡 AI СОВЕТ НЕДЕЛИ: Контент-батчинг

Вы публикуете {published} из {planned} постов. Попробуйте:
1. genesis content batch automation 5 — сгенерировать 5 постов за раз
2. genesis plan automation — план на неделю
3. Настроить отложенную публикацию в Telegram

Батчинг экономит 70% времени vs ежедневное создание.
""".format(published=metrics["posts_published"], planned=metrics["posts_planned"])
        
        if metrics["revenue_usd"] < 500:
            return """
💡 AI СОВЕТ НЕДЕЛИ: Emergency Revenue Protocol

Revenue ${revenue} ниже целевого. На этой неделе:
1. 🔴 Только MUST задачи — никаких NICE
2. 📞 2 outreach сессии в день (утро и вечер)
3. 💰 Upsell существующим клиентам ($100 audit → $350 pilot)
4. 🤝 Предложить партнёрство за referral commission

Фокус: закрыть ${needed} до конца недели.
""".format(revenue=metrics["revenue_usd"], needed=self._revenue_needed())
        
        return """
💡 AI СОВЕТ НЕДЕЛИ: Масштабирование через партнёрства

Отличная неделя! Теперь масштабируйте:
1. Создайте affiliate program для клиентов (10-20% commission)
2. genesis email referral — шаблон для referral request
3. Попросите 3 текущих клиентов о referral

Один satisfied client = 2-3 новых лида с теплой рекомендацией.
"""
    
    def _revenue_needed(self) -> int:
        """Calculate revenue needed per week"""
        return int(self.daily_burn_rate * 7 * 1.5)
    
    def generate_report(
        self,
        new_leads: int = 0,
        sales_count: int = 0,
        revenue_usd: int = 0,
        posts_published: int = 0,
        posts_planned: int = 0,
        tasks_completed: int = 0,
        tasks_planned: int = 0,
        followers: int = 0
    ) -> str:
        """Generate formatted weekly report"""
        
        review = self.generate_weekly_review(
            new_leads, sales_count, revenue_usd,
            posts_published, posts_planned,
            tasks_completed, tasks_planned, followers
        )
        
        report = f"""
╔══════════════════════════════════════════════════════════════════╗
║  📊 AI GENESIS WEEKLY BUSINESS COMMAND CENTER                     ║
║  Неделя: {review['week_start']} → {review['week_end']}                    ║
╚══════════════════════════════════════════════════════════════════╝

═══════════════════════════════════════════════════════════════════
  💰 ФИНАНСОВЫЙ КОНТЕКСТ
═══════════════════════════════════════════════════════════════════
  Runway: {review['financial_context']['runway_months']} месяцев | Debt: ${review['financial_context']['debt']:,}
  Нужно на неделю: ${review['financial_context']['revenue_needed_next_week']:,}

═══════════════════════════════════════════════════════════════════
  📈 БЛОК 1 — ИТОГИ НЕДЕЛИ
═══════════════════════════════════════════════════════════════════
  📞 Новые лиды: {review['block_1_results']['metrics']['new_leads']}
  💰 Продажи: {review['block_1_results']['metrics']['sales']}
  💵 Доход: ${review['block_1_results']['metrics']['revenue_usd']}
  📱 Посты: {review['block_1_results']['metrics']['posts_published']}/{review['block_1_results']['metrics']['posts_planned']} ({review['block_1_results']['vs_plan']['posts_completion']}%)
  ✅ Задачи: {review['block_1_results']['metrics']['tasks_completed']}/{review['block_1_results']['metrics']['tasks_planned']} ({review['block_1_results']['vs_plan']['tasks_completion']}%)
  👥 Подписчики: {review['block_1_results']['metrics']['followers']}

═══════════════════════════════════════════════════════════════════
  🔍 БЛОК 2 — АНАЛИЗ
═══════════════════════════════════════════════════════════════════
  ✅ ЧТО СРАБОТАЛО (топ-3):
"""
        for item in review['block_2_analysis']['what_worked']:
            report += f"     • {item}\n"
        
        report += "\n  ❌ ЧТО НЕ СРАБОТАЛО (топ-3):\n"
        for item in review['block_2_analysis']['what_failed']:
            report += f"     • {item}\n"
        
        report += f"\n  💡 ГЛАВНЫЙ ИНСАЙТ:\n     {review['block_2_analysis']['key_insight']}\n"
        
        report += """
═══════════════════════════════════════════════════════════════════
  🎯 БЛОК 3 — ПЛАН НА СЛЕДУЮЩУЮ НЕДЕЛЮ
═══════════════════════════════════════════════════════════════════
"""
        report += "  🔴 MUST DO (критично — до 3 задач):\n"
        for i, task in enumerate(review['block_3_next_week']['MUST'], 1):
            report += f"     {i}. {task}\n"
        
        report += "\n  🟡 SHOULD DO (важно — до 5 задач):\n"
        for i, task in enumerate(review['block_3_next_week']['SHOULD'], 1):
            report += f"     {i}. {task}\n"
        
        report += "\n  🟢 NICE TO DO (желательно — до 3 задач):\n"
        for i, task in enumerate(review['block_3_next_week']['NICE'], 1):
            report += f"     {i}. {task}\n"
        
        report += """
═══════════════════════════════════════════════════════════════════
  📊 БЛОК 4 — DASHBOARD МЕТРИКИ
═══════════════════════════════════════════════════════════════════
  | Метрика          | Эта неделя | Прошлая | Тренд |
  |------------------|------------|---------|-------|
"""
        for metric, values in review['block_4_dashboard']['trends'].items():
            name_map = {
                "new_leads": "Новые лиды",
                "sales": "Продажи",
                "revenue_usd": "Доход ($)",
                "posts_published": "Посты",
                "tasks_completed": "Задачи",
                "followers": "Подписчики"
            }
            name = name_map.get(metric, metric)
            curr = review['block_4_dashboard']['current'].get(metric, 0)
            trend = values['trend']
            report += f"  | {name:<16} | {curr:<10} | ...     | {trend:<5} |\n"
        
        report += f"""
═══════════════════════════════════════════════════════════════════
  💡 БЛОК 5 — AI СОВЕТ НЕДЕЛИ
═══════════════════════════════════════════════════════════════════
{review['block_5_ai_advice']}

═══════════════════════════════════════════════════════════════════
  ⚠️ ПРАВИЛА НЕДЕЛИ
═══════════════════════════════════════════════════════════════════
  • Если MUST не закрыт — не брать SHOULD
  • Если runway < 2 мес — только revenue-generating задачи
  • Контент важен, но продажи критичны

═══════════════════════════════════════════════════════════════════
  📅 Следующий отчёт: {(datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')}
═══════════════════════════════════════════════════════════════════
"""
        
        return report

def main():
    import sys
    
    wcc = WeeklyCommandCenter()
    
    if len(sys.argv) < 2 or sys.argv[1] == "demo":
        # Demo report with sample data
        print(wcc.generate_report(
            new_leads=4,
            sales_count=1,
            revenue_usd=350,
            posts_published=3,
            posts_planned=4,
            tasks_completed=8,
            tasks_planned=10,
            followers=127
        ))
        sys.exit(0)
    
    if sys.argv[1] == "json":
        review = wcc.generate_weekly_review(
            new_leads=4,
            sales_count=1,
            revenue_usd=350,
            posts_published=3,
            posts_planned=4,
            tasks_completed=8,
            tasks_planned=10,
            followers=127
        )
        print(json.dumps(review, indent=2, ensure_ascii=False))
        sys.exit(0)
    
    if sys.argv[1] == "custom":
        # Custom report with provided metrics
        print(wcc.generate_report(
            new_leads=int(sys.argv[2]) if len(sys.argv) > 2 else 0,
            sales_count=int(sys.argv[3]) if len(sys.argv) > 3 else 0,
            revenue_usd=int(sys.argv[4]) if len(sys.argv) > 4 else 0,
            posts_published=int(sys.argv[5]) if len(sys.argv) > 5 else 0,
            posts_planned=int(sys.argv[6]) if len(sys.argv) > 6 else 0,
            tasks_completed=int(sys.argv[7]) if len(sys.argv) > 7 else 0,
            tasks_planned=int(sys.argv[8]) if len(sys.argv) > 8 else 0,
            followers=int(sys.argv[9]) if len(sys.argv) > 9 else 0
        ))
        sys.exit(0)
    
    print("📊 Weekly Business Command Center for AI Genesis")
    print("")
    print("Usage:")
    print("  python3 weekly_command.py              # Demo with sample data")
    print("  python3 weekly_command.py json         # JSON output")
    print("  python3 weekly_command.py custom L S R PP PT TC TP F")
    print("     L=leads, S=sales, R=revenue, PP=posts_pub, PT=posts_plan")
    print("     TC=tasks_done, TP=tasks_plan, F=followers")
    print("")
    print("Example:")
    print("  python3 weekly_command.py custom 5 2 700 4 4 10 12 150")

if __name__ == "__main__":
    main()
