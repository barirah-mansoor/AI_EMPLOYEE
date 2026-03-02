# Facebook & Instagram Post Skill

**Mode:** AUTO-EXECUTE (requires HITL)
**Trigger:** Manual

## Purpose

Handles Facebook Page and Instagram Business posting with image support.

## Usage

```bash
# Create Facebook post
python3 -c "
from Skills.facebook_instagram_post import create_facebook_post
result = create_facebook_post('Check out our new feature!', image_url='https://example.com/image.png')
print(result)
"

# Create Instagram post
python3 -c "
from Skills.facebook_instagram_post import create_instagram_post
result = create_instagram_post('https://example.com/image.png', 'Excited to launch! #startup')
print(result)
"
```

## How It Works

1. Validates image URL format
2. Generates post caption
3. Creates `Pending_Approval/SOCIAL_{platform}_{timestamp}.md`
4. Only publishes when file moves to `/Approved/`

## Supported Platforms

- **Facebook**: Page posts with images
- **Instagram**: Business posts with images

## Image Requirements

- Supported formats: JPG, PNG, WebP
- Max size: 8MB (Instagram), 12MB (Facebook)
- Aspect ratios: 1:1 (square), 4:5 (portrait), 1.91:1 (landscape)

## HITL Flow

```
Create Post → Pending_Approval/ → Human Review → Approved/ → Publish
```

## Required API Keys

- `FACEBOOK_ACCESS_TOKEN`
- `INSTAGRAM_ACCESS_TOKEN`
- Facebook Page ID (in .env as `FACEBOOK_PAGE_ID`)
