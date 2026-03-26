"""
Google Sheets CRM v2.0 — Anti-CRM for Human Relationships
Not your typical sales pipeline. We track emotions, not deals.
"""

import os
import json
import re
import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from enum import Enum
import random

# Optional imports for enhanced features
try:
    import gspread
    from google.oauth2.service_account import Credentials
    GOOGLE_AVAILABLE = True
except ImportError:
    GOOGLE_AVAILABLE = False


class EmotionalState(Enum):
    """7 emotional states of a lead journey"""
    CURIOUS = "curious"      # Just discovered, exploring
    EXCITED = "excited"      # Interested, enthusiastic
    CONCERNED = "concerned"  # Has objections, hesitating
    CONFIDENT = "confident"  # Trusts, evaluating options
    COMMITTED = "committed"  # Decided to buy
    CHAMPION = "champion"    # Bought, advocates for you
    DORMANT = "dormant"      # Silent, needs reactivation


class SignalType(Enum):
    """Visual signals for quick understanding"""
    ALARM = "🚨"      # Needs immediate attention
    INSIGHT = "💡"    # Opportunity discovered
    WIN = "🎉"        # Positive development
    RISK = "⚠️"       # Potential problem
    FIRE = "🔥"       # Hot momentum
    ICE = "❄️"        # Cooling down


@dataclass
class RelationshipMetrics:
    """Dynamic relationship health metrics"""
    temperature: float  # 0-100°
    temperature_trend: str  # "rising" | "stable" | "falling"
    velocity: float  # messages per day
    reciprocity: float  # 0-1, how balanced is communication
    engagement_depth: int  # 1-5, quality of interactions
    last_response_time: Optional[int]  # minutes
    
    def get_signal(self) -> SignalType:
        """Generate signal based on metrics"""
        if self.temperature >= 80 and self.temperature_trend == "rising":
            return SignalType.FIRE
        elif self.temperature <= 30:
            return SignalType.ICE
        elif self.last_response_time and self.last_response_time > 10080:  # 7 days
            return SignalType.ALARM
        elif self.reciprocity < 0.3:
            return SignalType.RISK
        elif self.engagement_depth >= 4:
            return SignalType.WIN
        else:
            return SignalType.INSIGHT


@dataclass
class TriggerEvent:
    """Personal trigger events for meaningful outreach"""
    type: str  # "birthday", "business_anniversary", "holiday", "custom"
    date: str
    description: str
    notified: bool = False
    
    def is_upcoming(self, days: int = 7) -> bool:
        event_date = datetime.fromisoformat(self.date)
        now = datetime.now()
        # Handle recurring dates (birthdays)
        if self.type == "birthday":
            event_date = event_date.replace(year=now.year)
            if event_date < now:
                event_date = event_date.replace(year=now.year + 1)
        return 0 <= (event_date - now).days <= days


@dataclass
class SmartCadence:
    """AI-generated follow-up schedule"""
    next_contact: str  # ISO date
    reason: str  # Why this specific time
    channel: str  # telegram, email, call
    message_tone: str  # friendly, professional, urgent
    personal_hook: Optional[str]  # Reference to previous conversation
    
    @classmethod
    def generate(cls, lead: 'LeadProfile') -> 'SmartCadence':
        """Generate personalized cadence based on lead behavior"""
        metrics = lead.relationship_metrics
        
        # Determine timing based on engagement
        if metrics.velocity > 5:  # Very active
            days = 1
            reason = "High engagement — strike while hot"
            tone = "friendly"
        elif metrics.temperature >= 70:
            days = 2
            reason = "Warm lead, maintain momentum"
            tone = "professional"
        elif metrics.last_response_time and metrics.last_response_time > 2880:  # 2 days
            days = 1
            reason = "Re-engagement needed"
            tone = "urgent"
        else:
            days = 3
            reason = "Standard follow-up"
            tone = "professional"
        
        next_date = (datetime.now() + timedelta(days=days)).isoformat()
        
        # Choose channel
        if lead.preferred_channel:
            channel = lead.preferred_channel
        elif metrics.engagement_depth >= 3:
            channel = "call"  # Escalate to call for engaged leads
        else:
            channel = "telegram"
        
        # Personal hook from conversation memory
        hook = None
        if lead.conversation_memory:
            recent = lead.conversation_memory[-1] if lead.conversation_memory else None
            if recent:
                hook = f"Last time you mentioned: {recent.get('topic', 'your interest')}"
        
        return cls(
            next_contact=next_date,
            reason=reason,
            channel=channel,
            message_tone=tone,
            personal_hook=hook
        )


