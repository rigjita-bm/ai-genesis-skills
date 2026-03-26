"""
Google Sheets CRM Skill
Lead management with deduplication and automated follow-ups
"""

import os
import json
import gspread
from datetime import datetime, timedelta
from google.oauth2.service_account import Credentials
from typing import Dict, List, Optional, Tuple


class GoogleSheetsCRM:
    """CRM system using Google Sheets as backend"""
    
    SCOPES = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]
    
    def __init__(self, credentials_path: Optional[str] = None):
        self.credentials_path = credentials_path or os.getenv(
            'GOOGLE_SHEETS_CREDENTIALS',
            '/root/.openclaw/config/google-sheets-credentials.json'
        )
        self.spreadsheet_id = os.getenv(
            'CRM_SPREADSHEET_ID',
            '1CRM_DEFAULT_SPREADSHEET_ID'
        )
        self.client = None
        self.sheet = None
        self._connect()
    
    def _connect(self):
        """Connect to Google Sheets API"""
        try:
            credentials = Credentials.from_service_account_file(
                self.credentials_path,
                scopes=self.SCOPES
            )
            self.client = gspread.authorize(credentials)
            
            # Open spreadsheet or create new
            try:
                spreadsheet = self.client.open_by_key(self.spreadsheet_id)
            except gspread.exceptions.SpreadsheetNotFound:
                spreadsheet = self.client.create('AI Genesis CRM')
                self.spreadsheet_id = spreadsheet.id
                self._init_structure(spreadsheet)
            
            self.sheet = spreadsheet.worksheet('Leads')
            
        except Exception as e:
            print(f"CRM Connection Error: {e}")
            # Fallback to local storage
            self.client = None
    
    def _init_structure(self, spreadsheet):
        """Initialize CRM spreadsheet structure"""
        # Leads worksheet
        leads_sheet = spreadsheet.add_worksheet('Leads', 1000, 20)
        headers = [
            'ID', 'Date Added', 'Source', 'Name', 'Phone', 'Email',
            'Company', 'Status', 'Priority', 'Last Contact', 'Notes',
            'Follow-up 24h', 'Follow-up 72h', 'Follow-up 7d', 'Owner Notified'
        ]
        leads_sheet.append_row(headers)
        
        # Settings worksheet
        settings_sheet = spreadsheet.add_worksheet('Settings', 10, 2)
        settings_sheet.append_row(['Key', 'Value'])
        settings_sheet.append_row(['Created', datetime.now().isoformat()])
        settings_sheet.append_row(['Owner Email', ''])
    
    def _get_local_storage(self) -> str:
        """Get path to local fallback storage"""
        return '/tmp/crm_local_backup.json'
    
    def _save_local(self, lead: Dict):
        """Save lead to local fallback storage"""
        storage_path = self._get_local_storage()
        leads = []
        
        if os.path.exists(storage_path):
            with open(storage_path, 'r') as f:
                leads = json.load(f)
        
        leads.append(lead)
        
        with open(storage_path, 'w') as f:
            json.dump(leads, f, indent=2)
    
    def check_duplicate(self, phone: Optional[str] = None, email: Optional[str] = None) -> Tuple[bool, Optional[Dict]]:
        """Check if lead already exists by phone or email"""
        if not self.client:
            # Check local storage
            storage_path = self._get_local_storage()
            if os.path.exists(storage_path):
                with open(storage_path, 'r') as f:
                    leads = json.load(f)
                    for lead in leads:
                        if phone and lead.get('phone') == phone:
                            return True, lead
                        if email and lead.get('email') == email:
                            return True, lead
            return False, None
        
        try:
            all_leads = self.sheet.get_all_records()
            for lead in all_leads:
                if phone and lead.get('Phone') == phone:
                    return True, lead
                if email and lead.get('Email') == email:
                    return True, lead
            return False, None
        except Exception as e:
            print(f"Duplicate check error: {e}")
            return False, None
    
    def add_lead(self, lead_data: Dict) -> Dict:
        """Add new lead with deduplication check"""
        
        # Normalize data
        phone = lead_data.get('phone', '').strip()
        email = lead_data.get('email', '').lower().strip()
        
        # Check for duplicates
        is_duplicate, existing = self.check_duplicate(phone, email)
        
        if is_duplicate:
            return {
                'success': False,
                'duplicate': True,
                'message': f'⚠️ Лид уже существует (добавлен {existing.get("Date Added", "ранее")})',
                'existing': existing
            }
        
        # Prepare lead data
        lead_id = f"LD{datetime.now().strftime('%Y%m%d%H%M%S')}"
        now = datetime.now()
        
        lead_record = {
            'id': lead_id,
            'date_added': now.isoformat(),
            'source': lead_data.get('source', 'telegram'),
            'name': lead_data.get('name', ''),
            'phone': phone,
            'email': email,
            'company': lead_data.get('company', ''),
            'status': lead_data.get('status', 'NEW'),
            'priority': lead_data.get('priority', '🟡 WARM'),
            'last_contact': now.isoformat(),
            'notes': lead_data.get('notes', ''),
            'followup_24h': (now + timedelta(hours=24)).isoformat(),
            'followup_72h': (now + timedelta(hours=72)).isoformat(),
            'followup_7d': (now + timedelta(days=7)).isoformat(),
            'owner_notified': 'No'
        }
        
        # Save to Google Sheets
        if self.client:
            try:
                row = [
                    lead_id,
                    lead_record['date_added'],
                    lead_record['source'],
                    lead_record['name'],
                    phone,
                    email,
                    lead_record['company'],
                    lead_record['status'],
                    lead_record['priority'],
                    lead_record['last_contact'],
                    lead_record['notes'],
                    lead_record['followup_24h'],
                    lead_record['followup_72h'],
                    lead_record['followup_7d'],
                    lead_record['owner_notified']
                ]
                self.sheet.append_row(row)
            except Exception as e:
                print(f"Sheets save error: {e}, using local backup")
                self._save_local(lead_record)
        else:
            self._save_local(lead_record)
        
        # Schedule follow-ups via cron
        self._schedule_followups(lead_id, lead_record)
        
        return {
            'success': True,
            'duplicate': False,
            'message': f'✅ Лид сохранён! ID: {lead_id}',
            'lead': lead_record,
            'next_actions': [
                f'+24ч: Проверка вопросов ({lead_record["followup_24h"][:16]})',
                f'+72ч: Полезный факт ({lead_record["followup_72h"][:16]})',
                f'+7дн: Финальное сообщение ({lead_record["followup_7d"][:16]})'
            ]
        }
    
    def _schedule_followups(self, lead_id: str, lead: Dict):
        """Schedule automated follow-ups via cron"""
        try:
            from cron import add_job
            
            # 24h follow-up
            add_job(
                time=lead['followup_24h'],
                message=f'Follow-up 24h for lead {lead_id}: {lead["name"]}',
                tag=f'crm_followup_24h_{lead_id}'
            )
            
            # 72h follow-up
            add_job(
                time=lead['followup_72h'],
                message=f'Follow-up 72h for lead {lead_id}: {lead["name"]}',
                tag=f'crm_followup_72h_{lead_id}'
            )
            
            # 7d follow-up
            add_job(
                time=lead['followup_7d'],
                message=f'Follow-up 7d for lead {lead_id}: {lead["name"]}',
                tag=f'crm_followup_7d_{lead_id}'
            )
            
        except Exception as e:
            print(f"Cron scheduling error: {e}")
    
    def get_hot_leads(self) -> List[Dict]:
        """Get all HOT priority leads"""
        if not self.client:
            storage_path = self._get_local_storage()
            if os.path.exists(storage_path):
                with open(storage_path, 'r') as f:
                    leads = json.load(f)
                    return [l for l in leads if '🔴' in l.get('priority', '')]
            return []
        
        try:
            all_leads = self.sheet.get_all_records()
            hot_leads = [l for l in all_leads if '🔴' in str(l.get('Priority', ''))]
            return hot_leads
        except Exception as e:
            print(f"Get hot leads error: {e}")
            return []
    
    def update_lead(self, lead_id: str, updates: Dict) -> Dict:
        """Update existing lead"""
        if not self.client:
            return {'success': False, 'message': 'Local mode - updates not supported'}
        
        try:
            # Find lead row
            cell = self.sheet.find(lead_id)
            if cell:
                row = cell.row
                # Update fields
                if 'status' in updates:
                    self.sheet.update_cell(row, 8, updates['status'])
                if 'priority' in updates:
                    self.sheet.update_cell(row, 9, updates['priority'])
                if 'notes' in updates:
                    self.sheet.update_cell(row, 11, updates['notes'])
                if 'last_contact' in updates:
                    self.sheet.update_cell(row, 10, updates['last_contact'])
                
                return {'success': True, 'message': f'✅ Лид {lead_id} обновлён'}
            else:
                return {'success': False, 'message': f'⚠️ Лид {lead_id} не найден'}
        except Exception as e:
            return {'success': False, 'message': f'❌ Ошибка: {e}'}
    
    def get_pending_followups(self) -> List[Dict]:
        """Get leads with pending follow-ups"""
        now = datetime.now()
        
        if not self.client:
            storage_path = self._get_local_storage()
            if os.path.exists(storage_path):
                with open(storage_path, 'r') as f:
                    leads = json.load(f)
                    pending = []
                    for lead in leads:
                        fu_24h = datetime.fromisoformat(lead.get('followup_24h', '2000-01-01'))
                        fu_72h = datetime.fromisoformat(lead.get('followup_72h', '2000-01-01'))
                        fu_7d = datetime.fromisoformat(lead.get('followup_7d', '2000-01-01'))
                        
                        if fu_24h <= now or fu_72h <= now or fu_7d <= now:
                            pending.append(lead)
                    return pending
            return []
        
        try:
            all_leads = self.sheet.get_all_records()
            pending = []
            for lead in all_leads:
                fu_24h = datetime.fromisoformat(lead.get('Follow-up 24h', '2000-01-01'))
                fu_72h = datetime.fromisoformat(lead.get('Follow-up 72h', '2000-01-01'))
                fu_7d = datetime.fromisoformat(lead.get('Follow-up 7d', '2000-01-01'))
                
                if fu_24h <= now or fu_72h <= now or fu_7d <= now:
                    pending.append(lead)
            return pending
        except Exception as e:
            print(f"Get pending followups error: {e}")
            return []


