"""
Carousel Pro - Main Controller
Multi-Mode Instagram Carousel Generator
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

# Add modes package to path
sys.path.insert(0, str(Path(__file__).parent))

from modes import get_mode, list_modes, MODES
from png_export import PNGExporter, InstagramPreview, create_zip_archive


class CarouselPro:
    """Main controller for carousel generation"""
    
    def __init__(self):
        self.output_dir = Path("/tmp/carousel_output")
        self.output_dir.mkdir(exist_ok=True)
    
    def generate_content(self, topic: str, mode_name: str = "auto") -> Dict:
        """Generate carousel content for a topic"""
        
        # Content templates by topic type (simplified - in production use AI)
        templates = {
            "business": {
                "hook": f"Transform Your {topic} with AI Automation",
                "problem": f"Still managing {topic} manually?",
                "solution": f"AI-powered {topic} automation",
                "features": ["24/7 Operation", "Smart Analytics", "Auto-Responses", "Cost Reduction"],
                "details": "Proven Results",
                "steps": ["Connect your systems", "Train the AI", "Launch automation"],
                "cta": "Get Started"
            },
            "product": {
                "hook": f"Meet the Future of {topic}",
                "problem": f"Tired of outdated {topic} solutions?",
                "solution": f"Revolutionary {topic} technology",
                "features": ["Cutting-edge Design", "Premium Quality", "Easy Setup", "24/7 Support"],
                "details": "Why Choose Us",
                "steps": ["Order today", "Quick delivery", "Enjoy benefits"],
                "cta": "Order Now"
            },
            "service": {
                "hook": f"Expert {topic} Services",
                "problem": f"Struggling with {topic}?",
                "solution": f"Professional {topic} solutions",
                "features": ["Certified Experts", "Fast Turnaround", "Guaranteed Quality", "Fair Pricing"],
                "details": "Our Approach",
                "steps": ["Free consultation", "Custom solution", "Ongoing support"],
                "cta": "Book Call"
            }
        }
        
        # Auto-detect content type
        topic_lower = topic.lower()
        if any(word in topic_lower for word in ["saas", "ai", "app", "tech", "software"]):
            template = templates["business"]
        elif any(word in topic_lower for word in ["product", "device", "tool", "gadget"]):
            template = templates["product"]
        else:
            template = templates["service"]
        
        return template
    
    def generate_carousel(self, topic: str, mode_name: str = "startup", 
                         brand: Optional[Dict] = None) -> Dict:
        """Generate complete carousel with all 7 slides"""
        
        # Get mode
        if mode_name == "auto":
            mode_name = self._detect_mode(topic)
        
        mode = get_mode(mode_name)
        if not mode:
            raise ValueError(f"Unknown mode: {mode_name}. Available: {list(MODES.keys())}")
        
        # Default brand
        if brand is None:
            brand = {
                "name": "AI Genesis",
                "handle": "@aigenesis.ai",
                "tagline": "Automate your business"
            }
        
        # Generate content
        content = self.generate_content(topic, mode_name)
        
        # Generate all 7 slides
        slides = [
            mode.generate_slide_1_hero(content["hook"], brand, 7),
            mode.generate_slide_2_problem(content["problem"], brand, 7),
            mode.generate_slide_3_solution(content["solution"], brand, 7),
            mode.generate_slide_4_features(content["features"], brand, 7),
            mode.generate_slide_5_details(content["details"], brand, 7),
            mode.generate_slide_6_steps(content["steps"], brand, 7),
            mode.generate_slide_7_cta(brand, 7, content["cta"])
        ]
        
        return {
            "topic": topic,
            "mode": mode_name,
            "mode_info": {
                "name": mode.name,
                "description": mode.description,
                "audience": mode.audience
            },
            "slides": slides,
            "brand": brand
        }
    
    def _detect_mode(self, topic: str) -> str:
        """Auto-detect best mode for topic"""
        topic_lower = topic.lower()
        
        # Creator keywords
        if any(word in topic_lower for word in ["coach", "creator", "influencer", "personal brand", "course"]):
            return "creator"
        
        # Wellness keywords
        if any(word in topic_lower for word in ["health", "wellness", "yoga", "fitness", "organic", "supplement", "meditation"]):
            return "wellness"
        
        # Lifestyle keywords
        if any(word in topic_lower for word in ["beauty", "fashion", "travel", "food", "lifestyle", "decor", "design"]):
            return "lifestyle"
        
        # Corporate keywords
        if any(word in topic_lower for word in ["consulting", "finance", "legal", "b2b", "enterprise", "corporate"]):
            return "corporate"
        
        # Default to startup
        return "startup"
    
    def export_to_png(self, carousel: Dict, name: Optional[str] = None) -> List[str]:
        """Export carousel to PNG images"""
        if name is None:
            name = f"carousel_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        exporter = PNGExporter()
        paths = exporter.export_carousel_sync(carousel["slides"], name)
        
        return paths
    
    def generate_preview(self, carousel: Dict, slide_number: int = 1) -> str:
        """Generate Instagram preview for a specific slide"""
        exporter = PNGExporter()
        preview_gen = InstagramPreview()
        
        # First export the slide to PNG
        temp_dir = self.output_dir / "temp_preview"
        temp_dir.mkdir(exist_ok=True)
        
        slide_path = str(temp_dir / f"slide_{slide_number:02d}.png")
        exporter.export_slide_sync(carousel["slides"][slide_number - 1], slide_path)
        
        # Generate preview with iPhone frame
        preview_path = str(self.output_dir / f"preview_slide_{slide_number:02d}.png")
        
        import asyncio
        asyncio.run(preview_gen.generate_preview(
            slide_path, slide_number, len(carousel["slides"]), preview_path
        ))
        
        return preview_path
    
    def save_html(self, carousel: Dict, name: Optional[str] = None) -> str:
        """Save carousel as HTML file"""
        if name is None:
            name = f"carousel_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        output_path = self.output_dir / f"{name}.html"
        
        html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{carousel['topic']} - Instagram Carousel</title>
    <style>
        body {{
            background: #1a1a1a;
            padding: 40px;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
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
        .info {{
            color: #fff;
            text-align: center;
            margin-bottom: 40px;
        }}
        .info h1 {{
            font-size: 32px;
            margin-bottom: 8px;
        }}
        .info p {{
            color: #888;
        }}
    </style>
</head>
<body>
    <div class="info">
        <h1>{carousel['topic']}</h1>
        <p>Mode: {carousel['mode_info']['name']} | {carousel['mode_info']['description']}</p>
    </div>
    <div class="carousel-container">
        {''.join([f'<div class="slide-wrapper"><div class="slide-label">Slide {i+1}</div>{slide}</div>' for i, slide in enumerate(carousel['slides'])])}
    </div>
</body>
</html>'''
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return str(output_path)


def main():
    """CLI entry point"""
    parser = argparse.ArgumentParser(description='Generate Instagram carousels')
    parser.add_argument('topic', help='Topic for the carousel')
    parser.add_argument('--mode', '-m', default='startup', 
                       choices=['auto', 'corporate', 'startup', 'lifestyle', 'wellness', 'creator'],
                       help='Design mode (default: auto-detect)')
    parser.add_argument('--export', '-e', choices=['html', 'png', 'both', 'zip'],
                       default='html', help='Export format')
    parser.add_argument('--preview', '-p', action='store_true',
                       help='Generate Instagram preview')
    parser.add_argument('--preview-slide', type=int, default=1,
                       help='Which slide to preview (1-7, default: 1)')
    parser.add_argument('--name', '-n', help='Output name')
    parser.add_argument('--brand', help='Brand name')
    parser.add_argument('--handle', help='Social media handle')
    parser.add_argument('--list-modes', action='store_true',
                       help='List available modes')
    
    args = parser.parse_args()
    
    # List modes
    if args.list_modes:
        print("\n📱 Available Design Modes:\n")
        for key, info in list_modes().items():
            print(f"  {key:12} │ {info['name']:15} │ {info['description']}")
        print()
        return
    
    # Initialize generator
    generator = CarouselPro()
    
    # Build brand config
    brand = None
    if args.brand or args.handle:
        brand = {
            "name": args.brand or "AI Genesis",
            "handle": args.handle or "@aigenesis.ai",
            "tagline": "Automate your business"
        }
    
    # Generate carousel
    print(f"\n🎨 Generating carousel for: {args.topic}")
    print(f"   Mode: {args.mode}{' (auto-detected)' if args.mode == 'auto' else ''}")
    
    carousel = generator.generate_carousel(args.topic, args.mode, brand)
    
    print(f"   Design: {carousel['mode_info']['name']} - {carousel['mode_info']['description']}")
    
    # Determine output name
    name = args.name or f"carousel_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    results = []
    
    # Export based on format
    if args.export in ['html', 'both']:
        html_path = generator.save_html(carousel, name)
        results.append(f"📄 HTML: {html_path}")
    
    if args.export in ['png', 'both', 'zip']:
        print("\n📸 Exporting to PNG...")
        png_paths = generator.export_to_png(carousel, name)
        results.append(f"🖼️  PNGs: {len(png_paths)} slides")
        for path in png_paths[:3]:  # Show first 3
            results.append(f"   - {path}")
        if len(png_paths) > 3:
            results.append(f"   ... and {len(png_paths) - 3} more")
    
    if args.export == 'zip':
        import zipfile
        zip_path = f"/tmp/carousel_output/{name}.zip"
        create_zip_archive(f"/tmp/carousel_exports/{name}", zip_path)
        results.append(f"📦 ZIP: {zip_path}")
    
    # Generate preview
    if args.preview:
        print(f"\n📱 Generating Instagram preview (slide {args.preview_slide})...")
        preview_path = generator.generate_preview(carousel, args.preview_slide)
        results.append(f"👁️  Preview: {preview_path}")
    
    # Print results
    print("\n✅ Carousel generated successfully!\n")
    for result in results:
        print(f"   {result}")
    print()


if __name__ == "__main__":
    main()
