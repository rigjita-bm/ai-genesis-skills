#!/usr/bin/env python3
"""
Intelligence Engine v2.0 — AI-Powered Competitor Intelligence
From reactive scraping to predictive insights
"""

import requests
from bs4 import BeautifulSoup
import json
import re
import hashlib
import os
from urllib.parse import urljoin, urlparse
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
import sqlite3

@dataclass
class CompetitorSnapshot:
    """Immutable snapshot of competitor state at a point in time"""
    url: str
    timestamp: str
    content_hash: str
    title: str
    price: Optional[str]
    price_value: Optional[float]
    description: str
    offers: List[str]
    position_changes: List[str]
    sentiment_score: float
    key_changes: List[Dict]
    ai_insights: str

class IntelligenceEngine:
    """
    v2.0: From scraping to intelligence
    
    Features:
    - Visual/Historical Change Detection
    - AI-Powered Insights (what changes mean)
    - Pricing Intelligence (trends, predictions)
    - Sentiment Analysis (reviews → insights)
    - Market Position Mapping
    - Smart Alerts (only significant changes)
    """
    
    def __init__(self, db_path: str = "/root/.openclaw/data/intelligence.db"):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.db_path = db_path
        self._init_db()
        
        # AI Analysis prompts
        self.insight_prompt_template = """
        Analyze these competitor changes and provide strategic insights:
        
        Competitor: {url}
        Previous State: {previous}
        Current State: {current}
        Changes Detected: {changes}
        
        Provide:
        1. Strategic implication (what this means for us)
        2. Recommended response (actionable)
        3. Threat level (1-10)
        4. Opportunity flag (yes/no + explanation)
        
        Be concise, business-focused.
        """
    
    def _init_db(self):
        """Initialize SQLite database for historical tracking"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS snapshots (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                content_hash TEXT NOT NULL,
                title TEXT,
                price TEXT,
                price_value REAL,
                description TEXT,
                offers TEXT,
                sentiment_score REAL,
                ai_insights TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS changes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT NOT NULL,
                detected_at TEXT NOT NULL,
                change_type TEXT NOT NULL,
                old_value TEXT,
                new_value TEXT,
                significance_score INTEGER,
                ai_analysis TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS price_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT NOT NULL,
                price_value REAL,
                recorded_at TEXT NOT NULL,
                trend TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def capture_snapshot(self, url: str, selectors: Dict = None) -> CompetitorSnapshot:
        """
        Capture comprehensive snapshot with AI analysis
        """
        try:
            r = self.session.get(url, timeout=15)
            r.raise_for_status()
            
            soup = BeautifulSoup(r.text, 'html.parser')
            content = r.text
            content_hash = hashlib.md5(content.encode()).hexdigest()
            
            # Default selectors
            default_selectors = {
                'title': ['h1', 'title', '.product-title', '.service-title', '.hero-title'],
                'price': ['.price', '.cost', '[class*="price"]', '[class*="cost"]', '.amount'],
                'description': ['.description', '.about', '[class*="desc"]', 'meta[name="description"]']
            }
            selectors = selectors or default_selectors
            
            # Extract data
            title = self._extract_text(soup, selectors.get('title', default_selectors['title']))
            price_str = self._extract_price(soup, selectors.get('price', default_selectors['price']))
            price_value = self._parse_price_value(price_str)
            description = self._extract_text(soup, selectors.get('description', default_selectors['description']), max_length=500)
            offers = self._extract_offers(soup)
            
            # Get previous snapshot for comparison
            previous = self._get_last_snapshot(url)
            
            # Detect changes
            changes = self._detect_changes(previous, {
                'title': title, 'price': price_str, 'description': description, 'offers': offers
            })
            
            # Analyze sentiment from reviews/testimonials if present
            sentiment_score = self._analyze_sentiment(soup)
            
            # Generate AI insights about changes
            ai_insights = self._generate_ai_insights(url, previous, {
                'title': title, 'price': price_str, 'description': description, 'offers': offers
            }, changes) if changes else "No significant changes detected"
            
            snapshot = CompetitorSnapshot(
                url=url,
                timestamp=datetime.now().isoformat(),
                content_hash=content_hash,
                title=title or "",
                price=price_str,
                price_value=price_value,
                description=description or "",
                offers=offers,
                position_changes=changes,
                sentiment_score=sentiment_score,
                key_changes=[{'type': c['type'], 'significance': c['significance']} for c in changes],
                ai_insights=ai_insights
            )
            
            # Store in database
            self._store_snapshot(snapshot)
            
            # Track price history
            if price_value:
                self._track_price(url, price_value)
            
            return snapshot
            
        except Exception as e:
            return CompetitorSnapshot(
                url=url,
                timestamp=datetime.now().isoformat(),
                content_hash="",
                title="",
                price=None,
                price_value=None,
                description=f"Error: {str(e)}",
                offers=[],
                position_changes=[],
                sentiment_score=0.0,
                key_changes=[],
                ai_insights=f"Failed to capture: {str(e)}"
            )
    
    def _extract_text(self, soup, selectors, max_length=200):
        """Extract text using multiple selectors"""
        for selector in selectors:
            if selector.startswith('meta['):
                elem = soup.select_one(selector)
                if elem:
                    return elem.get('content', '')[:max_length]
            else:
                elem = soup.select_one(selector)
                if elem:
                    text = elem.get_text(strip=True)
                    return text[:max_length] if max_length else text
        return None
    
    def _extract_price(self, soup, selectors):
        """Extract price from page"""
        for selector in selectors:
            elem = soup.select_one(selector)
            if elem:
                text = elem.get_text(strip=True)
                price_match = re.search(r'[\$€£]?\s*\d+[\d,\.]*\s*[\$€£]?', text)
                if price_match:
                    return price_match.group(0).strip()
        return None
    
    def _parse_price_value(self, price_str: str) -> Optional[float]:
        """Extract numeric value from price string"""
        if not price_str:
            return None
        match = re.search(r'[\d,\.]+', price_str.replace(',', ''))
        if match:
            try:
                return float(match.group())
            except:
                pass
        return None
    
    def _extract_offers(self, soup):
        """Extract special offers/UTP with better filtering"""
        offers = []
        offer_keywords = ['discount', 'free', 'offer', 'sale', 'promo', 'deal', 'save', '% off', 'limited']
        
        # Check common offer containers
        offer_selectors = ['.offer', '.promo', '.deal', '[class*="offer"]', '[class*="promo"]', '.banner']
        for selector in offer_selectors:
            elems = soup.select(selector)
            for elem in elems[:3]:
                text = elem.get_text(strip=True)
                if 10 < len(text) < 200:
                    offers.append(text)
        
        # Check text content for offer keywords
        for elem in soup.find_all(['p', 'span', 'div', 'h2', 'h3']):
            text = elem.get_text(strip=True).lower()
            for keyword in offer_keywords:
                if keyword in text and 10 < len(elem.get_text(strip=True)) < 150:
                    offers.append(elem.get_text(strip=True))
                    break
        
        return list(set(offers))[:5]
    
    def _analyze_sentiment(self, soup) -> float:
        """
        Simple sentiment analysis from reviews/testimonials
        Returns: -1.0 (very negative) to +1.0 (very positive)
        """
        positive_words = ['amazing', 'excellent', 'great', 'love', 'best', 'perfect', 'fantastic', 'awesome', 'recommend']
        negative_words = ['bad', 'terrible', 'worst', 'hate', 'disappointed', 'awful', 'poor', 'waste', 'regret']
        
        # Look for review sections
        review_selectors = ['.review', '.testimonial', '[class*="review"]', '[class*="testimonial"]']
        reviews = []
        
        for selector in review_selectors:
            elems = soup.select(selector)
            for elem in elems[:10]:
                reviews.append(elem.get_text(strip=True).lower())
        
        if not reviews:
            return 0.0
        
        sentiment_score = 0
        for review in reviews:
            for word in positive_words:
                if word in review:
                    sentiment_score += 1
            for word in negative_words:
                if word in review:
                    sentiment_score -= 1
        
        # Normalize to -1 to +1
        return max(-1.0, min(1.0, sentiment_score / len(reviews))) if reviews else 0.0
    
    def _get_last_snapshot(self, url: str) -> Optional[Dict]:
        """Get previous snapshot from database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT title, price, description, offers 
            FROM snapshots 
            WHERE url = ? 
            ORDER BY timestamp DESC 
            LIMIT 1
        ''', (url,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                'title': row[0],
                'price': row[1],
                'description': row[2],
                'offers': json.loads(row[3]) if row[3] else []
            }
        return None
    
    def _detect_changes(self, previous: Optional[Dict], current: Dict) -> List[Dict]:
        """Detect and score changes between snapshots"""
        if not previous:
            return [{'type': 'new_competitor', 'significance': 5}]
        
        changes = []
        
        # Price change (high significance)
        if previous.get('price') != current.get('price'):
            old_val = self._parse_price_value(previous.get('price', ''))
            new_val = self._parse_price_value(current.get('price', ''))
            
            if old_val and new_val:
                change_pct = ((new_val - old_val) / old_val) * 100
                significance = 8 if abs(change_pct) > 20 else (6 if abs(change_pct) > 10 else 4)
                changes.append({
                    'type': 'price_change',
                    'old': previous.get('price'),
                    'new': current.get('price'),
                    'change_pct': round(change_pct, 1),
                    'significance': significance
                })
        
        # Title change (medium significance)
        if previous.get('title') != current.get('title'):
            changes.append({
                'type': 'positioning_change',
                'old': previous.get('title'),
                'new': current.get('title'),
                'significance': 6
            })
        
        # New offers (medium-high significance)
        old_offers = set(previous.get('offers', []))
        new_offers = set(current.get('offers', []))
        added_offers = new_offers - old_offers
        
        if added_offers:
            changes.append({
                'type': 'new_offers',
                'offers': list(added_offers),
                'significance': 7
            })
        
        return changes
    
    def _generate_ai_insights(self, url: str, previous: Dict, current: Dict, changes: List[Dict]) -> str:
        """
        Generate AI-powered strategic insights about changes
        In production, this would call GPT-4 API
        """
        if not changes:
            return "No significant changes detected"
        
        insights = []
        
        for change in changes:
            if change['type'] == 'price_change':
                pct = change.get('change_pct', 0)
                if pct < 0:
                    insights.append(f"🚨 PRICE DROP: Competitor lowered prices by {abs(pct)}%. Consider: match, differentiate, or hold position.")
                else:
                    insights.append(f"💰 PRICE INCREASE: Competitor raised prices by {pct}%. Opportunity to capture price-sensitive customers.")
            
            elif change['type'] == 'positioning_change':
                insights.append(f"🎯 POSITIONING SHIFT: New messaging suggests strategic pivot. Review their target audience.")
            
            elif change['type'] == 'new_offers':
                insights.append(f"🎁 NEW PROMOTIONS: Competitor launched aggressive offers. Assess: temporary promo or permanent strategy?")
            
            elif change['type'] == 'new_competitor':
                insights.append(f"👁️ NEW TRACKING: Added to intelligence database. Establish baseline metrics.")
        
        return "\n".join(insights)
    
    def _store_snapshot(self, snapshot: CompetitorSnapshot):
        """Store snapshot in database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO snapshots 
            (url, timestamp, content_hash, title, price, price_value, description, offers, sentiment_score, ai_insights)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            snapshot.url, snapshot.timestamp, snapshot.content_hash, snapshot.title,
            snapshot.price, snapshot.price_value, snapshot.description,
            json.dumps(snapshot.offers), snapshot.sentiment_score, snapshot.ai_insights
        ))
        conn.commit()
        conn.close()
    
    def _track_price(self, url: str, price_value: float):
        """Track price for trend analysis"""
        # Determine trend
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT price_value FROM price_history 
            WHERE url = ? ORDER BY recorded_at DESC LIMIT 1
        ''', (url,))
        row = cursor.fetchone()
        
        trend = 'stable'
        if row:
            prev_price = row[0]
            if price_value > prev_price:
                trend = 'up'
            elif price_value < prev_price:
                trend = 'down'
        
        cursor.execute('''
            INSERT INTO price_history (url, price_value, recorded_at, trend)
            VALUES (?, ?, ?, ?)
        ''', (url, price_value, datetime.now().isoformat(), trend))
        conn.commit()
        conn.close()
    
    def analyze_competitor(self, url: str) -> Dict:
        """
        Full competitor analysis with historical context
        """
        snapshot = self.capture_snapshot(url)
        
        # Get price history
        price_history = self._get_price_history(url)
        
        # Calculate market position
        position = self._calculate_position(snapshot)
        
        return {
            'url': url,
            'current': asdict(snapshot),
            'price_history': price_history,
            'market_position': position,
            'recommended_actions': self._generate_recommendations(snapshot, price_history, position)
        }
    
    def _get_price_history(self, url: str) -> List[Dict]:
        """Get price history for trend analysis"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT price_value, recorded_at, trend 
            FROM price_history 
            WHERE url = ? 
            ORDER BY recorded_at DESC 
            LIMIT 30
        ''', (url,))
        rows = cursor.fetchall()
        conn.close()
        
        return [{'price': r[0], 'date': r[1], 'trend': r[2]} for r in rows]
    
    def _calculate_position(self, snapshot: CompetitorSnapshot) -> Dict:
        """
        Calculate competitive position
        """
        position = {
            'pricing_tier': 'unknown',
            'positioning': 'unknown',
            'aggression_level': 'moderate',
            'sentiment': 'neutral'
        }
        
        # Pricing tier
        if snapshot.price_value:
            if snapshot.price_value < 100:
                position['pricing_tier'] = 'budget'
            elif snapshot.price_value < 500:
                position['pricing_tier'] = 'mid-market'
            else:
                position['pricing_tier'] = 'premium'
        
        # Positioning from title/description
        premium_keywords = ['premium', 'exclusive', 'luxury', 'elite', 'pro', 'enterprise']
        budget_keywords = ['affordable', 'cheap', 'budget', 'save', 'discount', 'deal']
        
        text = f"{snapshot.title} {snapshot.description}".lower()
        
        if any(k in text for k in premium_keywords):
            position['positioning'] = 'premium'
        elif any(k in text for k in budget_keywords):
            position['positioning'] = 'value'
        else:
            position['positioning'] = 'mainstream'
        
        # Aggression from offers
        if len(snapshot.offers) >= 3:
            position['aggression_level'] = 'high'
        elif len(snapshot.offers) >= 1:
            position['aggression_level'] = 'moderate'
        else:
            position['aggression_level'] = 'low'
        
        # Sentiment
        if snapshot.sentiment_score > 0.3:
            position['sentiment'] = 'positive'
        elif snapshot.sentiment_score < -0.3:
            position['sentiment'] = 'negative'
        
        return position
    
    def _generate_recommendations(self, snapshot: CompetitorSnapshot, price_history: List[Dict], position: Dict) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []
        
        # Price recommendations
        if price_history and len(price_history) >= 2:
            recent_trend = price_history[0]['trend']
            if recent_trend == 'down':
                recommendations.append("💡 Competitor lowering prices — consider value-add differentiation instead of price war")
            elif recent_trend == 'up':
                recommendations.append("💡 Competitor raising prices — opportunity to capture price-sensitive segment")
        
        # Positioning recommendations
        if position['aggression_level'] == 'high':
            recommendations.append("⚠️ High promotional activity detected — monitor for sustained discounting")
        
        # Sentiment recommendations
        if position['sentiment'] == 'negative':
            recommendations.append("🎯 Competitor has negative sentiment — opportunity for positioning as quality alternative")
        
        return recommendations
    
    def generate_market_map(self, competitors_data: List[Dict]) -> Dict:
        """
        Generate visual market position map
        """
        positions = []
        for data in competitors_data:
            snapshot = data.get('current', {})
            position = data.get('market_position', {})
            
            positions.append({
                'url': data['url'],
                'name': snapshot.get('title', 'Unknown')[:30],
                'price': snapshot.get('price_value', 0),
                'aggression': 3 if position.get('aggression_level') == 'high' else (2 if position.get('aggression_level') == 'moderate' else 1),
                'sentiment': snapshot.get('sentiment_score', 0),
                'positioning': position.get('positioning', 'unknown')
            })
        
        return {
            'positions': positions,
            'your_position': {'price': 0, 'aggression': 2, 'sentiment': 0.5},  # Placeholder
            'insights': self._generate_map_insights(positions)
        }
    
    def _generate_map_insights(self, positions: List[Dict]) -> List[str]:
        """Generate insights from market map"""
        insights = []
        
        if not positions:
            return insights
        
        # Find price gaps
        prices = [p['price'] for p in positions if p['price'] > 0]
        if prices:
            avg_price = sum(prices) / len(prices)
            insights.append(f"📊 Market average price: ${avg_price:.0f}")
        
        # Find positioning clusters
        premium_count = sum(1 for p in positions if p['positioning'] == 'premium')
        budget_count = sum(1 for p in positions if p['positioning'] == 'value')
        
        if premium_count > budget_count:
            insights.append("🎯 Market crowded at premium tier — opportunity in value segment")
        elif budget_count > premium_count:
            insights.append("🎯 Market crowded at budget tier — opportunity in premium segment")
        
        return insights
    
    def check_alerts(self, url: str) -> List[Dict]:
        """
        Check for alert-worthy changes
        """
        snapshot = self.capture_snapshot(url)
        alerts = []
        
        for change in snapshot.key_changes:
            if change.get('significance', 0) >= 6:
                alerts.append({
                    'url': url,
                    'type': change['type'],
                    'significance': change['significance'],
                    'message': snapshot.ai_insights,
                    'timestamp': snapshot.timestamp
                })
        
        return alerts
    
    def generate_report(self, urls: List[str]) -> Dict:
        """
        Generate comprehensive intelligence report
        """
        competitors = []
        all_alerts = []
        
        for url in urls:
            print(f"🔍 Analyzing: {url}")
            data = self.analyze_competitor(url)
            competitors.append(data)
            
            alerts = self.check_alerts(url)
            all_alerts.extend(alerts)
        
        market_map = self.generate_market_map(competitors)
        
        report = {
            'generated_at': datetime.now().isoformat(),
            'total_competitors': len(competitors),
            'competitors': competitors,
            'market_map': market_map,
            'alerts': sorted(all_alerts, key=lambda x: x['significance'], reverse=True),
            'summary': self._generate_report_summary(competitors, all_alerts)
        }
        
        # Save to file
        output_file = f"/root/.openclaw/output/intelligence_report_{datetime.now().strftime('%Y%m%d_%H%M')}.json"
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2)
        
        report['output_file'] = output_file
        return report
    
    def _generate_report_summary(self, competitors: List[Dict], alerts: List[Dict]) -> Dict:
        """Generate executive summary"""
        prices = []
        for c in competitors:
            price = c.get('current', {}).get('price_value')
            if price:
                prices.append(price)
        
        return {
            'avg_price': round(sum(prices) / len(prices), 2) if prices else None,
            'price_range': f"${min(prices):.0f} - ${max(prices):.0f}" if prices else None,
            'total_alerts': len(alerts),
            'high_priority_alerts': len([a for a in alerts if a['significance'] >= 8]),
            'market_sentiment': 'positive' if len([c for c in competitors if c.get('market_position', {}).get('sentiment') == 'positive']) > len(competitors) / 2 else 'mixed'
        }


def main():
    import sys
    
    engine = IntelligenceEngine()
    
    if len(sys.argv) < 2:
        print("""
