#!/usr/bin/env python3
"""
Voice Sales Agent v1.0 — AI Voice Calls for Sales Qualification
Human-like conversations with natural Russian-accented voices for immigrant business owners
"""

import json
import os
import re
import random
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from enum import Enum
import sqlite3

class CallOutcome(Enum):
    """Possible outcomes of a sales call"""
    QUALIFIED = "qualified"
    FOLLOW_UP = "follow_up"
    NOT_INTERESTED = "not_interested"
    VOICEMAIL = "voicemail"
    NO_ANSWER = "no_answer"
    APPOINTMENT_SET = "appointment_set"
    NEEDS_MORE_INFO = "needs_more_info"

class VoicePersona(Enum):
    """Voice personas for different contexts"""
    FRIENDLY = "friendly"  # Warm, approachable
    PROFESSIONAL = "professional"  # Business formal
    CONSULTANT = "consultant"  # Expert advisor
    URGENT = "urgent"  # Time-sensitive

@dataclass
class CallScript:
    """Complete call script with branching logic"""
    name: str
    opening: str
    qualification_questions: List[Dict]
    objection_handlers: Dict[str, str]
    closing_options: List[str]
    fallback_responses: List[str]

@dataclass
class CallRecord:
    """Record of a voice call"""
    id: str
    phone: str
    contact_name: str
    business_type: str
    started_at: str
    duration_seconds: int
    transcript: List[Dict]
    outcome: CallOutcome
    qualification_score: int  # 0-100
    notes: str
    follow_up_date: Optional[str]
    recording_url: Optional[str]


class VoiceSalesAgent:
    """
    AI Voice Sales Agent for qualification calls
    
    Features:
    - Natural Russian-accented voices (for immigrant businesses)
    - Dynamic call scripts with branching
    - Real-time qualification scoring
    - Objection handling library
    - CRM integration for logging
    - Call analytics and insights
    """
    
    def __init__(self, db_path: str = "/root/.openclaw/data/voice_sales.db"):
        self.db_path = db_path
        self._init_db()
        self.active_calls = {}
        
        # Voice configuration
        self.voice_config = {
            'provider': 'elevenlabs',  # or 'openai', 'google'
            'default_voice': 'onyx',  # warm male
            'female_voice': 'nova',   # warm female
            'accent': 'slight_russian',  # subtle accent for authenticity
            'speed': 0.95,  # slightly slower for clarity
            'stability': 0.7,
            'similarity_boost': 0.8
        }
    
    def _init_db(self):
        """Initialize database for call tracking"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS calls (
                id TEXT PRIMARY KEY,
                phone TEXT NOT NULL,
                contact_name TEXT,
                business_type TEXT,
                started_at TEXT,
                duration_seconds INTEGER,
                transcript TEXT,
                outcome TEXT,
                qualification_score INTEGER,
                notes TEXT,
                follow_up_date TEXT,
                recording_url TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS scripts (
                id TEXT PRIMARY KEY,
                name TEXT,
                script_data TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def get_script(self, script_name: str = "qualification") -> CallScript:
        """Get call script by name"""
        scripts = {
            "qualification": CallScript(
                name="Sales Qualification",
                opening="""Здравствуйте, {name}! Меня зовут {agent_name}, я из AI Genesis. 
