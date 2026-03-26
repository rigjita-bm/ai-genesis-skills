"""
Creator Mode - Bold Design System
For: Personal Brands, Coaches, Artists, Musicians, Hype Products
Style: Experimental, Maximalist, Typography-driven, Vibrant
"""

from typing import Dict, List
from .base_mode import BaseMode


class CreatorMode(BaseMode):
    """
    Bold mode for creators and personal brands who want to stand out.
    Philosophy: "Stand out or die"
    """
    
    name = "Bold"
    description = "Personal Brand, Coaches, Artists — Experimental & Maximalist"
    audience = "Personal brands, coaches, artists, musicians, content creators"
    
    # Typography - Bold, expressive
    heading_font = "Anton"                  # Bold, condensed
    body_font = "Space Grotesk"             # Technical, geometric
    heading_weights = [400]                 # Anton only has 400
    body_weight = 400
    
    # Colors - Vibrant, high contrast
    primary = "#FF006E"                    # Hot pink
    secondary = "#FB5607"                  # Orange
    accent = "#FFBE0B"                     # Yellow
    
    # Layout - Maximalist, chaotic but controlled
    hero_font_size = 88                    # Very bold
    heading_font_size = 52
    body_font_size = 16
    tag_font_size = 12
    
    content_alignment = "asymmetric"
    whitespace_scale = 0.8                 # Less whitespace, more content
    
    # Visual effects - Full experimental
    use_gradients = True
    use_glassmorphism = True
    use_asymmetric = True
    use_glow_effects = True
    use_noise_texture = True
    use_3d_transforms = True               # Unique to creator mode
    
    def generate_palette(self) -> Dict[str, str]:
        """Creator palette - vibrant, high contrast"""
        return {
            "BRAND_PRIMARY": self.primary,
            "BRAND_SECONDARY": self.secondary,
            "BRAND_ACCENT": self.accent,
            "PINK": "#FF006E",
            "ORANGE": "#FB5607",
            "YELLOW": "#FFBE0B",
            "CYAN": "#00F5FF",
            "PURPLE": "#8338EC",
            "BLACK": "#000000",
            "WHITE": "#FFFFFF",
            "GRADIENT_WILD": "linear-gradient(45deg, #FF006E, #FB5607, #FFBE0B, #00F5FF)",
            "GRADIENT_PINK_ORANGE": "linear-gradient(135deg, #FF006E 0%, #FB5607 100%)",
            "GRADIENT_RAINBOW": "linear-gradient(90deg, #FF006E, #FB5607, #FFBE0B, #00F5FF, #8338EC)",
            "LIGHT_BG": "#0A0A0A",             # Near black
            "LIGHT_BG_ALT": "#111111",         # Dark gray
            "DARK_BG": "#000000",              # Pure black
            "TEXT_PRIMARY": "#FFFFFF",
            "TEXT_SECONDARY": "#888888",
            "GLOW_PINK": "rgba(255,0,110,0.6)",
            "GLOW_ORANGE": "rgba(251,86,7,0.5)",
            "GLITCH_RED": "#FF0000",
            "GLITCH_CYAN": "#00FFFF"
        }
    
    def _get_glitch_effect(self) -> str:
        """Generate CSS for glitch effect"""
        return '''
        @keyframes glitch {
          0% { transform: translate(0); }
          20% { transform: translate(-2px, 2px); }
          40% { transform: translate(-2px, -2px); }
          60% { transform: translate(2px, 2px); }
          80% { transform: translate(2px, -2px); }
          100% { transform: translate(0); }
        }
        '''
    
    def _get_container_style(self, bg_type: str = "dark", alignment: str = "center") -> str:
        """Generate slide container with bold styling"""
        p = self.palette
        
        if bg_type == "gradient":
            bg = p['GRADIENT_WILD']
        elif bg_type == "pink":
            bg = p['PINK']
        elif bg_type == "black":
            bg = p['BLACK']
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
padding:0 {self.slide_padding}px {self.bottom_padding}px;
box-sizing:border-box;
font-family:'{self.body_font}',sans-serif;
overflow:hidden;'''
    
    def generate_slide_1_hero(self, content: str, brand: Dict, total_slides: int) -> str:
        """Slide 1: Maximalist hero with 3D text effect"""
        p = self.palette
        
        html = f'''<div style="{self._get_container_style('black', 'center')};">
  <!-- Animated gradient background -->
  <div style="position:absolute;inset:0;background:{p['GRADIENT_WILD']};opacity:0.15;"></div>
  
  <!-- Noise texture overlay -->
  <div style="position:absolute;inset:0;background:url('data:image/svg+xml,...');opacity:0.05;"></div>
  
  <!-- Glowing orbs -->
  <div style="position:absolute;top:10%;left:10%;width:300px;height:300px;background:{p['PINK']};filter:blur(100px);opacity:0.4;border-radius:50%;"></div>
  <div style="position:absolute;bottom:10%;right:10%;width:250px;height:250px;background:{p['CYAN']};filter:blur(80px);opacity:0.3;border-radius:50%;"></div>
  
  <div style="position:relative;z-index:2;text-align:center;max-width:950px;">
    <!-- Logo with glow -->
    <div style="display:inline-block;padding:12px 24px;background:{p['PINK']};border-radius:8px;box-shadow:0 0 40px {p['GLOW_PINK']};margin-bottom:40px;">
      <span style="font-size:16px;font-weight:700;color:#fff;letter-spacing:2px;text-transform:uppercase;">
        {brand.get('name', 'CREATOR').upper()}
      </span>
    </div>
    
    <!-- 3D Text effect -->
    <div style="position:relative;">
      <h1 style="font-family:'{self.heading_font}',sans-serif;
                font-size:{self.hero_font_size}px;
                font-weight:400;
                color:#fff;
                line-height:0.95;
                margin:0;
                text-transform:uppercase;
                letter-spacing:-2px;
                text-shadow: 
                  4px 4px 0px {p['PINK']},
                  8px 8px 0px {p['ORANGE']},
                  12px 12px 30px rgba(0,0,0,0.5);">
        {content.upper()}
      </h1>
    </div>
    
    <div style="margin-top:50px;">
      <span style="display:inline-block;font-size:14px;font-weight:700;color:#fff;background:{p['ORANGE']};padding:12px 28px;border-radius:4px;text-transform:uppercase;letter-spacing:2px;">
        {brand.get('tagline', 'NO BS. JUST RESULTS.')}
      </span>
    </div>
  </div>
  
  {self.swipe_arrow(is_light=False)}
  {self.progress_bar(0, total_slides, is_light=False)}
