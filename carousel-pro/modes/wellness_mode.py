"""
Wellness Mode - Serenity Design System
For: Health, Supplements, Yoga, Meditation, Organic Products
Style: Calm, Natural, Earth Tones, Centered Balance
"""

from typing import Dict, List
from .base_mode import BaseMode


class WellnessMode(BaseMode):
    """
    Serenity mode for wellness and health-focused brands.
    Philosophy: "Breathe, balance, be"
    """
    
    name = "Serenity"
    description = "Health, Yoga, Organic — Calm & Natural"
    audience = "Wellness brands, health products, yoga studios, organic food"
    
    # Typography - Soft, humanist, friendly
    heading_font = "Cormorant Garamond"    # Elegant serif
    body_font = "Nunito Sans"               # Rounded, friendly
    heading_weights = [500, 600]
    body_weight = 400
    
    # Colors - Sage green, sand, natural earth tones
    primary = "#7C9A92"                    # Sage green
    secondary = "#E8DCC4"                  # Sand/beige
    accent = "#D4B896"                     # Warm tan
    
    # Layout - Centered, balanced, breathing room
    hero_font_size = 44
    heading_font_size = 32
    body_font_size = 16                    # Slightly larger for readability
    tag_font_size = 10
    
    content_alignment = "center"
    whitespace_scale = 1.4                 # Most whitespace
    
    # Visual effects - Soft, organic
    use_gradients = True                   # Soft, natural gradients
    use_glassmorphism = False
    use_asymmetric = False                 # Symmetric for balance
    use_glow_effects = False
    use_noise_texture = True               # Natural texture
    
    def generate_palette(self) -> Dict[str, str]:
        """Wellness palette - earth tones, calming"""
        return {
            "BRAND_PRIMARY": self.primary,
            "BRAND_SECONDARY": self.secondary,
            "BRAND_ACCENT": self.accent,
            "SAGE": "#7C9A92",                 # Main sage
            "SAGE_LIGHT": "#A8C4B0",           # Light sage
            "SAGE_DARK": "#5A756B",            # Dark sage
            "SAND": "#E8DCC4",                 # Sand
            "SAND_LIGHT": "#F5F0E6",           # Light sand
            "EARTH": "#8B7355",                # Earth brown
            "CREAM": "#F7F5F3",                # Warm white
            "LIGHT_BG": "#F7F5F3",             # Warm off-white
            "LIGHT_BG_ALT": "#EDE8E0",         # Alternative
            "LIGHT_BORDER": "#DDD8D0",         # Soft border
            "DARK_BG": "#2C3E36",              # Forest green
            "DARK_BG_ALT": "#3D4F45",          # Lighter forest
            "TEXT_PRIMARY": "#2C3E36",         # Dark green text
            "TEXT_SECONDARY": "#6B7B73",       # Muted green
            "TEXT_LIGHT": "#F7F5F3",           # Cream text
            "LEAF": "#6B8E6B",                 # Leaf green
            "STONE": "#9E9A93"                 # Stone gray
        }
    
    def _get_container_style(self, bg_type: str = "cream", alignment: str = "center") -> str:
        """Generate slide container with wellness styling"""
        p = self.palette
        padding = int(self.slide_padding * self.whitespace_scale)
        
        if bg_type == "sage":
            bg = p['SAGE']
        elif bg_type == "sage_light":
            bg = p['SAGE_LIGHT']
        elif bg_type == "sand":
            bg = p['SAND']
        elif bg_type == "cream_alt":
            bg = p['CREAM']
        elif bg_type == "dark":
            bg = p['DARK_BG']
        else:
            bg = p['LIGHT_BG']
        
        return f'''background:{bg};
width:1080px;
height:1350px;
position:relative;
display:flex;
flex-direction:column;
justify-content:{alignment};
align-items:center;
padding:0 {padding}px {self.bottom_padding}px;
box-sizing:border-box;
font-family:'{self.body_font}',sans-serif;'''
    
    def _get_organic_shape(self, shape_type: str = "circle", color: str = "#7C9A92", opacity: float = 0.1) -> str:
        """Generate organic decorative shape"""
        if shape_type == "circle":
            return f"border-radius:50%;background:{color};opacity:{opacity};"
        elif shape_type == "blob":
            return f"border-radius:60% 40% 50% 50%;background:{color};opacity:{opacity};"
        elif shape_type == "leaf":
            return f"border-radius:0 100% 0 100%;background:{color};opacity:{opacity};"
        return ""
    
    def generate_slide_1_hero(self, content: str, brand: Dict, total_slides: int) -> str:
        """Slide 1: Calm hero with breathing space"""
        p = self.palette
        
        html = f'''<div style="{self._get_container_style('cream', 'center')};">
  <!-- Organic decorative elements -->
  <div style="position:absolute;top:80px;left:80px;width:100px;height:100px;{self._get_organic_shape('circle', p['SAGE_LIGHT'], 0.3)}"></div>
  <div style="position:absolute;top:150px;right:100px;width:60px;height:60px;{self._get_organic_shape('circle', p['SAND'], 0.5)}"></div>
  <div style="position:absolute;bottom:200px;left:120px;width:80px;height:80px;{self._get_organic_shape('blob', p['SAGE'], 0.15)}"></div>
  
  <div style="position:relative;z-index:2;text-align:center;max-width:800px;">
    <div style="display:flex;align-items:center;justify-content:center;gap:12px;margin-bottom:40px;">
      <div style="width:50px;height:50px;border-radius:50%;background:{p['SAGE']};display:flex;align-items:center;justify-content:center;">
        <span style="color:#fff;font-size:20px;">🌿</span>
      </div>
      <span style="font-size:14px;font-weight:600;letter-spacing:2px;color:{p['SAGE_DARK']};text-transform:uppercase;">
        {brand.get('name', 'Wellness')}
      </span>
    </div>
    
    <div style="margin-top:20px;">
      <span class="sans" style="display:inline-block;font-size:10px;font-weight:600;letter-spacing:3px;color:{p['SAGE_DARK']};text-transform:uppercase;background:{p['SAND']};padding:10px 24px;border-radius:100px;">
        Natural Wellness
      </span>
      
      <h1 class="serif" style="font-size:{self.hero_font_size}px;
                            font-weight:500;
                            color:{p['TEXT_PRIMARY']};
                            line-height:1.15;
                            margin:50px 0;">
        {content}
      </h1>
      
      <div style="width:60px;height:1px;background:{p['SAGE']};margin:0 auto;"></div>
      
      <p class="sans" style="font-size:16px;color:{p['TEXT_SECONDARY']};line-height:1.7;margin-top:40px;">
        {brand.get('tagline', 'Nurture your body, calm your mind')}
      </p>
    </div>
  </div>
  
  {self.swipe_arrow(is_light=True)}
  {self.progress_bar(0, total_slides, is_light=True)}
</div>'''
        
        return self.get_base_styles() + html
    
    def generate_slide_2_problem(self, content: str, brand: Dict, total_slides: int) -> str:
        """Slide 2: Problem with calming dark background"""
        p = self.palette
        
        html = f'''<div style="{self._get_container_style('dark', 'center')};">
  <div style="position:absolute;top:60px;right:60px;width:150px;height:150px;{self._get_organic_shape('circle', p['SAGE'], 0.1)}"></div>
  
  <div style="position:relative;z-index:2;text-align:center;max-width:750px;">
    <span style="font-size:48px;margin-bottom:30px;display:block;">😔</span>
    
    <span class="sans" style="font-size:10px;font-weight:600;letter-spacing:3px;color:{p['SAGE_LIGHT']};text-transform:uppercase;">
      The Challenge
    </span>
    
    <h2 class="serif" style="font-size:{self.heading_font_size}px;
                          font-weight:500;
                          color:{p['TEXT_LIGHT']};
                          line-height:1.25;
                          margin:30px 0;">
      {content}
    </h2>
    
    <div style="display:flex;justify-content:center;gap:20px;margin-top:40px;">
      <div style="text-align:center;padding:20px;">
        <span style="font-size:32px;">😫</span>
        <p style="font-size:13px;color:rgba(247,245,243,0.6);margin-top:8px;">Stressed</p>
      </div>
      <div style="text-align:center;padding:20px;">
        <span style="font-size:32px;">😴</span>
        <p style="font-size:13px;color:rgba(247,245,243,0.6);margin-top:8px;">Tired</p>
      </div>
      <div style="text-align:center;padding:20px;">
        <span style="font-size:32px;">🤒</span>
        <p style="font-size:13px;color:rgba(247,245,243,0.6);margin-top:8px;">Unwell</p>
      </div>
    </div>
  </div>
  
  {self.swipe_arrow(is_light=False)}
  {self.progress_bar(1, total_slides, is_light=False)}
</div>'''
        
        return html
    
    def generate_slide_3_solution(self, content: str, brand: Dict, total_slides: int) -> str:
        """Slide 3: Solution with sage background"""
        p = self.palette
        
        html = f'''<div style="{self._get_container_style('sage', 'center')};">
  <div style="position:absolute;bottom:0;left:0;right:0;height:300px;background:linear-gradient(to top,{p['SAGE_DARK']}30,transparent);"></div>
  
  <div style="position:relative;z-index:2;text-align:center;max-width:800px;">
    <span style="font-size:56px;margin-bottom:20px;display:block;">✨</span>
    
    <span class="sans" style="font-size:10px;font-weight:600;letter-spacing:3px;color:rgba(255,255,255,0.7);text-transform:uppercase;">
      Natural Solution
    </span>
    
    <h2 class="serif" style="font-size:{self.heading_font_size}px;
                          font-weight:500;
                          color:#fff;
                          line-height:1.2;
                          margin:30px 0;">
      {content}
    </h2>
    
    <div style="margin-top:40px;padding:28px;background:rgba(255,255,255,0.15);border-radius:20px;border:1px solid rgba(255,255,255,0.2);">
      <div style="display:flex;align-items:center;gap:12px;margin-bottom:12px;">
        <span style="font-size:20px;">🌱</span>
        <span style="font-size:16px;font-weight:600;color:#fff;">100% Natural Ingredients</span>
      </div>
      
      <p style="font-size:14px;color:rgba(255,255,255,0.8);line-height:1.6;margin:0;">
        "{brand.get('name', 'Our products')} are crafted with care for your body and the planet"
      </p>
    </div>
  </div>
  
  {self.swipe_arrow(is_light=False)}
  {self.progress_bar(2, total_slides, is_light=False)}
</div>'''
        
        return html
    
    def generate_slide_4_features(self, features: List[str], brand: Dict, total_slides: int) -> str:
        """Slide 4: Features with nature icons"""
        p = self.palette
        
        features_html = ""
        icons = ["🌿", "💚", "✨", "🧘"]
        
        for i, feat in enumerate(features[:4]):
            icon = icons[i % len(icons)]
            features_html += f'''
        <div style="padding:28px;background:#fff;border-radius:20px;border:1px solid {p['LIGHT_BORDER']};text-align:center;box-shadow:0 4px 20px rgba(0,0,0,0.02);">
          <span style="font-size:36px;display:block;margin-bottom:16px;">{icon}</span>
          <span class="sans" style="font-size:15px;font-weight:600;color:{p['TEXT_PRIMARY']};display:block;">{feat}</span>
        </div>'''
        
        html = f'''<div style="{self._get_container_style('cream', 'center')};">
  <div style="position:absolute;top:100px;left:100px;width:120px;height:120px;{self._get_organic_shape('blob', p['SAGE_LIGHT'], 0.2)}"></div>
  
  <div style="position:relative;z-index:2;width:100%;max-width:950px;">
    <div style="text-align:center;margin-bottom:50px;">
      <span class="sans" style="font-size:10px;font-weight:600;letter-spacing:3px;color:{p['SAGE_DARK']};text-transform:uppercase;">
        Benefits
      </span>
      
      <h2 class="serif" style="font-size:{self.heading_font_size}px;font-weight:500;color:{p['TEXT_PRIMARY']};margin-top:20px;">
        Why choose us
      </h2>
    </div>
    
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:24px;">
      {features_html}
    </div>
  </div>
  
  {self.swipe_arrow(is_light=True)}
  {self.progress_bar(3, total_slides, is_light=True)}
</div>'''
        
        return html
    
    def generate_slide_5_details(self, content: str, brand: Dict, total_slides: int) -> str:
        """Slide 5: Details with earthy tones"""
        p = self.palette
        
        html = f'''<div style="{self._get_container_style('sand', 'center')};">
  <div style="position:relative;z-index:2;width:100%;max-width:850px;">
    <div style="text-align:center;margin-bottom:50px;">
      <span class="sans" style="font-size:10px;font-weight:600;letter-spacing:3px;color:{p['EARTH']};text-transform:uppercase;">
        Quality
      </span>
      
      <h2 class="serif" style="font-size:{self.heading_font_size}px;font-weight:500;color:{p['TEXT_PRIMARY']};margin-top:20px;">
        {content}
      </h2>
    </div>
    
    <div style="display:flex;gap:24px;justify-content:center;">
      <div style="width:160px;padding:24px;background:#fff;border-radius:16px;text-align:center;border:1px solid {p['LIGHT_BORDER']};">
        <span style="font-size:40px;">🌱</span>
        <p style="font-size:14px;font-weight:600;color:{p['TEXT_PRIMARY']};margin-top:12px;">Organic</p>
        <p style="font-size:12px;color:{p['TEXT_SECONDARY']};margin-top:4px;">Certified</p>
      </div>
      
      <div style="width:160px;padding:24px;background:#fff;border-radius:16px;text-align:center;border:1px solid {p['LIGHT_BORDER']};">
        <span style="font-size:40px;">🧪</span>
        <p style="font-size:14px;font-weight:600;color:{p['TEXT_PRIMARY']};margin-top:12px;">Tested</p>
        <p style="font-size:12px;color:{p['TEXT_SECONDARY']};margin-top:4px;">Lab verified</p>
      </div>
      
      <div style="width:160px;padding:24px;background:#fff;border-radius:16px;text-align:center;border:1px solid {p['LIGHT_BORDER']};">
        <span style="font-size:40px;">♻️</span>
        <p style="font-size:14px;font-weight:600;color:{p['TEXT_PRIMARY']};margin-top:12px;">Sustainable</p>
        <p style="font-size:12px;color:{p['TEXT_SECONDARY']};margin-top:4px;">Eco-friendly</p>
      </div>
    </div>
  </div>
  
  {self.swipe_arrow(is_light=True)}
  {self.progress_bar(4, total_slides, is_light=True)}
</div>'''
        
        return html
    
    def generate_slide_6_steps(self, steps: List[str], brand: Dict, total_slides: int) -> str:
        """Slide 6: Gentle process steps"""
        p = self.palette
        
        steps_html = ""
        icons = ["🌅", "🍃", "🌙"]
        
        for i, step in enumerate(steps[:3], 1):
            icon = icons[i - 1] if i <= len(icons) else "✨"
            steps_html += f'''
        <div style="display:flex;align-items:center;gap:24px;padding:24px 0;border-bottom:1px solid {p['LIGHT_BORDER']};">
          <div style="width:56px;height:56px;background:{p['SAGE']};border-radius:50%;display:flex;align-items:center;justify-content:center;">
            <span style="font-size:24px;">{icon}</span>
          </div>
          <div style="flex:1;">
            <span style="font-size:12px;font-weight:600;color:{p['SAGE_DARK']};text-transform:uppercase;letter-spacing:1px;">Step {i}</span>
            <span class="serif" style="font-size:18px;font-weight:500;color:{p['TEXT_PRIMARY']};display:block;margin-top:4px;">{step}</span>
          </div>
        </div>'''
        
        html = f'''<div style="{self._get_container_style('cream', 'center')};">
  <div style="position:relative;z-index:2;width:100%;max-width:800px;">
    <div style="text-align:center;margin-bottom:40px;">
      <span class="sans" style="font-size:10px;font-weight:600;letter-spacing:3px;color:{p['SAGE_DARK']};text-transform:uppercase;">
        Routine
      </span>
      
      <h2 class="serif" style="font-size:{self.heading_font_size}px;font-weight:500;color:{p['TEXT_PRIMARY']};margin-top:16px;">
        Simple daily ritual
      </h2>
    </div>
    
    {steps_html}
  </div>
  
  {self.swipe_arrow(is_light=True)}
  {self.progress_bar(5, total_slides, is_light=True)}
</div>'''
        
        return html
    
    def generate_slide_7_cta(self, brand: Dict, total_slides: int, cta_text: str = "Begin Journey") -> str:
        """Slide 7: CTA with calming sage"""
        p = self.palette
        
        html = f'''<div style="{self._get_container_style('sage', 'center')};">
  <div style="position:absolute;inset:0;background:radial-gradient(ellipse at bottom,{p['SAGE_DARK']}40,transparent 60%);"></div>
  
  <div style="position:relative;z-index:2;text-align:center;max-width:750px;">
    <div style="display:flex;align-items:center;justify-content:center;gap:12px;margin-bottom:30px;">
      <div style="width:60px;height:60px;border-radius:50%;background:#fff;display:flex;align-items:center;justify-content:center;">
        <span style="font-size:28px;">🌿</span>
      </div>
    </div>
    
    <div style="margin-top:20px;">
      <h2 class="serif" style="font-size:{self.hero_font_size}px;font-weight:500;color:#fff;line-height:1.15;margin:0 0 20px;">
        Start your wellness journey
      </h2>
      
      <p class="sans" style="font-size:17px;color:rgba(255,255,255,0.8);margin:0 0 50px;">
        {brand.get('handle', '@wellness')}
      </p>
      
      <div style="display:inline-flex;align-items:center;gap:12px;padding:18px 40px;background:#fff;color:{p['SAGE_DARK']};font-weight:600;font-size:16px;border-radius:100px;">
        {cta_text} →
      </div>
      
      <p style="font-size:13px;color:rgba(255,255,255,0.6);margin-top:30px;">
        Join our community of mindful living
      </p>
    </div>
  </div>
  
  {self.progress_bar(6, total_slides, is_light=False)}
</div>'''
        
        return html