Вы оставляли заявку на нашем сайте насчёт автоматизации для {business_type}. 
У вас есть 5 минут, чтобы я рассказал, как это работает?""",
                qualification_questions=[
                    {
                        "id": "business_type",
                        "question": "Расскажите, чем занимается ваш бизнес? Сколько у вас клиентов в неделю?",
                        "purpose": "Understand business size and needs",
                        "follow_up": {
                            "low_volume": "А вы вручную всё ведёте? Как долго это занимает?",
                            "high_volume": "Как вы справляетесь с таким потоком? Есть ли система записи?"
                        }
                    },
                    {
                        "id": "pain_point",
                        "question": "Что больше всего отнимает ваше время сейчас?",
                        "purpose": "Identify main pain point",
                        "options": ["записи", "переписка", "напоминания", "документы", "другое"]
                    },
                    {
                        "id": "current_solution",
                        "question": "Пробовали ли уже что-то автоматизировать?",
                        "purpose": "Check previous experience",
                        "follow_up": {
                            "yes": "Что не устроило в прошлом решении?",
                            "no": "Почему решили посмотреть сейчас? Что изменилось?"
                        }
                    },
                    {
                        "id": "decision_maker",
                        "question": "Кроме вас, кто ещё принимает решения о внедрении?",
                        "purpose": "Identify decision makers"
                    },
                    {
                        "id": "budget",
                        "question": "Если мы найдём решение, которое сэкономит вам 10 часов в неделю, в какой бюджет вы смотрите?",
                        "purpose": "Budget qualification",
                        "indicators": {
                            "under_100": "probably_not_ready",
                            "100_350": "pilot_candidate",
                            "350_700": "full_solution",
                            "over_700": "premium"
                        }
                    },
                    {
                        "id": "timeline",
                        "question": "Насколько срочно вам нужно решение?",
                        "purpose": "Timeline qualification",
                        "options": ["срочно", "в течение месяца", "просто смотрю"]
                    }
                ],
                objection_handlers={
                    "дорого": """Я понимаю. Давайте посчитаем: сколько часов в неделю вы тратите на переписку с клиентами? 
Умножьте на вашу часовую ставку — это ваша реальная стоимость. 
Пилот за $350 окупается, если экономит всего 7 часов.""",
                    
                    "не сейчас": """Конечно, выберите удобное время. Но могу я задать один вопрос? 
Что изменится через месяц? Иногда "потом" превращается в "уже поздно", когда клиенты уходят к конкурентам с автоматизацией.""",
                    
                    "нужно подумать": """Разумно. Подумайте над этим: сколько клиентов вы потеряли за последний месяц из-за того, 
что не успели ответить или забыли перезвонить? Одного клиента достаточно, чтобы окупить пилот.""",
                    
                    "не уверен что поможет": """Сомнения нормальны. Поэтому у нас есть пилот — вы тестируете 2 недели, 
видите реальные цифры, и только потом решаете. Никакого риска. Если не понравится — вернём деньги.""",
                    
                    "уже есть система": """Отлично! Значит, вы понимаете ценность автоматизации. 
Вопрос: ваша текущая система решает проблему полностью или есть "слепые зоны"?""",
                    
                    "нет времени": """Это именно то, с чем мы помогаем. За 20-минутный звонок я покажу, 
как вернуть вам 10+ часов в неделю. Это инвестиция времени, которая окупается в первую же неделю.""",
                    
                    "сам сделаю": """Уважаю! Вы техничный человек. Вопрос: сколько времени займёт разработка? 
И главное — кто будет поддерживать, когда что-то сломается? Иногда дешевле купить, чем создавать своё.""",
                    
                    "надо спросить партнёра": """Конечно, важное решение. Давайте так: я пришлю короткое видео — 3 минуты, 
как работает система. Покажите партнёру, и если заинтересуетесь — договоримся о созвоне втроём. Окей?"""
                },
                closing_options=[
                    "Давайте я назначу встречу на этой неделе. Какой день удобнее — вторник или четверг?",
                    "Я пришлю демо-видео и PDF с ценами. Какой мессенджер удобнее — Telegram или WhatsApp?",
                    "Давайте запустим пилот. Он займёт 20 минут настройки, и вы увидите результат уже сегодня.",
                    "Я понимаю, что нужно время. Могу я перезвонить через неделю? Или напишу вам тогда?"
                ],
                fallback_responses=[
                    "Понял вас. Расскажите подробнее?",
                    "Интересно. А что по этому поводу думаете?",
                    "Понятно. Давайте вернёмся к главному — какую задачу хотите решить в первую очередь?",
                    "Записал. Ещё один вопрос..."
                ]
            ),
            
            "follow_up": CallScript(
                name="Follow-Up Call",
                opening="""Привет, {name}! Это {agent_name} из AI Genesis. 
