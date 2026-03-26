"""
Lifestyle Mode - Essence Design System
For: Beauty, Fashion, Travel, Food, Home Decor
Style: Editorial, Warm, Aspirational, Photo-centric
"""

from typing import Dict, List
from .base_mode import BaseMode


class LifestyleMode(BaseMode):
    """
    Essence mode for lifestyle brands and aspirational content.
    Philosophy: "Live the life you deserve"
    """
    
    name = "Essence"
    description = "Beauty, Fashion, Travel — Editorial & Warm"
    audience = "Lifestyle brands, influencers, travel, beauty"
    
    # Typography - Editorial, elegant
    heading_font = "Playfair Display"     # Editorial serif
    body_font = "Lora"                     # Warm, readable
    heading_weights = [600, 700]
    body_weight = 400
    
    # Colors - Warm terracotta, soft sage, cream
    primary = "#D4A373"                    # Terracotta
    secondary = "#E9EDC9"                  # Soft sage
    accent = "#FEFAE0"                     # Cream
    
    # Layout - Editorial, asymmetric
    hero_font_size = 48
    heading_font_size = 36
    body_font_size = 15
    tag_font_size = 10
    
    content_alignment = "flex-end"         # Text at bottom (photo space)
    whitespace_scale = 1.2
    
    # Visual effects
    use_gradients = True
    use_glassmorphism = False
    use_asymmetric = True
    use_glow_effects = False
    use_noise_texture = True               # Paper texture
    
    def generate_palette(self) -> Dict[str, str]:
        """Lifestyle palette - warm, organic, aspirational"""
        return {
            "BRAND_PRIMARY": self.primary,
            "BRAND_SECONDARY": self.secondary,
            "BRAND_ACCENT": self.accent,
            "BRAND_LIGHT": "#E6C9A8",          # Light terracotta
            "BRAND_DARK": "#A67C52",           # Dark terracotta
            "TERRACOTTA": "#D4A373",
            "SAGE": "#E9EDC9",
            "CREAM": "#FEFAE0",
            "SAND": "#E8DCC4",
            "LIGHT_BG": "#FDFBF7",             # Warm off-white
            "LIGHT_BORDER": "#EDE8E0",         # Warm border
            "DARK_BG": "#3D405B",              # Soft navy
            "DARK_BG_ALT": "#5C5C5C",          # Warm gray
            "TEXT_PRIMARY": "#2C2C2C",         # Soft black
            "TEXT_SECONDARY": "#6B6560",       # Warm gray
            "TEXT_LIGHT": "#FDFBF7",           # Cream white
            "PAPER_TEXTURE": "url('data:image/svg+xml,...')"  # Subtle paper
        }
    
    def _get_container_style(self, bg_type: str = "light", alignment: str = "flex-end") -> str:
        """Generate slide container with editorial styling"""
        p = self.palette
        padding = int(self.slide_padding * self.whitespace_scale)
        
        if bg_type == "terracotta":
            bg = p['TERRACOTTA']
        elif bg_type == "sage":
            bg = p['SAGE']
        elif bg_type == "cream":
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
padding:0 {padding}px {self.bottom_padding}px;
box-sizing:border-box;
font-family:'{self.body_font}',serif;'''
    
    def _get_image_overlay(self, gradient_direction: str = "to top") -> str:
        """Generate gradient overlay for image backgrounds"""
        return f'''position:absolute;inset:0;
background:linear-gradient({gradient_direction},rgba(0,0,0,0.7) 0%,rgba(0,0,0,0.3) 50%,transparent 100%);
z-index:1;'''
    
    def generate_slide_1_hero(self, content: str, brand: Dict, total_slides: int) -> str:
        """Slide 1: Editorial hero with large typography"""
        p = self.palette
        
        html = f'''<div style="{self._get_container_style('light', 'center')};align-items:center;">
  <!-- Decorative organic shape -->
  <div style="position:absolute;top:-50px;right:-50px;width:300px;height:300px;background:{p['SAGE']};border-radius:60% 40% 50% 50%;opacity:0.5;"></div>
  <div style="position:absolute;bottom:100px;left:-30px;width:200px;height:200px;background:{p['TERRACOTTA']};border-radius:40% 60% 70% 30%;opacity:0.1;"></div>
  
  <div style="position:relative;z-index:2;text-align:center;max-width:850px;">
    {self.logo_lockup(brand.get('name', 'Brand'), is_light=True)}
    
    <div style="margin-top:60px;">
      <span class="sans" style="display:inline-block;font-size:11px;font-weight:600;letter-spacing:3px;color:{p['BRAND_DARK']};text-transform:uppercase;background:{p['CREAM']};padding:10px 20px;border-radius:100px;">
        Lifestyle
      </span>
      
      <h1 class="serif" style="font-size:{self.hero_font_size}px;
                            font-weight:600;
                            color:{p['TEXT_PRIMARY']};
                            line-height:1.1;
                            margin:40px 0;
                            font-style:italic;">
        {content}
      </h1>
      
      <div style="width:80px;height:2px;background:{p['TERRACOTTA']};margin:0 auto;"></div>
      
      <p class="sans" style="font-size:16px;color:{p['TEXT_SECONDARY']};line-height:1.6;margin-top:30px;font-style:italic;">
        {brand.get('tagline', 'Discover the art of living well')}
      </p>
    </div>
  </div>
  
  {self.swipe_arrow(is_light=True)}
  {self.progress_bar(0, total_slides, is_light=True)}
