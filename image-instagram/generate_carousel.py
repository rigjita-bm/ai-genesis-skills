#!/usr/bin/env python3
"""
Instagram Content Generator for AI Genesis
Generates carousel posts, stories, and captions for ANY niche
"""

import sys
import os
import json
from datetime import datetime

# Niche-based templates with auto-detection
NICHE_TEMPLATES = {
    "wellness": {
        "bg_color": "#F0F7F4",
        "text_color": "#2D3436",
        "accent_color": "#00B894",
        "font": "Inter",
        "emoji": "🌿",
        "category": "Здоровье и энергия",
        "hashtags": "#здоровье #энергия #велнес #здоровоепитание #ньюйорк"
    },
    "construction": {
        "bg_color": "#2D3436",
        "text_color": "#FFFFFF",
        "accent_color": "#E17055",
        "font": "Montserrat",
        "emoji": "🛠️",
        "category": "Ремонт и строительство",
        "hashtags": "#ремонт #строительство #дизайнинтерьера #недвижимость #ньюйорк"
    },
    "beauty": {
        "bg_color": "#FFF5F5",
        "text_color": "#2D3436",
        "accent_color": "#FD79A8",
        "font": "Playfair Display",
        "emoji": "💄",
        "category": "Красота и уход",
        "hashtags": "#красота #уход #салонкрасоты #красотаньюйорк #beautynyc"
    },
    "business": {
        "bg_color": "#0A0A0A",
        "text_color": "#FFFFFF",
        "accent_color": "#00D9FF",
        "font": "Inter",
        "emoji": "🚀",
        "category": "Бизнес и автоматизация",
        "hashtags": "#бизнес #автоматизация #предприниматель #стартап #ньюйорк"
    },
    "education": {
        "bg_color": "#FEF9E7",
        "text_color": "#2D3436",
        "accent_color": "#F39C12",
        "font": "Georgia",
        "emoji": "📚",
        "category": "Образование и курсы",
        "hashtags": "#образование #курсы #обучение #онлайнкурс #ньюйорк"
    },
    "food": {
        "bg_color": "#FFF8F0",
        "text_color": "#2D3436",
        "accent_color": "#E74C3C",
        "font": "Helvetica Neue",
        "emoji": "🍽️",
        "category": "Еда и рестораны",
        "hashtags": "#еда #ресторан #ньюйорк #nycfood #foodie"
    },
    "realestate": {
        "bg_color": "#1A1A2E",
        "text_color": "#FFFFFF",
        "accent_color": "#E94560",
        "font": "Montserrat",
        "emoji": "🏠",
        "category": "Недвижимость",
        "hashtags": "#недвижимость #ньюйорк #квартира #дом #риелтор"
    },
    "fitness": {
        "bg_color": "#17223B",
        "text_color": "#FFFFFF",
        "accent_color": "#FF6B6B",
        "font": "Oswald",
        "emoji": "💪",
        "category": "Фитнес и спорт",
        "hashtags": "#фитнес #спорт #тренировки #зож #ньюйорк"
    },
    "tech": {
        "bg_color": "#0F0F0F",
        "text_color": "#00FF88",
        "accent_color": "#00FF88",
        "font": "Courier New",
        "emoji": "💻",
        "category": "Технологии и IT",
        "hashtags": "#технологии #it #программирование #стартап #tech"
    },
    "fashion": {
        "bg_color": "#FAFAFA",
        "text_color": "#1A1A1A",
        "accent_color": "#9B59B6",
        "font": "Playfair Display",
        "emoji": "👗",
        "category": "Мода и стиль",
        "hashtags": "#мода #стиль #fashion #ньюйорк #outfit"
    },
    "travel": {
        "bg_color": "#E8F4F8",
        "text_color": "#2C3E50",
        "accent_color": "#3498DB",
        "font": "Helvetica Neue",
        "emoji": "✈️",
        "category": "Путешествия",
        "hashtags": "#путешествия #туризм #travel #ньюйорк #wanderlust"
    },
    "finance": {
        "bg_color": "#1B1B2F",
        "text_color": "#EAEAEA",
        "accent_color": "#F7B731",
        "font": "Montserrat",
        "emoji": "💰",
        "category": "Финансы и инвестиции",
        "hashtags": "#финансы #инвестиции #деньги #бизнес #финансоваяграмотность"
    },
    "default": {
        "bg_color": "#FAFAFA",
        "text_color": "#1A1A1A",
        "accent_color": "#6C5CE7",
        "font": "Inter",
        "emoji": "✨",
        "category": "AI Genesis",
        "hashtags": "#советы #лайфхак #бизнес #ньюйорк #ai_genesis"
    }
}