Неделю назад обсуждали автоматизацию для {business_type}. 
Как дела? Успели подумать?""",
                qualification_questions=[
                    {
                        "id": "decision_progress",
                        "question": "Как продвигается с решением?",
                        "purpose": "Check decision progress"
                    },
                    {
                        "id": "new_info",
                        "question": "Появились ли новые вопросы после нашего разговора?",
                        "purpose": "Address new concerns"
                    },
                    {
                        "id": "competition",
                        "question": "Смотрели ещё чьи-то решения? Что вам там понравилось?",
                        "purpose": "Competitive intelligence"
                    }
                ],
                objection_handlers={
                    "ещё думаю": "Понимаю. Что именно осталось неясным? Может, уточню детали?",
                    "выбрал другого": "Жаль, что не мы. Можно узнать, что стало решающим фактором? Это поможет нам улучшиться.",
                    "не актуально": "Понял. Что изменилось? Если передумаете — всегда на связи."
                },
                closing_options=[
                    "Давайте попробуем пилот. Если не зайдёт — просто откажетесь, без обид.",
                    "Я пришлю новый кейс, который может быть релевантен. Посмотрите?",
                    "Окей, тогда я напомню через месяц, если вы не против?"
                ],
                fallback_responses=[
                    "Понятно. Спасибо за честность.",
                    "Записал. Будем на связи!"
                ]
            ),
            
            "appointment_reminder": CallScript(
                name="Appointment Reminder",
                opening="""Здравствуйте, {name}! Напоминаю, что завтра в {time} у нас созвон 