</div>'''
        
        return self.get_base_styles() + html
    
    def generate_slide_2_problem(self, content: str, brand: Dict, total_slides: int) -> str:
        """Slide 2: Problem with image placeholder area"""
        p = self.palette
        
        html = f'''<div style="{self._get_container_style('dark', 'flex-end')};">
  <!-- Image placeholder area (top 60%) -->
  <div style="position:absolute;top:0;left:0;right:0;height:60%;background:linear-gradient(to bottom,{p['DARK_BG_ALT']},{p['DARK_BG']});display:flex;align-items:center;justify-content:center;">
    <span style="font-size:14px;color:rgba(255,255,255,0.3);font-style:italic;">[Image: lifestyle context]</span>
  </div>
  
  <div style="position:relative;z-index:2;text-align:left;width:100%;padding-bottom:40px;">
    <span class="sans" style="font-size:11px;font-weight:600;letter-spacing:3px;color:{p['TERRACOTTA']};text-transform:uppercase;">
      The Challenge
    </span>
    
    <h2 class="serif" style="font-size:{self.heading_font_size}px;
                          font-weight:600;
                          color:{p['TEXT_LIGHT']};
                          line-height:1.2;
                          margin:20px 0 30px;
                          font-style:italic;">
      {content}
    </h2>
    
    <p class="sans" style="font-size:15px;color:rgba(253,251,247,0.7);line-height:1.6;font-style:italic;">
      We've all been there. The struggle is real, but it doesn't have to be.
    </p>
  </div>
  
  {self.swipe_arrow(is_light=False)}
  {self.progress_bar(1, total_slides, is_light=False)}
</div>'''
        
        return html
    
    def generate_slide_3_solution(self, content: str, brand: Dict, total_slides: int) -> str:
        """Slide 3: Solution with sage background"""
        p = self.palette
        
        html = f'''<div style="{self._get_container_style('sage', 'center')};align-items:center;">
  <div style="position:absolute;top:40px;right:40px;width:120px;height:120px;border:2px solid {p['TERRACOTTA']};border-radius:50%;opacity:0.3;"></div>
  
  <div style="position:relative;z-index:2;text-align:center;max-width:800px;">
    <span class="sans" style="font-size:11px;font-weight:600;letter-spacing:3px;color:{p['BRAND_DARK']};text-transform:uppercase;">
      The Solution
    </span>
    
    <h2 class="serif" style="font-size:{self.heading_font_size}px;
                          font-weight:600;
                          color:{p['TEXT_PRIMARY']};
                          line-height:1.2;
                          margin:24px 0;
                          font-style:italic;">
      {content}
    </h2>
    
    <div style="margin-top:40px;padding:28px;background:{p['CREAM']};border-radius:20px;border:1px solid {p['SAND']};text-align:center;">
      <span style="font-size:48px;">✨</span>
      
      <p class="sans" style="font-size:16px;color:{p['TEXT_SECONDARY']};line-height:1.6;margin:16px 0 0;font-style:italic;">
        "{brand.get('name', 'Our brand')} transforms everyday moments into something extraordinary"
      </p>
    </div>
  </div>
  
  {self.swipe_arrow(is_light=True)}
  {self.progress_bar(2, total_slides, is_light=True)}
