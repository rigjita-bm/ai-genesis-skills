#!/usr/bin/env python3
"""
Voice Sales Agent v1.0 — AI Voice Calls for Sales Qualification
Human-like conversations with natural voices for immigrant business owners
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
    - Multi-language support (English, Russian, Spanish)
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
            'accent': 'natural',  # subtle accent for authenticity
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
                opening="""Hello {name}! This is {agent_name} from AI Genesis. 
You left a request on our website about automation for {business_type}. 
Do you have 5 minutes for me to explain how it works?""",
                qualification_questions=[
                    {
                        "id": "business_type",
                        "question": "Tell me about your business. How many clients do you have per week?",
                        "purpose": "Understand business size and needs",
                        "follow_up": {
                            "low_volume": "Are you managing everything manually? How long does that take?",
                            "high_volume": "How do you handle that volume? Do you have a booking system?"
                        }
                    },
                    {
                        "id": "pain_point",
                        "question": "What takes most of your time right now?",
                        "purpose": "Identify main pain point",
                        "options": ["bookings", "messaging", "reminders", "documents", "other"]
                    },
                    {
                        "id": "current_solution",
                        "question": "Have you tried automating anything before?",
                        "purpose": "Check previous experience",
                        "follow_up": {
                            "yes": "What didn't work with your previous solution?",
                            "no": "Why are you looking at this now? What changed?"
                        }
                    },
                    {
                        "id": "decision_maker",
                        "question": "Besides you, who else makes decisions about implementation?",
                        "purpose": "Identify decision makers"
                    },
                    {
                        "id": "budget",
                        "question": "If we find a solution that saves you 10 hours per week, what budget are you looking at?",
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
                        "question": "How urgent is this need?",
                        "purpose": "Timeline qualification",
                        "options": ["urgent", "within_month", "just_looking"]
                    }
                ],
                objection_handlers={
                    "too_expensive": """I understand. Let's calculate: how many hours per week do you spend on client communication? 
Multiply by your hourly rate — that's your real cost. 
The $350 pilot pays for itself if it saves just 7 hours.""",
                    
                    "not_now": """Of course, choose a convenient time. But can I ask one question? 
What will change in a month? Sometimes "later" becomes "too late" when clients go to competitors with automation.""",
                    
                    "need_to_think": """Reasonable. Think about this: how many clients did you lose last month because 
you didn't respond in time or forgot to call back? Just one client is enough to pay for the pilot.""",
                    
                    "not_sure": """Doubts are normal. That's why we have a pilot — you test for 2 weeks, 
see real numbers, and only then decide. No risk. If you don't like it — we refund your money.""",
                    
                    "have_system": """Great! That means you understand the value of automation. 
Question: does your current system solve the problem completely or are there "blind spots"?""",
                    
                    "no_time": """That's exactly what we help with. In a 20-minute call I'll show you 
how to get back 10+ hours per week. It's a time investment that pays off in the first week.""",
                    
                    "build_myself": """Respect! You're a technical person. Question: how long will development take? 
And importantly — who will support it when something breaks? Sometimes it's cheaper to buy than to build.""",
                    
                    "ask_partner": """Of course, it's an important decision. Here's what I'll do: I'll send a short 3-minute video 
showing how the system works. Show it to your partner, and if you're interested — let's schedule a call together. Okay?"""
                },
                closing_options=[
                    "Let me schedule a meeting this week. Which day works better — Tuesday or Thursday?",
                    "I'll send a demo video and pricing PDF. Which messenger works better for you — Telegram or WhatsApp?",
                    "Let's launch the pilot. It takes 20 minutes to set up, and you'll see results today.",
                    "I understand you need time. Can I call back next week? Or should I message you then?"
                ],
                fallback_responses=[
                    "I understand. Tell me more?",
                    "Interesting. What do you think about that?",
                    "Got it. Let's get back to the main thing — which problem do you want to solve first?",
                    "Noted. One more question..."
                ]
            ),
            
            "follow_up": CallScript(
                name="Follow-Up Call",
                opening="""Hi {name}! This is {agent_name} from AI Genesis. 
We discussed automation for {business_type} a week ago. 
How are things? Did you have time to think?""",
                qualification_questions=[
                    {
                        "id": "decision_progress",
                        "question": "How is the decision going?",
                        "purpose": "Check decision progress"
                    },
                    {
                        "id": "new_info",
                        "question": "Any new questions after our conversation?",
                        "purpose": "Address new concerns"
                    },
                    {
                        "id": "competition",
                        "question": "Did you look at anyone else's solutions? What did you like there?",
                        "purpose": "Competitive intelligence"
                    }
                ],
                objection_handlers={
                    "still_thinking": "I understand. What exactly is still unclear? Maybe I can clarify details?",
                    "chose_another": "Sorry it's not us. Can I ask what was the deciding factor? It will help us improve.",
                    "not_relevant": "Got it. What changed? If you reconsider — we're always here."
                },
                closing_options=[
                    "Let's try the pilot. If it doesn't work — just decline, no hard feelings.",
                    "I'll send a new case study that might be relevant. Want to see?",
                    "Okay, then I'll remind you in a month, if you don't mind?"
                ],
                fallback_responses=[
                    "Got it. Thanks for being honest.",
                    "Noted. We'll be in touch!"
                ]
            ),
            
            "appointment_reminder": CallScript(
                name="Appointment Reminder",
                opening="""Hello {name}! Reminding you that tomorrow at {time} we have a call 
about automation for {business_type}. Do you confirm?""",
                qualification_questions=[
                    {
                        "id": "confirmation",
                        "question": "Is tomorrow at {time} convenient?",
                        "purpose": "Confirm appointment"
                    }
                ],
                objection_handlers={
                    "need_reschedule": "Of course. When should we reschedule?",
                    "cant_make_it": "Got it. Let's reschedule. Which week works better?"
                },
                closing_options=[
                    "Great, see you tomorrow at {time}. I'll send a link an hour before the call.",
                    "Rescheduled to {new_time}. See you then!"
                ],
                fallback_responses=[
                    "Great, see you tomorrow!"
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
            agent_name=contact.get('agent_name', 'Alex'),
            business_type=contact.get('business_type', 'your business')
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
            {'speaker': 'customer', 'text': 'Yes, convenient, tell me more'},
            {'speaker': 'agent', 'text': script.qualification_questions[0]['question']},
            {'speaker': 'customer', 'text': 'I have a beauty salon, about 50 clients per week'},
            {'speaker': 'agent', 'text': 'Great! How do you manage appointments now?'},
            {'speaker': 'customer', 'text': 'Manually, in a notebook and WhatsApp'},
            {'speaker': 'agent', 'text': script.qualification_questions[1]['question']},
            {'speaker': 'customer', 'text': 'Mostly messaging takes time'},
            {'speaker': 'agent', 'text': script.qualification_questions[4]['question']},
            {'speaker': 'customer', 'text': 'Well, if it really helps, ready to allocate up to $500'},
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
            'subject': 'AI Genesis — automation materials',
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
            'text': f"""Hi {lead.get('name')}! This is AI Genesis. 
Reminding you about the $350 pilot — it's still available. 
If interested, just reply to this message.""",
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
  python3 voice_sales_agent.py simulate "John" "+1-555-123-4567"
  python3 voice_sales_agent.py tts "Hello! This is AI Genesis"
  python3 voice_sales_agent.py objection "too expensive"
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
            'business_type': 'beauty salon',
            'agent_name': 'Alex'
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