насчёт автоматизации {business_type}. Вы подтверждаете?""",
                qualification_questions=[
                    {
                        "id": "confirmation",
                        "question": "Завтра в {time} удобно?",
                        "purpose": "Confirm appointment"
                    }
                ],
                objection_handlers={
                    "нужно перенести": "Конечно. На когда перенести?",
                    "не могу": "Понял. Давайте перенесём. Какая неделя удобнее?"
                },
                closing_options=[
                    "Отлично, жду вас завтра в {time}. Пришлю ссылку за час до звонка.",
                    "Перенёс на {new_time}. До встречи!"
                ],
                fallback_responses=[
                    "Отлично, до завтра!"
                ]
            )
        }
        
        return scripts.get(script_name, scripts["qualification"])
    
    def generate_call_script(self, contact: Dict, script_name: str = "qualification") -> str:
        """Generate personalized call script for TTS"""
        script = self.get_script(script_name)
        
        # Personalize opening
        opening = script.opening.format(
            name=contact.get('name', ''),
            agent_name=contact.get('agent_name', 'Алекс'),
            business_type=contact.get('business_type', 'вашего бизнеса')
        )
        
        return opening
    
    def generate_tts(self, text: str, voice: str = None, output_path: str = None) -> str:
        """
        Generate text-to-speech audio
        Returns path to audio file
        """
        voice = voice or self.voice_config['default_voice']
        
        if not output_path:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_path = f"/root/.openclaw/output/voice_{timestamp}.mp3"
        
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # In production, this would call TTS API
        # For now, create a placeholder that shows what would be generated
        placeholder = {
            'text': text,
            'voice': voice,
            'config': self.voice_config,
            'output_path': output_path,
            'duration_estimate': len(text.split()) * 0.5  # ~0.5 sec per word
        }
        
        with open(output_path.replace('.mp3', '.json'), 'w', encoding='utf-8') as f:
            json.dump(placeholder, f, indent=2, ensure_ascii=False)
        
        return output_path
    
    def simulate_call(self, contact: Dict, script_name: str = "qualification") -> CallRecord:
        """
        Simulate a voice call (for testing/demo)
        In production, this would integrate with telephony API
        """
        import uuid
        
        call_id = str(uuid.uuid4())[:8]
        script = self.get_script(script_name)
        
        # Generate opening audio
        opening_text = self.generate_call_script(contact, script_name)
        audio_path = self.generate_tts(opening_text, output_path=f"/root/.openclaw/output/call_{call_id}_opening.mp3")
        
        # Simulate conversation flow
        transcript = [
            {
                'speaker': 'agent',
                'text': opening_text,
                'timestamp': datetime.now().isoformat()
            }
        ]
        
        # Add simulated responses (in production, these would be real)
        simulated_flow = [
            {'speaker': 'customer', 'text': 'Да, удобно, расскажите'},
            {'speaker': 'agent', 'text': script.qualification_questions[0]['question']},
            {'speaker': 'customer', 'text': 'У меня салон красоты, около 50 клиентов в неделю'},
            {'speaker': 'agent', 'text': 'Отлично! А как сейчас ведёте записи?'},
            {'speaker': 'customer', 'text': 'Вручную, в блокноте и WhatsApp'},
            {'speaker': 'agent', 'text': script.qualification_questions[1]['question']},
            {'speaker': 'customer', 'text': 'В основном переписка отнимает время'},
            {'speaker': 'agent', 'text': script.qualification_questions[4]['question']},
            {'speaker': 'customer', 'text': 'Ну, если реально поможет, готов выделить до 500 долларов'},
        ]
        
        transcript.extend(simulated_flow)
        
        # Determine outcome based on responses
        qualification_score = 75  # Simulated
        outcome = CallOutcome.QUALIFIED if qualification_score >= 70 else CallOutcome.FOLLOW_UP
        
        call_record = CallRecord(
            id=call_id,
            phone=contact.get('phone', ''),
            contact_name=contact.get('name', ''),
            business_type=contact.get('business_type', ''),
            started_at=datetime.now().isoformat(),
            duration_seconds=len(transcript) * 30,  # Estimate
            transcript=transcript,
            outcome=outcome,
            qualification_score=qualification_score,
            notes="Simulated call for demo purposes",
            follow_up_date=(datetime.now() + timedelta(days=3)).strftime('%Y-%m-%d') if outcome == CallOutcome.FOLLOW_UP else None,
            recording_url=audio_path
        )
        
        # Store in database
        self._store_call(call_record)
        
        return call_record
    
    def _store_call(self, call: CallRecord):
        """Store call record in database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO calls 
            (id, phone, contact_name, business_type, started_at, duration_seconds, 
             transcript, outcome, qualification_score, notes, follow_up_date, recording_url)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            call.id, call.phone, call.contact_name, call.business_type,
            call.started_at, call.duration_seconds, json.dumps(call.transcript, ensure_ascii=False),
            call.outcome.value, call.qualification_score, call.notes,
            call.follow_up_date, call.recording_url
        ))
        
        conn.commit()
        conn.close()
    
    def get_call_analytics(self, days: int = 30) -> Dict:
        """Get analytics for calls in last N days"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT outcome, COUNT(*), AVG(qualification_score), AVG(duration_seconds)
            FROM calls
            WHERE started_at >= datetime('now', '-{} days')
            GROUP BY outcome
        '''.format(days))
        
        results = cursor.fetchall()
        conn.close()
        
        analytics = {
            'total_calls': sum(r[1] for r in results),
            'by_outcome': {r[0]: {'count': r[1], 'avg_score': round(r[2], 1)} for r in results},
            'avg_duration': round(sum(r[1] * r[3] for r in results) / sum(r[1] for r in results) / 60, 1) if results else 0,
            'conversion_rate': 0
        }
        
        if analytics['total_calls'] > 0:
            qualified = analytics['by_outcome'].get('qualified', {}).get('count', 0)
            appointments = analytics['by_outcome'].get('appointment_set', {}).get('count', 0)
            analytics['conversion_rate'] = round((qualified + appointments) / analytics['total_calls'] * 100, 1)
        
        return analytics
    
    def get_objection_handler(self, objection_text: str, script_name: str = "qualification") -> str:
        """Get appropriate objection handler"""
        script = self.get_script(script_name)
        
        objection_lower = objection_text.lower()
        
        # Match objection to handler
        for key, handler in script.objection_handlers.items():
            if key in objection_lower:
                return handler
        
        # Default fallback
        return random.choice(script.fallback_responses)
    
    def generate_call_sequence(self, lead: Dict) -> List[Dict]:
        """Generate complete call sequence for a lead"""
        sequence = []
        
        # Call 1: Initial qualification (Day 0)
        sequence.append({
            'step': 1,
            'day': 0,
            'type': 'call',
            'script': 'qualification',
            'purpose': 'Qualify and present pilot',
            'duration_estimate': '5-10 min'
        })
        
        # Email follow-up (Day 1)
        sequence.append({
            'step': 2,
            'day': 1,
            'type': 'email',
            'subject': 'AI Genesis — материалы по автоматизации',
            'purpose': 'Send case studies and pricing'
        })
        
        # Call 2: Follow-up (Day 3)
        sequence.append({
            'step': 3,
            'day': 3,
            'type': 'call',
            'script': 'follow_up',
            'purpose': 'Address objections and close',
            'duration_estimate': '3-5 min'
        })
        
        # Voice message (Day 7)
        sequence.append({
            'step': 4,
            'day': 7,
            'type': 'voice_message',
            'text': f"""Привет, {lead.get('name')}! Это AI Genesis. 
            Напоминаю про пилот за $350 — он всё ещё доступен. 
            Если заинтересовало, просто ответьте на это сообщение.""",
            'purpose': 'Gentle reminder'
        })
        
        # Final call (Day 14)
        sequence.append({
            'step': 5,
            'day': 14,
            'type': 'call',
            'script': 'final_follow_up',
            'purpose': 'Last attempt or close file',
            'duration_estimate': '2-3 min'
        })
        
        return sequence
    
    def export_for_crm(self, call_id: str) -> Dict:
        """Export call data for CRM integration"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM calls WHERE id = ?', (call_id,))
        row = cursor.fetchone()
        conn.close()
        
        if not row:
            return None
        
        return {
            'id': row[0],
            'phone': row[1],
            'contact_name': row[2],
            'business_type': row[3],
            'started_at': row[4],
            'duration_minutes': round(row[5] / 60, 1),
            'outcome': row[7],
            'qualification_score': row[8],
            'follow_up_date': row[10],
            'notes': row[9],
            'next_action': 'Schedule follow-up' if row[7] == 'follow_up' else 'Send proposal' if row[7] == 'qualified' else 'Archive'
        }