def extract_lead_info(text: str) -> Dict:
    """Extract lead information from message text"""
    import re
    
    lead = {
        'name': '',
        'phone': '',
        'email': '',
        'company': '',
        'notes': text
    }
    
    # Extract phone (Russian and international formats)
    phone_patterns = [
        r'\+7\s?\(?\d{3}\)?\s?\d{3}[-.\s]?\d{2}[-.\s]?\d{2}',  # +7 (XXX) XXX-XX-XX
        r'8\s?\(?\d{3}\)?\s?\d{3}[-.\s]?\d{2}[-.\s]?\d{2}',     # 8 (XXX) XXX-XX-XX
        r'\+?\d{1,3}[-.\s]?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}' # International
    ]
    
    for pattern in phone_patterns:
        match = re.search(pattern, text)
        if match:
            lead['phone'] = match.group().replace(' ', '').replace('-', '').replace('(', '').replace(')', '')
            break
    
    # Extract email
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    email_match = re.search(email_pattern, text)
    if email_match:
        lead['email'] = email_match.group()
    
    # Extract name (simple heuristic - first 2-3 words before contact info)
    lines = text.split('\n')
    for line in lines[:3]:  # Check first 3 lines
        words = line.split()
        if len(words) >= 2 and not any(char.isdigit() for char in line[:20]):
            lead['name'] = ' '.join(words[:3])
            break
    
    # Detect priority
    text_lower = text.lower()
    if any(w in text_lower for w in ['горячий', 'hot', 'срочно', 'urgent', 'куплю сейчас']):
        lead['priority'] = '🔴 HOT'
    elif any(w in text_lower for w in ['заинтересован', 'interested', 'хочу', 'цена']):
        lead['priority'] = '🟡 WARM'
    else:
        lead['priority'] = '🔵 COLD'
    
    return lead


