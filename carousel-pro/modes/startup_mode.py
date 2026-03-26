"""
Startup Mode - Velocity Design System
For: SaaS, Tech, AI, Apps, Startups
Style: Bold, Dynamic, Glassmorphism, Gradients
"""

from typing import Dict, List
from .base_mode import BaseMode


class StartupMode(BaseMode):
    """
    Velocity mode for tech startups and innovative products.
    Philosophy: "Move fast, break things, look good"
    """
    
    name = "Velocity"
    description = "SaaS, Tech, AI — Bold & Dynamic"
    audience = "Startups, tech companies, innovators"
    
    # Typography - Geometric, modern
    heading_font = "Space Grotesk"      # Technical, geometric
    body_font = "DM Sans"                # Clean, modern
    heading_weights = [700, 600]
    body_weight = 400
    
    # Colors - Vibrant indigo to pink to yellow gradient
    primary = "#6366F1"                  # Indigo
    secondary = "#EC4899"                # Pink
    accent = "#F59E0B"                   # Amber/Yellow
    
    # Layout - Bold, asymmetric
    hero_font_size = 64                  # Very bold
    heading_font_size = 42
    body_font_size = 15
    tag_font_size = 11
    
    content_alignment = "asymmetric"     # Broken grid
    whitespace_scale = 1.0
    
    # Visual effects - Full arsenal
    use_gradients = True
    use_glassmorphism = True
    use_asymmetric = True
    use_glow_effects = True
    use_noise_texture = False
    
    def generate_palette(self) -> Dict[str, str]:
        """Startup palette - vibrant, gradient-friendly"""
        return {
            "BRAND_PRIMARY": self.primary,
            "BRAND_SECONDARY": self.secondary,
            "BRAND_ACCENT": self.accent,
            "BRAND_LIGHT": "#818CF8",           # Light indigo
            "BRAND_DARK": "#4338CA",            # Dark indigo
            "GRADIENT_MAIN": f"linear-gradient(135deg, {self.primary} 0%, {self.secondary} 50%, {self.accent} 100%)",
            "GRADIENT_SUBTLE": f"linear-gradient(165deg, #1E1B4B 0%, {self.primary} 100%)",
            "LIGHT_BG": "#F8FAFC",              # Cool white
            "LIGHT_BORDER": "#E2E8F0",
            "DARK_BG": "#0F172A",               # Slate 900
            "DARK_BG_ALT": "#1E1B4B",           # Indigo 950
            "GLASS_BG": "rgba(255,255,255,0.08)",
            "GLOW_PRIMARY": "rgba(99,102,241,0.5)",
            "GLOW_SECONDARY": "rgba(236,72,153,0.4)",
            "TEXT_PRIMARY": "#0F172A",
            "TEXT_SECONDARY": "#64748B",
            "TEXT_LIGHT": "#FFFFFF"
        }
    
    def _get_gradient_background(self) -> str:
        """Generate animated gradient background"""
        p = self.palette
        return f"""
        background: {p['GRADIENT_MAIN']};
        position: relative;
        overflow: hidden;
        """
    
    def _get_glass_card(self, p: Dict) -> str:
        """Generate glassmorphism card style"""
        return f"""
        background: {p['GLASS_BG']};
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255,255,255,0.18);
        border-radius: 24px;
        """
    
    def _get_container_style(self, bg_type: str = "light", alignment: str = "center") -> str:
        """Generate slide container with effects"""
        p = self.palette
        
        if bg_type == "gradient":
            bg = p['GRADIENT_MAIN']
        elif bg_type == "dark":
            bg = p['DARK_BG']
        elif bg_type == "dark_alt":
            bg = p['DARK_BG_ALT']
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
        """Slide 1: Bold hero with gradient and glow"""
        p = self.palette
        
        html = f'''<div style="{self._get_container_style('gradient', 'center')};">
  <!-- Background glow effects -->
  <div style="position:absolute;top:-200px;right:-200px;width:600px;height:600px;background:radial-gradient(circle,rgba(236,72,153,0.4) 0%,transparent 70%);border-radius:50%;"></div>
  <div style="position:absolute;bottom:-100px;left:-100px;width:500px;height:500px;background:radial-gradient(circle,rgba(245,158,11,0.3) 0%,transparent 70%);border-radius:50%;"></div>
  
  <div style="position:relative;z-index:2;text-align:center;max-width:900px;">
    {self.logo_lockup(brand.get('name', 'Brand'), is_light=False)}
    
    <div style="margin-top:60px;">
      <span class="sans" style="display:inline-block;font-size:12px;font-weight:600;letter-spacing:3px;color:rgba(255,255,255,0.6);text-transform:uppercase;background:rgba(255,255,255,0.1);padding:8px 16px;border-radius:100px;">
        The Future is Now
      </span>
      
      <h1 class="serif" style="font-size:{self.hero_font_size}px;
                            font-weight:700;
                            color:#fff;
                            line-height:1.05;
                            margin:32px 0;
                            text-shadow:0 4px 30px rgba(99,102,241,0.5);">
        {content}
      </h1>
      
      <p class="sans" style="font-size:18px;color:rgba(255,255,255,0.7);line-height:1.5;max-width:600px;margin:0 auto;">
        {brand.get('tagline', 'Innovate faster with AI-powered solutions')}
      </p>
    </div>
  </div>
  
  {self.swipe_arrow(is_light=False)}
  {self.progress_bar(0, total_slides, is_light=False)}
</div>'''
        
        return self.get_base_styles() + html
    
    def generate_slide_2_problem(self, content: str, brand: Dict, total_slides: int) -> str:
        """Slide 2: Problem with strikethrough pills"""
        p = self.palette
        
        html = f'''<div style="{self._get_container_style('dark', 'center')};">
  <div style="position:absolute;top:0;left:0;right:0;height:400px;background:linear-gradient(to bottom,{p['BRAND_DARK']},transparent);"></div>
  
  <div style="position:relative;z-index:2;text-align:left;width:100%;max-width:900px;">
    <span class="sans" style="font-size:12px;font-weight:600;letter-spacing:3px;color:{p['BRAND_SECONDARY']};text-transform:uppercase;">
      The Problem
    </span>
    
    <h2 class="serif" style="font-size:{self.heading_font_size}px;
                          font-weight:700;
                          color:#fff;
                          line-height:1.1;
                          margin:20px 0 40px;">
      {content}
    </h2>
    
    <div style="display:flex;gap:12px;flex-wrap:wrap;margin-top:30px;">
      <span style="font-size:14px;padding:12px 20px;background:rgba(239,68,68,0.1);border:1px solid rgba(239,68,68,0.3);border-radius:100px;color:#EF4444;text-decoration:line-through;">
        ❌ Manual work
      </span>
      <span style="font-size:14px;padding:12px 20px;background:rgba(239,68,68,0.1);border:1px solid rgba(239,68,68,0.3);border-radius:100px;color:#EF4444;text-decoration:line-through;">
        ❌ Slow processes
      </span>
      <span style="font-size:14px;padding:12px 20px;background:rgba(239,68,68,0.1);border:1px solid rgba(239,68,68,0.3);border-radius:100px;color:#EF4444;text-decoration:line-through;">
        ❌ High costs
      </span>
    </div>
    
    <div style="margin-top:50px;padding:24px;background:{p['GLASS_BG']};backdrop-filter:blur(10px);border-radius:16px;border:1px solid rgba(255,255,255,0.1);">
      <p style="font-size:16px;color:rgba(255,255,255,0.8);margin:0;">
        💡 "{brand.get('name', 'Our solution')} fixes this in 5 minutes, not 5 hours"
      </p>
    </div>
  </div>
  
  {self.swipe_arrow(is_light=False)}
  {self.progress_bar(1, total_slides, is_light=False)}
</div>'''
        
        return html
    
    def generate_slide_3_solution(self, content: str, brand: Dict, total_slides: int) -> str:
        """Slide 3: Solution with glassmorphism card"""
        p = self.palette
        
        html = f'''<div style="{self._get_container_style('gradient', 'center')};">
  <div style="position:absolute;inset:0;background:radial-gradient(ellipse at top,rgba(255,255,255,0.1),transparent 50%);"></div>
  
  <div style="position:relative;z-index:2;text-align:center;max-width:850px;">
    <span class="sans" style="font-size:12px;font-weight:600;letter-spacing:3px;color:rgba(255,255,255,0.7);text-transform:uppercase;">
      The Solution
    </span>
    
    <h2 class="serif" style="font-size:{self.heading_font_size}px;
                          font-weight:700;
                          color:#fff;
                          line-height:1.1;
                          margin:24px 0;">
      {content}
    </h2>
    
    <div style="margin-top:40px;padding:32px;background:{p['GLASS_BG']};backdrop-filter:blur(20px);border-radius:24px;border:1px solid rgba(255,255,255,0.2);box-shadow:0 8px 32px rgba(0,0,0,0.2);text-align:left;">
      <div style="display:flex;align-items:center;gap:12px;margin-bottom:16px;">
        <span style="width:40px;height:40px;background:{p['BRAND_ACCENT']};border-radius:12px;display:flex;align-items:center;justify-content:center;font-size:20px;">⚡</span>
        <span style="font-size:18px;font-weight:600;color:#fff;">Lightning Fast</span>
      </div>
      
      <p style="font-size:15px;color:rgba(255,255,255,0.8);line-height:1.6;margin:0;">
        Process 1000x faster than traditional methods. AI handles the heavy lifting while you focus on strategy.
      </p>
    </div>
  </div>
  
  {self.swipe_arrow(is_light=False)}
  {self.progress_bar(2, total_slides, is_light=False)}
</div>'''
        
        return html
    
    def generate_slide_4_features(self, features: List[str], brand: Dict, total_slides: int) -> str:
        """Slide 4: Features with icons in glass cards"""
        p = self.palette
        
        features_html = ""
        icons = ["🚀", "🤖", "📊", "🔒"]
        colors = [p['BRAND_PRIMARY'], p['BRAND_SECONDARY'], p['BRAND_ACCENT'], p['BRAND_LIGHT']]
        
        for i, feat in enumerate(features[:4]):
            icon = icons[i % len(icons)]
            color = colors[i % len(colors)]
            features_html += f'''
        <div style="padding:24px;background:#fff;border-radius:20px;border:1px solid {p['LIGHT_BORDER']};box-shadow:0 4px 20px rgba(0,0,0,0.05);">
          <div style="width:48px;height:48px;background:{color}20;border-radius:12px;display:flex;align-items:center;justify-content:center;font-size:24px;margin-bottom:16px;">
            {icon}
          </div>
          <span class="sans" style="font-size:16px;font-weight:600;color:{p['TEXT_PRIMARY']};display:block;">{feat}</span>
        </div>'''
        
        html = f'''<div style="{self._get_container_style('light', 'center')};">
  <div style="position:absolute;top:-100px;right:-100px;width:400px;height:400px;background:radial-gradient(circle,{p['GLOW_PRIMARY']} 0%,transparent 70%);opacity:0.3;border-radius:50%;"></div>
  
  <div style="position:relative;z-index:2;width:100%;max-width:950px;">
    <div style="text-align:center;margin-bottom:40px;">
      <span class="sans" style="font-size:12px;font-weight:600;letter-spacing:3px;color:{p['BRAND_PRIMARY']};text-transform:uppercase;">
        Features
      </span>
      
      <h2 class="serif" style="font-size:{self.heading_font_size}px;font-weight:700;color:{p['TEXT_PRIMARY']};margin-top:16px;">
        What you get
      </h2>
    </div>
    
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:20px;">
      {features_html}
    </div>
  </div>
  
  {self.swipe_arrow(is_light=True)}
  {self.progress_bar(3, total_slides, is_light=True)}
</div>'''
        
        return html
    
    def generate_slide_5_details(self, content: str, brand: Dict, total_slides: int) -> str:
        """Slide 5: Details with stats"""
        p = self.palette
        
        html = f'''<div style="{self._get_container_style('dark_alt', 'center')};">
  <div style="position:absolute;bottom:0;left:0;right:0;height:300px;background:linear-gradient(to top,{p['BRAND_PRIMARY']}40,transparent);"></div>
  
  <div style="position:relative;z-index:2;width:100%;max-width:900px;">
    <span class="sans" style="font-size:12px;font-weight:600;letter-spacing:3px;color:{p['BRAND_LIGHT']};text-transform:uppercase;">
      By the Numbers
    </span>
    
    <h2 class="serif" style="font-size:{self.heading_font_size}px;font-weight:700;color:#fff;margin:20px 0 50px;">
      {content}
    </h2>
    
    <div style="display:flex;gap:24px;">
      <div style="flex:1;text-align:center;padding:32px;background:{p['GLASS_BG']};backdrop-filter:blur(10px);border-radius:20px;border:1px solid rgba(255,255,255,0.1);">
        <span style="font-size:56px;font-weight:700;background:{p['GRADIENT_MAIN']};-webkit-background-clip:text;-webkit-text-fill-color:transparent;">10x</span>
        <p style="font-size:15px;color:rgba(255,255,255,0.7);margin-top:12px;">Faster processing</p>
      </div>
      
      <div style="flex:1;text-align:center;padding:32px;background:{p['GLASS_BG']};backdrop-filter:blur(10px);border-radius:20px;border:1px solid rgba(255,255,255,0.1);">
        <span style="font-size:56px;font-weight:700;background:{p['GRADIENT_MAIN']};-webkit-background-clip:text;-webkit-text-fill-color:transparent;">99%</span>
        <p style="font-size:15px;color:rgba(255,255,255,0.7);margin-top:12px;">Accuracy rate</p>
      </div>
      
      <div style="flex:1;text-align:center;padding:32px;background:{p['GLASS_BG']};backdrop-filter:blur(10px);border-radius:20px;border:1px solid rgba(255,255,255,0.1);">
        <span style="font-size:56px;font-weight:700;background:{p['GRADIENT_MAIN']};-webkit-background-clip:text;-webkit-text-fill-color:transparent;">24/7</span>
        <p style="font-size:15px;color:rgba(255,255,255,0.7);margin-top:12px;">Always on</p>
      </div>
    </div>
  </div>
  
  {self.swipe_arrow(is_light=False)}
  {self.progress_bar(4, total_slides, is_light=False)}
</div>'''
        
        return html
    
    def generate_slide_6_steps(self, steps: List[str], brand: Dict, total_slides: int) -> str:
        """Slide 6: Process with visual timeline"""
        p = self.palette
        
        steps_html = ""
        for i, step in enumerate(steps[:3], 1):
            steps_html += f'''
        <div style="display:flex;align-items:center;gap:24px;padding:24px 0;">
          <div style="width:56px;height:56px;background:{p['GRADIENT_MAIN']};border-radius:16px;display:flex;align-items:center;justify-content:center;box-shadow:0 4px 20px {p['GLOW_PRIMARY']};">
            <span style="font-size:24px;font-weight:700;color:#fff;">{i}</span>
          </div>
          <div style="flex:1;">
            <span class="sans" style="font-size:18px;font-weight:600;color:{p['TEXT_PRIMARY']};display:block;">{step}</span>
          </div>
          <span style="font-size:24px;">→</span>
        </div>'''
        
        html = f'''<div style="{self._get_container_style('light', 'center')};">
  <div style="position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);width:600px;height:600px;background:radial-gradient(circle,{p['GLOW_SECONDARY']} 0%,transparent 70%);opacity:0.2;border-radius:50%;"></div>
  
  <div style="position:relative;z-index:2;width:100%;max-width:800px;">
    <div style="text-align:center;margin-bottom:40px;">
      <span class="sans" style="font-size:12px;font-weight:600;letter-spacing:3px;color:{p['BRAND_PRIMARY']};text-transform:uppercase;">
        How it works
      </span>
      
      <h2 class="serif" style="font-size:{self.heading_font_size}px;font-weight:700;color:{p['TEXT_PRIMARY']};margin-top:16px;">
        Simple 3-step process
      </h2>
    </div>
    
    <div style="background:#fff;padding:32px;border-radius:24px;border:1px solid {p['LIGHT_BORDER']};box-shadow:0 8px 40px rgba(0,0,0,0.08);">
      {steps_html}
    </div>
  </div>
  
  {self.swipe_arrow(is_light=True)}
  {self.progress_bar(5, total_slides, is_light=True)}
</div>'''
        
        return html
    
    def generate_slide_7_cta(self, brand: Dict, total_slides: int, cta_text: str = "Get Started") -> str:
        """Slide 7: CTA with gradient button"""
        p = self.palette
        
        html = f'''<div style="{self._get_container_style('gradient', 'center')};">
  <div style="position:absolute;inset:0;background:radial-gradient(ellipse at center,rgba(255,255,255,0.1),transparent 70%);"></div>
  
  <div style="position:relative;z-index:2;text-align:center;max-width:800px;">
    {self.logo_lockup(brand.get('name', 'Brand'), is_light=False)}
    
    <div style="margin-top:60px;">
      <h2 class="serif" style="font-size:{self.hero_font_size}px;font-weight:700;color:#fff;line-height:1.05;margin:0 0 20px;">
        Ready to start?
      </h2>
      
      <p class="sans" style="font-size:18px;color:rgba(255,255,255,0.7);margin:0 0 50px;">
        {brand.get('handle', '@company')}
      </p>
      
      <div style="display:inline-flex;align-items:center;gap:12px;padding:20px 48px;background:#fff;color:{p['BRAND_DARK']};font-weight:700;font-size:18px;border-radius:100px;box-shadow:0 8px 30px rgba(0,0,0,0.3);cursor:pointer;transition:transform 0.2s;">
        {cta_text} 🚀
      </div>
      
      <p style="font-size:14px;color:rgba(255,255,255,0.5);margin-top:30px;">
        No credit card required • Setup in 5 minutes
      </p>
    </div>
  </div>
  
  {self.progress_bar(6, total_slides, is_light=False)}
</div>'''
        
        return html