@dataclass
class LeadProfile:
    """Complete lead profile — the Anti-CRM way"""
    id: str
    created_at: str
    
    # Identity
    name: str
    phone: Optional[str]
    email: Optional[str]
    company: Optional[str]
    timezone: str = "UTC"
    language: str = "en"
    
    # Emotional State (not status!)
    emotional_state: EmotionalState = EmotionalState.CURIOUS
    state_history: List[Dict] = None  # Track emotional journey
    
    # Relationship Metrics (dynamic)
    relationship_metrics: RelationshipMetrics = None
    
    # Trigger Events
    trigger_events: List[TriggerEvent] = None
    
    # Conversation Memory (full context)
    conversation_memory: List[Dict] = None
    
    # Buying Intent
    buying_intent_score: float = 0.0  # 0-100, ML-calculated
    intent_factors: Dict[str, float] = None  # What drives the score
    
    # Smart Cadence
    smart_cadence: SmartCadence = None
    
    # Mutual Action Plan
    mutual_plan: List[Dict] = None  # Shared commitments
    
    # Preferences
    preferred_channel: Optional[str] = None
    communication_style: str = "balanced"  # formal, casual, technical
    
    # Signals
    active_signals: List[SignalType] = None
    
    def __post_init__(self):
        if self.state_history is None:
            self.state_history = []
        if self.relationship_metrics is None:
            self.relationship_metrics = RelationshipMetrics(
                temperature=50.0,
                temperature_trend="stable",
                velocity=0.0,
                reciprocity=0.5,
                engagement_depth=1,
                last_response_time=None
            )
        if self.trigger_events is None:
            self.trigger_events = []
        if self.conversation_memory is None:
            self.conversation_memory = []
        if self.intent_factors is None:
            self.intent_factors = {}
        if self.mutual_plan is None:
            self.mutual_plan = []
        if self.active_signals is None:
            self.active_signals = []
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for storage"""
        return {
            'id': self.id,
            'created_at': self.created_at,
            'name': self.name,
            'phone': self.phone,
            'email': self.email,
            'company': self.company,
            'timezone': self.timezone,
            'language': self.language,
            'emotional_state': self.emotional_state.value,
            'state_history': self.state_history,
            'relationship_metrics': asdict(self.relationship_metrics),
            'trigger_events': [asdict(te) for te in self.trigger_events],
            'conversation_memory': self.conversation_memory,
            'buying_intent_score': self.buying_intent_score,
            'intent_factors': self.intent_factors,
            'smart_cadence': asdict(self.smart_cadence) if self.smart_cadence else None,
            'mutual_plan': self.mutual_plan,
            'preferred_channel': self.preferred_channel,
            'communication_style': self.communication_style,
            'active_signals': [s.value for s in self.active_signals]
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'LeadProfile':
        """Create from dictionary"""
        # Reconstruct complex objects
        metrics = RelationshipMetrics(**data.get('relationship_metrics', {}))
        triggers = [TriggerEvent(**te) for te in data.get('trigger_events', [])]
        cadence = SmartCadence(**data['smart_cadence']) if data.get('smart_cadence') else None
        signals = [SignalType(s) for s in data.get('active_signals', [])]
        
        return cls(
            id=data['id'],
            created_at=data['created_at'],
            name=data['name'],
            phone=data.get('phone'),
            email=data.get('email'),
            company=data.get('company'),
            timezone=data.get('timezone', 'UTC'),
            language=data.get('language', 'en'),
            emotional_state=EmotionalState(data.get('emotional_state', 'curious')),
            state_history=data.get('state_history', []),
            relationship_metrics=metrics,
            trigger_events=triggers,
            conversation_memory=data.get('conversation_memory', []),
            buying_intent_score=data.get('buying_intent_score', 0.0),
            intent_factors=data.get('intent_factors', {}),
            smart_cadence=cadence,
            mutual_plan=data.get('mutual_plan', []),
            preferred_channel=data.get('preferred_channel'),
            communication_style=data.get('communication_style', 'balanced'),
            active_signals=signals
        )


class BuyingIntentCalculator:
    """Calculate buying intent based on behavior patterns"""
    
    FACTORS = {
        'response_speed': 0.20,      # Fast responses = high intent
        'question_depth': 0.15,      # Asking detailed questions
        'price_inquiry': 0.20,       # Asked about pricing
        'timeframe_mention': 0.15,   # Mentioned timeline
        'stakeholder_involvement': 0.15,  # Involved others
        'engagement_consistency': 0.15    # Regular engagement
    }
    
    @classmethod
    def calculate(cls, lead: LeadProfile) -> Tuple[float, Dict[str, float]]:
        """Return intent score (0-100) and factor breakdown"""
        factors = {}
        
        # Response speed factor
        metrics = lead.relationship_metrics
        if metrics.last_response_time:
            if metrics.last_response_time < 60:  # Under 1 hour
                factors['response_speed'] = 100
            elif metrics.last_response_time < 240:  # Under 4 hours
                factors['response_speed'] = 80
            elif metrics.last_response_time < 1440:  # Under 24 hours
                factors['response_speed'] = 60
            else:
                factors['response_speed'] = 30
        else:
            factors['response_speed'] = 0
        
        # Question depth from conversation memory
        depth_score = 0
        for conv in lead.conversation_memory[-5:]:  # Last 5 conversations
            text = conv.get('text', '').lower()
            if any(w in text for w in ['how', 'what', 'when', 'why', 'can you', 'explain']):
                depth_score += 20
        factors['question_depth'] = min(100, depth_score)
        
        # Price inquiry
        price_mentioned = any(
            'price' in conv.get('text', '').lower() or
            'cost' in conv.get('text', '').lower() or
            'budget' in conv.get('text', '').lower()
            for conv in lead.conversation_memory
        )
        factors['price_inquiry'] = 100 if price_mentioned else 20
        
        # Timeframe mention
        timeframe_words = ['this week', 'next week', 'asap', 'soon', 'urgent', 'fast', 'this month']
        timeframe_mentioned = any(
            any(w in conv.get('text', '').lower() for w in timeframe_words)
            for conv in lead.conversation_memory
        )
        factors['timeframe_mention'] = 100 if timeframe_mentioned else 30
        
        # Stakeholder involvement
        stakeholder_words = ['team', 'partner', 'boss', 'colleague', 'wife', 'husband', 'my']
        stakeholders_mentioned = any(
            any(w in conv.get('text', '').lower() for w in stakeholder_words)
            for conv in lead.conversation_memory
        )
        factors['stakeholder_involvement'] = 100 if stakeholders_mentioned else 40
        
        # Engagement consistency
        if len(lead.conversation_memory) >= 3:
            factors['engagement_consistency'] = 90
        elif len(lead.conversation_memory) >= 2:
            factors['engagement_consistency'] = 70
        else:
            factors['engagement_consistency'] = 40
        
        # Calculate weighted score
        total_score = sum(
            factors[factor] * weight
            for factor, weight in cls.FACTORS.items()
        )
        
        return round(total_score), factors


class EmotionalStateTracker:
    """Track and predict emotional state changes"""
    
    TRANSITIONS = {
        EmotionalState.CURIOUS: [EmotionalState.EXCITED, EmotionalState.CONCERNED, EmotionalState.DORMANT],
        EmotionalState.EXCITED: [EmotionalState.CONFIDENT, EmotionalState.CONCERNED, EmotionalState.COMMITTED],
        EmotionalState.CONCERNED: [EmotionalState.CONFIDENT, EmotionalState.DORMANT],
        EmotionalState.CONFIDENT: [EmotionalState.COMMITTED, EmotionalState.CONCERNED],
        EmotionalState.COMMITTED: [EmotionalState.CHAMPION, EmotionalState.CONCERNED],
        EmotionalState.CHAMPION: [EmotionalState.CHAMPION],
        EmotionalState.DORMANT: [EmotionalState.CURIOUS]
    }
    
    @classmethod
    def detect_state_change(cls, lead: LeadProfile, message_text: str) -> Optional[EmotionalState]:
        """Detect if message indicates emotional state change"""
        text_lower = message_text.lower()
        current = lead.emotional_state
        
        # Excitement indicators
        if any(w in text_lower for w in ['amazing', 'perfect', 'love it', 'great', 'awesome', 'wow', '🔥']):
            if EmotionalState.EXCITED in cls.TRANSITIONS.get(current, []):
                return EmotionalState.EXCITED
        
        # Concern indicators
        if any(w in text_lower for w in ['expensive', 'too much', 'not sure', 'hesitant', 'but', 'however']):
            if EmotionalState.CONCERNED in cls.TRANSITIONS.get(current, []):
                return EmotionalState.CONCERNED
        
        # Commitment indicators
        if any(w in text_lower for w in ['lets do it', 'sign me up', 'ready to buy', 'go ahead', 'ready', 'when can we start']):
            if EmotionalState.COMMITTED in cls.TRANSITIONS.get(current, []):
                return EmotionalState.COMMITTED
        
        # Dormant indicators
        if any(w in text_lower for w in ['not now', 'later', 'maybe next year', 'postpone', 'not yet']):
            return EmotionalState.DORMANT
        
        return None


class GoogleSheetsCRMV2:
    """Anti-CRM v2.0 — For human relationships, not deals"""
    
    def __init__(self, credentials_path: Optional[str] = None):
        self.credentials_path = credentials_path or os.getenv(
            'GOOGLE_SHEETS_CREDENTIALS',
            '/root/.openclaw/config/google-sheets-credentials.json'
        )
        self.spreadsheet_id = os.getenv('CRM_SPREADSHEET_ID')
        self.client = None
        self.leads_sheet = None
        self.analytics_sheet = None
        self._local_storage = '/tmp/crm_v2_local.json'
        self._connect()
    
    def _connect(self):
        """Connect to Google Sheets"""
        if not GOOGLE_AVAILABLE:
            print("⚠️  gspread not available, using local mode")
            return
        
        try:
            credentials = Credentials.from_service_account_file(
                self.credentials_path,
                scopes=['https://www.googleapis.com/auth/spreadsheets', 
                        'https://www.googleapis.com/auth/drive']
            )
            self.client = gspread.authorize(credentials)
            
            if self.spreadsheet_id:
                spreadsheet = self.client.open_by_key(self.spreadsheet_id)
            else:
                spreadsheet = self.client.create('AI Genesis CRM v2.0')
                self.spreadsheet_id = spreadsheet.id
                self._init_structure(spreadsheet)
                print(f"✅ Created new CRM: {spreadsheet.url}")
            
            self.leads_sheet = spreadsheet.worksheet('Leads')
            self.analytics_sheet = spreadsheet.worksheet('Analytics')
            
        except Exception as e:
            print(f"⚠️  Connection error: {e}, using local mode")
            self.client = None
    
    def _init_structure(self, spreadsheet):
        """Initialize v2.0 structure"""
        # Leads sheet with Anti-CRM columns
        leads = spreadsheet.add_worksheet('Leads', 1000, 25)
        headers = [
            'ID', 'Created', 'Name', 'Phone', 'Email', 'Company',
            'Emotional State', 'Temperature', 'Temp Trend', 'Velocity',
            'Intent Score', 'Next Contact', 'Contact Reason', 'Channel',
            'Timezone', 'Language', 'Signals', 'Last Contact',
            'Trigger Events', 'Mutual Plan', 'Conversation Summary'
        ]
        leads.append_row(headers)
        
        # Analytics sheet
        analytics = spreadsheet.add_worksheet('Analytics', 50, 10)
        analytics.append_row(['Metric', 'Value', 'Last Updated'])
        analytics.append_row(['Active Leads', '0', datetime.now().isoformat()])
        analytics.append_row(['Avg Temperature', '50', datetime.now().isoformat()])
        analytics.append_row(['Hot Leads (80°+)', '0', datetime.now().isoformat()])
    
    def add_lead(self, profile: LeadProfile) -> Dict:
        """Add new lead with Anti-CRM intelligence"""
        
        # Check for duplicates
        is_dup, existing = self._check_duplicate(profile.phone, profile.email)
        if is_dup:
            return {
                'success': False,
                'duplicate': True,
                'message': f'⚠️ Already connected with {existing.get("name", "someone")}',
                'existing_id': existing.get('id')
            }
        
        # Calculate buying intent
        intent_score, factors = BuyingIntentCalculator.calculate(profile)
        profile.buying_intent_score = intent_score
        profile.intent_factors = factors
        
        # Generate smart cadence
        profile.smart_cadence = SmartCadence.generate(profile)
        
        # Determine active signals
        profile.active_signals = [profile.relationship_metrics.get_signal()]
        
        # Save
        if self.client:
            try:
                row = [
                    profile.id,
                    profile.created_at,
                    profile.name,
                    profile.phone or '',
                    profile.email or '',
                    profile.company or '',
                    profile.emotional_state.value,
                    profile.relationship_metrics.temperature,
                    profile.relationship_metrics.temperature_trend,
                    profile.relationship_metrics.velocity,
                    profile.buying_intent_score,
                    profile.smart_cadence.next_contact if profile.smart_cadence else '',
                    profile.smart_cadence.reason if profile.smart_cadence else '',
                    profile.smart_cadence.channel if profile.smart_cadence else '',
                    profile.timezone,
                    profile.language,
                    ', '.join([s.value for s in profile.active_signals]),
                    datetime.now().isoformat(),
                    json.dumps([asdict(te) for te in profile.trigger_events]),
                    json.dumps(profile.mutual_plan),
                    profile.conversation_memory[-1].get('summary', '') if profile.conversation_memory else ''
                ]
                self.leads_sheet.append_row(row)
            except Exception as e:
                print(f"⚠️ Sheets error: {e}, using local storage")
                self._save_local(profile)
        else:
            self._save_local(profile)
        
        # Generate welcome message
        signal = profile.active_signals[0].value if profile.active_signals else '💡'
        
        return {
            'success': True,
            'message': f'{signal} Added {profile.name} to your relationship map',
            'lead_id': profile.id,
            'emotional_state': profile.emotional_state.value,
            'temperature': f"{profile.relationship_metrics.temperature}°",
            'intent_score': f"{profile.buying_intent_score}/100",
            'next_contact': {
                'when': profile.smart_cadence.next_contact[:10] if profile.smart_cadence else None,
                'why': profile.smart_cadence.reason if profile.smart_cadence else None,
                'how': profile.smart_cadence.channel if profile.smart_cadence else None
            },
            'signals': [s.value for s in profile.active_signals]
        }
    
    def _check_duplicate(self, phone: Optional[str], email: Optional[str]) -> Tuple[bool, Optional[Dict]]:
        """Check for existing lead"""
        if not self.client:
            if os.path.exists(self._local_storage):
                with open(self._local_storage, 'r') as f:
                    leads = json.load(f)
                    for lead in leads:
                        if phone and lead.get('phone') == phone:
                            return True, lead
                        if email and lead.get('email') == email:
                            return True, lead
            return False, None
        
        try:
            all_leads = self.leads_sheet.get_all_records()
            for lead in all_leads:
                if phone and lead.get('Phone') == phone:
                    return True, lead
                if email and lead.get('Email') == email:
                    return True, lead
            return False, None
        except:
            return False, None
    
    def _save_local(self, profile: LeadProfile):
        """Save to local fallback"""
        leads = []
        if os.path.exists(self._local_storage):
            with open(self._local_storage, 'r') as f:
                leads = json.load(f)
        leads.append(profile.to_dict())
        with open(self._local_storage, 'w') as f:
            json.dump(leads, f, indent=2)
    
    def get_relationship_dashboard(self) -> Dict:
        """Get Anti-CRM dashboard"""
        leads = self._get_all_leads()
        
        # Calculate metrics
        temps = [l.relationship_metrics.temperature for l in leads]
        avg_temp = sum(temps) / len(temps) if temps else 0
        hot_count = sum(1 for t in temps if t >= 80)
        cold_count = sum(1 for t in temps if t <= 30)
        
        # Group by emotional state
        states = {}
        for lead in leads:
            state = lead.emotional_state.value
            states[state] = states.get(state, 0) + 1
        
        # Upcoming triggers
        upcoming_triggers = []
        for lead in leads:
            for trigger in lead.trigger_events:
                if trigger.is_upcoming(7):
                    upcoming_triggers.append({
                        'lead': lead.name,
                        'event': trigger.description,
                        'date': trigger.date[:10]
                    })
        
        return {
            'total_relationships': len(leads),
            'avg_temperature': round(avg_temp, 1),
            'hot_relationships': hot_count,
            'cold_relationships': cold_count,
            'emotional_states': states,
            'upcoming_triggers': sorted(upcoming_triggers, key=lambda x: x['date'])[:5],
            'needing_attention': [
                {'name': l.name, 'signal': l.active_signals[0].value if l.active_signals else '💡'}
                for l in leads
                if l.relationship_metrics.temperature < 40 or 
                   (l.relationship_metrics.last_response_time and l.relationship_metrics.last_response_time > 2880)
            ][:5]
        }
    
    def _get_all_leads(self) -> List[LeadProfile]:
        """Get all leads as profiles"""
        if not self.client:
            if os.path.exists(self._local_storage):
                with open(self._local_storage, 'r') as f:
                    return [LeadProfile.from_dict(d) for d in json.load(f)]
            return []
        
        try:
            records = self.leads_sheet.get_all_records()
            profiles = []
            for record in records:
                # Convert record to LeadProfile
                profile = LeadProfile(
                    id=record.get('ID', ''),
                    created_at=record.get('Created', ''),
                    name=record.get('Name', ''),
                    phone=record.get('Phone') or None,
                    email=record.get('Email') or None,
                    company=record.get('Company') or None,
                    timezone=record.get('Timezone', 'UTC'),
                    language=record.get('Language', 'en'),
                    emotional_state=EmotionalState(record.get('Emotional State', 'curious')),
                    buying_intent_score=float(record.get('Intent Score', 0))
                )
                profiles.append(profile)
            return profiles
        except:
            return []


def extract_lead_v2(text: str, source: str = "telegram") -> LeadProfile:
    """Extract lead with Anti-CRM intelligence"""
    import re
    
    # Basic extraction
    name = "Unknown"
    phone = None
    email = None
    company = None
    
    # Extract phone
    phone_match = re.search(r'\+?\d[\d\s\-\(\)]{7,}\d', text)
    if phone_match:
        phone = phone_match.group().replace(' ', '').replace('-', '').replace('(', '').replace(')', '')
    
    # Extract email
    email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text)
    if email_match:
        email = email_match.group()
    
    # Extract name (first 2-3 words)
    words = text.split()[:3]
    if words:
        name = ' '.join(words)
    
    # Create profile
    profile = LeadProfile(
        id=f"RL{datetime.now().strftime('%Y%m%d%H%M%S')}",  # RL = Relationship Lead
        created_at=datetime.now().isoformat(),
        name=name,
        phone=phone,
        email=email,
        company=company,
        conversation_memory=[{
            'date': datetime.now().isoformat(),
            'text': text,
            'summary': text[:100] + '...' if len(text) > 100 else text
        }]
    )
    
    # Detect emotional state from first message
    text_lower = text.lower()
    if any(w in text_lower for w in ['interested', 'want', 'love', 'like']):
        profile.emotional_state = EmotionalState.EXCITED
    elif any(w in text_lower for w in ['expensive', 'not sure', 'hesitant', 'maybe']):
        profile.emotional_state = EmotionalState.CONCERNED
    
    # Set initial temperature based on state
    if profile.emotional_state == EmotionalState.EXCITED:
        profile.relationship_metrics.temperature = 70.0
    elif profile.emotional_state == EmotionalState.CONCERNED:
        profile.relationship_metrics.temperature = 40.0
    
    return profile


# CLI Interface
def main():
    import sys
    
    crm = GoogleSheetsCRMV2()
    
    if len(sys.argv) < 2:
        print("""
