# Twitter Post Skill

**Mode:** AUTO-EXECUTE (requires HITL)
**Trigger:** Manual or research-driven

## Purpose

Generates tweet threads from business context and research.

## Usage

```bash
# Generate Twitter thread
python3 -c "
import sys
sys.path.insert(0, '.')
from Skills.twitter_post import generate_twitter_thread
result = generate_twitter_thread('AI automation')
print(result)
"
```

## How It Works

1. Reads `Business_Goals.md` for context
2. Reads current research in `Knowledge_Base/`
3. Generates thread (up to 10 tweets)
4. Creates `Pending_Approval/SOCIAL_twitter_{timestamp}.md`
5. Only publishes when file moves to `/Approved/`

## Thread Format

- Hook (tweet 1): Attention-grabbing opener
- Context (tweets 2-8): Main content
- CTA (final tweet): Call to action

## HITL Flow

```
Generate Thread → Pending_Approval/ → Human Review → Approved/ → Publish
```

## Character Limits

- Each tweet: 280 characters max
- Thread: Up to 10 tweets
- Includes tweet numbering (1/10, 2/10, etc.)
