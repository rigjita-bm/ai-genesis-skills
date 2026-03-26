"""
Carousel Pro v3.0 - AI-Powered Instagram Carousel Generator
Enhanced with GPT-4 content, viral scoring, and A/B testing
"""

import argparse
import json
import os
import sys
import asyncio
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import random

# Add modes package to path
sys.path.insert(0, str(Path(__file__).parent))

from modes import get_mode, list_modes, MODES
from png_export import PNGExporter, InstagramPreview, create_zip_archive


class AIContentGenerator:
    """GPT-4 powered content generation for carousels"""
    
    def __init__(self):
        self.api_key = os.getenv("KIMI_API_KEY", "")
    
    async def generate_content(self, topic: str, mode: str, language: str = "en") -> Dict:
        """Generate AI-powered carousel content"""
        
        if not self.api_key:
            # Fallback to template-based generation
            return self._generate_template_content(topic, mode, language)
        
        try:
            import aiohttp
            
            prompt = f"""Create an Instagram carousel about "{topic}" in {language}.
            
Generate a JSON object with these 7 slides:
1. hook: Attention-grabbing headline (max 8 words)
2. problem: Pain point question (max 12 words)
3. solution: Value proposition (max 10 words)
4. features: Array of 4 key benefits (3-5 words each)
5. details: Section title for deep dive (max 4 words)
6. steps: Array of 3 actionable steps (4-6 words each)
7. cta: Call-to-action button text (2-3 words)

Also include:
- hashtags: Array of 10 relevant hashtags
- best_time: Best time to post (e.g., "Tuesday 2PM")
- viral_score: Predicted viral potential (1-100)
- target_audience: Primary audience description

Respond ONLY with valid JSON."""

            async with aiohttp.ClientSession() as session:
                async with session.post(
                    "https://api.moonshot.cn/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": "kimi-k2-72b",
                        "messages": [{"role": "user", "content": prompt}],
                        "temperature": 0.7,
                        "max_tokens": 1000
                    }
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        content_text = data["choices"][0]["message"]["content"]
                        # Extract JSON from response
                        import re
                        json_match = re.search(r'\{.*\}', content_text, re.DOTALL)
                        if json_match:
                            return json.loads(json_match.group())
        except Exception as e:
            print(f"⚠️  AI generation failed: {e}. Using templates.")
        
        return self._generate_template_content(topic, mode, language)
    
    def _generate_template_content(self, topic: str, mode: str, language: str) -> Dict:
        """Template-based fallback content generation"""
        
        templates = {
            "business": {
                "hook": f"Transform Your {topic} with AI",
                "problem": f"Still managing {topic} manually?",
                "solution": f"AI-powered {topic} automation",
                "features": ["24/7 Operation", "Smart Analytics", "Auto-Responses", "Cost Reduction"],
                "details": "Proven Results",
                "steps": ["Connect systems", "Train AI", "Launch automation"],
                "cta": "Get Started",
                "hashtags": ["#AI", "#Automation", "#BusinessGrowth", "#DigitalTransformation", "#Innovation"],
                "best_time": "Tuesday 2PM",
                "viral_score": 72,
                "target_audience": "Business owners and managers"
            },
            "product": {
                "hook": f"Meet the Future of {topic}",
                "problem": f"Tired of outdated {topic}?",
                "solution": f"Revolutionary {topic} technology",
                "features": ["Premium Quality", "Easy Setup", "24/7 Support", "Proven Results"],
                "details": "Why Choose Us",
                "steps": ["Order today", "Quick delivery", "Enjoy benefits"],
                "cta": "Order Now",
                "hashtags": ["#ProductLaunch", "#Innovation", "#Tech", "#NewProduct", "#MustHave"],
                "best_time": "Thursday 11AM",
                "viral_score": 68,
                "target_audience": "Early adopters and tech enthusiasts"
            },
            "service": {
                "hook": f"Expert {topic} Services",
                "problem": f"Struggling with {topic}?",
                "solution": f"Professional {topic} solutions",
                "features": ["Certified Experts", "Fast Results", "Guaranteed Quality", "Fair Pricing"],
                "details": "Our Approach",
                "steps": ["Free consultation", "Custom solution", "Ongoing support"],
                "cta": "Book Call",
                "hashtags": ["#Service", "#Expert", "#Professional", "#Consultation", "#Results"],
                "best_time": "Wednesday 10AM",
                "viral_score": 65,
                "target_audience": "Professionals seeking expert help"
            }
        }
        
        # Determine content type
        topic_lower = topic.lower()
        if any(word in topic_lower for word in ["saas", "ai", "app", "tech", "software"]):
            return templates["business"]
        elif any(word in topic_lower for word in ["product", "device", "tool"]):
            return templates["product"]
        else:
            return templates["service"]


