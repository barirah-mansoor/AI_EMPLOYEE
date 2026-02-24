# Gold Analytics Skill

**Mode:** AUTO-EXECUTE
**Trigger:** Daily schedule (6 PM) or manual
**Agent:** Integrated analytics from all agents

## Purpose
Generate productivity metrics, trend analysis, and comprehensive performance reports.

## Execution

```bash
python3 -c "
from Gold_Tier.Automation.orchestrator import GoldOrchestrator
orch = GoldOrchestrator()
result = orch._collect_analytics()
print(result)
"
```

## Capabilities

1. **Metrics Collection**
   - Emails processed
   - Tasks analyzed
   - Briefings generated
   - Workflows executed
   - Auto-responses sent

2. **Trend Analysis**
   - Daily productivity scores
   - Response time trends
   - Task completion rates
   - Workflow efficiency

3. **Report Generation**
   - Daily summary
   - Weekly overview
   - Monthly trends
   - Custom date ranges

4. **Visualization Data**
   - Time distribution charts
   - Priority breakdown
   - Agent performance metrics

## Output Files

- `Gold_Tier/Analytics/Reports/Daily/daily_report_*.json` - Daily reports
- `Gold_Tier/Analytics/Reports/Weekly/weekly_report_*.json` - Weekly reports
- `Gold_Tier/Analytics/Reports/Monthly/monthly_report_*.json` - Monthly reports

## Report Structure

```json
{
  "timestamp": "2024-01-15T18:00:00",
  "metrics": {
    "emails_processed": 12,
    "tasks_analyzed": 8,
    "briefings_generated": 2,
    "workflows_executed": 5,
    "auto_responses_sent": 3
  },
  "productivity_score": 85,
  "trends": {
    "email_trend": "increasing",
    "task_completion_rate": 0.78,
    "avg_response_time_minutes": 45
  },
  "recommendations": [
    "Focus on Quadrant 2 tasks",
    "Reduce meeting time by 20%"
  ]
}
```

## Dashboard Integration

Updates `Dashboard.md` with:
- Current task counts
- Recent activity
- Priority distribution
- Agent status

## Configuration

Settings in `Gold_Tier/Configs/gold_config.yaml`:
- `analytics.enabled`: Enable/disable
- `analytics.generate_daily_report`: Daily report setting
- `analytics.report_path`: Output directory
