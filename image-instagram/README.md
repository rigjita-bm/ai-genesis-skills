# Instagram Content Generator

Generate Instagram carousel posts, stories, and reels captions from text content.

## Usage

```bash
python3 /root/.openclaw/skills/skills/image-instagram/generate_carousel.py "Your text content here" --output /path/to/output
```

## API

- `generate_carousel(text, style="modern")` - Generate carousel slides
- `generate_story(text)` - Generate story format
- `generate_caption(topic)` - Generate engaging caption

## Examples

```python
from image_instagram import generate_carousel

slides = generate_carousel(
    text="Anti-aging tips: 1. Sleep 8h 2. Hydrate 3. Vitamin D",
    style="minimal",
    num_slides=3
)
```

## Configuration

Set DEFAULT_STYLE in config.json: minimal, modern, bold, elegant