</div>'''
        
        return self.get_base_styles() + html
    
    def generate_slide_2_problem(self, content: str, brand: Dict, total_slides: int) -> str:
        """Slide 2: Problem with strikethrough chaos"""
        p = self.palette
        
        html = f'''<div style="{self._get_container_style('black', 'center')};">
  <div style="position:absolute;top:0;left:0;right:0;height:50%;background:{p['GRADIENT_PINK_ORANGE']};opacity:0.1;"></div>
  
  <div style="position:relative;z-index:2;text-align:left;width:100%;max-width:900px;">
    <span style="font-size:80px;position:absolute;top:-40px;left:-20px;opacity:0.1;">💀</span>
    
    <span style="font-size:14px;font-weight:700;color:{p['PINK']};text-transform:uppercase;letter-spacing:3px;">
      The Problem
    </span>
    
    <h2 style="font-family:'{self.heading_font}',sans-serif;
              font-size:{self.heading_font_size}px;
              font-weight:400;
              color:#fff;
              line-height:1;
              margin:20px 0 40px;
              text-transform:uppercase;">
      {content.upper()}
    </h2>
    
    <div style="display:flex;flex-direction:column;gap:12px;">
      <div style="display:flex;align-items:center;gap:16px;padding:16px;background:rgba(255,0,0,0.1);border-left:4px solid {p['PINK']};">
        <span style="font-size:24px;">❌</span>
        <span style="font-size:18px;color:#fff;text-decoration:line-through;text-decoration-color:{p['PINK']};text-decoration-thickness:3px;">
          Generic advice that doesn't work
        </span>
      </div>
      
      <div style="display:flex;align-items:center;gap:16px;padding:16px;background:rgba(255,0,0,0.1);border-left:4px solid {p['PINK']};">
        <span style="font-size:24px;">❌</span>
        <span style="font-size:18px;color:#fff;text-decoration:line-through;text-decoration-color:{p['PINK']};text-decoration-thickness:3px;">
          Wasting time on things that don't matter
        </span>
      </div>
      
      <div style="display:flex;align-items:center;gap:16px;padding:16px;background:rgba(255,0,0,0.1);border-left:4px solid {p['PINK']};">
        <span style="font-size:24px;">❌</span>
        <span style="font-size:18px;color:#fff;text-decoration:line-through;text-decoration-color:{p['PINK']};text-decoration-thickness:3px;">
          Following the crowd to mediocrity
        </span>
      </div>
    </div>
  </div>
  
  {self.swipe_arrow(is_light=False)}
  {self.progress_bar(1, total_slides, is_light=False)}
