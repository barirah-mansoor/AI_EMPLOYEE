# CEO Briefing Skill

**Mode:** AUTO-EXECUTE
**Trigger:** Weekly (Sunday 11:00 PM) or manual

## Purpose

Generates comprehensive weekly business briefing combining:
- Revenue from Odoo accounting
- Completed tasks from Done folder
- Subscription audit
- Bottleneck analysis
- Proactive suggestions

## Usage

```bash
# Generate weekly briefing
python3 weekly_ceo_briefing.py

# Via runner
bash run_ai_employee.sh weekly_briefing
```

## Output

Creates `Briefings/{YYYY-MM-DD}_Monday_CEO_Briefing.md`

## Format

```markdown
# Weekly CEO Briefing

## Executive Summary
- Week overview

## Revenue Summary
- This Week, MTD, Expenses, Net

## Completed Tasks
- Checkbox list from Done/

## Bottlenecks
- Table: Task | Expected | Actual | Delay

## Proactive Suggestions
- Subscription audit
- Cost optimization
- Upcoming deadlines
```

## Scheduling

Add to orchestrator for automatic weekly generation:
```yaml
weekly_ceo_briefing:
  enabled: true
  trigger: {type: "schedule", day: "sunday", time: "23:00"}
```
