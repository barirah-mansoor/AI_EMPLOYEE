# Social Summary Skill

**Mode:** AUTO-EXECUTE
**Trigger:** Weekly or manual

## Purpose

Aggregates social media activity and generates performance reports.

## Usage

```bash
# Generate social summary
python3 social_summary.py

# Via runner
bash run_ai_employee.sh social_summary
```

## How It Works

1. Reads `Logs/social_mcp_dev.log` for post history
2. Aggregates by platform (Twitter, LinkedIn, Facebook, Instagram)
3. Generates markdown report with:
   - Posts published
   - Posts scheduled
   - Posts pending approval
   - Engagement metrics (if available)

## Output

Creates `Briefings/social_summary_{date}.md`

## Report Format

```markdown
# Social Media Summary

**Period:** Last 7 days
**Generated:** YYYY-MM-DD

## Twitter
- Published: 3
- Scheduled: 1
- Pending: 0

## LinkedIn
- Published: 2
- Scheduled: 0
- Pending: 1

## Engagement
- Total impressions: X
- Total engagement: Y
- Top post: [link]
```