class ViralPredictor:
    """Predict viral potential of carousel content"""
    
    def __init__(self):
        self.engagement_factors = {
            "hook_power": 0.25,      # Strong hook matters most
            "visual_appeal": 0.20,    # Design quality
            "timeliness": 0.15,       # Trending topics
            "audience_match": 0.15,   # Target audience alignment
            "shareability": 0.15,     # Easy to share
            "hashtag_optimization": 0.10  # Hashtag strategy
        }
    
    def analyze(self, content: Dict, topic: str) -> Dict:
        """Analyze content and return viral score with recommendations"""
        
        scores = {}
        
        # Hook power analysis
        hook = content.get("hook", "")
        scores["hook_power"] = self._score_hook(hook)
        
        # Visual appeal (based on topic keywords)
        scores["visual_appeal"] = self._score_visual(topic)
        
        # Timeliness
        scores["timeliness"] = self._score_timeliness(topic)
        
        # Audience match (placeholder - would need audience data)
        scores["audience_match"] = 75
        
        # Shareability
        scores["shareability"] = self._score_shareability(content)
        
        # Hashtag optimization
        hashtags = content.get("hashtags", [])
        scores["hashtag_optimization"] = self._score_hashtags(hashtags)
        
        # Calculate weighted total
        total_score = sum(
            scores[factor] * weight 
            for factor, weight in self.engagement_factors.items()
        )
        
        return {
            "viral_score": round(total_score),
            "breakdown": scores,
            "rating": self._get_rating(total_score),
            "recommendations": self._generate_recommendations(scores, content)
        }
    
    def _score_hook(self, hook: str) -> int:
        """Score hook strength 0-100"""
        score = 50
        hook_lower = hook.lower()
        
        # Power words
        power_words = ["transform", "secret", "discover", "ultimate", "proven", "guaranteed", 
                      "instant", "free", "exclusive", "breakthrough", "revolutionary"]
        for word in power_words:
            if word in hook_lower:
                score += 8
        
        # Numbers perform well
        if any(char.isdigit() for char in hook):
            score += 10
        
        # Optimal length: 5-8 words
        word_count = len(hook.split())
        if 5 <= word_count <= 8:
            score += 10
        elif word_count > 10:
            score -= 10
        
        return min(100, max(0, score))
    
    def _score_visual(self, topic: str) -> int:
        """Score visual appeal potential"""
        score = 65
        visual_topics = ["design", "fashion", "beauty", "food", "travel", "art", "photography"]
        
        if any(word in topic.lower() for word in visual_topics):
            score += 20
        
        return min(100, score)
    
    def _score_timeliness(self, topic: str) -> int:
        """Score topic timeliness"""
        trending = ["ai", "automation", "chatgpt", "tiktok", "reels", "shorts"]
        score = 60
        
        if any(word in topic.lower() for word in trending):
            score += 25
        
        return min(100, score)
    
    def _score_shareability(self, content: Dict) -> int:
        """Score how shareable the content is"""
        score = 60
        
        # Lists and steps are shareable
        features = content.get("features", [])
        if len(features) >= 4:
            score += 15
        
        steps = content.get("steps", [])
        if len(steps) == 3:
            score += 10
        
        return min(100, score)
    
    def _score_hashtags(self, hashtags: List[str]) -> int:
        """Score hashtag strategy"""
        score = 50
        
        if not hashtags:
            return score
        
        # Optimal count: 5-10 hashtags
        if 5 <= len(hashtags) <= 10:
            score += 20
        elif len(hashtags) > 15:
            score -= 15
        
        # Mix of popular and niche
        if any(len(tag) > 15 for tag in hashtags):  # Niche hashtags tend to be longer
            score += 10
        
        return min(100, score)
    
    def _get_rating(self, score: float) -> str:
        """Convert score to rating"""
        if score >= 85:
            return "🔥 Viral Potential"
        elif score >= 70:
            return "⭐ High Engagement"
        elif score >= 55:
            return "📈 Good Performance"
        else:
            return "💡 Needs Optimization"
    
    def _generate_recommendations(self, scores: Dict, content: Dict) -> List[str]:
        """Generate improvement recommendations"""
        recommendations = []
        
        if scores["hook_power"] < 70:
            recommendations.append("Add power words to hook: 'Secret', 'Proven', 'Ultimate'")
        
        if scores["hashtag_optimization"] < 70:
            recommendations.append("Use 5-10 mix of popular and niche hashtags")
        
        if scores["shareability"] < 70:
            recommendations.append("Add more list-based content (Top 5, 3 Steps)")
        
        if not recommendations:
            recommendations.append("Content looks great! Consider A/B testing hooks.")
        
        return recommendations


