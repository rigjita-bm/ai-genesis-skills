#!/usr/bin/env python3
"""
CRM Data Analysis Skill for AI Genesis
Analyzes Notion CRM data and generates reports
"""

import requests
import json
from datetime import datetime, timedelta
from collections import Counter

NOTION_KEY = "ntn_G3984562747b1J3ZmSTk5fo3nn7BQjyr5TrDsr2P7td9lq"
CRM_DB_ID = "32a0ed7f-9a3b-8149-bc86-d7ea47e4711b"

class CRMAnalyzer:
    """Analyze CRM data from Notion"""
    
    def __init__(self):
        self.headers = {
            "Authorization": f"Bearer {NOTION_KEY}",
            "Notion-Version": "2022-06-28",
            "Content-Type": "application/json"
        }
        self.clients = []
    
    def fetch_clients(self):
        """Fetch all clients from Notion CRM"""
        url = f"https://api.notion.com/v1/databases/{CRM_DB_ID}/query"
        
        all_clients = []
        has_more = True
        start_cursor = None
        
        while has_more:
            data = {}
            if start_cursor:
                data["start_cursor"] = start_cursor
            
            r = requests.post(url, headers=self.headers, json=data)
            r.raise_for_status()
            
            result = r.json()
            all_clients.extend(result.get("results", []))
            
            has_more = result.get("has_more", False)
            start_cursor = result.get("next_cursor")
        
        self.clients = all_clients
        return all_clients
    
    def analyze_pipeline(self):
        """Analyze sales pipeline"""
        if not self.clients:
            self.fetch_clients()
        
        # Count by status
        statuses = Counter()
        products = Counter()
        sources = Counter()
        
        # Time analysis
        recent_clients = []
        week_ago = datetime.now() - timedelta(days=7)
        
        for client in self.clients:
            props = client.get("properties", {})
            
            # Status
            status = props.get("Status", {}).get("select", {}).get("name", "Unknown")
            statuses[status] += 1
            
            # Product
            product = props.get("Product", {}).get("select", {}).get("name", "Unknown")
            products[product] += 1
            
            # Source
            source = props.get("Source", {}).get("select", {}).get("name", "Unknown")
            sources[source] += 1
            
            # Check if recent
            created = client.get("created_time", "")
            if created:
                try:
                    created_dt = datetime.fromisoformat(created.replace('Z', '+00:00'))
                    if created_dt > week_ago:
                        name = props.get("Name", {}).get("title", [{}])[0].get("text", {}).get("content", "Unknown")
                        recent_clients.append({
                            "name": name,
                            "status": status,
                            "product": product,
                            "created": created
                        })
                except:
                    pass
        
        return {
            "total_clients": len(self.clients),
            "by_status": dict(statuses),
            "by_product": dict(products),
            "by_source": dict(sources),
            "recent_week": recent_clients,
            "conversion_rate": self._calculate_conversion(statuses)
        }
    
    def _calculate_conversion(self, statuses):
        """Calculate conversion rates"""
        total = sum(statuses.values())
        if total == 0:
            return {}
        
        return {
            status: f"{(count/total*100):.1f}%"
            for status, count in statuses.items()
        }
    
    def generate_weekly_report(self):
        """Generate weekly report"""
        analysis = self.analyze_pipeline()
        
        report = f"""
📊 AI GENESIS — Отчёт за неделю

👥 Всего клиентов: {analysis['total_clients']}
📈 Новых за неделю: {len(analysis['recent_week'])}

📋 По статусам:
"""
        
        for status, count in analysis['by_status'].items():
            report += f"   • {status}: {count}\n"
        
        report += f"\n💰 По продуктам:\n"
        for product, count in analysis['by_product'].items():
            report += f"   • {product}: {count}\n"
        
        if analysis['recent_week']:
            report += f"\n🆕 Новые лиды:\n"
            for client in analysis['recent_week'][:5]:
                report += f"   • {client['name']} — {client['product']}\n"
        
        report += f"\n📊 Конверсия:\n"
        for status, rate in analysis['conversion_rate'].items():
            report += f"   • {status}: {rate}\n"
        
        return report
    
    def save_report(self, output_dir="/root/.openclaw/output/crm_reports"):
        """Save report to file"""
        import os
        os.makedirs(output_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # JSON report
        analysis = self.analyze_pipeline()
        json_file = os.path.join(output_dir, f"crm_analysis_{timestamp}.json")
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(analysis, f, ensure_ascii=False, indent=2)
        
        # Text report
        report = self.generate_weekly_report()
        txt_file = os.path.join(output_dir, f"crm_report_{timestamp}.txt")
        with open(txt_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        return json_file, txt_file

def main():
    print("🔍 Анализирую данные CRM...")
    
    analyzer = CRMAnalyzer()
    analyzer.fetch_clients()
    
    json_file, txt_file = analyzer.save_report()
    
    print(f"✅ Отчёты созданы:")
    print(f"   📊 JSON: {json_file}")
    print(f"   📝 TXT: {txt_file}")
    
    # Print summary
    print(f"\n{analyzer.generate_weekly_report()}")

if __name__ == "__main__":
    main()
