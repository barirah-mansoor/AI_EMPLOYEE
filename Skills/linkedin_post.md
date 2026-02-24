# LinkedIn Post Skill

**Mode:** AUTO-EXECUTE (requires HITL)
**Trigger:** Manual or weekly

## Purpose

Generates LinkedIn posts from business context and routes through HITL approval.

## Usage

```bash
# Generate LinkedIn post draft
python3 -c "
import sys
sys.path.insert(0, '.')
from Skills.linkedin_post import generate_linkedin_post
result = generate_linkedin_post()
print(result)
"
```

## How It Works

1. Reads `Business_Goals.md` for context
2. Reads recent `Done/` tasks for content
3. Generates 3 post options
4. Creates `Pending_Approval/SOCIAL_linkedin_{timestamp}.md`
5. Only publishes when file moves to `/Approved/`

## HITL Flow

```
Generate Post → Pending_Approval/ → Human Review → Approved/ → Publish
```

## Post Themes

- Week achievements
- Industry insights
- Project highlights
- Thought leadership

## Output Format

```markdown
---
type: social_media_post
platform: linkedin
status: pending_approval
---

# LinkedIn Post Draft

[Generated content here]

## Approval Required

- [ ] Review content
- [ ] Approve or reject
- [ ] Move to /Approved/ to publish
```
