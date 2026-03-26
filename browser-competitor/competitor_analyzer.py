#!/usr/bin/env python3
"""
Competitor Analysis Skill for AI Genesis
Scrapes competitor websites, extracts pricing and offers
"""

import requests
from bs4 import BeautifulSoup
import json
import re
from urllib.parse import urljoin, urlparse
from datetime import datetime

class CompetitorAnalyzer:
    """Analyze competitor websites"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.results = []
    
    def scrape_page(self, url, selectors=None):
        """
        Scrape a single page
        
        Args:
            url: Target URL
            selectors: dict with CSS selectors for title, price, description
        
        Returns:
            dict with extracted data
        """
        try:
            r = self.session.get(url, timeout=10)
            r.raise_for_status()
            
            soup = BeautifulSoup(r.text, 'html.parser')
            
            # Default selectors
            default_selectors = {
                'title': ['h1', 'title', '.product-title', '.service-title'],
                'price': ['.price', '.cost', '[class*="price"]', '[class*="cost"]'],
                'description': ['.description', '.about', '[class*="desc"]', 'p']
            }
            
            selectors = selectors or default_selectors
            
            data = {
                'url': url,
                'scraped_at': datetime.now().isoformat(),
                'title': self._extract_text(soup, selectors.get('title', default_selectors['title'])),
                'price': self._extract_price(soup, selectors.get('price', default_selectors['price'])),
                'description': self._extract_text(soup, selectors.get('description', default_selectors['description']), max_length=500),
                'offers': self._extract_offers(soup),
                'contact': self._extract_contact(soup)
            }
            
            return data
            
        except Exception as e:
            return {
                'url': url,
                'error': str(e),
                'scraped_at': datetime.now().isoformat()
            }
    
    def _extract_text(self, soup, selectors, max_length=200):
        """Extract text using multiple selectors"""
        for selector in selectors:
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
                # Extract price patterns
                price_match = re.search(r'[\$€£]?\s*\d+[\d,\.]*\s*[\$€£]?', text)
                if price_match:
                    return price_match.group(0).strip()
        return None
    
    def _extract_offers(self, soup):
        """Extract special offers/UTP"""
        offers = []
        
        # Common offer keywords
        offer_keywords = ['акция', 'скидка', 'подарок', 'бесплатно', 'discount', 'free', 'offer', 'sale']
        
        for elem in soup.find_all(text=True):
            text = elem.strip().lower()
            for keyword in offer_keywords:
                if keyword in text and len(text) < 200:
                    offers.append(elem.strip())
                    break
        
        return list(set(offers))[:5]  # Unique offers, max 5
    
    def _extract_contact(self, soup):
        """Extract contact info"""
        contacts = {
            'phones': [],
            'emails': [],
            'social': []
        }
        
        # Phone patterns
        phone_pattern = r'\+?1?\d{9,15}'
        for match in re.finditer(phone_pattern, soup.get_text()):
            contacts['phones'].append(match.group())
        
        # Email pattern
        email_pattern = r'[\w\.-]+@[\w\.-]+\.\w+'
        for match in re.finditer(email_pattern, soup.get_text()):
            contacts['emails'].append(match.group())
        
        # Social links
        social_platforms = ['instagram', 'facebook', 'telegram', 'twitter', 'linkedin']
        for a in soup.find_all('a', href=True):
            href = a['href'].lower()
            for platform in social_platforms:
                if platform in href:
                    contacts['social'].append({
                        'platform': platform,
                        'url': a['href']
                    })
        
        return contacts
    
    def analyze_competitors(self, urls):
        """Analyze multiple competitor URLs"""
        results = []
        
        for url in urls:
            print(f"🔍 Analyzing: {url}")
            data = self.scrape_page(url)
            results.append(data)
        
        self.results = results
        return results
    
    def generate_report(self, output_file="/root/.openclaw/output/competitor_analysis.json"):
        """Generate JSON report"""
        import os
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        report = {
            'generated_at': datetime.now().isoformat(),
            'total_competitors': len(self.results),
            'competitors': self.results,
            'summary': self._generate_summary()
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        return report
    
    def _generate_summary(self):
        """Generate summary insights"""
        prices = []
        offers_count = {}
        
        for r in self.results:
            if 'price' in r and r['price']:
                # Extract numeric price
                price_match = re.search(r'[\d,\.]+', r['price'].replace(',', ''))
                if price_match:
                    try:
                        prices.append(float(price_match.group()))
                    except:
                        pass
            
            if 'offers' in r:
                for offer in r['offers']:
                    offers_count[offer] = offers_count.get(offer, 0) + 1
        
        return {
            'avg_price': sum(prices) / len(prices) if prices else None,
            'min_price': min(prices) if prices else None,
            'max_price': max(prices) if prices else None,
            'top_offers': sorted(offers_count.items(), key=lambda x: x[1], reverse=True)[:5]
        }

def main():
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python3 competitor_analyzer.py URL1 [URL2] [URL3]...")
        print("Example: python3 competitor_analyzer.py https://competitor1.com https://competitor2.com")
        sys.exit(1)
    
    urls = sys.argv[1:]
    
    analyzer = CompetitorAnalyzer()
    results = analyzer.analyze_competitors(urls)
    report = analyzer.generate_report()
    
    print(f"\n✅ Analysis complete!")
    print(f"   Competitors: {len(results)}")
    print(f"   Report: /root/.openclaw/output/competitor_analysis.json")
    
    if report['summary']['avg_price']:
        print(f"\n💰 Price range: ${report['summary']['min_price']:.0f} - ${report['summary']['max_price']:.0f}")
        print(f"   Average: ${report['summary']['avg_price']:.0f}")

if __name__ == "__main__":
    main()