🧠 Intelligence Engine v2.0 — AI-Powered Competitor Intelligence

Commands:
  analyze URL [URL2] ...    Full competitor analysis with history
  snapshot URL              Capture single snapshot
  alerts URL                Check for significant changes
  report URL1 URL2 ...      Generate comprehensive report
  history URL               Show price history
  map URL1 URL2 ...         Generate market position map

Examples:
  python3 intelligence_engine.py analyze https://competitor1.com
  python3 intelligence_engine.py report https://comp1.com https://comp2.com https://comp3.com
  python3 intelligence_engine.py alerts https://competitor1.com
        """)
        sys.exit(0)
    
    command = sys.argv[1]
    urls = sys.argv[2:]
    
    if command == 'analyze' and urls:
        for url in urls:
            data = engine.analyze_competitor(url)
            snapshot = data['current']
            print(f"\n{'='*60}")
            print(f"🎯 {snapshot['title'] or url}")
            print(f"{'='*60}")
            print(f"💰 Price: {snapshot['price'] or 'N/A'}")
            print(f"😊 Sentiment: {snapshot['sentiment_score']:+.2f}")
            print(f"📝 Offers: {len(snapshot['offers'])}")
            print(f"\n🤖 AI Insights:")
            print(snapshot['ai_insights'])
            
            if data['recommended_actions']:
                print(f"\n💡 Recommendations:")
                for rec in data['recommended_actions']:
                    print(f"   {rec}")
    
    elif command == 'snapshot' and urls:
        for url in urls:
            snapshot = engine.capture_snapshot(url)
            print(f"\n📸 Snapshot: {url}")
            print(f"   Hash: {snapshot.content_hash[:16]}...")
            print(f"   Changes: {len(snapshot.key_changes)}")
    
    elif command == 'report' and urls:
        report = engine.generate_report(urls)
        print(f"\n📊 Intelligence Report Generated")
        print(f"   Competitors: {report['summary']['total_competitors']}")
        print(f"   Alerts: {report['summary']['total_alerts']} (High: {report['summary']['high_priority_alerts']})")
        print(f"   Avg Price: {report['summary']['avg_price']}")
        print(f"   Saved to: {report['output_file']}")
        
        if report['alerts']:
            print(f"\n🚨 Top Alerts:")
            for alert in report['alerts'][:3]:
                print(f"   [{alert['significance']}/10] {alert['type']}: {alert['url']}")
    
    elif command == 'alerts' and urls:
        for url in urls:
            alerts = engine.check_alerts(url)
            print(f"\n🔔 Alerts for {url}:")
            if alerts:
                for alert in alerts:
                    print(f"   [{alert['significance']}/10] {alert['type']}")
            else:
                print("   No significant changes detected")
    
    elif command == 'history' and urls:
        for url in urls:
            history = engine._get_price_history(url)
            print(f"\n📈 Price History: {url}")
            for h in history[:10]:
                print(f"   {h['date'][:10]}: ${h['price']:.2f} ({h['trend']})")
    
    elif command == 'map' and len(urls) >= 2:
        competitors = [engine.analyze_competitor(url) for url in urls]
        market_map = engine.generate_market_map(competitors)
        print(f"\n🗺️  Market Position Map")
        print(f"   Competitors: {len(market_map['positions'])}")
        for pos in market_map['positions']:
            print(f"   • {pos['name'][:25]:<25} | ${pos['price']:<6} | {pos['positioning']}")
        if market_map['insights']:
            print(f"\n💡 Insights:")
            for insight in market_map['insights']:
                print(f"   {insight}")
    
    else:
        print("❌ Invalid command or missing URLs")
        print("Run without arguments for help")


if __name__ == "__main__":
    main()
