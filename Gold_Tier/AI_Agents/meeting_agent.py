#!/usr/bin/env python3
"""
Meeting Agent - Automated meeting preparation and follow-up
"""

import os
import json
import re
import yaml
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any, List, Optional

# Import base agent
import sys
sys.path.insert(0, str(Path(__file__).parent))
from base_agent import BaseAgent


class MeetingAgent(BaseAgent):
    """AI-powered meeting automation agent."""

    def __init__(self):
        super().__init__("meeting_agent")
        self.agent_config = self._load_agent_config()

    def _load_agent_config(self) -> Dict[str, Any]:
        """Load agent-specific configuration."""
        config_path = self.vault_path / "Gold_Tier" / "Configs" / "agents_config.yaml"
        if config_path.exists():
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
                return config.get("agents", {}).get("meeting_agent", {})
        return {"enabled": True, "prep_hours_before": 2, "followup_hours_after": 1}

    def prepare_meeting(self, meeting_info: Dict[str, Any]) -> Dict[str, Any]:
        """Prepare comprehensive meeting briefing."""
        # Gather all context
        context = self.gather_meeting_context(meeting_info)

        # Research attendees
        attendee_info = self.research_attendees(meeting_info.get("attendees", []))

        # Generate briefing
        briefing = self.generate_briefing(meeting_info, context, attendee_info)

        return {
            "meeting_id": meeting_info.get("id"),
            "prepared_at": datetime.now().isoformat(),
            "context": context,
            "attendee_research": attendee_info,
            "briefing": briefing
        }

    def gather_meeting_context(self, meeting_info: Dict[str, Any]) -> Dict[str, Any]:
        """Gather relevant context from emails, documents, and history."""
        context = {
            "recent_emails": [],
            "relevant_docs": [],
            "meeting_history": [],
            "action_items": []
        }

        # Search for relevant emails
        needs_action = self.vault_path / "Needs_Action"
        if needs_action.exists():
            for email_file in list(needs_action.glob("EMAIL_*.md"))[:10]:
                content = email_file.read_text()
                # Check if email relates to meeting topic or attendees
                topic = meeting_info.get("topic", "").lower()
                attendees = meeting_info.get("attendees", [])

                if topic and topic in content.lower():
                    context["recent_emails"].append({
                        "file": str(email_file.name),
                        "preview": content[:200]
                    })

        # Check for previous meeting notes
        done_dir = self.vault_path / "Done"
        if done_dir.exists():
            for note_file in done_dir.glob("MEETING_*.md"):
                content = note_file.read_text()
                # Look for same attendees or topic
                if any(att.lower() in content.lower() for att in attendees if att):
                    context["meeting_history"].append({
                        "file": str(note_file.name),
                        "preview": content[:300]
                    })

        # Check for pending action items
        plans_dir = self.vault_path / "Plans"
        if plans_dir.exists():
            for plan_file in plans_dir.glob("*.md"):
                content = plan_file.read_text()
                if "action" in content.lower() or "todo" in content.lower():
                    context["action_items"].append({
                        "file": str(plan_file.name),
                        "preview": content[:200]
                    })

        return context

    def research_attendees(self, attendees: List[str]) -> Dict[str, Any]:
        """Research meeting attendees."""
        if not attendees:
            return {"attendees": [], "summary": "No attendees to research"}

        prompt = f"""Research these meeting attendees and provide useful context.

Attendees:
{json.dumps(attendees, indent=2)}

Return JSON:
{{
    "attendee_profiles": [
        {{
            "name": "attendee name",
            "likely_role": "inferred role/profession",
            "talking_points": ["topic1", "topic2"],
            "questions_to_ask": ["question1"],
            "professional_interests": ["interest1"]
        }}
    ],
    "relationship_insights": "How these people might be connected",
    "conversation_starters": ["starter1", "starter2"],
    "potential_synergies": "What collaboration opportunities exist"
}}"""

        response = self.call_claude(prompt, system="You are a networking expert. Return only valid JSON.")

        try:
            json_match = re.search(r'\{[\s\S]*\}', response)
            if json_match:
                return json.loads(json_match.group())
            return json.loads(response)
        except json.JSONDecodeError:
            return {
                "attendee_profiles": [{"name": att, "note": "Unable to research"} for att in attendees],
                "error": "Failed to parse research"
            }

    def generate_briefing(self, meeting_info: Dict[str, Any],
                          context: Dict[str, Any],
                          attendee_info: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive meeting briefing."""
        prompt = f"""Generate a comprehensive meeting briefing.

Meeting Info:
{json.dumps(meeting_info, indent=2, default=str)}

Context:
{json.dumps(context, indent=2, default=str)}

Attendee Research:
{json.dumps(attendee_info, indent=2, default=str)}

Return JSON:
{{
    "executive_summary": "Brief overview of what this meeting is about",
    "objectives": ["objective1", "objective2"],
    "agenda_suggestions": ["item1", "item2", "item3"],
    "key_talking_points": ["point1", "point2", "point3"],
    "questions_to_prepare": ["question1", "question2"],
    "recent_interactions": "Summary of recent emails/meetings with attendees",
    "preparation_checklist": ["item1", "item2"],
    "desired_outcomes": ["outcome1", "outcome2"],
    "follow_up_items": "Items to address after meeting"
}}"""

        response = self.call_claude(prompt, system="You are an executive assistant. Return only valid JSON.")

        try:
            json_match = re.search(r'\{[\s\S]*\}', response)
            if json_match:
                result = json.loads(json_match.group())
            else:
                result = json.loads(response)
        except json.JSONDecodeError:
            result = {
                "executive_summary": "Unable to generate briefing",
                "error": "JSON parsing failed"
            }

        result["generated_at"] = datetime.now().isoformat()
        return result

    def send_followup(self, meeting_info: Dict[str, Any],
                      meeting_notes: str = None) -> Dict[str, Any]:
        """Generate follow-up communication after meeting."""
        prompt = f"""Generate meeting follow-up content.

Meeting Info:
{json.dumps(meeting_info, indent=2, default=str)}

Meeting Notes:
{meeting_notes or "No notes provided"}

Return JSON:
{{
    "summary_email": {{
        "subject": "Meeting Summary - [Topic]",
        "body": "Professional email summarizing the meeting"
    }},
    "action_items": [
        {{
            "item": "description",
            "owner": "who should do it",
            "deadline": "when"
        }}
    ],
    "next_steps": "What should happen next",
    "thank_you_notes": ["Personalized thank you for attendee 1", "etc"]
}}"""

        response = self.call_claude(prompt, system="You are an executive assistant. Return only valid JSON.")

        try:
            json_match = re.search(r'\{[\s\S]*\}', response)
            if json_match:
                result = json.loads(json_match.group())
            else:
                result = json.loads(response)
        except json.JSONDecodeError:
            result = {
                "summary_email": {"subject": "Meeting Follow-up", "body": "Thank you for the meeting."},
                "error": "Failed to generate follow-up"
            }

        result["generated_at"] = datetime.now().isoformat()
        return result

    def save_briefing(self, briefing: Dict[str, Any], meeting_id: str) -> Path:
        """Save briefing to Briefings folder."""
        briefings_dir = self.vault_path / "Briefings"
        briefings_dir.mkdir(parents=True, exist_ok=True)

        # Generate markdown content
        md_content = f"""# Meeting Briefing

**Generated:** {briefing.get("generated_at", datetime.now().isoformat())}
**Meeting ID:** {meeting_id}

## Executive Summary
{briefing.get("executive_summary", "No summary available")}

## Objectives
"""
        for obj in briefing.get("objectives", []):
            md_content += f"- {obj}\n"

        md_content += "\n## Agenda Suggestions\n"
        for item in briefing.get("agenda_suggestions", []):
            md_content += f"- {item}\n"

        md_content += "\n## Key Talking Points\n"
        for point in briefing.get("key_talking_points", []):
            md_content += f"- {point}\n"

        md_content += "\n## Questions to Prepare\n"
        for q in briefing.get("questions_to_prepare", []):
            md_content += f"- {q}\n"

        md_content += "\n## Preparation Checklist\n"
        for item in briefing.get("preparation_checklist", []):
            md_content += f"- [ ] {item}\n"

        file_path = briefings_dir / f"MEETING_BRIEFING_{meeting_id}_{datetime.now().strftime('%Y%m%d')}.md"
        file_path.write_text(md_content)

        self.logger.info(f"Briefing saved to {file_path}")
        return file_path

    def execute(self, action: str = "prepare", meeting_info: Dict[str, Any] = None,
                **kwargs) -> Dict[str, Any]:
        """Main execution method."""
        if action == "prepare":
            if not meeting_info:
                meeting_info = kwargs.get("meeting_info", {
                    "id": f"auto_{datetime.now().strftime('%Y%m%d%H%M')}",
                    "topic": kwargs.get("topic", "General Meeting"),
                    "attendees": kwargs.get("attendees", []),
                    "time": kwargs.get("time", datetime.now().isoformat())
                })

            preparation = self.prepare_meeting(meeting_info)

            # Save briefing
            briefing_path = self.save_briefing(
                preparation.get("briefing", {}),
                meeting_info.get("id", "unknown")
            )

            # Log action
            self.log_action("meeting_prep", {
                "meeting_id": meeting_info.get("id"),
                "attendees": meeting_info.get("attendees", []),
                "briefing_saved": str(briefing_path)
            })

            return {
                "status": "success",
                "preparation": preparation,
                "briefing_file": str(briefing_path),
                "timestamp": datetime.now().isoformat()
            }

        elif action == "followup":
            followup = self.send_followup(
                kwargs.get("meeting_info", {}),
                kwargs.get("notes")
            )
            return {
                "status": "success",
                "followup": followup,
                "timestamp": datetime.now().isoformat()
            }

        else:
            return {"status": "error", "message": f"Unknown action: {action}"}


if __name__ == "__main__":
    import yaml  # Ensure yaml is imported

    agent = MeetingAgent()

    # Default test meeting
    meeting = {
        "id": "test_001",
        "topic": "Q1 Strategy Review",
        "attendees": ["John Smith", "Jane Doe"],
        "time": (datetime.now() + timedelta(hours=2)).isoformat()
    }

    result = agent.execute("prepare", meeting_info=meeting)
    print(json.dumps(result, indent=2, default=str))
