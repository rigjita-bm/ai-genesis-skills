# Post Generator — AI Content for Social Media

AI-powered content generation using OpenAI GPT-4 for Instagram, Telegram, Facebook, and LinkedIn.

## Setup

### 1. Install OpenAI
```bash
pip install openai --break-system-packages
```

### 2. Set API Key
```bash
export OPENAI_API_KEY='sk-your-key-here'
```

Add to `~/.bashrc` for persistence:
```bash
echo 'export OPENAI_API_KEY="sk-your-key-here"' >> ~/.bashrc
source ~/.bashrc
```

## Usage

### Basic Post Generation
```bash
# 3 variants for Instagram (default)
genesis post "Почему автоматизация важна для бизнеса"

# Telegram with casual tone
genesis post "Тема" -p telegram -t casual

# 5 variants, save to file
genesis post "Тема" -v 5 --save

# English post for LinkedIn
genesis post "Topic" -p linkedin -l en
```

### Content Calendar
```bash
# 7-day content calendar
genesis post -c 7

# 30-day calendar focused on specific theme
genesis post -c 30
```

### Image Caption
```bash
# Caption for Instagram carousel
genesis post "Описание: профессиональный ремонт гостиной в манхэттенском стиле, светлые тона, минимализм" --caption
```

## Platforms

- `instagram` — Visual, emotional, 10-15 hashtags
- `telegram` — Informative, 3-5 hashtags
- `facebook` — Conversational, discussion-focused
- `linkedin` — Professional, expert tone

## Tones

- `professional` — Business tone, expert language
- `casual` — Friendly, like talking to a friend
- `storytelling` — Narrative, emotional, through stories
- `educational` — Structured, with bullet points
- `inspirational` — Motivational, positive
- `urgent` — FOMO, time-limited

## Output

Posts include:
- Catchy title
- Full post text with emoji
- Relevant hashtags
- Best posting time
- Character count

Files saved to: `/root/.openclaw/output/posts/`

## Examples

### Before/After
```bash
# Old way — manual
genesis content plan automation
# Then write manually

# New way — AI generated
genesis post "5 ошибок при автоматизации малого бизнеса" -t educational -v 3
```

### Business Context
All posts automatically include AI Genesis context:
- Russian-speaking entrepreneurs in NYC
- Services: digital administrators, AI assistants
- Price points: $100/$350/$700/$1000
- Tone: expert but friendly

## Cost Estimation

GPT-4o pricing (approximate):
- 1 post (3 variants): ~$0.02-0.05
- 30-day calendar: ~$0.15-0.30

Very affordable for content generation!

## Integration with Other Skills

```bash
# Generate carousel + caption
genesis carousel "ремонт квартир"
genesis post "Профессиональный ремонт квартиры: до и после" --caption

# Content calendar + batch generation
genesis post -c 7 > calendar.txt
# Use topics from calendar with post generator
```
