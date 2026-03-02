# Email Intelligence Skill

**Mode:** AUTO-EXECUTE
**Trigger:** Manual or scheduled
**Agent:** email_agent.py

## Purpose
Autonomous email processing with sentiment analysis, intent detection, action item extraction, and intelligent auto-response drafting.

## Execution

```bash
python3 Gold_Tier/AI_Agents/email_agent.py
```

## Capabilities

1. **Email Analysis**
   - Sentiment detection (positive/neutral/negative)
   - Urgency classification (urgent/high/normal/low)
   - Intent recognition (request/question/information/complaint/followup)
   - Confidence scoring

2. **Action Item Extraction**
   - Pull tasks from email content
   - Identify deadlines
   - Assign priority levels

3. **Response Drafting**
   - Generate 3 response options (formal/professional/casual)
   - Context-aware responses
   - Tone-appropriate language

4. **Auto-Response Decision**
   - Confidence threshold check (default: 85%)
   - Daily limit enforcement (default: 20)
   - Intent complexity analysis

## Output Files

- `Gold_Tier/Logs/agent_logs/email_agent.log` - Execution logs
- `Gold_Tier/Logs/agent_logs/*_analysis.json` - Individual email analyses

## Configuration

Settings in `Gold_Tier/Configs/agents_config.yaml`:
- `auto_respond`: Enable/disable auto-responses
- `confidence_threshold`: Minimum confidence for auto-response
- `max_daily_auto_responses`: Daily limit

## Integration

Processes emails from:
- `/Needs_Action/EMAIL_*.md` files

Results logged to:
- `/Gold_Tier/Logs/audit_logs/YYYY-MM-DD.json`