</div>'''
        
        return html
    
    def generate_slide_3_solution(self, content: str, brand: Dict, total_slides: int) -> str:
        """Slide 3: Solution with glitch text"""
        p = self.palette
        
        html = f'''<div style="{self._get_container_style('gradient', 'center')};">
  <div style="position:absolute;inset:0;background:#000;opacity:0.7;"></div>
  
  <div style="position:relative;z-index:2;text-align:center;max-width:900px;">
    <span style="font-size:14px;font-weight:700;color:{p['YELLOW']};text-transform:uppercase;letter-spacing:3px;background:#000;padding:8px 16px;">
      The Solution
    </span>
    
    <h2 style="font-family:'{self.heading_font}',sans-serif;
              font-size:{self.heading_font_size}px;
              font-weight:400;
              color:#fff;
              line-height:1;
              margin:30px 0;
              text-transform:uppercase;
              text-shadow: 3px 3px 0px {p['CYAN']}, -3px -3px 0px {p['PINK']};">
      {content.upper()}
    </h2>
    
    <div style="margin-top:40px;padding:24px;background:rgba(0,0,0,0.8);border:2px solid {p['YELLOW']};position:relative;">
      <div style="position:absolute;top:-2px;left:20px;right:20px;height:2px;background:{p['YELLOW']};"></div>
      
      <p style="font-size:18px;color:#fff;line-height:1.5;margin:0;">
        🔥 "{brand.get('name', 'This')} is the <span style="color:{p['YELLOW']};font-weight:700;"<u>ONLY</u></span> thing that actually works"
      </p>
    </div>
  </div>
  
  {self.swipe_arrow(is_light=False)}
  {self.progress_bar(2, total_slides, is_light=False)}
