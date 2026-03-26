"""
PNG Export Module for Carousel Pro
Converts HTML slides to PNG images using Playwright
"""

import asyncio
import os
from pathlib import Path
from typing import List, Optional
from playwright.async_api import async_playwright


class PNGExporter:
    """Export HTML carousels to PNG images"""
    
    # Instagram carousel dimensions
    WIDTH = 1080
    HEIGHT = 1350
    
    def __init__(self, output_dir: str = "/tmp/carousel_exports"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    async def export_slide(self, html_content: str, output_path: str) -> str:
        """Export single HTML slide to PNG"""
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page()
            
            # Set viewport to Instagram dimensions
            await page.set_viewport_size({
                "width": self.WIDTH,
                "height": self.HEIGHT
            })
            
            # Load HTML content
            await page.set_content(html_content)
            
            # Wait for fonts to load
            await page.wait_for_timeout(1000)
            
            # Take screenshot
            await page.screenshot(
                path=output_path,
                full_page=False,
                type="png"
            )
            
            await browser.close()
        
        return output_path
    
    async def export_carousel(self, slides_html: List[str], name: str) -> List[str]:
        """Export all slides of a carousel"""
        output_paths = []
        
        # Create subdirectory for this carousel
        carousel_dir = self.output_dir / name
        carousel_dir.mkdir(exist_ok=True)
        
        for i, html in enumerate(slides_html):
            output_path = str(carousel_dir / f"slide_{i+1:02d}.png")
            await self.export_slide(html, output_path)
            output_paths.append(output_path)
        
        return output_paths
    
    def export_slide_sync(self, html_content: str, output_path: str) -> str:
        """Synchronous wrapper for export_slide"""
        return asyncio.run(self.export_slide(html_content, output_path))
    
    def export_carousel_sync(self, slides_html: List[str], name: str) -> List[str]:
        """Synchronous wrapper for export_carousel"""
        return asyncio.run(self.export_carousel(slides_html, name))


class InstagramPreview:
    """Generate Instagram preview with iPhone frame"""
    
    # iPhone 14 Pro dimensions for mockup
    MOCKUP_WIDTH = 430
    MOCKUP_HEIGHT = 932
    SCREEN_X = 27
    SCREEN_Y = 125
    SCREEN_WIDTH = 393
    SCREEN_HEIGHT = 852
    
    def __init__(self):
        self.exporter = PNGExporter()
    
    def generate_preview_html(self, slide_png_path: str, slide_number: int, total_slides: int) -> str:
        """Generate HTML with iPhone frame containing the slide"""
        
        # Read the PNG and convert to base64
        import base64
        with open(slide_png_path, 'rb') as f:
            png_base64 = base64.b64encode(f.read()).decode()
        
        html = f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 40px;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        }}
        .preview-container {{
            display: flex;
            gap: 40px;
            align-items: center;
        }}
        .iphone-frame {{
            width: {self.MOCKUP_WIDTH}px;
            height: {self.MOCKUP_HEIGHT}px;
            background: #000;
            border-radius: 55px;
            padding: 12px;
            box-shadow: 
                0 0 0 2px #333,
                0 25px 50px -12px rgba(0,0,0,0.8),
                0 0 100px rgba(99,102,241,0.2);
            position: relative;
        }}
        .iphone-notch {{
            position: absolute;
            top: 12px;
            left: 50%;
            transform: translateX(-50%);
            width: 126px;
            height: 37px;
            background: #000;
            border-radius: 20px;
            z-index: 10;
        }}
        .iphone-screen {{
            width: 100%;
            height: 100%;
            background: #000;
            border-radius: 43px;
            overflow: hidden;
            position: relative;
        }}
        .slide-image {{
            width: 100%;
            height: 100%;
            object-fit: contain;
            background: #000;
        }}
        .instagram-ui {{
            position: absolute;
            bottom: 0;
            left: 0;
            right: 0;
            height: 80px;
            background: linear-gradient(to top, rgba(0,0,0,0.9), transparent);
            display: flex;
            justify-content: space-around;
            align-items: center;
            padding: 0 20px;
        }}
        .ig-icon {{
            width: 28px;
            height: 28px;
            opacity: 0.9;
        }}
        .info-panel {{
            color: #fff;
            max-width: 400px;
        }}
        .info-panel h2 {{
            font-size: 28px;
            margin-bottom: 16px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        .info-panel .meta {{
            color: #888;
            font-size: 14px;
            margin-bottom: 20px;
        }}
        .slide-counter {{
            display: inline-flex;
            align-items: center;
            gap: 8px;
            background: rgba(255,255,255,0.1);
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 14px;
            margin-bottom: 20px;
        }}
        .dots {{
            display: flex;
            gap: 6px;
        }}
        .dot {{
            width: 6px;
            height: 6px;
            border-radius: 50%;
            background: rgba(255,255,255,0.3);
        }}
        .dot.active {{
            background: #fff;
        }}
        .specs {{
            background: rgba(255,255,255,0.05);
            border-radius: 12px;
            padding: 20px;
            margin-top: 20px;
        }}
        .specs h3 {{
            font-size: 12px;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: #888;
            margin-bottom: 12px;
        }}
        .spec-row {{
            display: flex;
            justify-content: space-between;
            padding: 8px 0;
            border-bottom: 1px solid rgba(255,255,255,0.1);
            font-size: 14px;
        }}
        .spec-row:last-child {{
            border-bottom: none;
        }}
    </style>
</head>
<body>
    <div class="preview-container">
        <div class="iphone-frame">
            <div class="iphone-notch"></div>
            <div class="iphone-screen">
                <img src="data:image/png;base64,{png_base64}" class="slide-image" alt="Slide {slide_number}">
                <div class="instagram-ui">
                    <svg class="ig-icon" fill="white" viewBox="0 0 24 24"><path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zm0 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 6.163 6.162 6.163 6.162-2.759 6.162-6.163c0-3.403-2.759-6.162-6.162-6.162zm0 10.162c-2.209 0-4-1.79-4-4 0-2.209 1.791-4 4-4s4 1.791 4 4c0 2.21-1.791 4-4 4zm6.406-11.845c-.796 0-1.441.645-1.441 1.44s.645 1.44 1.441 1.44c.795 0 1.439-.645 1.439-1.44s-.644-1.44-1.439-1.44z"/></svg>
                    <svg class="ig-icon" fill="white" viewBox="0 0 24 24"><path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/></svg>
                    <svg class="ig-icon" fill="white" viewBox="0 0 24 24"><path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"/></svg>
                </div>
            </div>
        </div>
        
        <div class="info-panel">
            <div class="slide-counter">
                <span>Slide {slide_number} of {total_slides}</span>
                <div class="dots">
                    {''.join([f'<div class="dot{" active" if i+1 == slide_number else ""}"></div>' for i in range(total_slides)])}
                </div>
            </div>
            <h2>Instagram Carousel Preview</h2>
            <p class="meta">See exactly how your carousel will appear on Instagram</p>
            
            <div class="specs">
                <h3>Specifications</h3>
                <div class="spec-row">
                    <span>Dimensions</span>
                    <span>1080 × 1350 px</span>
                </div>
                <div class="spec-row">
                    <span>Aspect Ratio</span>
                    <span>4:5 (Portrait)</span>
                </div>
                <div class="spec-row">
                    <span>Format</span>
                    <span>PNG (High Quality)</span>
                </div>
                <div class="spec-row">
                    <span>Color Profile</span>
                    <span>sRGB</span>
                </div>
            </div>
        </div>
    </div>
</body>
</html>'''
        
        return html
    
    async def generate_preview(self, slide_png_path: str, slide_number: int, total_slides: int, output_path: str):
        """Generate preview image with iPhone frame"""
        preview_html = self.generate_preview_html(slide_png_path, slide_number, total_slides)
        
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page()
            
            await page.set_viewport_size({"width": 1200, "height": 1000})
            await page.set_content(preview_html)
            await page.wait_for_timeout(500)
            
            await page.screenshot(path=output_path, full_page=True, type="png")
            await browser.close()
        
        return output_path


def create_zip_archive(source_dir: str, output_path: str) -> str:
    """Create ZIP archive of carousel images"""
    import zipfile
    
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(source_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, source_dir)
                zipf.write(file_path, arcname)
    
    return output_path
