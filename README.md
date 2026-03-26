# AI Genesis Skills

A curated collection of 34 automation skills for AI-powered business workflows.

## Overview

This repository contains production-ready skills designed for OpenClaw framework integration. Each skill is a modular automation component that can be combined to create complex business workflows.

## Skills Inventory

### Content Creation
| Skill | Description | Tier |
|-------|-------------|------|
| `post-generator` | AI-powered social media post generator | Full |
| `carousel-pro` | Instagram carousel generator with 5 design modes | Full |
| `video-script` | A/B video script generator (Reels/TikTok/Shorts) | Pilot |
| `viral-hooks` | Viral content hook generator | Pilot |
| `content-strategist` | Strategic content planning assistant | Full |

### CRM & Sales
| Skill | Description | Tier |
|-------|-------------|------|
| `bot-system` | World-class sales qualification bot (v10.4) | Full |
| `client-onboarding` | Automated client onboarding workflow | Basic |
| `lead-scoring` | Lead qualification and scoring system | Pilot |
| `objection-handler` | Automated objection handling | Basic |
| `followup-system` | Multi-channel follow-up sequences | Pilot |
| `google-sheets-crm` | Lead management via Google Sheets | Pilot |

### Automation
| Skill | Description | Tier |
|-------|-------------|------|
| `proposal-generator` | Automated proposal generation | Full |
| `email-sequence` | Email automation sequences | Pilot |
| `email-responder` | Smart email response handler | Pilot |
| `cron-scheduler` | Scheduled task automation | Basic |
| `coding-agent` | AI coding assistant (Claude integration) | Pilot |

### Analytics & Intelligence
| Skill | Description | Tier |
|-------|-------------|------|
| `competitive-intel` | Competitor analysis automation | Full |
| `browser-competitor` | Web scraping for competitive research | Pilot |
| `data-analysis` | Data processing and visualization | Full |
| `data-analysis-crm` | CRM data analytics | Pilot |

### Integrations
| Skill | Description | Tier |
|-------|-------------|------|
| `notion` | Notion API integration | Full |
| `notion-sync` | Skills database synchronization | Full |
| `github` | GitHub CLI automation | Full |
| `gog` | Google Workspace integration | Full |

### Marketing
| Skill | Description | Tier |
|-------|-------------|------|
| `brand-architect` | Brand identity development | Full |
| `course-launch` | Online course launch automation | Full |
| `image-instagram` | Instagram image optimization | Pilot |
| `weekly-command` | Weekly planning and reporting | Pilot |

### Specialized
| Skill | Description | Tier |
|-------|-------------|------|
| `sofia-sales` | Sales assistant for Sofia | Pilot |
| `wellness-sales` | Wellness industry sales bot | Pilot |
| `alex-cmo` | CMO assistant persona | Pilot |
| `lab-protocols` | Laboratory protocol management | Pilot |
| `max-copy` | Copywriting assistant (Max persona) | Pilot |
| `file-writer` | Automated file generation | Basic |

## Usage

Each skill contains:
- `SKILL.md` - Documentation and usage instructions
- Implementation files (Python, Bash, etc.)
- Configuration examples

### Example

```bash
cd post-generator
python3 post_generator.py "AI automation for business"
```

## Requirements

- Python 3.8+
- OpenClaw framework (for integration)
- Environment variables for API keys (see individual skill docs)

## Security

- No hardcoded secrets in any skill files
- API keys are loaded from environment variables
- Review `.gitignore` for excluded sensitive files

## License

MIT License - See individual skill directories for specific licensing.

## Author

Created by [Adis](https://github.com/Brigjite) for AI Genesis.