</div>'''
        
        return html
    
    def generate_slide_4_features(self, features: List[str], brand: Dict, total_slides: int) -> str:
        """Slide 4: Features as bold cards"""
        p = self.palette
        
        features_html = ""
        colors = [p['PINK'], p['ORANGE'], p['YELLOW'], p['CYAN']]
        
        for i, feat in enumerate(features[:4]):
            color = colors[i % len(colors)]
            features_html += f'''
        <div style="padding:24px;background:#000;border:2px solid {color};position:relative;">
          <div style="position:absolute;top:-12px;left:16px;background:{color};padding:4px 12px;">
            <span style="font-size:12px;font-weight:700;color:#000;text-transform:uppercase;">0{i+1}</span>
          </div>
          <span style="font-size:18px;font-weight:700;color:#fff;display:block;margin-top:8px;text-transform:uppercase;">{feat}</span>
        </div>'''
        
        html = f'''<div style="{self._get_container_style('black', 'center')};">
  <div style="position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);width:800px;height:800px;background:{p['PINK']};filter:blur(150px);opacity:0.2;border-radius:50%;"></div>
  
  <div style="position:relative;z-index:2;width:100%;max-width:900px;">
    <div style="text-align:center;margin-bottom:50px;">
      <span style="font-size:14px;font-weight:700;color:{p['CYAN']};text-transform:uppercase;letter-spacing:3px;">
        What You Get
      </span>
      
      <h2 style="font-family:'{self.heading_font}',sans-serif;font-size:{self.heading_font_size}px;font-weight:400;color:#fff;margin-top:16px;text-transform:uppercase;">
        No Bullsh*t
      </h2>
    </div>
    
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:24px;">
      {features_html}
    </div>
  </div>
  
  {self.swipe_arrow(is_light=False)}
  {self.progress_bar(3, total_slides, is_light=False)}
</div>'''
        
        return html
    
    def generate_slide_5_details(self, content: str, brand: Dict, total_slides: int) -> str:
        """Slide 5: Details with bold stats"""
        p = self.palette
        
        html = f'''<div style="{self._get_container_style('pink', 'center')};">
  <div style="position:absolute;inset:0;background:#000;opacity:0.3;"></div>
  
  <div style="position:relative;z-index:2;width:100%;max-width:950px;">
    <div style="text-align:center;margin-bottom:50px;">
      <span style="font-size:14px;font-weight:700;color:#fff;text-transform:uppercase;letter-spacing:3px;">
        By The Numbers
      </span>
      
      <h2 style="font-family:'{self.heading_font}',sans-serif;font-size:{self.heading_font_size}px;font-weight:400;color:#fff;margin-top:16px;text-transform:uppercase;text-shadow:3px 3px 0 #000;">
        {content.upper()}
      </h2>
    </div>
    
    <div style="display:flex;gap:20px;justify-content:center;">
      <div style="text-align:center;padding:32px;background:#000;border:3px solid {p['YELLOW']};min-width:180px;">
        <span style="font-family:'{self.heading_font}',sans-serif;font-size:64px;font-weight:400;color:{p['YELLOW']};line-height:1;">10K+</span>
        <p style="font-size:14px;color:#fff;margin-top:8px;text-transform:uppercase;font-weight:700;">Students</p>
      </div>
      
      <div style="text-align:center;padding:32px;background:#000;border:3px solid {p['CYAN']};min-width:180px;">
        <span style="font-family:'{self.heading_font}',sans-serif;font-size:64px;font-weight:400;color:{p['CYAN']};line-height:1;">$2M+</span>
        <p style="font-size:14px;color:#fff;margin-top:8px;text-transform:uppercase;font-weight:700;">Revenue</p>
      </div>
      
      <div style="text-align:center;padding:32px;background:#000;border:3px solid #fff;min-width:180px;">
        <span style="font-family:'{self.heading_font}',sans-serif;font-size:64px;font-weight:400;color:#fff;line-height:1;">100%</span>
        <p style="font-size:14px;color:#fff;margin-top:8px;text-transform:uppercase;font-weight:700;">Results</p>
      </div>
    </div>
  </div>
  
  {self.swipe_arrow(is_light=False)}
  {self.progress_bar(4, total_slides, is_light=False)}