def main():
    import sys
    
    agent = VoiceSalesAgent()
    
    if len(sys.argv) < 2:
        print("""
🎙️ Voice Sales Agent v1.0 — AI Voice Calls for Sales

Commands:
  script [name]              Show call script
  simulate [name] [phone]    Simulate a call
  tts "text"                 Generate voice audio
  objection "text"           Get objection handler
  sequence [name] [phone]    Generate call sequence
  analytics [days]           Show call analytics
  export [call_id]           Export call for CRM

Examples:
  python3 voice_sales_agent.py script qualification
  python3 voice_sales_agent.py simulate "Иван" "+1-555-123-4567"
  python3 voice_sales_agent.py tts "Здравствуйте! Это AI Genesis"
  python3 voice_sales_agent.py objection "дорого"
  python3 voice_sales_agent.py analytics 30
        """)
        sys.exit(0)
    
    command = sys.argv[1]
    
    if command == 'script':
        script_name = sys.argv[2] if len(sys.argv) > 2 else 'qualification'
        script = agent.get_script(script_name)
        print(f"\n📋 Script: {script.name}\n")
        print(f"Opening:\n{script.opening}\n")
        print(f"Questions ({len(script.qualification_questions)}):")
        for i, q in enumerate(script.qualification_questions, 1):
            print(f"  {i}. {q['question']}")
        print(f"\nObjection Handlers ({len(script.objection_handlers)}):")
        for obj in script.objection_handlers.keys():
            print(f"  • {obj}")
    
    elif command == 'simulate':
        name = sys.argv[2] if len(sys.argv) > 2 else 'Test Contact'
        phone = sys.argv[3] if len(sys.argv) > 3 else '+1-555-000-0000'
        
        contact = {
            'name': name,
            'phone': phone,
            'business_type': 'салон красоты',
            'agent_name': 'Алекс'
        }
        
        print(f"\n📞 Simulating call to {name} ({phone})...")
        call = agent.simulate_call(contact)
        
        print(f"\n✅ Call completed!")
        print(f"   ID: {call.id}")
        print(f"   Duration: {call.duration_seconds} seconds")
        print(f"   Outcome: {call.outcome.value}")
        print(f"   Qualification Score: {call.qualification_score}/100")
        print(f"   Follow-up: {call.follow_up_date or 'Not scheduled'}")
        print(f"\n📝 Transcript preview:")
        for entry in call.transcript[:5]:
            print(f"   {entry['speaker']}: {entry['text'][:60]}...")
        print(f"   ... ({len(call.transcript) - 5} more entries)")
    
    elif command == 'tts' and len(sys.argv) > 2:
        text = sys.argv[2]
        path = agent.generate_tts(text)
        print(f"\n🎙️ TTS Generated")
        print(f"   Text: {text[:60]}...")
        print(f"   Config: {agent.voice_config}")
        print(f"   Output: {path}")
    
    elif command == 'objection' and len(sys.argv) > 2:
        objection = sys.argv[2]
        handler = agent.get_objection_handler(objection)
        print(f"\n💬 Objection: {objection}")
        print(f"\n🎯 Handler:\n{handler}")
    
    elif command == 'sequence':
        name = sys.argv[2] if len(sys.argv) > 2 else 'Lead'
        phone = sys.argv[3] if len(sys.argv) > 3 else ''
        
        lead = {'name': name, 'phone': phone}
        sequence = agent.generate_call_sequence(lead)
        
        print(f"\n📞 Call Sequence for {name}:")
        for step in sequence:
            print(f"\n  Step {step['step']} (Day +{step['day']}):")
            print(f"    Type: {step['type']}")
            print(f"    Purpose: {step['purpose']}")
            if 'script' in step:
                print(f"    Script: {step['script']}")
            if 'duration_estimate' in step:
                print(f"    Duration: {step['duration_estimate']}")
    
    elif command == 'analytics':
        days = int(sys.argv[2]) if len(sys.argv) > 2 else 30
        analytics = agent.get_call_analytics(days)
        
        print(f"\n📊 Call Analytics (Last {days} days)")
        print(f"   Total Calls: {analytics['total_calls']}")
        print(f"   Avg Duration: {analytics['avg_duration']} min")
        print(f"   Conversion Rate: {analytics['conversion_rate']}%")
        print(f"\n   By Outcome:")
        for outcome, data in analytics['by_outcome'].items():
            print(f"      {outcome}: {data['count']} calls (avg score: {data['avg_score']})")
    
    elif command == 'export' and len(sys.argv) > 2:
        call_id = sys.argv[2]
        data = agent.export_for_crm(call_id)
        if data:
            print(f"\n📤 CRM Export for Call {call_id}:")
            print(json.dumps(data, indent=2, ensure_ascii=False))
        else:
            print(f"❌ Call {call_id} not found")
    
    else:
        print(f"❌ Unknown command: {command}")
        print("Run without arguments for help")


if __name__ == "__main__":
    main()
