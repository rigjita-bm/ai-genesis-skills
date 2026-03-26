# Carousel Pro — Multi-Mode Instagram Carousel Generator

Professional Instagram carousel generator with 5 design modes for different audiences.

## Installation

```bash
pip install playwright
playwright install chromium
```

## Design Modes

| Mode | Audience | Style |
|------|----------|-------|
| **Executive** (corporate) | B2B, Finance, Consulting | Clean, trustworthy, gold accents |
| **Velocity** (startup) | SaaS, Tech, AI | Bold gradients, glassmorphism, glow |
| **Essence** (lifestyle) | Beauty, Fashion, Travel | Editorial, warm tones, photo-centric |
| **Serenity** (wellness) | Health, Yoga, Organic | Calm, earth tones, natural |
| **Bold** (creator) | Personal brand, Coaches | Maximalist, experimental, vibrant |

## Quick Start

```bash
# List all modes
python carousel_pro.py --list-modes

# Generate with auto mode detection
python carousel_pro.py "AI автоматизация для бизнеса"

# Specify mode explicitly
python carousel_pro.py "Юридические услуги" --mode=corporate
python carousel_pro.py "Новый SaaS продукт" --mode=startup
python carousel_pro.py "Йога курсы" --mode=wellness
python carousel_pro.py "Коучинг" --mode=creator

# Export to PNG
python carousel_pro.py "Тема" --mode=startup --export=png

# Generate ZIP with all assets
python carousel_pro.py "Тема" --export=zip

# Preview with Instagram iPhone frame
python carousel_pro.py "Тема" --preview --preview-slide=1

# Custom brand
python carousel_pro.py "Тема" --brand="My Company" --handle="@mycompany"
```

## CLI Options

```
positional arguments:
  topic                 Topic for the carousel

optional arguments:
  -h, --help            show help message
  -m, --mode            Design mode: auto, corporate, startup, lifestyle, wellness, creator
  -e, --export          Export format: html, png, both, zip
  -p, --preview         Generate Instagram preview
  --preview-slide       Which slide to preview (1-7, default: 1)
  -n, --name            Output name
  --brand               Brand name
  --handle              Social media handle
  --list-modes          List available modes
```

## Mode Selection

### Corporate (Executive)
- **Typography:** Libre Baskerville (serif headings) + Inter (body)
- **Colors:** Deep navy (#1E3A5F) with gold accents (#C9A227)
- **Effects:** None (clean), conservative whitespace
- **Best for:** B2B, Finance, Legal, Consulting

### Startup (Velocity)
- **Typography:** Space Grotesk (geometric) + DM Sans (modern)
- **Colors:** Indigo→Pink→Yellow gradient
- **Effects:** Glassmorphism, glow, gradient text
- **Best for:** SaaS, Tech, AI, Apps

### Lifestyle (Essence)
- **Typography:** Playfair Display (editorial serif) + Lora (warm)
- **Colors:** Terracotta, sage, warm cream
- **Effects:** Organic shapes, paper texture, italic headings
- **Best for:** Beauty, Fashion, Travel, Food

### Wellness (Serenity)
- **Typography:** Cormorant Garamond (elegant serif) + Nunito Sans (friendly)
- **Colors:** Sage green, sand, warm white
- **Effects:** Soft organic shapes, nature icons
- **Best for:** Health, Supplements, Yoga, Organic

### Creator (Bold)
- **Typography:** Anton (bold condensed) + Space Grotesk (technical)
- **Colors:** Hot pink (#FF006E), orange, yellow, cyan
- **Effects:** 3D shadows, glitch text, glowing orbs, rainbow gradients
- **Best for:** Personal brands, Coaches, Artists

## Architecture

```
carousel-pro/
├── modes/
│   ├── __init__.py          # Mode registry
│   ├── base_mode.py         # Abstract base class
│   ├── corporate_mode.py    # Executive mode
│   ├── startup_mode.py      # Velocity mode
│   ├── lifestyle_mode.py    # Essence mode
│   ├── wellness_mode.py     # Serenity mode
│   └── creator_mode.py      # Bold mode
├── templates/               # Jinja2 templates (future)
├── carousel_pro.py         # Main CLI controller
├── png_export.py           # PNG export + Instagram preview
└── SKILL.md                # Documentation
```

## Slide Structure (7 slides)

1. **Hero** — Hook with logo lockup
2. **Problem** — Pain points (varies by mode)
3. **Solution** — Answer with mode-specific styling
4. **Features** — What you get (icon grid)
5. **Details** — Stats and numbers
6. **How-to** — Process steps
7. **CTA** — Call to action (no arrow, full progress)

## Export Options

### HTML Only
```bash
python carousel_pro.py "Тема" --export=html
```
Creates interactive HTML with all slides displayed vertically.

### PNG Images
```bash
python carousel_pro.py "Тема" --export=png
```
Generates 7 PNG files (1080×1350px) ready for Instagram upload.

### Both HTML + PNG
```bash
python carousel_pro.py "Тема" --export=both
```

### ZIP Archive
```bash
python carousel_pro.py "Тема" --export=zip
```
Creates ZIP with all PNGs for easy download.

### Instagram Preview
```bash
python carousel_pro.py "Тема" --preview --preview-slide=1
```
Generates preview with iPhone 14 Pro frame showing exactly how the carousel will look on Instagram.

## Customization

### Brand Config
```python
brand = {
    "name": "AI Genesis",
    "handle": "@aigenesis.ai",
    "tagline": "Automate your business"
}
```

### Content Generation
Content auto-generated based on topic type:
- Business topics → Business template
- Product topics → Product template
- Service topics → Service template

## Bot Integration (Sprint 4) ✅

Telegram bot commands available:

```
/carousel <topic> [mode]     # Generate and send carousel
/carousel_modes              # List available modes
```

### Bot Usage Examples

```
/carousel AI Automation startup
/carousel Legal Services corporate  
/carousel Yoga Courses wellness
/carousel Personal Brand creator
/carousel Fashion Collection lifestyle
```

### Mode Auto-Detection

Bot automatically detects mode from keywords:
- `startup`, `saas`, `tech`, `ai` → Velocity mode
- `corporate`, `b2b`, `finance` → Executive mode
- `wellness`, `health`, `yoga` → Serenity mode
- `lifestyle`, `beauty`, `fashion` → Essence mode
- `creator`, `coach`, `personal brand` → Bold mode

## Implementation Status

| Sprint | Task | Status |
|--------|------|--------|
| 1 | Foundation + BaseMode | ✅ Done |
| 1 | Corporate mode | ✅ Done |
| 1 | Startup mode | ✅ Done |
| 2 | Lifestyle mode | ✅ Done |
| 2 | Wellness mode | ✅ Done |
| 2 | Creator mode | ✅ Done |
| 3 | PNG Export | ✅ Done |
| 3 | Instagram Preview | ✅ Done |
| 4 | Bot Integration | ✅ Done |
| 5 | AI Content Generation | ⏳ Optional |

## Dependencies

```
playwright>=1.40.0
```

## Bot Integration (Sprint 4)

Planned Telegram bot commands:
```
/carousel <topic> [mode]   # Generate carousel
/carousel modes            # List modes
```