</div>'''
        
        return html
    
    def generate_slide_4_features(self, features: List[str], brand: Dict, total_slides: int) -> str:
        """Slide 4: Features with elegant cards"""
        p = self.palette
        
        features_html = ""
        icons = ["🌿", "✨", "🕯️", "📖"]
        
        for i, feat in enumerate(features[:4]):
            icon = icons[i % len(icons)]
            features_html += f'''
        <div style="padding:24px;background:#fff;border-radius:16px;border:1px solid {p['LIGHT_BORDER']};box-shadow:0 4px 20px rgba(0,0,0,0.03);text-align:center;">
          <span style="font-size:32px;display:block;margin-bottom:12px;">{icon}</span>
          <span class="serif" style="font-size:17px;font-weight:600;color:{p['TEXT_PRIMARY']};display:block;font-style:italic;">{feat}</span>
        </div>'''
        
        html = f'''<div style="{self._get_container_style('cream', 'center')};align-items:center;">
  <div style="position:relative;z-index:2;width:100%;max-width:950px;">
    <div style="text-align:center;margin-bottom:50px;">
      <span class="sans" style="font-size:11px;font-weight:600;letter-spacing:3px;color:{p['BRAND_DARK']};text-transform:uppercase;">
        Features
      </span>
      
      <h2 class="serif" style="font-size:{self.heading_font_size}px;font-weight:600;color:{p['TEXT_PRIMARY']};margin-top:20px;font-style:italic;">
        What makes us special
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
        """Slide 5: Details with terracotta accent"""
        p = self.palette
        
        html = f'''<div style="{self._get_container_style('light', 'center')};align-items:center;">
  <div style="position:absolute;left:0;top:0;bottom:0;width:40%;background:{p['TERRACOTTA']};opacity:0.08;"></div>
  
  <div style="position:relative;z-index:2;width:100%;max-width:850px;display:flex;gap:60px;align-items:center;">
    <div style="flex:1;">
      <span class="sans" style="font-size:11px;font-weight:600;letter-spacing:3px;color:{p['BRAND_DARK']};text-transform:uppercase;">
        Details
      </span>
      
      <h2 class="serif" style="font-size:{self.heading_font_size}px;font-weight:600;color:{p['TEXT_PRIMARY']};margin:20px 0 30px;line-height:1.2;font-style:italic;">
        {content}
      </h2>
      
      <p class="sans" style="font-size:15px;color:{p['TEXT_SECONDARY']};line-height:1.7;font-style:italic;">
        Every detail is carefully considered to create an experience that feels both luxurious and approachable.
      </p>
    </div>
    
    <div style="width:280px;height:350px;background:{p['SAGE']};border-radius:200px 200px 20px 20px;display:flex;align-items:center;justify-content:center;">
      <span style="font-size:14px;color:{p['BRAND_DARK']};font-style:italic;">[Product Image]</span>
    </div>
  </div>
  
  {self.swipe_arrow(is_light=True)}
  {self.progress_bar(4, total_slides, is_light=True)}
</div>'''
        
        return html
    
    def generate_slide_6_steps(self, steps: List[str], brand: Dict, total_slides: int) -> str:
        """Slide 6: Process with elegant numbering"""
        p = self.palette
        
        steps_html = ""
        for i, step in enumerate(steps[:3], 1):
            steps_html += f'''
        <div style="display:flex;align-items:center;gap:30px;padding:24px 0;border-bottom:1px solid {p['LIGHT_BORDER']};">
          <span class="serif" style="font-size:42px;font-weight:300;color:{p['TERRACOTTA']};font-style:italic;width:60px;">{i:02d}</span>
          <span class="serif" style="font-size:19px;font-weight:600;color:{p['TEXT_PRIMARY']};flex:1;font-style:italic;">{step}</span>
        </div>'''
        
        html = f'''<div style="{self._get_container_style('light', 'flex-end')};">
  <div style="position:relative;z-index:2;width:100%;max-width:800px;">
    <div style="text-align:left;margin-bottom:40px;">
      <span class="sans" style="font-size:11px;font-weight:600;letter-spacing:3px;color:{p['BRAND_DARK']};text-transform:uppercase;">
        Process
      </span>
      
      <h2 class="serif" style="font-size:{self.heading_font_size}px;font-weight:600;color:{p['TEXT_PRIMARY']};margin-top:16px;font-style:italic;">
        How it works
      </h2>
    </div>
    
    {steps_html}
  </div>
  
  {self.swipe_arrow(is_light=True)}
  {self.progress_bar(5, total_slides, is_light=True)}
</div>'''
        
        return html
    
    def generate_slide_7_cta(self, brand: Dict, total_slides: int, cta_text: str = "Discover More") -> str:
        """Slide 7: CTA with terracotta background"""
        p = self.palette
        
        html = f'''<div style="{self._get_container_style('terracotta', 'center')};align-items:center;">
  <div style="position:absolute;inset:0;background:radial-gradient(ellipse at top,rgba(255,255,255,0.1),transparent 50%);"></div>
  <div style="position:absolute;top:60px;left:60px;right:60px;height:2px;background:rgba(255,255,255,0.2);"></div>
  <div style="position:relative;z-index:2;text-align:center;max-width:750px;">
    {self.logo_lockup(brand.get('name', 'Brand'), is_light=False)}
    
    <div style="margin-top:50px;">
      <h2 class="serif" style="font-size:{self.hero_font_size}px;font-weight:600;color:#fff;line-height:1.1;margin:0 0 20px;font-style:italic;">
        Begin your journey
      </h2>
      
      <p class="sans" style="font-size:17px;color:rgba(255,255,255,0.8);margin:0 0 50px;font-style:italic;">
        {brand.get('handle', '@brand')}
      </p>
      
      <div style="display:inline-flex;align-items:center;gap:12px;padding:18px 40px;background:#fff;color:{p['BRAND_DARK']};font-weight:600;font-size:16px;border-radius:100px;">
        {cta_text} →
      </div>
      
      <p style="font-size:13px;color:rgba(255,255,255,0.6);margin-top:30px;font-style:italic;">
        Join thousands living their best life
      </p>
    </div>
  </div>
  
  {self.progress_bar(6, total_slides, is_light=False)}
</div>'''
        
        return html
