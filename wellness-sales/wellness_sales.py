#!/usr/bin/env python3
"""
Wellness & Supplement Sales Automator for AI Genesis
Organic sales of wellness products through educational content
Scientific approach (PhD-level) without aggressive sales
"""

import json
import random
from typing import Dict, List, Optional, Tuple
from datetime import datetime

class WellnessSalesAutomator:
    """
    Creates organic sales content for wellness products
    - Teas, supplements, skincare
    - Reels, Stories, Telegram content
    - Science-based, no medical claims
    """
    
    # Product Database Template
    PRODUCT_TEMPLATES = {
        "anti_aging_supplement": {
            "name": "NMN Complex",
            "category": "supplement",
            "key_ingredients": [
                {"name": "NMN (β-Nicotinamide Mononucleotide)", "dosage": "250mg", "benefit": "NAD+ precursor, cellular energy"},
                {"name": "Resveratrol", "dosage": "100mg", "benefit": "Antioxidant, sirtuin activator"},
                {"name": "Quercetin", "dosage": "50mg", "benefit": "Senolytic, inflammation support"}
            ],
            "mechanism": "NMN boosts NAD+ levels, declining 50% by age 50. Resveratrol activates 'longevity genes' (sirtuins). Combined effect: cellular repair + energy production.",
            "science_refs": [
                "Harvard Medical School: NAD+ declines with age (Sinclair, 2019)",
                "Nature: NMN improves muscle function in aging mice (2021)",
                "Cell Metabolism: Resveratrol and sirtuin activation"
            ],
            "target_audience": "35-60, biohackers, health-conscious professionals",
            "pain_points": ["Low energy", "Aging concerns", "Brain fog", "Recovery time"],
            "price_position": "Premium ($45-75/month)",
            "differentiators": ["Third-party tested", "Clean ingredients", "PhD-formulated"]
        },
        "adaptogenic_tea": {
            "name": "Calm Focus Tea",
            "category": "tea",
            "key_ingredients": [
                {"name": "Ashwagandha (KSM-66)", "dosage": "300mg", "benefit": "Cortisol reduction, stress resilience"},
                {"name": "L-Theanine", "dosage": "100mg", "benefit": "Calm alertness, alpha brain waves"},
                {"name": "Rhodiola Rosea", "dosage": "200mg", "benefit": "Fatigue resistance, mental clarity"}
            ],
            "mechanism": "Ashwagandha modulates HPA axis, reducing cortisol 20-30%. L-Theanine increases alpha waves without drowsiness. Rhodiola supports ATP production under stress.",
            "science_refs": [
                "Journal of Ayurveda: Ashwagandha cortisol reduction (2019)",
                "Nutritional Neuroscience: L-Theanine alpha waves (2008)",
                "Phytomedicine: Rhodiola fatigue resistance (2015)"
            ],
            "target_audience": "25-45, entrepreneurs, students, stressed professionals",
            "pain_points": ["Anxiety", "Procrastination", "Mental fatigue", "Sleep issues"],
            "price_position": "Mid-range ($25-35/month)",
            "differentiators": ["Organic sourced", "No caffeine crash", "Backed by 15+ studies"]
        },
        "skincare_serum": {
            "name": "Cellular Renewal Serum",
            "category": "skincare",
            "key_ingredients": [
                {"name": "Retinol 0.3%", "dosage": "0.3%", "benefit": "Cell turnover, collagen synthesis"},
                {"name": "Niacinamide 5%", "dosage": "5%", "benefit": "Barrier repair, pore reduction"},
                {"name": "Peptide Complex", "dosage": "2%", "benefit": "Signal proteins, firmness"}
            ],
            "mechanism": "Retinol accelerates cell turnover (28→14 days). Niacinamide strengthens skin barrier + reduces inflammation. Peptides signal collagen production.",
            "science_refs": [
                "Journal of Cosmetic Dermatology: Retinol efficacy (2006)",
                "British Journal of Dermatology: Niacinamide barrier function (2010)",
                "Cosmetics: Peptides in anti-aging (2017)"
            ],
            "target_audience": "30-55, skincare enthusiasts, aging concerns",
            "pain_points": ["Fine lines", "Uneven texture", "Dullness", "Sensitivity"],
            "price_position": "Premium ($60-90/bottle)",
            "differentiators": ["Encapsulated retinol", "Gentle formula", "Dermatologist-tested"]
        }
    }
    
    # Content Matrix Templates
    CONTENT_TEMPLATES = {
        "reels_script": {
            "duration": "60 сек",
            "structure": {
                "hook_0_3": [
                    "Я биолог с PhD и вот что я обнаружила про {product}...",
                    "3 ингредиента, которые реально работают (не маркетинг)",
                    "Почему я перестала покупать дешёвые {category}",
                    "В 2025 я исследовала 50+ формул. Вывод:"
                ],
                "education_3_45": {
                    "format": "Простое объяснение механизма",
                    "elements": ["Визуал ингредиента", "Анимация механизма", "Сравнение до/после"]
                },
                "cta_45_60": [
                    "Ссылка в шапке — состав и исследования",
                    "Пиши 'СОСТАВ' — вышлю разбор",
                    "Больше науки — подписка",
                    "Заказать с тестом на совместимость"
                ]
            },
            "captions": {
                "russian": "🔬 Научный разбор {product}\n\nКлючевые находки:\n✓ {ingredient_1}\n✓ {ingredient_2}\n✓ {ingredient_3}\n\n⚠️ Не медицинский совет. Для образовательных целей.\n\n#antiaging #biohacking #наука #здоровье",
                "english": "🔬 Science breakdown of {product}\n\nKey findings:\n✓ {ingredient_1}\n✓ {ingredient_2}\n✓ {ingredient_3}\n\n⚠️ Not medical advice. Educational purposes only.\n\n#antiaging #biohacking #science #wellness"
            }
        },
        "instagram_post": {
            "format": "Carousel (5-7 slides)",
            "slides": [
                {"type": "hook", "content": "Почему {product} работает (научно)"},
                {"type": "problem", "content": "Миф vs Реальность: {common_myth}"},
                {"type": "mechanism", "content": "Как это работает: {mechanism_short}"},
                {"type": "ingredients", "content": "3 ключевых ингредиента:\n{ingredients_list}"},
                {"type": "research", "content": "Исследование: {study_summary}"},
                {"type": "results", "content": "Что ожидать: {expected_results}"},
                {"type": "cta", "content": "🔗 Ссылка в bio\n💬 Вопросы в комментариях"}
            ]
        },
        "telegram_post": {
            "format": "Глубокий разбор (1500-2000 символов)",
            "structure": [
                "## Почему я начала использовать {product}",
                "### Личный контекст (2-3 предложения)",
                "### Научный механизм",
                "### Ключевые ингредиенты с дозировками",
                "### Исследования (2-3 ссылки/названия)",
                "### Мой протокол использования",
                "### Ограничения и противопоказания",
                "### Где заказать + промокод"
            ],
            "tone": "Честный исследователь, не продавец"
        },
        "youtube_shorts": {
            "duration": "30-60 сек",
            "hooks": [
                "5 фактов о {product}, которые изменят твой подход",
                "Я проверила 20 формул. Вот единственная, которая работает",
                "Доктор объясняет: почему {ingredient} — это не хайп"
            ],
            "structure": [
                "Факт 1: {fact_1} (6-8 сек)",
                "Факт 2: {fact_2} (6-8 сек)",
                "Факт 3: {fact_3} (6-8 сек)",
                "Факт 4: {fact_4} (6-8 сек)",
                "Факт 5: {fact_5} + CTA (6-8 сек)"
            ]
        },
        "email_sequence": {
            "subject_lines": [
                "🔬 Исследование: что я нашла про {product}",
                "Состав, который реально работает (не маркетинг)",
                "Мой личный эксперимент с {product}",
                "Вопрос: почему дорогие {category} лучше дешёвых?"
            ],
            "structure": {
                "intro": "Привет! Я {name}, биолог с PhD. 3 года исследую...",
                "education": "Ключевой ингредиент: {ingredient}\n\nМеханизм: {mechanism}",
                "social_proof": "Исследование {study}: {results}",
                "objection": "\"Но ведь дорого?\" — разбор стоимости за день",
                "cta": "Попробовать с гарантией / Задать вопрос"
            }
        }
    }
    
    # Objection Handling (Science-Based)
    OBJECTIONS_LIBRARY = {
        "too_expensive": {
            "objection": "Дорого по сравнению с обычными витаминами",
            "response": "Разница в биодоступности. Дешёвые формы (оксид цинка, синтетические витамины) усваиваются 5-10%. Наши — хелатные/активные формы с 80%+ усвоением. Пересчёт: 1 качественная капсула = 8-10 дешёвых.",
            "science": "Journal of Nutrition: bioavailability comparison study (2018)"
        },
        "does_it_work": {
            "objection": "А доказано, что работает?",
            "response": "NMN — 200+ исследований на PubMed. Ключевое: Harvard 2019 — восстановление NAD+ у мышей. Human trials: 2020-2024 показывают повышение NAD+ 40-60%. Это не 'чудо-таблетка', а восполнение дефицита, который накапливается с 30 лет.",
            "science": "Imai & Guarente, Cell Metabolism (2014); Harvard Health (2019)"
        },
        "side_effects": {
            "objection": "А побочки? Боюсь начинать",
            "response": "Известные: лёгкая тошнота в первую неделю (5% людей). Контриндикации: беременность, химиотерапия. Важно: начинать с ½ дозы, принимать утром (может бодрить). Я начинала так и отслеживала 2 недели.",
            "science": "Clinical safety trials: 2020-2023, doses up to 900mg/day"
        },
        "how_long": {
            "objection": "Сколько пить до результата?",
            "response": "NAD+ повышается через 2 недели (метаболиты в крови). Субъективно: энергия — 3-4 недели, кожа — 8-12 недель. Я фиксировала через Oura Ring: глубокий сон +15%, HRV +12% через месяц.",
            "science": "Irie et al., 2020; subjective wellness markers meta-analysis"
        },
        "fake_science": {
            "objection": "Опять псевдонаука для лохов",
            "response": "Согласна, рынок замусорен. Отличить: 1) Есть ли исследования in vivo (не just in vitro)? 2) Дозировки как в исследованиях? 3) Форма (NMN vs NR vs NAD+ — разница огромна). Я выбираю по PubMed-ссылкам, не по рекламе. Вот 3 ключевых исследования...",
            "science": "PubMed links provided on request"
        }
    }
    
    # Compliance Guidelines (FDA/FTC Safe)
    COMPLIANCE_RULES = [
        "✓ Использовать: 'поддерживает', 'способствует', 'восполняет дефицит'",
        "✓ Добавлять: 'Не является медицинским советом'",
        "✓ Цитировать: реальные исследования с DOI",
        "✗ Запрещено: 'лечит', 'предотвращает', 'гарантированный результат'",
        "✗ Запрещено: 'FDA approved' (для суплементов)",
        "✗ Запрещено: до/после фото без disclaimer"
    ]
    
    def __init__(self):
        self.products = self.PRODUCT_TEMPLATES
    
    def analyze_product(self, product_key: str) -> Dict:
        """Get full product analysis"""
        if product_key not in self.products:
            return {"error": f"Product not found. Available: {list(self.products.keys())}"}
        return self.products[product_key]
    
    def generate_reels_script(self, product_key: str) -> Dict:
        """Generate Reels script with hook, education, CTA"""
        product = self.products.get(product_key)
        if not product:
            return {"error": "Product not found"}
        
        ingredients = ", ".join([i["name"] for i in product["key_ingredients"][:3]])
        
        script = {
            "duration": "60 сек",
            "hook": random.choice(self.CONTENT_TEMPLATES["reels_script"]["structure"]["hook_0_3"]).format(
                product=product["name"],
                category=product["category"]
            ),
            "education": {
                "content": product["mechanism"],
                "visuals": ["Structure of " + i["name"] for i in product["key_ingredients"]],
                "key_points": [
                    f"{i['name']}: {i['benefit']}" 
                    for i in product["key_ingredients"]
                ]
            },
            "cta": random.choice(self.CONTENT_TEMPLATES["reels_script"]["structure"]["cta_45_60"]),
            "captions": {
                "ru": self.CONTENT_TEMPLATES["reels_script"]["captions"]["russian"].format(
                    product=product["name"],
                    ingredient_1=product["key_ingredients"][0]["name"],
                    ingredient_2=product["key_ingredients"][1]["name"],
                    ingredient_3=product["key_ingredients"][2]["name"]
                ),
                "en": self.CONTENT_TEMPLATES["reels_script"]["captions"]["english"].format(
                    product=product["name"],
                    ingredient_1=product["key_ingredients"][0]["name"],
                    ingredient_2=product["key_ingredients"][1]["name"],
                    ingredient_3=product["key_ingredients"][2]["name"]
                )
            },
            "compliance_note": "⚠️ Добавить: 'Не медицинский совет. Обратитесь к врачу'"
        }
        return script
    
    def generate_instagram_carousel(self, product_key: str) -> List[Dict]:
        """Generate Instagram carousel slides"""
        product = self.products.get(product_key)
        if not product:
            return []
        
        slides = []
        template = self.CONTENT_TEMPLATES["instagram_post"]
        
        for slide in template["slides"]:
            content = slide["content"]
            # Replace placeholders
            content = content.replace("{product}", product["name"])
            content = content.replace("{category}", product["category"])
            content = content.replace("{mechanism_short}", product["mechanism"][:100] + "...")
            content = content.replace("{ingredients_list}", "\n".join([
                f"• {i['name']} — {i['benefit']}" 
                for i in product["key_ingredients"]
            ]))
            content = content.replace("{study_summary}", product["science_refs"][0])
            content = content.replace("{expected_results}", "Энергия, фокус, восстановление")
            content = content.replace("{common_myth}", "все добавки одинаковые")
            
            slides.append({
                "type": slide["type"],
                "content": content
            })
        
        return slides
    
    def generate_telegram_post(self, product_key: str) -> str:
        """Generate long-form Telegram post"""
        product = self.products.get(product_key)
        if not product:
            return "Product not found"
        
        ingredients_text = "\n".join([
            f"**{i['name']}** — {i['dosage']}\n{i['benefit']}\n" 
            for i in product["key_ingredients"]
        ])
        
        post = f"""## 🧬 Почему я использую {product['name']}

*{datetime.now().strftime('%d %B %Y')}*

### От биолога с 10-летним стажем

Я долгое время скептически относилась к добавкам. Слишком много хайпа, слишком мало данных. Но после 3 лет исследований и тестирования на себе, нашла комбинацию, которая реально работает — с доказательной базой.

### Что внутри (и почему это важно)

{ingredients_text}

### Механизм простыми словами

{product['mechanism']}

### Исследования, которые изменили моё мнение

"""
        for ref in product["science_refs"]:
            post += f"• {ref}\n"
        
        post += f"""
### Мой личный протокол

• Дозировка: как на упаковке
• Время: утром, с едой
• Длительность: минимум 3 месяца для оценки
• Отслеживание: энергия, сон, восстановление

### Честно о минусах

• Цена: выше масс-маркета
• Эффект: не мгновенный, 3-4 недели
• Не для: беременных, при химиотерапии

### Где заказать

Ссылка в шапке канала. Код **SCIENCE10** — 10% на первый заказ.

⚠️ *Не является медицинским советом. Проконсультируйтесь с врачом.*

#биохакинг #наука #{product['category']} #antiaging
"""
        return post
    
    def generate_objections_guide(self, product_key: str) -> Dict:
        """Generate objection handling for product"""
        return {
            "product": product_key,
            "objections": self.OBJECTIONS_LIBRARY,
            "usage_guide": "Использовать в ответах на комментарии, Stories Q&A, личных сообщениях"
        }
    
    def compare_ingredients(self, product1_key: str, product2_key: str) -> Dict:
        """Compare two products ingredient by ingredient"""
        p1 = self.products.get(product1_key)
        p2 = self.products.get(product2_key)
        
        if not p1 or not p2:
            return {"error": "One or both products not found"}
        
        comparison = {
            "product_1": p1["name"],
            "product_2": p2["name"],
            "ingredient_comparison": [],
            "price_comparison": f"{p1['price_position']} vs {p2['price_position']}",
            "winner": None
        }
        
        # Compare key ingredients
        for i1 in p1["key_ingredients"]:
            found = False
            for i2 in p2["key_ingredients"]:
                if i1["name"].lower() in i2["name"].lower() or i2["name"].lower() in i1["name"].lower():
                    comparison["ingredient_comparison"].append({
                        "ingredient": i1["name"],
                        "product_1_dosage": i1["dosage"],
                        "product_2_dosage": i2["dosage"],
                        "comparison": "Match" if i1["dosage"] == i2["dosage"] else "Different dosage"
                    })
                    found = True
                    break
            if not found:
                comparison["ingredient_comparison"].append({
                    "ingredient": i1["name"],
                    "product_1_dosage": i1["dosage"],
                    "product_2_dosage": "Not present",
                    "comparison": "Unique to product 1"
                })
        
        return comparison
    
    def generate_content_calendar(self, days: int = 30) -> List[Dict]:
        """Generate monthly content calendar"""
        calendar = []
        product_keys = list(self.products.keys())
        content_types = ["reels", "carousel", "telegram", "stories", "email"]
        
        for day in range(1, days + 1):
            product = random.choice(product_keys)
            content_type = content_types[day % len(content_types)]
            
            calendar.append({
                "day": day,
                "product": product,
                "content_type": content_type,
                "topic": random.choice([
                    "Ingredient deep dive",
                    "Science breakdown",
                    "Personal experience",
                    "Myth busting",
                    "Comparison"
                ]),
                "status": "planned"
            })
        
        return calendar
    
    def generate_full_package(self, product_key: str) -> Dict:
        """Generate complete content package for product"""
        return {
            "product": self.analyze_product(product_key),
            "reels_script": self.generate_reels_script(product_key),
            "instagram_carousel": self.generate_instagram_carousel(product_key),
            "telegram_post": self.generate_telegram_post(product_key),
            "objections_guide": self.generate_objections_guide(product_key),
            "compliance_checklist": self.COMPLIANCE_RULES,
            "generated_at": datetime.now().isoformat()
        }
    
    def generate_report(self, product_key: str) -> str:
        """Generate human-readable report"""
        package = self.generate_full_package(product_key)
        
        report = f"""
╔══════════════════════════════════════════════════════════════════╗
║  🌿 WELLNESS SALES AUTOMATOR — Content Package                    ║
║  Product: {package['product']['name'][:40]:<40} ║
║  Generated: {datetime.now().strftime('%Y-%m-%d'):<40} ║
╚══════════════════════════════════════════════════════════════════╝

═══════════════════════════════════════════════════════════════════
  📊 PRODUCT ANALYSIS
═══════════════════════════════════════════════════════════════════

Name: {package['product']['name']}
Category: {package['product']['category']}
Target: {package['product']['target_audience']}
Price: {package['product']['price_position']}

Key Ingredients:
"""
        for ing in package['product']['key_ingredients']:
            report += f"   • {ing['name']} ({ing['dosage']}) — {ing['benefit']}\n"
        
        report += f"""
Mechanism:
   {package['product']['mechanism'][:200]}...

═══════════════════════════════════════════════════════════════════
  🎬 REELS SCRIPT (60 sec)
═══════════════════════════════════════════════════════════════════

🪝 HOOK (0-3 sec):
   "{package['reels_script']['hook']}"

📚 EDUCATION (3-45 sec):
   {package['reels_script']['education']['content'][:150]}...
   
   Key points:
"""
        for point in package['reels_script']['education']['key_points']:
            report += f"   • {point}\n"
        
        report += f"""
📢 CTA (45-60 sec):
   {package['reels_script']['cta']}

📝 CAPTION (Russian):
{package['reels_script']['captions']['ru']}

═══════════════════════════════════════════════════════════════════
  📸 INSTAGRAM CAROUSEL (7 slides)
═══════════════════════════════════════════════════════════════════
"""
        for i, slide in enumerate(package['instagram_carousel'], 1):
            report += f"""
Slide {i} ({slide['type']}):
   {slide['content'][:100]}{'...' if len(slide['content']) > 100 else ''}
"""
        
        report += f"""
═══════════════════════════════════════════════════════════════════
  💬 TELEGRAM POST (excerpt)
═══════════════════════════════════════════════════════════════════

{package['telegram_post'][:500]}...

═══════════════════════════════════════════════════════════════════
  🛡️ OBJECTION HANDLING
═══════════════════════════════════════════════════════════════════
"""
        for key, obj in package['objections_guide']['objections'].items():
            report += f"""
❓ {obj['objection']}
💬 {obj['response'][:150]}...
📚 Source: {obj['science']}
"""
        
        report += """
═══════════════════════════════════════════════════════════════════
  ✅ COMPLIANCE CHECKLIST
═══════════════════════════════════════════════════════════════════
"""
        for rule in package['compliance_checklist']:
            report += f"   {rule}\n"
        
        report += """
═══════════════════════════════════════════════════════════════════
  📅 NEXT STEPS
═══════════════════════════════════════════════════════════════════
   1. Record Reels with hook + education + CTA
   2. Design carousel slides in Canva
   3. Post Telegram with proper formatting
   4. Set up Stories Q&A for objections
   5. Track engagement metrics

═══════════════════════════════════════════════════════════════════
"""
        return report


