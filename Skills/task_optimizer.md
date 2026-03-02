# Task Optimizer Skill

**Mode:** AUTO-EXECUTE
**Trigger:** Manual, hourly schedule, or on-demand
**Agent:** task_optimizer.py

## Purpose
AI-powered task prioritization using Eisenhower Matrix, schedule optimization, bottleneck identification, and actionable recommendations.

## Execution

```bash
python3 Gold_Tier/AI_Agents/task_optimizer.py
```

## Capabilities

1. **Task Loading**
   - Load from `/Needs_Action/`
   - Load from `/Plans/`
   - Extract from `/Briefings/`
   - Unified task list

2. **Eisenhower Matrix**
   - **Urgent + Important**: Do First
   - **Important + Not Urgent**: Schedule
   - **Urgent + Not Important**: Delegate
   - **Not Urgent + Not Important**: Eliminate

3. **Schedule Optimization**
   - Deep work block protection
   - Energy-level matching
   - Flexibility buffers
   - Break scheduling

4. **Bottleneck Detection**
   - Dependency conflicts
   - Resource constraints
   - Time conflicts
   - Information gaps

5. **Recommendations**
   - Priority actions
   - Delegation opportunities
   - Time-saving tips
   - Weekly goals

## Output Files

- `Gold_Tier/Analytics/Reports/Daily/task_optimization_*.json` - Full reports
- `Gold_Tier/Logs/agent_logs/task_optimizer.log` - Execution logs

## Configuration

Settings in `Gold_Tier/Configs/agents_config.yaml`:
- `optimization_frequency`: "hourly", "daily", etc.
- `enabled`: Enable/disable agent

## Eisenhower Matrix Visualization

```
                    URGENT          NOT URGENT
              ┌─────────────────┬─────────────────┐
              │                 │                 │
   IMPORTANT  │   DO FIRST      │   SCHEDULE      │
              │   (Quadrant 1)   │   (Quadrant 2)  │
              │                 │                 │
              ├─────────────────┼─────────────────┤
              │                 │                 │
 NOT IMPORTANT│   DELEGATE      │   ELIMINATE     │
              │   (Quadrant 3)   │   (Quadrant 4)  │
              │                 │                 │
              └─────────────────┴─────────────────┘
```

## Example Output

```json
{
  "eisenhower_matrix": {
    "urgent_important": [
      {"task": "Client deadline", "suggested_action": "Do first"}
    ],
    "important_not_urgent": [
      {"task": "Strategy planning", "suggested_action": "Schedule"}
    ],
    "urgent_not_important": [
      {"task": "Non-critical meeting", "suggested_action": "Delegate"}
    ],
    "not_urgent_not_important": [
      {"task": "Old documentation", "suggested_action": "Eliminate"}
    ]
  },
  "recommendations": {
    "priority_actions": [...],
    "focus_recommendations": [...]
  }
}
```

## Integration

Works with:
- Email Agent (action item extraction)
- Meeting Agent (meeting prep tasks)
- Orchestrator (scheduled optimization)