class ABTestGenerator:
    """Generate A/B test variants for carousels"""
    
    async def generate_variants(self, topic: str, mode: str, ai_gen: AIContentGenerator) -> Tuple[Dict, Dict]:
        """Generate two variants: Emotional vs Rational"""
        
        # Variant A: Emotional (appeals to feelings)
        emotional_hooks = [
            "Imagine never worrying about",
            "The moment everything changes",
            "Stop dreaming, start achieving",
            "Your future self will thank you",
            "What if it was easier?"
        ]
        
        # Variant B: Rational (appeals to logic)
        rational_hooks = [
            "3 proven ways to",
            "Data shows this works",
            "The science behind",
            "Maximize your ROI with",
            "Reduce costs by 40%"
        ]
        
        base_content = await ai_gen.generate_content(topic, mode)
        
        variant_a = base_content.copy()
        variant_a["hook"] = f"{random.choice(emotional_hooks)} {topic}"
        variant_a["approach"] = "emotional"
        
        variant_b = base_content.copy()
        variant_b["hook"] = f"{random.choice(rational_hooks)} {topic}"
        variant_b["approach"] = "rational"
        
        return variant_a, variant_b


class CarouselProV3:
    """Enhanced carousel generator with AI and viral prediction"""
    
    def __init__(self):
        self.output_dir = Path("/tmp/carousel_output")
        self.output_dir.mkdir(exist_ok=True)
        self.ai_generator = AIContentGenerator()
        self.viral_predictor = ViralPredictor()
        self.ab_generator = ABTestGenerator()
    
    async def generate_carousel(self, topic: str, mode_name: str = "auto",
                                brand: Optional[Dict] = None, 
                                language: str = "en",
                                ab_test: bool = False) -> Dict:
        """Generate complete carousel with AI content and viral scoring"""
        
        # Get mode
        if mode_name == "auto":
            mode_name = self._detect_mode(topic)
        
        mode = get_mode(mode_name)
        if not mode:
            raise ValueError(f"Unknown mode: {mode_name}")
        
        # Default brand
        if brand is None:
            brand = {
                "name": "AI Genesis",
                "handle": "@aigenesis.ai",
                "tagline": "Automate your business"
            }
        
        # Generate content (AI or template)
        if ab_test:
            content_a, content_b = await self.ab_generator.generate_variants(
                topic, mode_name, self.ai_generator
            )
            # Use variant A as primary
            content = content_a
            variants = {"A": content_a, "B": content_b}
        else:
            content = await self.ai_generator.generate_content(topic, mode_name, language)
            variants = None
        
        # Generate slides
        slides = [
            mode.generate_slide_1_hero(content["hook"], brand, 7),
            mode.generate_slide_2_problem(content["problem"], brand, 7),
            mode.generate_slide_3_solution(content["solution"], brand, 7),
            mode.generate_slide_4_features(content["features"], brand, 7),
            mode.generate_slide_5_details(content["details"], brand, 7),
            mode.generate_slide_6_steps(content["steps"], brand, 7),
            mode.generate_slide_7_cta(brand, 7, content["cta"])
        ]
        
        # Viral prediction
        viral_analysis = self.viral_predictor.analyze(content, topic)
        
        return {
            "topic": topic,
            "mode": mode_name,
            "mode_info": {
                "name": mode.name,
                "description": mode.description,
                "audience": mode.audience
            },
            "slides": slides,
            "brand": brand,
            "content": content,
            "viral_analysis": viral_analysis,
            "variants": variants,
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "language": language,
                "ab_test": ab_test
            }
        }
    
    def _detect_mode(self, topic: str) -> str:
        """Auto-detect best mode for topic"""
        topic_lower = topic.lower()
        
        keywords_map = {
            "creator": ["coach", "creator", "influencer", "personal brand", "course"],
            "wellness": ["health", "wellness", "yoga", "fitness", "organic", "meditation"],
            "lifestyle": ["beauty", "fashion", "travel", "food", "lifestyle", "decor"],
            "corporate": ["consulting", "finance", "legal", "b2b", "enterprise"]
        }
        
        for mode, keywords in keywords_map.items():
            if any(word in topic_lower for word in keywords):
                return mode
        
        return "startup"
    
    async def export_batch_png(self, carousel: Dict, name: Optional[str] = None) -> List[str]:
        """Export all slides to PNG in batch"""
        if name is None:
            name = f"carousel_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        exporter = PNGExporter()
        
        # Create batch directory
        batch_dir = self.output_dir / name
        batch_dir.mkdir(exist_ok=True)
        
        paths = []
        for i, slide in enumerate(carousel["slides"], 1):
            slide_path = str(batch_dir / f"slide_{i:02d}.png")
            await exporter.export_slide_async(slide, slide_path)
            paths.append(slide_path)
        
        return paths
    
    def save_html(self, carousel: Dict, name: Optional[str] = None) -> str:
        """Save carousel as HTML with viral analytics"""
        if name is None:
            name = f"carousel_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        output_path = self.output_dir / f"{name}.html"
        
        # Add viral score badge
        viral = carousel.get("viral_analysis", {})
        score = viral.get("viral_score", 0)
        rating = viral.get("rating", "")
        
        score_color = "#22c55e" if score >= 70 else "#f59e0b" if score >= 55 else "#ef4444"
        
        html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{carousel['topic']} - Instagram Carousel</title>
    <style>
        body {{
            background: #0a0a0a;
            padding: 40px;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            color: #fff;
        }}
        .header {{
            text-align: center;
            margin-bottom: 40px;
            padding: 30px;
            background: linear-gradient(135deg, #1a1a2e, #16213e);
            border-radius: 16px;
            border: 1px solid rgba(255,255,255,0.1);
        }}
        .header h1 {{
            font-size: 36px;
            margin-bottom: 12px;
            background: linear-gradient(90deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        .viral-score {{
            display: inline-flex;
            align-items: center;
            gap: 12px;
            padding: 12px 24px;
            background: rgba(255,255,255,0.05);
            border-radius: 50px;
            margin-top: 16px;
        }}
        .score-badge {{
            font-size: 32px;
            font-weight: 700;
            color: {score_color};
        }}
        .score-label {{
            font-size: 14px;
            color: #888;
        }}
        .meta {{
            display: flex;
            justify-content: center;
            gap: 32px;
            margin-top: 20px;
            flex-wrap: wrap;
        }}
        .meta-item {{
            text-align: center;
        }}
        .meta-value {{
            font-size: 20px;
            font-weight: 600;
            color: #fff;
        }}
        .meta-label {{
            font-size: 12px;
            color: #666;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        .carousel-container {{
            display: flex;
            flex-direction: column;
            gap: 40px;
            align-items: center;
        }}
        .slide-wrapper {{
            background: #000;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.5);
        }}
        .slide-label {{
            color: #888;
            font-size: 14px;
            margin-bottom: 12px;
            text-align: center;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        iframe {{
            border: none;
            width: 1080px;
            height: 1350px;
            background: white;
        }}
        .analytics {{
            margin-top: 40px;
            padding: 30px;
            background: rgba(255,255,255,0.03);
            border-radius: 16px;
        }}
        .analytics h2 {{
            font-size: 24px;
            margin-bottom: 20px;
        }}
        .recommendations {{
            list-style: none;
            padding: 0;
        }}
        .recommendations li {{
            padding: 12px 0;
            border-bottom: 1px solid rgba(255,255,255,0.1);
            color: #ccc;
        }}
        .recommendations li:last-child {{
            border-bottom: none;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>{carousel['topic']}</h1>
        <p>{carousel['mode_info']['name']} • {carousel['mode_info']['description']}</p>
        <div class="viral-score">
            <span class="score-badge">{score}/100</span>
            <span class="score-label">{rating}</span>
        </div>
        <div class="meta">
            <div class="meta-item">
                <div class="meta-value">{carousel.get('content', {}).get('best_time', 'TBD')}</div>
                <div class="meta-label">Best Time</div>
            </div>
            <div class="meta-item">
                <div class="meta-value">{len(carousel.get('content', {}).get('hashtags', []))}</div>
                <div class="meta-label">Hashtags</div>
            </div>
            <div class="meta-item">
                <div class="meta-value">{carousel['mode']}</div>
                <div class="meta-label">Design Mode</div>
            </div>
        </div>
    </div>
    <div class="carousel-container">
        {''.join([f'<div class="slide-wrapper"><div class="slide-label">Slide {i+1}</div>{slide}</div>' for i, slide in enumerate(carousel['slides'])])}
    </div>
    {f'''<div class="analytics">
        <h2>🚀 Viral Optimization Tips</h2>
        <ul class="recommendations">
            {''.join([f'<li>💡 {rec}</li>' for rec in viral.get('recommendations', [])])}
        </ul>
    </div>''' if viral.get('recommendations') else ''}
</body>
</html>'''
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return str(output_path)


async def main_async():
    """Async CLI entry point"""
    parser = argparse.ArgumentParser(description='Carousel Pro v3.0 - AI-Powered Instagram Carousels')
    parser.add_argument('topic', help='Topic for the carousel')
    parser.add_argument('--mode', '-m', default='auto',
                       choices=['auto', 'corporate', 'startup', 'lifestyle', 'wellness', 'creator'],
                       help='Design mode (default: auto-detect)')
    parser.add_argument('--export', '-e', choices=['html', 'png', 'both', 'zip'],
                       default='html', help='Export format')
    parser.add_argument('--preview', '-p', action='store_true',
                       help='Generate Instagram preview')
    parser.add_argument('--preview-slide', type=int, default=1,
                       help='Which slide to preview (1-7)')
    parser.add_argument('--name', '-n', help='Output name')
    parser.add_argument('--brand', help='Brand name')
    parser.add_argument('--handle', help='Social media handle')
    parser.add_argument('--language', '-l', default='en',
                       help='Content language (en, ru, es, etc.)')
    parser.add_argument('--ab-test', action='store_true',
                       help='Generate A/B test variants')
    parser.add_argument('--list-modes', action='store_true',
                       help='List available modes')
    parser.add_argument('--batch-png', action='store_true',
                       help='Export all slides as PNG batch')
    
    args = parser.parse_args()
    
    if args.list_modes:
        print("\n🎨 Available Design Modes:\n")
        for key, info in list_modes().items():
            print(f"  {key:12} │ {info['name']:15} │ {info['description']}")
        print()
        return
    
    generator = CarouselProV3()
    
    brand = None
    if args.brand or args.handle:
        brand = {
            "name": args.brand or "AI Genesis",
            "handle": args.handle or "@aigenesis.ai",
            "tagline": "Automate your business"
        }
    
    print(f"\n🎨 Carousel Pro v3.0")
    print(f"   Topic: {args.topic}")
    print(f"   Mode: {args.mode}")
    if args.ab_test:
        print(f"   A/B Testing: Enabled")
    
    carousel = await generator.generate_carousel(
        args.topic, args.mode, brand, args.language, args.ab_test
    )
    
    print(f"   Design: {carousel['mode_info']['name']}")
    print(f"   Viral Score: {carousel['viral_analysis']['viral_score']}/100 {carousel['viral_analysis']['rating']}")
    
    name = args.name or f"carousel_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    results = []
    
    if args.export in ['html', 'both']:
        html_path = generator.save_html(carousel, name)
        results.append(f"📄 HTML: {html_path}")
    
    if args.export in ['png', 'both', 'zip'] or args.batch_png:
        print("\n📸 Exporting PNG batch...")
        png_paths = await generator.export_batch_png(carousel, name)
        results.append(f"🖼️  PNGs: {len(png_paths)} slides exported")
        results.append(f"   Location: /tmp/carousel_output/{name}/")
    
    if args.export == 'zip':
        zip_path = f"/tmp/carousel_output/{name}.zip"
        create_zip_archive(f"/tmp/carousel_output/{name}", zip_path)
        results.append(f"📦 ZIP: {zip_path}")
    
    if args.preview:
        print(f"\n📱 Generating preview...")
        preview_gen = InstagramPreview()
        preview_path = f"/tmp/carousel_output/{name}_preview.png"
        await preview_gen.generate_preview(
            png_paths[args.preview_slide - 1], 
            args.preview_slide, 
            7, 
            preview_path
        )
        results.append(f"👁️  Preview: {preview_path}")
    
    if carousel.get('variants'):
        print("\n🔄 A/B Test Variants:")
        for variant_id, variant in carousel['variants'].items():
            print(f"   Variant {variant_id}: {variant['approach'].upper()} - '{variant['hook']}'")
    
    if carousel['viral_analysis'].get('recommendations'):
        print("\n💡 Optimization Tips:")
        for tip in carousel['viral_analysis']['recommendations'][:3]:
            print(f"   • {tip}")
    
    print("\n✅ Carousel generated successfully!\n")
    for result in results:
        print(f"   {result}")
    print()


def main():
    """CLI entry point"""
    asyncio.run(main_async())


if __name__ == "__main__":
    main()