def main():
    import sys
    
    automator = WellnessSalesAutomator()
    
    if len(sys.argv) < 2:
        print("🌿 Wellness & Supplement Sales Automator")
        print("")
        print("Usage:")
        print("  python3 wellness_sales.py products              # List available products")
        print("  python3 wellness_sales.py analyze [product]     # Product analysis")
        print("  python3 wellness_sales.py reels [product]       # Generate Reels script")
        print("  python3 wellness_sales.py carousel [product]    # Instagram carousel")
        print("  python3 wellness_sales.py telegram [product]    # Telegram post")
        print("  python3 wellness_sales.py objections [product]  # Objection handling")
        print("  python3 wellness_sales.py compare [p1] [p2]     # Compare products")
        print("  python3 wellness_sales.py calendar [days]       # Content calendar")
        print("  python3 wellness_sales.py package [product]     # Full content package")
        print("  python3 wellness_sales.py report [product]      # Human-readable report")
        print("")
        print("Products: anti_aging_supplement, adaptogenic_tea, skincare_serum")
        sys.exit(0)
    
    command = sys.argv[1]
    
    if command == "products":
        print("🌿 Available Products:\n")
        for key, product in automator.products.items():
            print(f"  {key}:")
            print(f"    Name: {product['name']}")
            print(f"    Category: {product['category']}")
            print(f"    Price: {product['price_position']}")
            print()
    
    elif command == "analyze":
        product = sys.argv[2] if len(sys.argv) > 2 else "anti_aging_supplement"
        result = automator.analyze_product(product)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    elif command == "reels":
        product = sys.argv[2] if len(sys.argv) > 2 else "anti_aging_supplement"
        result = automator.generate_reels_script(product)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    elif command == "carousel":
        product = sys.argv[2] if len(sys.argv) > 2 else "anti_aging_supplement"
        result = automator.generate_instagram_carousel(product)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    elif command == "telegram":
        product = sys.argv[2] if len(sys.argv) > 2 else "anti_aging_supplement"
        print(automator.generate_telegram_post(product))
    
    elif command == "objections":
        product = sys.argv[2] if len(sys.argv) > 2 else "anti_aging_supplement"
        result = automator.generate_objections_guide(product)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    elif command == "compare":
        if len(sys.argv) < 4:
            print("❌ Need 2 products to compare")
            print("Usage: python3 wellness_sales.py compare anti_aging_supplement adaptogenic_tea")
            sys.exit(1)
        result = automator.compare_ingredients(sys.argv[2], sys.argv[3])
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    elif command == "calendar":
        days = int(sys.argv[2]) if len(sys.argv) > 2 else 30
        result = automator.generate_content_calendar(days)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    elif command == "package":
        product = sys.argv[2] if len(sys.argv) > 2 else "anti_aging_supplement"
        result = automator.generate_full_package(product)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    elif command == "report":
        product = sys.argv[2] if len(sys.argv) > 2 else "anti_aging_supplement"
        report = automator.generate_report(product)
        print(report)
        
        # Save to file
        from datetime import datetime
        output_file = f"/root/.openclaw/output/wellness_{product}_{datetime.now().strftime('%Y%m%d')}.md"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"\n💾 Saved to: {output_file}")
    
    else:
        print(f"❌ Unknown command: {command}")
        print("Run without arguments for help")


if __name__ == "__main__":
    main()
