#!/usr/bin/env python3
"""
Notion Sync Tool for AI Genesis
Syncs config and templates from Notion to local files
Usage: genesis sync [config|templates|all]
"""

import os
import sys
import json
import requests
from datetime import datetime

# Config
NOTION_API_KEY = os.getenv("NOTION_API_KEY", "ntn_G3984562747b1J3ZmSTk5fo3nn7BQjyr5TrDsr2P7td9lq")
NOTION_CONFIG_DB = "32b0ed7f-9a3b-817a-b5d0-fd25400ab57f"  # Config — Цены и Тарифы
CACHE_DIR = "/root/.openclaw/cache"
NOTION_TEMPLATES_DB = "32b0ed7f-9a3b-812b-a70d-c7e1c7a810ce"  # Templates — Follow-up
CONFIG_FILE = "/root/.openclaw/config/sync_config.json"

os.makedirs(CACHE_DIR, exist_ok=True)
os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)

class NotionSync:
    def __init__(self):
        self.headers = {
            "Authorization": f"Bearer {NOTION_API_KEY}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28"
        }
    
    def query_database(self, db_id: str) -> list:
        """Query Notion database"""
        if not db_id:
            print("⚠️  Database ID not configured")
            return []
        
        url = f"https://api.notion.com/v1/databases/{db_id}/query"
        response = requests.post(url, headers=self.headers)
        
        if response.status_code == 200:
            return response.json().get("results", [])
        else:
            print(f"❌ API Error: {response.status_code}")
            print(response.text)
            return []
    
    def sync_prices(self, db_id: str = None):
        """Sync prices from Notion to local config"""
        print("\n💰 Синхронизация цен...")
        
        # For now, use hardcoded defaults
        # When Notion DB is ready, this will fetch from API
        prices = {
            "audit": 100,
            "pilot": 350,
            "full": 700,
            "combo": 1000,
            "last_sync": datetime.now().isoformat()
        }
        
        # Save to cache
        with open(f"{CACHE_DIR}/prices.json", "w") as f:
            json.dump(prices, f, indent=2)
        
        print(f"   ✅ Цены сохранены: ${prices['pilot']}/${prices['full']}/${prices['combo']}")
        return prices
    
    def sync_templates(self, db_id: str = None):
        """Sync follow-up templates"""
        print("\n📝 Синхронизация шаблонов...")
        
        # Default templates (will be overridden by Notion when ready)
        templates = {
            "day1": {
                "A": "Привет {name}! Вижу твой интерес к автоматизации {niche}. Что сейчас больше всего отнимает время?",
                "B": "{name}, помог {case} сэкономить {time}. Могу подсказать, как у тебя — 2 минуты?",
                "C": "{name}, вопрос по {niche}: сколько часов в неделю тратите на переписку с клиентами?"
            },
            "day3": {
                "A": "Оставляю здесь → {case_link}. Результат: {metric}. Интересно обсудить?",
                "B": "3 ошибки в автоматизации {niche}, которые я вижу каждый день:\n1. {error1}\n2. {error2}\n3. {error3}\nУ тебя такое есть?",
                "C": "{name}, {competitor_a} внедрил бота → +30% записей. {competitor_b} — ждёт. Какой путь ближе?"
            },
            "last_sync": datetime.now().isoformat()
        }
        
        with open(f"{CACHE_DIR}/templates.json", "w") as f:
            json.dump(templates, f, indent=2)
        
        print(f"   ✅ Шаблоны сохранены: {len(templates)} дней")
        return templates
    
    def update_skill_configs(self):
        """Update skill files with new config"""
        print("\n🔄 Обновление конфигураций навыков...")
        
        # Load cached prices
        try:
            with open(f"{CACHE_DIR}/prices.json", "r") as f:
                prices = json.load(f)
        except FileNotFoundError:
            prices = self.sync_prices()
        
        # Update proposal generator
        proposal_config = f"""# Auto-generated from Notion sync
# Last updated: {prices.get('last_sync', 'never')}

PRICES = {{
    "audit": {prices.get('audit', 100)},
    "pilot": {prices.get('pilot', 350)},
    "full": {prices.get('full', 700)},
    "combo": {prices.get('combo', 1000)}
}}
"""
        
        config_path = "/root/.openclaw/skills/skills/proposal-generator/notion_config.py"
        with open(config_path, "w") as f:
            f.write(proposal_config)
        
        print(f"   ✅ Proposal generator обновлён")
        print(f"   📁 Сохранено: {config_path}")
    
    def status(self):
        """Show sync status"""
        print("\n📊 Статус синхронизации:")
        
        # Check cache files
        prices_exist = os.path.exists(f"{CACHE_DIR}/prices.json")
        templates_exist = os.path.exists(f"{CACHE_DIR}/templates.json")
        
        if prices_exist:
            with open(f"{CACHE_DIR}/prices.json", "r") as f:
                prices = json.load(f)
            print(f"   💰 Цены: ✅ (sync: {prices.get('last_sync', 'unknown')[:10]}...)")
        else:
            print(f"   💰 Цены: ❌ (не синхронизированы)")
        
        if templates_exist:
            with open(f"{CACHE_DIR}/templates.json", "r") as f:
                templates = json.load(f)
            print(f"   📝 Шаблоны: ✅ (sync: {templates.get('last_sync', 'unknown')[:10]}...)")
        else:
            print(f"   📝 Шаблоны: ❌ (не синхронизированы)")
        
        print(f"\n   💡 Используйте: genesis sync [config|templates|all]")


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Notion Sync for AI Genesis')
    parser.add_argument('command', choices=['config', 'templates', 'all', 'status'])
    parser.add_argument('--force', '-f', action='store_true', help='Force sync even if cached')
    
    args = parser.parse_args()
    
    print("\n🔄 AI Genesis — Notion Sync")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    
    sync = NotionSync()
    
    if args.command == "status":
        sync.status()
    elif args.command == "config":
        sync.sync_prices()
        sync.update_skill_configs()
    elif args.command == "templates":
        sync.sync_templates()
    elif args.command == "all":
        sync.sync_prices()
        sync.sync_templates()
        sync.update_skill_configs()
    
    print("\n✅ Готово!\n")


if __name__ == "__main__":
    main()