def detect_niche(text):
    """Automatically detect niche from text content"""
    text_lower = text.lower()
    
    niche_keywords = {
        "wellness": ["витамин", "здоровье", "энергия", "чай", "nmn", "суплемент", "иммунитет", "anti-aging", "велнес"],
        "construction": ["ремонт", "строительство", "квартира", "дом", "отделка", "дизайн", "интерьер", "строитель"],
        "beauty": ["салон", "красота", "уход", "космет", "макияж", "маникюр", "процедур", "spa", "кожа"],
        "business": ["бизнес", "автоматизация", "продажи", "клиенты", "crm", "бот", "компания", "услуги"],
        "education": ["курс", "обучение", "урок", "тренинг", "школа", "образование", "учиться", "мастер-класс"],
        "food": ["ресторан", "кафе", "еда", "доставка", "меню", "бронирование", "кухня", "шеф", "блюдо"],
        "realestate": ["недвижимость", "квартира", "продажа", "аренда", "риелтор", "дом", "жильё", "broker"],
        "fitness": ["фитнес", "спорт", "тренировка", "зал", "похудение", "мышцы", "йога", "gym"],
        "tech": ["программирование", "it", "сайт", "приложение", "разработка", "технологии", "software", "app"],
        "fashion": ["мода", "одежда", "стиль", "бренд", "look", "outfit", "тренд", "дизайнер"],
        "travel": ["путешествие", "тур", "отпуск", "отель", "экскурсия", "страна", "город"],
        "finance": ["финансы", "инвестиции", "деньги", "бюджет", "экономия", "доход", "пассивныйдоход"]
    }
    
    scores = {}
    for niche, keywords in niche_keywords.items():
        score = sum(1 for kw in keywords if kw in text_lower)
        if score > 0:
            scores[niche] = score
    
    if scores:
        return max(scores, key=scores.get)
    return "default"

def generate_carousel(text, niche=None, num_slides=None):
    """
    Generate Instagram carousel content for ANY niche
    
    Args:
        text: Source text content
        niche: wellness, construction, beauty, business, etc. (auto-detect if None)
        num_slides: Number of slides (auto if None)
    
    Returns:
        dict with slides content and HTML
    """
    # Auto-detect niche if not specified
    if not niche:
        niche = detect_niche(text)
    
    # Split text into points
    points = [p.strip() for p in text.split('\n') if p.strip()]
    
    if not num_slides:
        num_slides = min(len(points), 7)  # Max 7 slides
    
    template = NICHE_TEMPLATES.get(niche, NICHE_TEMPLATES["default"])
    
    slides = []
    for i, point in enumerate(points[:num_slides]):
        slide = {
            "number": i + 1,
            "content": point[:180],  # Shorter for better readability
            "template": template,
            "emoji": template["emoji"],
            "niche": niche
        }
        slides.append(slide)
    
    # Generate HTML for each slide
    html_slides = []
    for slide in slides:
        html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <link href="https://fonts.googleapis.com/css2?family={template['font'].replace(' ', '+')}:wght@400;700&display=swap" rel="stylesheet">
</head>
<body>
    <div style="background: {slide['template']['bg_color']}; 
                color: {slide['template']['text_color']}; 
                font-family: '{slide['template']['font']}', sans-serif;
                padding: 80px;
                width: 1080px;
                height: 1080px;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                text-align: center;
                box-sizing: border-box;">
        
        <div style="font-size: 32px; margin-bottom: 40px; color: {slide['template']['accent_color']}; font-weight: bold;">
            {slide['emoji']} {slide['number']}/{len(slides)}
        </div>
        
        <h2 style="font-size: 56px; margin-bottom: 50px; line-height: 1.4; font-weight: 700;">
            {slide['content']}
        </h2>
        
        <div style="font-size: 24px; color: {slide['template']['accent_color']}; margin-top: 30px; font-weight: 600;">
            {slide['template']['category']}
        </div>
        
        <div style="font-size: 18px; color: {slide['template']['text_color']}80; margin-top: 50px;">
            AI Genesis
        </div>
    </div>
</body>
</html>"""
        html_slides.append(html)
    
    return {
        "niche": niche,
        "slides": slides,
        "html_slides": html_slides,
        "template": template,
        "caption": generate_caption(text, template, niche)
    }

def generate_caption(text, template, niche):
    """Generate niche-specific Instagram caption"""
    
    lines = text.split('\n')
    topic = lines[0][:60] if lines else "Полезные советы"
    
    captions = {
        "wellness": f"""{topic} 🌿

{text[:150]}...

Сохраните, чтобы не потерять! 📌

Какой совет был самым полезным? Пишите в комментариях 👇