🚀 Google Sheets CRM v2.0 — Anti-CRM for Human Relationships

Commands:
  add "text"              Add new relationship
  dashboard               Show relationship dashboard  
  hot                     Show hot relationships (80°+)
  cold                    Show relationships needing warmth
  signals                 Show all active signals

Examples:
  python crm_v2.py add "Anna, +1 555 123-45-67, interested in automation"
  python crm_v2.py dashboard
        """)
        return
    
    command = sys.argv[1]
    
    if command == 'add':
        if len(sys.argv) < 3:
            print("❌ Please provide text with contact info")
            return
        
        text = sys.argv[2]
        profile = extract_lead_v2(text)
        result = crm.add_lead(profile)
        
        print(f"\n{result['message']}")
        if result['success']:
            print(f"\n📊 Relationship Profile:")
            print(f"   Emotional State: {result['emotional_state']}")
            print(f"   Temperature: {result['temperature']}")
            print(f"   Buying Intent: {result['intent_score']}")
            if result['next_contact']['when']:
                print(f"\n📅 Suggested Next Contact:")
                print(f"   When: {result['next_contact']['when']}")
                print(f"   Why: {result['next_contact']['why']}")
                print(f"   Channel: {result['next_contact']['how']}")
    
    elif command == 'dashboard':
        dashboard = crm.get_relationship_dashboard()
        
        print("\n📊 Relationship Dashboard")
        print(f"   Total Relationships: {dashboard['total_relationships']}")
        print(f"   Average Temperature: {dashboard['avg_temperature']}°")
        print(f"   🔥 Hot ({dashboard['hot_relationships']}) | ❄️ Cold ({dashboard['cold_relationships']})")
        
        if dashboard['emotional_states']:
            print(f"\n💭 Emotional States:")
            for state, count in dashboard['emotional_states'].items():
                print(f"   {state}: {count}")
        
        if dashboard['upcoming_triggers']:
            print(f"\n🎉 Upcoming Events:")
            for trigger in dashboard['upcoming_triggers']:
                print(f"   {trigger['date']}: {trigger['lead']} — {trigger['event']}")
        
        if dashboard['needing_attention']:
            print(f"\n🚨 Need Attention:")
            for item in dashboard['needing_attention']:
                print(f"   {item['signal']} {item['name']}")
    
    elif command == 'hot':
        leads = crm._get_all_leads()
        hot = [l for l in leads if l.relationship_metrics.temperature >= 80]
        
        print(f"\n🔥 Hot Relationships ({len(hot)}):")
        for lead in hot:
            print(f"   {lead.name} | {lead.relationship_metrics.temperature}° | Intent: {lead.buying_intent_score}/100")
    
    elif command == 'cold':
        leads = crm._get_all_leads()
        cold = [l for l in leads if l.relationship_metrics.temperature <= 30]
        
        print(f"\n❄️ Cold Relationships ({len(cold)}):")
        for lead in cold:
            print(f"   {lead.name} | {lead.relationship_metrics.temperature}° | State: {lead.emotional_state.value}")
    
    else:
        print(f"❌ Unknown command: {command}")


if __name__ == '__main__':
    main()
