"""
Corporate Mode - Executive Design System
For: B2B, Consulting, Finance, Legal, Enterprise
Style: Clean, Trustworthy, Premium, Conservative
"""

from typing import Dict, List
from .base_mode import BaseMode


class CorporateMode(BaseMode):
    """
    Executive mode for professional B2B content.
    Philosophy: "Your presentation deserves better"
    """
    
    name = "Executive"
    description = "B2B, Consulting, Finance — Clean & Trustworthy"
    audience = "Corporate clients, professionals, enterprise"
    
    # Typography - Classic, trustworthy
    heading_font = "Libre Baskerville"  # Classic serif
    body_font = "Inter"                  # Clean sans
    heading_weights = [600, 700]
    body_weight = 400
    
    # Colors - Deep navy, gold accents, premium feel
    primary = "#1E3A5F"        # Deep navy blue
    accent_gold = "#C9A227"    # Premium gold
    
    # Layout - Conservative, generous whitespace
    hero_font_size = 34
    heading_font_size = 28
    body_font_size = 14
    tag_font_size = 10
    
    content_alignment = "center"
    whitespace_scale = 1.5     # More whitespace
    
    # Visual effects - Minimal, no gradients or glassmorphism
    use_gradients = False
    use_glassmorphism = False
    use_asymmetric = False
    use_glow_effects = False
    use_noise_texture = False
    
    def generate_palette(self) -> Dict[str, str]:
        """Corporate palette - cool tones, professional"""
        return {
            "BRAND_PRIMARY": self.primary,
            "BRAND_LIGHT": "#4A6FA5",      # Lighter navy
            "BRAND_DARK": "#0F1F33",       # Darker navy
            "ACCENT_GOLD": self.accent_gold,
            "LIGHT_BG": "#F5F7FA",         # Cool off-white
            "LIGHT_BORDER": "#E2E4E8",     # Subtle borders
            "DARK_BG": "#0F1419",          # Near black
            "TEXT_PRIMARY": "#1A1A1A",     # For light slides
            "TEXT_SECONDARY": "#6B7280",   # Gray for secondary
            "TEXT_LIGHT": "#FFFFFF"        # For dark slides
        }
    
    def _get_container_style(self, bg_color: str, alignment: str = "center") -> str:
        """Generate slide container style"""
        p = self.palette
        padding = int(self.slide_padding * self.whitespace_scale)
        
        return f'''background:{bg_color};
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
    
    def generate_slide_1_hero(self, content: str, brand: Dict, total_slides: int) -> str:
        """Slide 1: Hero - Professional hook with logo"""
        p = self.palette
        is_light = True
        
        html = f'''<div style="{self._get_container_style(p['LIGHT_BG'], 'center')};">
  {self.logo_lockup(brand.get('name', 'Brand'), is_light)}
  
  <div style="margin-top:80px;text-align:center;max-width:800px;">
    <span class="sans tag-label" style="color:{p['BRAND_PRIMARY']};">
      ПРОФЕССИОНАЛЬНЫЙ ПОДХОД
    </span>
    
    <h1 class="serif" style="font-size:{self.hero_font_size}px;
                          font-weight:600;
                          color:{p['TEXT_PRIMARY']};
                          line-height:1.2;
                          margin:24px 0;">
      {content}
    </h1>
    
    <div style="width:60px;height:3px;background:{p['ACCENT_GOLD']};margin:40px auto;"></div>
    
    <p class="sans" style="font-size:16px;color:{p['TEXT_SECONDARY']};line-height:1.6;">
      {brand.get('handle', '@company')}
    </p>
  </div>
  
  {self.swipe_arrow(is_light)}
  {self.progress_bar(0, total_slides, is_light)}