——
{template['hashtags']}

Хотите персональную консультацию? Ссылка в профиле ☝️""",
        
        "construction": f"""{topic} 🛠️

{text[:150]}...

Ремонт — это серьёзно. Доверьте профессионалам! 💪

Есть вопросы? Задавайте в комментариях — отвечу каждому 👇

——
{template['hashtags']}

Бесплатная консультация — ссылка в профиле ☝️""",
        
        "business": f"""{topic} 🚀

{text[:150]}...

Автоматизация экономит 15+ часов в неделю. Проверено! ✅

Какие задачи отнимают больше всего времени у вас? 👇

——
{template['hashtags']}

Обсудим ваш кейс — ссылка в профиле ☝️""",
        
        "default": f"""{topic} ✨

{text[:150]}...

Сохраните, чтобы не потерять! 📌

Какой совет был самым полезным? Пишите в комментариях 👇

——
{template['hashtags']}

Хотите узнать больше? Ссылка в профиле ☝️"""
    }
    
    return captions.get(niche, captions["default"])

def generate_story(text, niche=None):
    """Generate story format (9:16) for any niche"""
    if not niche:
        niche = detect_niche(text)
    
    template = NICHE_TEMPLATES.get(niche, NICHE_TEMPLATES["default"])
    
    html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <link href="https://fonts.googleapis.com/css2?family={template['font'].replace(' ', '+')}:wght@400;700&display=swap" rel="stylesheet">
</head>
<body>
    <div style="background: {template['bg_color']}; 
                color: {template['text_color']}; 
                font-family: '{template['font']}', sans-serif;
                padding: 80px 60px;
                width: 1080px;
                height: 1920px;
                display: flex;
                flex-direction: column;
                justify-content: center;
                box-sizing: border-box;">
        <div style="font-size: 72px; line-height: 1.5; margin-bottom: 60px; font-weight: 700;">
            {template['emoji']} {text[:250]}
        </div>
        <div style="font-size: 36px; color: {template['accent_color']}; margin-top: auto; font-weight: 600;">
            {template['category']}
        </div>
        <div style="font-size: 32px; color: {template['accent_color']}; margin-top: 40px;">
            👆 Свайпай →
        </div>
    </div>
</body>
</html>"""
    
    return {
        "format": "story",
        "niche": niche,
        "html": html,
        "text": text[:500],
        "template": template
    }

def save_carousel(result, output_dir="/root/.openclaw/output/instagram"):
    """Save carousel to files"""
    os.makedirs(output_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    folder = os.path.join(output_dir, f"carousel_{timestamp}")
    os.makedirs(folder, exist_ok=True)
    
    # Save metadata
    with open(os.path.join(folder, "metadata.json"), "w", encoding="utf-8") as f:
        json.dump({
            "niche": result["niche"],
            "category": result["template"]["category"],
            "total_slides": len(result["slides"]),
            "caption": result["caption"],
            "slides": [{"number": s["number"], "content": s["content"]} for s in result["slides"]]
        }, f, ensure_ascii=False, indent=2)
    
    # Save HTML files
    for i, html in enumerate(result["html_slides"]):
        with open(os.path.join(folder, f"slide_{i+1}.html"), "w", encoding="utf-8") as f:
            f.write(html)
    
    # Save caption
    with open(os.path.join(folder, "caption.txt"), "w", encoding="utf-8") as f:
        f.write(result["caption"])
    
    return folder

def main():
    if len(sys.argv) < 2:
        print("🎨 Instagram Carousel Generator for ANY Niche")
        print("")
        print("Usage:")
        print("  python3 generate_carousel.py 'Your text content' [niche]")
        print("")
        print("Available niches:")
        for niche in NICHE_TEMPLATES.keys():
            if niche != "default":
                print(f"  • {niche}")
        print("")
        print("Examples:")
        print("  python3 generate_carousel.py '5 советов по ремонту' construction")
        print("  python3 generate_carousel.py 'Витамины для энергии' wellness")
        print("  python3 generate_carousel.py 'Автоматизация бизнеса' (auto-detect)")
        sys.exit(1)
    
    text = sys.argv[1]
    niche = sys.argv[2] if len(sys.argv) > 2 else None
    
    result = generate_carousel(text, niche=niche)
    folder = save_carousel(result)
    
    print(f"✅ Carousel generated: {folder}")
    print(f"   Niche: {result['niche']} ({result['template']['category']})")
    print(f"   Slides: {len(result['slides'])}")
    print(f"   Emoji: {result['template']['emoji']}")
    print(f"\n📱 Caption preview:")
    print(result['caption'][:300] + "...")

if __name__ == "__main__":
    main()
