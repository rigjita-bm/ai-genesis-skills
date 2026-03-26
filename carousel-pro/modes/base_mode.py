"""
Base Mode Class for Instagram Carousel Generator
Multi-Mode Design System Foundation
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Tuple


class BaseMode(ABC):
    """
    Abstract base class for all carousel design modes.
    Each mode defines its own visual language, typography, colors, and layout rules.
    """
    
    # Mode identification
    name: str = "Base"
    description: str = "Base mode"
    audience: str = "General"
    
    # Typography - Override in subclasses
    heading_font: str = "Inter"
    body_font: str = "Inter"
    heading_weights: List[int] = [600, 700]
    body_weight: int = 400
    
    # Base colors - Override in subclasses
    primary: str = "#6366F1"
    
    # Layout settings
    hero_font_size: int = 32
    heading_font_size: int = 28
    body_font_size: int = 14
    tag_font_size: int = 10
    
    # Alignment: "center" | "flex-start" | "flex-end" | "asymmetric"
    content_alignment: str = "center"
    
    # Visual effects flags
    use_gradients: bool = False
    use_glassmorphism: bool = False
    use_asymmetric: bool = False
    use_glow_effects: bool = False
    use_noise_texture: bool = False
    
    # Spacing
    slide_padding: int = 36
    bottom_padding: int = 52  # Space for progress bar
    whitespace_scale: float = 1.0  # Multiplier for spacing
    
    # Aspect ratio (Instagram standard)
    SLIDE_WIDTH: int = 1080
    SLIDE_HEIGHT: int = 1350
    
    def __init__(self):
        """Initialize mode with generated palette"""
        self.palette = self.generate_palette()
    
    def hex_to_rgb(self, hex_color: str) -> Tuple[int, int, int]:
        """Convert hex color to RGB tuple"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    def rgb_to_hex(self, rgb: Tuple[int, int, int]) -> str:
        """Convert RGB tuple to hex"""
        return '#{:02x}{:02x}{:02x}'.format(*rgb)
    
    def adjust_brightness(self, hex_color: str, percent: float) -> str:
        """Lighten or darken a hex color by percentage"""
        rgb = self.hex_to_rgb(hex_color)
        factor = 1 + (percent / 100)
        new_rgb = tuple(min(255, max(0, int(c * factor))) for c in rgb)
        return self.rgb_to_hex(new_rgb)
    
    def generate_palette(self) -> Dict[str, str]:
        """
        Generate 6-token color palette from primary color.
        Override for custom palette logic.
        """
        rgb = self.hex_to_rgb(self.primary)
        # Warm if more red than blue
        is_warm = rgb[0] > rgb[2]
        
        return {
            "BRAND_PRIMARY": self.primary,
            "BRAND_LIGHT": self.adjust_brightness(self.primary, 20),
            "BRAND_DARK": self.adjust_brightness(self.primary, -30),
            "LIGHT_BG": "#FDF8F3" if is_warm else "#F8F9FA",
            "LIGHT_BORDER": "#E8E4E0" if is_warm else "#E2E4E8",
            "DARK_BG": "#1A1918" if is_warm else "#0F172A"
        }
    
    def get_fonts_css(self) -> str:
        """Generate Google Fonts import URL"""
        fonts = set([self.heading_font, self.body_font])
        font_params = []
        for font in fonts:
            font_encoded = font.replace(' ', '+')
            font_params.append(f"family={font_encoded}:wght@400;600;700")
        
        return f"https://fonts.googleapis.com/css2?{'&'.join(font_params)}&display=swap"
    
    def get_base_styles(self) -> str:
        """Generate base CSS styles for this mode"""
        p = self.palette
        
        styles = f"""
        <style>
            @import url('{self.get_fonts_css()}');
            
            .slide {{
                width: {self.SLIDE_WIDTH}px;
                height: {self.SLIDE_HEIGHT}px;
                position: relative;
                display: flex;
                flex-direction: column;
                box-sizing: border-box;
                font-family: '{self.body_font}', sans-serif;
                overflow: hidden;
            }}
            
            .serif {{
                font-family: '{self.heading_font}', serif;
            }}
            
            .sans {{
                font-family: '{self.body_font}', sans-serif;
            }}
            
            .tag-label {{
                display: inline-block;
                font-size: {self.tag_font_size}px;
                font-weight: 600;
                letter-spacing: 2px;
                text-transform: uppercase;
                margin-bottom: 16px;
            }}
            
            h1, h2, h3 {{
                font-family: '{self.heading_font}', serif;
                font-weight: {self.heading_weights[0]};
                letter-spacing: -0.3px;
                line-height: 1.15;
                margin: 0;
            }}
            
            p {{
                font-size: {self.body_font_size}px;
                line-height: 1.5;
                margin: 0;
            }}
        </style>
        """
        return styles
    
    def progress_bar(self, index: int, total: int, is_light: bool) -> str:
        """Generate progress bar HTML"""
        pct = ((index + 1) / total) * 100
        p = self.palette
        
        if is_light:
            track = "rgba(0,0,0,0.08)"
            fill = p['BRAND_PRIMARY']
            label = "rgba(0,0,0,0.3)"
        else:
            track = "rgba(255,255,255,0.12)"
            fill = "#fff"
            label = "rgba(255,255,255,0.4)"
        
        return f'''<div style="position:absolute;bottom:0;left:0;right:0;padding:16px 28px 20px;z-index:10;display:flex;align-items:center;gap:10px;">
  <div style="flex:1;height:3px;background:{track};border-radius:2px;overflow:hidden;">
    <div style="height:100%;width:{pct}%;background:{fill};border-radius:2px;"></div>
  </div>
  <span style="font-size:11px;color:{label};font-weight:500;">{index + 1}/{total}</span>
</div>'''
    
    def swipe_arrow(self, is_light: bool, is_last: bool = False) -> str:
        """Generate swipe arrow HTML (empty for last slide)"""
        if is_last:
            return ""
        
        p = self.palette
        
        if is_light:
            bg = "rgba(0,0,0,0.06)"
            stroke = "rgba(0,0,0,0.25)"
        else:
            bg = "rgba(255,255,255,0.08)"
            stroke = "rgba(255,255,255,0.35)"
        
        return f'''<div style="position:absolute;right:0;top:0;bottom:0;width:48px;z-index:9;display:flex;align-items:center;justify-content:center;background:linear-gradient(to right,transparent,{bg});">
  <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
    <path d="M9 6l6 6-6 6" stroke="{stroke}" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
  </svg>
</div>'''
    
    def logo_lockup(self, brand_name: str, is_light: bool = True) -> str:
        """Generate logo lockup (initial in circle + brand name)"""
        initial = brand_name[0].upper() if brand_name else "A"
        text_color = "#1A1A1A" if is_light else "#FFFFFF"
        p = self.palette
        
        return f'''<div style="display:flex;align-items:center;gap:12px;">
  <div style="width:40px;height:40px;border-radius:50%;background:{p['BRAND_PRIMARY']};display:flex;align-items:center;justify-content:center;">
    <span style="color:#fff;font-size:18px;font-weight:600;">{initial}</span>
  </div>
  <span style="font-size:13px;font-weight:600;letter-spacing:0.5px;color:{text_color};">{brand_name}</span>
</div>'''
    
    @abstractmethod
    def generate_slide_1_hero(self, content: str, brand: Dict, total_slides: int) -> str:
        """Slide 1: Hook/Hero - Must be implemented by each mode"""
        pass
    
    @abstractmethod
    def generate_slide_2_problem(self, content: str, brand: Dict, total_slides: int) -> str:
        """Slide 2: Problem/Pain point"""
        pass
    
    @abstractmethod
    def generate_slide_3_solution(self, content: str, brand: Dict, total_slides: int) -> str:
        """Slide 3: Solution/Answer"""
        pass
    
    @abstractmethod
    def generate_slide_4_features(self, features: List[str], brand: Dict, total_slides: int) -> str:
        """Slide 4: Features/Benefits"""
        pass
    
    @abstractmethod
    def generate_slide_5_details(self, content: str, brand: Dict, total_slides: int) -> str:
        """Slide 5: Details/Depth"""
        pass
    
    @abstractmethod
    def generate_slide_6_steps(self, steps: List[str], brand: Dict, total_slides: int) -> str:
        """Slide 6: How-to/Process"""
        pass
    
    @abstractmethod
    def generate_slide_7_cta(self, brand: Dict, total_slides: int, cta_text: str = "Связаться") -> str:
        """Slide 7: Call to Action (no arrow)"""
        pass
    
    def get_slide_sequence(self) -> List[str]:
        """Return default 7-slide sequence"""
        return [
            "hero", "problem", "solution", "features", 
            "details", "steps", "cta"
        ]