</div>'''
        
        return self.get_base_styles() + html
    
    def generate_slide_2_problem(self, content: str, brand: Dict, total_slides: int) -> str:
        """Slide 2: Problem - Dark background, serious tone"""
        p = self.palette
        is_light = False
        
        html = f'''<div style="{self._get_container_style(p['DARK_BG'], 'flex-end')};">
  <div style="text-align:left;width:100%;padding-bottom:40px;">
    <span class="sans tag-label" style="color:{p['BRAND_LIGHT']};">
      ПРОБЛЕМА
    </span>
    
    <h2 class="serif" style="font-size:{self.heading_font_size}px;
                          font-weight:600;
                          color:{p['TEXT_LIGHT']};
                          line-height:1.2;
                          margin:16px 0 40px;">
      {content}
    </h2>
    
    <div style="display:flex;gap:12px;flex-wrap:wrap;">
      <span style="font-size:12px;padding:8px 16px;border:1px solid rgba(255,255,255,0.2);border-radius:4px;color:rgba(255,255,255,0.6);">
        Неэффективно
      </span>
      <span style="font-size:12px;padding:8px 16px;border:1px solid rgba(255,255,255,0.2);border-radius:4px;color:rgba(255,255,255,0.6);">
        Дорого
      </span>
      <span style="font-size:12px;padding:8px 16px;border:1px solid rgba(255,255,255,0.2);border-radius:4px;color:rgba(255,255,255,0.6);">
        Риски
      </span>
    </div>
  </div>
  
  {self.swipe_arrow(is_light)}
  {self.progress_bar(1, total_slides, is_light)}
</div>'''
        
        return html
    
    def generate_slide_3_solution(self, content: str, brand: Dict, total_slides: int) -> str:
        """Slide 3: Solution - Navy background with gold accent"""
        p = self.palette
        
        html = f'''<div style="{self._get_container_style(p['BRAND_PRIMARY'], 'center')};">
  <div style="text-align:center;max-width:800px;">
    <span class="sans tag-label" style="color:rgba(255,255,255,0.7);">
      РЕШЕНИЕ
    </span>
    
    <h2 class="serif" style="font-size:{self.heading_font_size}px;
                          font-weight:600;
                          color:{p['TEXT_LIGHT']};
                          line-height:1.2;
                          margin:16px 0 40px;">
      {content}
    </h2>
    
    <div style="padding:24px;background:rgba(255,255,255,0.1);border-radius:8px;border-left:4px solid {p['ACCENT_GOLD']};text-align:left;">
      <p class="sans" style="font-size:14px;color:rgba(255,255,255,0.8);line-height:1.6;margin:0;">
        "{brand.get('name', 'Наш подход')} обеспечивает надёжность и профессионализм на каждом этапе"
      </p>
    </div>
  </div>
  
  {self.swipe_arrow(is_light=False)}
  {self.progress_bar(2, total_slides, is_light=False)}
</div>'''
        
        return html
    
    def generate_slide_4_features(self, features: List[str], brand: Dict, total_slides: int) -> str:
        """Slide 4: Features - Clean list with checkmarks"""
        p = self.palette
        is_light = True
        
        features_html = ""
        for feat in features[:4]:
            features_html += f'''
        <div style="display:flex;align-items:flex-start;gap:16px;padding:16px 0;border-bottom:1px solid {p['LIGHT_BORDER']};">
          <span style="color:{p['ACCENT_GOLD']};font-size:18px;width:24px;text-align:center;">✓</span>
          <span class="sans" style="font-size:15px;font-weight:500;color:{p['TEXT_PRIMARY']};">{feat}</span>
        </div>'''
        
        html = f'''<div style="{self._get_container_style(p['LIGHT_BG'], 'flex-end')};">
  <div style="width:100%;text-align:left;">
    <span class="sans tag-label" style="color:{p['BRAND_PRIMARY']};">
      ПРЕИМУЩЕСТВА
    </span>
    
    <h2 class="serif" style="font-size:{self.heading_font_size}px;
                          font-weight:600;
                          color:{p['TEXT_PRIMARY']};
                          margin:16px 0 32px;">
      Что вы получаете
    </h2>
    
    <div style="margin-top:20px;">
      {features_html}
    </div>
  </div>
  
  {self.swipe_arrow(is_light)}
  {self.progress_bar(3, total_slides, is_light)}
