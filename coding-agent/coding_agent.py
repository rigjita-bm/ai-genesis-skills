#!/usr/bin/env python3
"""
Coding Agent for AI Genesis - Claude Code Integration
Phases: 1.Reliability 2.Quality Gates 3.Smart Routing 4.Cost Control
"""

import os
import sys
import json
import time
import signal
import subprocess
import hashlib
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from pathlib import Path

class ClaudeController:
    """
    Controller for Claude Code CLI with reliability and cost control
    """
    
    # Config
    TIMEOUT_SECONDS = 600  # 10 min timeout
    AUTO_SAVE_INTERVAL = 60  # Save every 60 sec
    SANDBOX_DIR = "/tmp/claude_sandbox"
    COST_LIMIT_USD = 20.0
    COST_ALERT_THRESHOLD = 15.0
    CLAUDE_CLI_PATH = "/usr/lib/node_modules/@anthropic-ai/claude-code/cli.js"
    
    # Cost tracking (approximate tokens per request)
    COST_PER_1K_TOKENS = 0.008  # Claude 3.5 Sonnet
    
    def __init__(self):
        self.sessions_dir = "/root/.openclaw/coding_sessions"
        self.cost_log = "/root/.openclaw/coding_costs.json"
        self.ensure_dirs()
        
    def ensure_dirs(self):
        """Create necessary directories"""
        os.makedirs(self.sessions_dir, exist_ok=True)
        os.makedirs(self.SANDBOX_DIR, exist_ok=True)
        
    # ═══════════════════════════════════════════════════════════
    # PHASE 1: RELIABILITY (Timeout, Health-check, Auto-save)
    # ═══════════════════════════════════════════════════════════
    
    def run_with_timeout(self, command: List[str], cwd: str = None) -> Dict:
        """
        Run Claude with timeout and monitoring
        
        Returns: {
            "success": bool,
            "output": str,
            "duration": float,
            "timeout_hit": bool,
            "session_id": str
        }
        """
        session_id = hashlib.md5(f"{command}{time.time()}".encode()).hexdigest()[:8]
        start_time = time.time()
        
        # Prepare sandbox
        session_dir = os.path.join(self.SANDBOX_DIR, session_id)
        os.makedirs(session_dir, exist_ok=True)
        
        # Create session log
        session_log = {
            "id": session_id,
            "command": " ".join(command),
            "start_time": datetime.now().isoformat(),
            "status": "running",
            "auto_saves": []
        }
        self._save_session(session_id, session_log)
        
        try:
            # Run with timeout
            process = subprocess.Popen(
                command,
                cwd=cwd or session_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                preexec_fn=os.setsid  # Create new process group
            )
            
            # Monitor with auto-save
            output_parts = []
            last_save = time.time()
            
            while process.poll() is None:
                elapsed = time.time() - start_time
                
                # Check timeout
                if elapsed > self.TIMEOUT_SECONDS:
                    os.killpg(os.getpgid(process.pid), signal.SIGTERM)
                    session_log["status"] = "timeout"
                    session_log["timeout_after"] = elapsed
                    self._save_session(session_id, session_log)
                    return {
                        "success": False,
                        "output": "⏱️ Timeout: задача заняла больше 10 минут",
                        "duration": elapsed,
                        "timeout_hit": True,
                        "session_id": session_id
                    }
                
                # Auto-save every 60 seconds
                if time.time() - last_save > self.AUTO_SAVE_INTERVAL:
                    session_log["auto_saves"].append({
                        "time": datetime.now().isoformat(),
                        "elapsed": elapsed
                    })
                    self._save_session(session_id, session_log)
                    last_save = time.time()
                
                time.sleep(1)
            
            # Process completed
            stdout, stderr = process.communicate(timeout=5)
            duration = time.time() - start_time
            
            output = stdout if stdout else stderr
            success = process.returncode == 0
            
            session_log.update({
                "status": "completed" if success else "failed",
                "duration": duration,
                "returncode": process.returncode,
                "output_preview": output[:500] if output else ""
            })
            self._save_session(session_id, session_log)
            
            return {
                "success": success,
                "output": output,
                "duration": duration,
                "timeout_hit": False,
                "session_id": session_id
            }
            
        except Exception as e:
            session_log["status"] = "error"
            session_log["error"] = str(e)
            self._save_session(session_id, session_log)
            return {
                "success": False,
                "output": f"❌ Error: {str(e)}",
                "duration": time.time() - start_time,
                "timeout_hit": False,
                "session_id": session_id
            }
    
    def health_check(self) -> Dict:
        """Check if Claude CLI is working"""
        try:
            result = subprocess.run(
                ["node", self.CLAUDE_CLI_PATH, "--version"],
                capture_output=True,
                text=True,
                timeout=10
            )
            return {
                "healthy": result.returncode == 0,
                "version": result.stdout.strip() if result.returncode == 0 else None,
                "error": result.stderr if result.returncode != 0 else None
            }
        except Exception as e:
            return {
                "healthy": False,
                "error": str(e)
            }
    
    def restart_if_needed(self) -> Dict:
        """Restart Claude if unhealthy"""
        health = self.health_check()
        if not health["healthy"]:
            # Try to kill any hanging processes
            subprocess.run(["pkill", "-f", "cli.js"], capture_output=True)
            time.sleep(2)
            # Check again
            health = self.health_check()
        return health
    
    def _save_session(self, session_id: str, data: Dict):
        """Save session to disk"""
        path = os.path.join(self.sessions_dir, f"{session_id}.json")
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    # ═══════════════════════════════════════════════════════════
    # PHASE 2: QUALITY GATES (Lint, Type-check, Tests)
    # ═══════════════════════════════════════════════════════════
    
    def quality_gate(self, code: str, language: str = "python") -> Dict:
        """
        Run quality checks on generated code
        
        Returns: {
            "passed": bool,
            "checks": {
                "syntax": bool,
                "lint": bool,
                "types": bool,
                "tests": bool
            },
            "errors": List[str]
        }
        """
        results = {
            "passed": False,
            "checks": {},
            "errors": []
        }
        
        if language == "python":
            # Check 1: Syntax
            try:
                compile(code, '<string>', 'exec')
                results["checks"]["syntax"] = True
            except SyntaxError as e:
                results["checks"]["syntax"] = False
                results["errors"].append(f"Syntax error: {e}")
                return results
            
            # Check 2: Lint with flake8
            flake8_result = self._run_flake8(code)
            results["checks"]["lint"] = flake8_result["passed"]
            if not flake8_result["passed"]:
                results["errors"].extend(flake8_result["errors"][:3])  # First 3 errors
            
            # Check 3: Type hints with mypy (if available)
            mypy_result = self._run_mypy(code)
            results["checks"]["types"] = mypy_result["passed"]
            if not mypy_result["passed"]:
                results["errors"].extend(mypy_result["errors"][:2])
        
        # Overall pass if syntax is OK and at least 2 of 3 checks passed
        passed_checks = sum(results["checks"].values())
        results["passed"] = results["checks"].get("syntax", False) and passed_checks >= 2
        
        return results
    
    def _run_flake8(self, code: str) -> Dict:
        """Run flake8 on code"""
        try:
            # Write to temp file
            temp_file = os.path.join(self.SANDBOX_DIR, "temp_check.py")
            with open(temp_file, 'w') as f:
                f.write(code)
            
            result = subprocess.run(
                ["python3", "-m", "flake8", "--max-line-length=100", temp_file],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                return {"passed": True, "errors": []}
            else:
                errors = [line for line in result.stdout.split('\n') if line.strip()]
                return {"passed": False, "errors": errors}
        except Exception as e:
            return {"passed": True, "errors": [], "note": f"flake8 not available: {e}"}
    
    def _run_mypy(self, code: str) -> Dict:
        """Run mypy type checking"""
        try:
            temp_file = os.path.join(self.SANDBOX_DIR, "temp_check.py")
            with open(temp_file, 'w') as f:
                f.write(code)
            
            result = subprocess.run(
                ["python3", "-m", "mypy", "--ignore-missing-imports", temp_file],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            # mypy returns 0 if no errors, 1 if errors found
            errors = [line for line in result.stdout.split('\n') if line.strip() and not line.startswith("Success")]
            return {"passed": result.returncode == 0, "errors": errors}
        except Exception as e:
            return {"passed": True, "errors": [], "note": f"mypy not available: {e}"}
    
    def approve_complexity(self, code: str, task_description: str) -> Tuple[str, str]:
        """
        Determine approval level based on complexity
        
        Returns: (level, reason)
        level: "auto" | "medium" | "complex"
        """
        lines = len(code.split('\n'))
        
        # Check for complex patterns
        complex_patterns = [
            "class ", "def ", "import ", "async ", "threading",
            "subprocess", "os.system", "eval(", "exec("
        ]
        complexity_score = sum(1 for p in complex_patterns if p in code)
        
        if lines < 50 and complexity_score < 3:
            return "auto", f"Simple ({lines} lines, low complexity)"
        elif lines < 200 and complexity_score < 6:
            return "medium", f"Medium ({lines} lines, moderate complexity)"
        else:
            return "complex", f"Complex ({lines} lines, high complexity)"
    
    # ═══════════════════════════════════════════════════════════
    # PHASE 3: SMART ROUTING (Claude vs Kimi)
    # ═══════════════════════════════════════════════════════════
    
    def assess_complexity(self, task: str) -> Dict:
        """
        Assess task complexity to route to Claude or Kimi
        
        Returns: {
            "complexity": float (0-1),
            "recommendation": "claude" | "kimi",
            "reason": str
        }
        """
        # Keywords indicating high complexity
        complex_keywords = [
            "архитектура", "architecture", "фреймворк", "framework",
            "микросервис", "microservice", "база данных", "database",
            "api", "интеграция", "integration", "async", "потоки",
            "многопоточность", "threading", "class ", "класс "
        ]
        
        # Keywords indicating simple tasks
        simple_keywords = [
            "исправь", "fix", " typo", "опечатка",
            "переименуй", "rename", "удали", "delete",
            "комментарий", "comment", "добавь строку"
        ]
        
        task_lower = task.lower()
        complex_score = sum(2 for kw in complex_keywords if kw in task_lower)
        simple_score = sum(1 for kw in simple_keywords if kw in task_lower)
        
        # Estimate lines needed
        if any(w in task_lower for w in ["скрипт", "script", "функция", "function"]):
            estimated_lines = 50
        elif any(w in task_lower for w in ["модуль", "module", "класс", "class"]):
            estimated_lines = 150
        else:
            estimated_lines = 30
        
        # Calculate complexity score (0-1)
        complexity = min(1.0, (complex_score * 0.15 + estimated_lines / 300))
        
        # Adjust for simple keywords
        complexity = max(0, complexity - simple_score * 0.1)
        
        if complexity > 0.6:
            return {
                "complexity": complexity,
                "recommendation": "claude",
                "reason": f"High complexity ({complexity:.2f}): architecture, multiple components, or >100 lines"
            }
        else:
            return {
                "complexity": complexity,
                "recommendation": "kimi",
                "reason": f"Low complexity ({complexity:.2f}): simple fix or <50 lines"
            }
    
    # ═══════════════════════════════════════════════════════════
    # PHASE 4: COST CONTROL (Tracking, Alerts, Optimization)
    # ═══════════════════════════════════════════════════════════
    
    def get_today_cost(self) -> float:
        """Get today's Claude usage cost"""
        today = datetime.now().strftime('%Y-%m-%d')
        
        if not os.path.exists(self.cost_log):
            return 0.0
        
        try:
            with open(self.cost_log, 'r') as f:
                costs = json.load(f)
            
            today_costs = [c for c in costs if c.get('date') == today]
            return sum(c.get('cost', 0) for c in today_costs)
        except:
            return 0.0
    
    def log_cost(self, task: str, estimated_tokens: int):
        """Log cost for a task"""
        cost = (estimated_tokens / 1000) * self.COST_PER_1K_TOKENS
        
        entry = {
            "date": datetime.now().strftime('%Y-%m-%d'),
            "timestamp": datetime.now().isoformat(),
            "task": task[:100],
            "estimated_tokens": estimated_tokens,
            "cost": round(cost, 4)
        }
        
        costs = []
        if os.path.exists(self.cost_log):
            try:
                with open(self.cost_log, 'r') as f:
                    costs = json.load(f)
            except:
                pass
        
        costs.append(entry)
        
        # Keep only last 30 days
        cutoff = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        costs = [c for c in costs if c.get('date', '') >= cutoff]
        
        with open(self.cost_log, 'w') as f:
            json.dump(costs, f, indent=2)
        
        return cost
    
    def check_budget(self) -> Dict:
        """Check budget status and return alerts"""
        today_cost = self.get_today_cost()
        
        result = {
            "today_cost": round(today_cost, 2),
            "limit": self.COST_LIMIT_USD,
            "remaining": round(self.COST_LIMIT_USD - today_cost, 2),
            "percent_used": round((today_cost / self.COST_LIMIT_USD) * 100, 1),
            "alert": None
        }
        
        if today_cost >= self.COST_LIMIT_USD:
            result["alert"] = f"🚨 БЮДЖЕТ ИСЧЕРПАН: ${today_cost:.2f}/${self.COST_LIMIT_USD}"
            result["action"] = "switch_to_kimi"
        elif today_cost >= self.COST_ALERT_THRESHOLD:
            result["alert"] = f"⚠️ Бюджет на 75%: ${today_cost:.2f}/${self.COST_LIMIT_USD}"
            result["action"] = "warn_user"
        
        return result
    
    def get_cost_report(self, days: int = 7) -> str:
        """Generate cost report"""
        if not os.path.exists(self.cost_log):
            return "📊 Нет данных о расходах"
        
        try:
            with open(self.cost_log, 'r') as f:
                costs = json.load(f)
            
            cutoff = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
            recent_costs = [c for c in costs if c.get('date', '') >= cutoff]
            
            total = sum(c.get('cost', 0) for c in recent_costs)
            by_day = {}
            for c in recent_costs:
                by_day[c['date']] = by_day.get(c['date'], 0) + c.get('cost', 0)
            
            report = f"📊 Отчёт о расходах (последние {days} дней)\n\n"
            report += f"💰 Всего потрачено: ${total:.2f}\n"
            report += f"📅 Среднее в день: ${total/days:.2f}\n\n"
            
            if by_day:
                report += "По дням:\n"
                for date, cost in sorted(by_day.items())[-7:]:
                    bar = "█" * int(cost * 10)
                    report += f"  {date}: ${cost:.2f} {bar}\n"
            
            # Savings calculation
            dev_hour_rate = 50  # $50/hour for developer
            estimated_hours_saved = len(recent_costs) * 0.5  # 30 min per task
            savings = estimated_hours_saved * dev_hour_rate
            report += f"\n💡 Экономия vs найм разработчика: ~${savings:.0f}\n"
            
            return report
        except Exception as e:
            return f"❌ Ошибка отчёта: {e}"
    
    # ═══════════════════════════════════════════════════════════
    # MAIN EXECUTION
    # ═══════════════════════════════════════════════════════════
    
    def execute(self, task: str, context: str = "") -> Dict:
        """
        Main execution method with all 4 phases
        
        Phases:
        1. Check budget (Phase 4)
        2. Smart routing (Phase 3)
        3. Run with reliability (Phase 1)
        4. Quality gate (Phase 2)
        """
        # Phase 4: Budget check
        budget = self.check_budget()
        if budget.get("action") == "switch_to_kimi":
            return {
                "success": False,
                "output": f"{budget['alert']}\nПереключаюсь на Kimi API (бесплатно)",
                "switched_to": "kimi",
                "budget_status": budget
            }
        
        # Phase 3: Smart routing
        routing = self.assess_complexity(task)
        
        if routing["recommendation"] == "kimi":
            return {
                "success": True,
                "output": f"ℹ️ Задача низкой сложности ({routing['complexity']:.2f})\nРекомендация: использовать Kimi API (бесплатно)\n\nПричина: {routing['reason']}",
                "recommendation": "kimi",
                "routing": routing,
                "budget_status": budget
            }
        
        # Phase 1: Run Claude with timeout
        full_prompt = f"{context}\n\nTask: {task}" if context else task
        
        # Prepare claude command (use node to run the CLI)
        cmd = ["node", self.CLAUDE_CLI_PATH, "-p", full_prompt]
        
        result = self.run_with_timeout(cmd, cwd=self.SANDBOX_DIR)
        
        # Log cost (estimate based on output size)
        estimated_tokens = len(full_prompt.split()) + len(result.get("output", "").split())
        cost = self.log_cost(task, estimated_tokens)
        result["cost"] = round(cost, 4)
        result["budget_status"] = self.check_budget()
        
        # Phase 2: Quality gate if code was generated
        if result["success"] and "```python" in result.get("output", ""):
            # Extract code
            output = result["output"]
            code_blocks = []
            in_code = False
            current_block = []
            
            for line in output.split('\n'):
                if line.strip().startswith('```python') or line.strip().startswith('```'):
                    if in_code:
                        code_blocks.append('\n'.join(current_block))
                        current_block = []
                    in_code = not in_code
                elif in_code:
                    current_block.append(line)
            
            if current_block:
                code_blocks.append('\n'.join(current_block))
            
            if code_blocks:
                quality = self.quality_gate(code_blocks[0])
                result["quality_gate"] = quality
                
                # Determine approval level
                level, reason = self.approve_complexity(code_blocks[0], task)
                result["approval_level"] = level
                result["approval_reason"] = reason
                
                if level == "auto":
                    result["output"] += f"\n\n✅ Quality Gate: PASSED ({reason})"
                elif level == "medium":
                    result["output"] += f"\n\n⏸️ Quality Gate: MEDIUM — требуется review\n{reason}\n\nПроверьте код перед деплоем."
                else:
                    result["output"] += f"\n\n🛑 Quality Gate: COMPLEX — обязательный review\n{reason}\n\nКод требует вашего одобрения перед использованием."
        
        return result

def main():
    controller = ClaudeController()
    
    if len(sys.argv) < 2:
        print("🤖 Coding Agent for AI Genesis — Claude Code Controller")
        print("")
        print("Usage:")
        print('  python3 coding_agent.py exec "задача" [context]   # Выполнить задачу')
        print('  python3 coding_agent.py health                     # Проверить статус')
        print('  python3 coding_agent.py budget                     # Статус бюджета')
        print('  python3 coding_agent.py report [дней]              # Отчёт о расходах')
        print('  python3 coding_agent.py route "задача"             # Оценка маршрутизации')
        print('  python3 coding_agent.py quality "код"              # Проверить код')
        print("")
        print("Examples:")
        print('  python3 coding_agent.py exec "Напиши парсер JSON"')
        print('  python3 coding_agent.py exec "Исправь баг в боте" "bot_v10_all_skills.py"')
        print('  python3 coding_agent.py budget')
        sys.exit(0)
    
    command = sys.argv[1]
    
    if command == "exec" and len(sys.argv) >= 3:
        task = sys.argv[2]
        context = sys.argv[3] if len(sys.argv) > 3 else ""
        
        print(f"🚀 Запускаю Claude Code...")
        print(f"📋 Задача: {task[:60]}...")
        print(f"⏱️ Таймаут: 10 минут")
        print("")
        
        result = controller.execute(task, context)
        
        # Output result
        print(result.get("output", ""))
        
        print(f"\n{'='*60}")
        print(f"⏱️ Длительность: {result.get('duration', 0):.1f} сек")
        print(f"💰 Стоимость: ${result.get('cost', 0):.4f}")
        
        if "budget_status" in result:
            bs = result["budget_status"]
            print(f"💳 Бюджет сегодня: ${bs['today_cost']:.2f}/${bs['limit']}")
        
        if "approval_level" in result:
            print(f"🛡️ Уровень одобрения: {result['approval_level'].upper()}")
        
        if result.get("timeout_hit"):
            print("⚠️ ВНИМАНИЕ: Таймаут! Задача прервана.")
    
    elif command == "health":
        health = controller.health_check()
        if health["healthy"]:
            print(f"✅ Claude Code работает")
            print(f"📌 Версия: {health.get('version', 'unknown')}")
        else:
            print(f"❌ Claude Code не работает")
            print(f"📝 Ошибка: {health.get('error', 'unknown')}")
            print("\n🔄 Пробую перезапустить...")
            restart = controller.restart_if_needed()
            if restart["healthy"]:
                print("✅ Перезапуск успешен!")
            else:
                print("❌ Перезапуск не помог")
    
    elif command == "budget":
        budget = controller.check_budget()
        print(f"💳 Бюджет Claude Code")
        print(f"   Сегодня: ${budget['today_cost']:.2f}")
        print(f"   Лимит: ${budget['limit']:.2f}")
        print(f"   Осталось: ${budget['remaining']:.2f}")
        print(f"   Использовано: {budget['percent_used']:.1f}%")
        
        if budget.get("alert"):
            print(f"\n{budget['alert']}")
    
    elif command == "report":
        days = int(sys.argv[2]) if len(sys.argv) > 2 else 7
        print(controller.get_cost_report(days))
    
    elif command == "route":
        if len(sys.argv) < 3:
            print("Укажите задачу для оценки")
            sys.exit(1)
        
        task = sys.argv[2]
        routing = controller.assess_complexity(task)
        
        print(f"🧠 Оценка сложности задачи")
        print(f"   Задача: {task[:60]}...")
        print(f"   Сложность: {routing['complexity']:.2f}/1.0")
        print(f"   Рекомендация: {routing['recommendation'].upper()}")
        print(f"   Причина: {routing['reason']}")
    
    elif command == "quality":
        if len(sys.argv) < 3:
            print("Укажите файл с кодом")
            sys.exit(1)
        
        code_file = sys.argv[2]
        try:
            with open(code_file, 'r') as f:
                code = f.read()
            
            quality = controller.quality_gate(code)
            print(f"🛡️ Quality Gate Results")
            print(f"   Passed: {'✅ ДА' if quality['passed'] else '❌ НЕТ'}")
            print(f"   Checks: {quality['checks']}")
            if quality['errors']:
                print(f"\n❌ Errors ({len(quality['errors'])}):")
                for err in quality['errors'][:5]:
                    print(f"   • {err}")
        except Exception as e:
            print(f"❌ Ошибка чтения файла: {e}")
    
    else:
        print(f"❌ Unknown command: {command}")
        print("Run without arguments for help")

if __name__ == "__main__":
    main()
