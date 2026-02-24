# Meeting Maestro Skill

**Mode:** AUTO-EXECUTE
**Trigger:** Manual or scheduled (2 hours before meeting)
**Agent:** meeting_agent.py

## Purpose
Automated meeting preparation with context gathering, attendee research, briefing generation, and follow-up drafting.

## Execution

```bash
python3 Gold_Tier/AI_Agents/meeting_agent.py
```

## Capabilities

1. **Context Gathering**
   - Search recent emails for relevant content
   - Find previous meeting notes with same attendees
   - Identify pending action items
   - Link related documents

2. **Attendee Research**
   - Professional background inference
   - Talking points identification
   - Conversation starters
   - Potential synergies

3. **Briefing Generation**
   - Executive summary
   - Objectives and agenda suggestions
   - Key talking points
   - Questions to prepare
   - Preparation checklist

4. **Follow-up Drafting**
   - Meeting summary email
   - Action item extraction
   - Thank you notes
   - Next steps

## Output Files

- `Briefings/MEETING_BRIEFING_*.md` - Generated briefings
- `Gold_Tier/Logs/agent_logs/meeting_agent.log` - Execution logs
- `Gold_Tier/Logs/audit_logs/YYYY-MM-DD.json` - Audit trail

## Configuration

Settings in `Gold_Tier/Configs/agents_config.yaml`:
- `prep_hours_before`: Hours before meeting to prepare
- `followup_hours_after`: Hours after meeting for follow-up

## Workflow Integration

1. Triggered by:
   - Calendar event (future: Google Calendar integration)
   - Manual execution
   - Orchestrator schedule

2. Data sources:
   - `/Needs_Action/` - Email context
   - `/Done/` - Meeting history
   - `/Plans/` - Action items

## Example Briefing Structure

```markdown
# Meeting Briefing

**Generated:** 2024-01-15 14:30:00
**Meeting ID:** meeting_001

## Executive Summary
Brief overview...

## Objectives
- Objective 1
- Objective 2

## Key Talking Points
- Point 1
- Point 2

## Questions to Prepare
- Question 1
- Question 2
```