</div>'''
        
        return html
    
    def generate_slide_6_steps(self, steps: List[str], brand: Dict, total_slides: int) -> str:
        """Slide 6: Process with bold timeline"""
        p = self.palette
        
        steps_html = ""
        colors = [p['PINK'], p['ORANGE'], p['YELLOW']]
        
        for i, step in enumerate(steps[:3], 1):
            color = colors[i - 1]
            steps_html += f'''
        <div style="display:flex;align-items:center;gap:24px;padding:20px 0;">
          <div style="width:70px;height:70px;background:{color};display:flex;align-items:center;justify-content:center;position:relative;">
            <span style="font-family:'{self.heading_font}',sans-serif;font-size:36px;font-weight:400;color:#000;">{i}</span>
            <div style="position:absolute;top:100%;left:50%;transform:translateX(-50%);width:2px;height:40px;background:{color};"></div>
          </div>
          <div style="flex:1;padding:20px;background:#000;border-left:4px solid {color};">
            <span style="font-size:12px;font-weight:700;color:{color};text-transform:uppercase;letter-spacing:1px;">Step {i}</span>
            <span style="font-size:20px;font-weight:700;color:#fff;display:block;margin-top:4px;text-transform:uppercase;">{step}</span>
          </div>
        </div>'''
        
        html = f'''<div style="{self._get_container_style('black', 'center')};">
  <div style="position:relative;z-index:2;width:100%;max-width:800px;">
    <div style="text-align:center;margin-bottom:40px;">
      <span style="font-size:14px;font-weight:700;color:{p['ORANGE']};text-transform:uppercase;letter-spacing:3px;">
        The Process
      </span>
      
      <h2 style="font-family:'{self.heading_font}',sans-serif;font-size:{self.heading_font_size}px;font-weight:400;color:#fff;margin-top:16px;text-transform:uppercase;">
        How It Works
      </h2>
    </div>
    
    {steps_html}
  </div>
  
  {self.swipe_arrow(is_light=False)}
  {self.progress_bar(5, total_slides, is_light=False)}
</div>'''
        
        return html
    
    def generate_slide_7_cta(self, brand: Dict, total_slides: int, cta_text: str = "JOIN NOW") -> str:
        """Slide 7: CTA with maximum impact"""
        p = self.palette
        
        html = f'''<div style="{self._get_container_style('black', 'center')};">
  <div style="position:absolute;inset:0;background:{p['GRADIENT_WILD']};opacity:0.2;"></div>
  
  <div style="position:absolute;top:20%;left:10%;width:200px;height:200px;background:{p['PINK']};filter:blur(80px);opacity:0.5;border-radius:50%;"></div>
  <div style="position:absolute;bottom:20%;right:10%;width:200px;height:200px;background:{p['CYAN']};filter:blur(80px);opacity:0.4;border-radius:50%;"></div>
  
  <div style="position:relative;z-index:2;text-align:center;max-width:900px;">
    <div style="display:inline-block;padding:16px 32px;background:{p['PINK']};margin-bottom:30px;box-shadow:0 0 60px {p['GLOW_PINK']};">
      <span style="font-size:18px;font-weight:700;color:#fff;letter-spacing:3px;text-transform:uppercase;">
        {brand.get('name', 'CREATOR').upper()}
      </span>
    </div>
    
    <div style="margin-top:20px;">
      <h2 style="font-family:'{self.heading_font}',sans-serif;font-size:72px;font-weight:400;color:#fff;line-height:0.95;margin:0 0 20px;text-transform:uppercase;text-shadow:4px 4px 0px {p['PINK']}, 8px 8px 0px {p['ORANGE']};">
        READY?
      </h2>
      
      <p style="font-size:18px;color:#fff;margin:0 0 50px;">
        {brand.get('handle', '@creator')}
      </p>
      
      <div style="display:inline-block;padding:24px 56px;background:#fff;color:#000;font-family:'{self.heading_font}',sans-serif;font-size:28px;font-weight:400;text-transform:uppercase;letter-spacing:2px;cursor:pointer;box-shadow:8px 8px 0px {p['PINK']};transition:all 0.2s;">
        {cta_text} →
      </div>
      
      <p style="font-size:14px;color:#888;margin-top:30px;">
        ⚡ Limited spots available • Price increases soon
      </p>
    </div>
  </div>
  
  {self.progress_bar(6, total_slides, is_light=False)}
</div>'''
        
        return html