</div>'''
        
        return html
    
    def generate_slide_5_details(self, content: str, brand: Dict, total_slides: int) -> str:
        """Slide 5: Details - Depth information"""
        p = self.palette
        is_light = False
        
        html = f'''<div style="{self._get_container_style(p['DARK_BG'], 'flex-end')};">
  <div style="width:100%;text-align:left;">
    <span class="sans tag-label" style="color:{p['BRAND_LIGHT']};">
      ДЕТАЛИ
    </span>
    
    <h2 class="serif" style="font-size:{self.heading_font_size}px;
                          font-weight:600;
                          color:{p['TEXT_LIGHT']};
                          line-height:1.2;
                          margin:16px 0 40px;">
      {content}
    </h2>
    
    <div style="display:flex;gap:16px;">
      <div style="flex:1;padding:20px;background:rgba(255,255,255,0.05);border-radius:8px;border-top:3px solid {p['ACCENT_GOLD']};">
        <span style="font-size:24px;font-weight:700;color:{p['ACCENT_GOLD']};">15+</span>
        <p style="font-size:13px;color:rgba(255,255,255,0.6);margin-top:8px;">Лет опыта</p>
      </div>
      <div style="flex:1;padding:20px;background:rgba(255,255,255,0.05);border-radius:8px;border-top:3px solid {p['ACCENT_GOLD']};">
        <span style="font-size:24px;font-weight:700;color:{p['ACCENT_GOLD']};">500+</span>
        <p style="font-size:13px;color:rgba(255,255,255,0.6);margin-top:8px;">Клиентов</p>
      </div>
      <div style="flex:1;padding:20px;background:rgba(255,255,255,0.05);border-radius:8px;border-top:3px solid {p['ACCENT_GOLD']};">
        <span style="font-size:24px;font-weight:700;color:{p['ACCENT_GOLD']};">98%</span>
        <p style="font-size:13px;color:rgba(255,255,255,0.6);margin-top:8px;">Довольных</p>
      </div>
    </div>
  </div>
  
  {self.swipe_arrow(is_light)}
  {self.progress_bar(4, total_slides, is_light)}
</div>'''
        
        return html
    
    def generate_slide_6_steps(self, steps: List[str], brand: Dict, total_slides: int) -> str:
        """Slide 6: How-to - Numbered process"""
        p = self.palette
        is_light = True
        
        steps_html = ""
        for i, step in enumerate(steps[:3], 1):
            steps_html += f'''
        <div style="display:flex;align-items:flex-start;gap:20px;padding:20px 0;border-bottom:1px solid {p['LIGHT_BORDER']};">
          <span class="serif" style="font-size:32px;font-weight:300;color:{p['BRAND_PRIMARY']};min-width:50px;line-height:1;">{i:02d}</span>
          <div>
            <span class="sans" style="font-size:15px;font-weight:500;color:{p['TEXT_PRIMARY']};display:block;">{step}</span>
          </div>
        </div>'''
        
        html = f'''<div style="{self._get_container_style(p['LIGHT_BG'], 'flex-end')};">
  <div style="width:100%;text-align:left;">
    <span class="sans tag-label" style="color:{p['BRAND_PRIMARY']};">
      ПРОЦЕСС
    </span>
    
    <h2 class="serif" style="font-size:{self.heading_font_size}px;
                          font-weight:600;
                          color:{p['TEXT_PRIMARY']};
                          margin:16px 0 24px;">
      Как мы работаем
    </h2>
    
    {steps_html}
  </div>
  
  {self.swipe_arrow(is_light)}
  {self.progress_bar(5, total_slides, is_light)}
</div>'''
        
        return html
    
    def generate_slide_7_cta(self, brand: Dict, total_slides: int, cta_text: str = "Связаться") -> str:
        """Slide 7: Call to Action - No arrow, full progress"""
        p = self.palette
        
        html = f'''<div style="{self._get_container_style(p['BRAND_PRIMARY'], 'center')};">
  {self.logo_lockup(brand.get('name', 'Brand'), is_light=False)}
  
  <div style="margin-top:60px;text-align:center;max-width:700px;">
    <h2 class="serif" style="font-size:{self.hero_font_size}px;
                          font-weight:600;
                          color:{p['TEXT_LIGHT']};
                          line-height:1.2;
                          margin:0 0 20px;">
      Готовы начать?
    </h2>
    
    <p class="sans" style="font-size:16px;color:rgba(255,255,255,0.7);margin:0 0 50px;">
      {brand.get('handle', '@company')}
    </p>
    
    <div style="display:inline-flex;align-items:center;gap:12px;padding:18px 40px;background:{p['LIGHT_BG']};color:{p['BRAND_DARK']};font-weight:600;font-size:16px;border-radius:4px;border:2px solid {p['ACCENT_GOLD']};">
      {cta_text} →
    </div>
  </div>
  
  {self.progress_bar(6, total_slides, is_light=False)}
</div>'''
        
        return html
