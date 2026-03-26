#!/usr/bin/env python3
"""
Carousel Preview Generator — создаёт ASCII/визуальный превью карусели
"""

import json
import sys

def generate_preview(metadata_path):
    with open(metadata_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    brand = data['brand']
    palette = data['palette']
    
    preview = f"""
╔══════════════════════════════════════════════════════════════════╗
║           🎠 CAROUSEL PRO PREVIEW                                ║
╠══════════════════════════════════════════════════════════════════╣
║  Бренд: {brand['name']:<48}║
║  Handle: {brand['handle']:<47}║
║  Primary: {palette['BRAND_PRIMARY']}  Light: {palette['BRAND_LIGHT']}  Dark: {palette['BRAND_DARK']}    ║
╚══════════════════════════════════════════════════════════════════╝

"""
    
    slides_content = [
        ("HERO", "Светлый", "5 причин выбрать ремонт квартир в Нью-Йорке", True),
        ("PROBLEM", "Тёмный", "Без правильного подхода вы теряете время и деньги", True),
        ("SOLUTION", "Градиент", "Профессиональный ремонт — инвестиция в результат", True),
        ("FEATURES", "Светлый", "Преимущества: подход, смета, гарантия", True),
        ("DETAILS", "Тёмный", "Профессионализм в каждой детали", True),
        ("STEPS", "Светлый", "3 этапа: консультация → смета → работа", True),
        ("CTA", "Градиент", "Готовы начать? Начать проект →", False),
    ]
    
    for i, (slide_type, bg, content, has_arrow) in enumerate(slides_content, 1):
        arrow = "→" if has_arrow else " "
        progress = "█" * i + "░" * (7 - i)
        
        bg_emoji = {"Светлый": "⬜", "Тёмный": "⬛", "Градиент": "🟪"}[bg]
        
        preview += f"""
┌────────────────────────────────────────────────────────────────┐
│  СЛАЙД {i}/7  [{slide_type:<10}]  {bg_emoji} {bg:<10}              │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│   🅰️  {brand['name']:<50}│
│                                                                │
│   {content:<58}│
│                                                                │
│                                                                │
│   {progress} {i}/7     {arrow}                                   │
└────────────────────────────────────────────────────────────────┘
"""
    
    preview += f"""
╔══════════════════════════════════════════════════════════════════╗
║  📁 Файлы:                                                       ║
║    • carousel.html — полная карусель (все слайды)               ║
║    • slide_1.html ~ slide_7.html — отдельные слайды             ║
║    • caption.txt — подпись для Instagram                        ║
║    • metadata.json — бренд, палитра, шрифты                     ║
╚══════════════════════════════════════════════════════════════════╝

💡 Для конвертации в PNG:
   Откройте slide_*.html в браузере → Скриншот → 1080×1350px
"""
    
    return preview

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 preview.py <metadata.json>")
        sys.exit(1)
    
    print(generate_preview(sys.argv[1]))