def main():
    """CLI interface for CRM operations"""
    import sys
    
    if len(sys.argv) < 2:
        print("""Google Sheets CRM

Usage:
  python google_sheets_crm.py add "текст с контактом"
  python google_sheets_crm.py check +79991234567
  python google_sheets_crm.py hot
  python google_sheets_crm.py pending
  python google_sheets_crm.py update LD202403231234 status=CONVERTED
""")
        return
    
    command = sys.argv[1]
    crm = GoogleSheetsCRM()
    
    if command == 'add':
        if len(sys.argv) < 3:
            print("❌ Укажите текст с информацией о лиде")
            return
        
        text = sys.argv[2]
        lead_data = extract_lead_info(text)
        result = crm.add_lead(lead_data)
        print(result['message'])
        
        if result['success']:
            print("\n📅 Запланированные действия:")
            for action in result.get('next_actions', []):
                print(f"   • {action}")
    
    elif command == 'check':
        if len(sys.argv) < 3:
            print("❌ Укажите телефон или email")
            return
        
        query = sys.argv[2]
        is_dup, existing = crm.check_duplicate(
            phone=query if query.startswith('+') or query[0].isdigit() else None,
            email=query if '@' in query else None
        )
        
        if is_dup:
            print(f"⚠️ Дубликат найден!")
            print(f"   Имя: {existing.get('Name', 'N/A')}")
            print(f"   Добавлен: {existing.get('Date Added', 'N/A')}")
            print(f"   Статус: {existing.get('Status', 'N/A')}")
        else:
            print("✅ Дубликатов не найдено")
    
    elif command == 'hot':
        leads = crm.get_hot_leads()
        if leads:
            print(f"🔴 Горячие лиды ({len(leads)}):")
            for lead in leads:
                print(f"   • {lead.get('Name', 'N/A')} | {lead.get('Phone', 'N/A')} | {lead.get('Priority', 'N/A')}")
        else:
            print("🔴 Нет горячих лидов")
    
    elif command == 'pending':
        leads = crm.get_pending_followups()
        if leads:
            print(f"⏰ Ожидают follow-up ({len(leads)}):")
            for lead in leads:
                print(f"   • {lead.get('Name', lead.get('name', 'N/A'))} | {lead.get('Phone', lead.get('phone', 'N/A'))}")
        else:
            print("⏰ Нет ожидающих follow-up")
    
    elif command == 'update':
        if len(sys.argv) < 4:
            print("❌ Укажите ID лида и обновления")
            return
        
        lead_id = sys.argv[2]
        updates = {}
        for update in sys.argv[3:]:
            if '=' in update:
                key, value = update.split('=', 1)
                updates[key] = value
        
        result = crm.update_lead(lead_id, updates)
        print(result['message'])
    
    else:
        print(f"❌ Неизвестная команда: {command}")


if __name__ == '__main__':
    main()
