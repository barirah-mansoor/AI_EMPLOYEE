#!/usr/bin/env python3
"""
Email Agent - Intelligent email processing and auto-response
"""

import os
import json
import re
import yaml
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional

# Import base agent
import sys
sys.path.insert(0, str(Path(__file__).parent))
from base_agent import BaseAgent


class EmailAgent(BaseAgent):
    """AI-powered email intelligence agent."""

    def __init__(self):
        super().__init__("email_agent")
        self.agent_config = self._load_agent_config()
        self.daily_responses = 0

    def _load_agent_config(self) -> Dict[str, Any]:
        """Load agent-specific configuration."""
        config_path = self.vault_path / "Gold_Tier" / "Configs" / "agents_config.yaml"
        if config_path.exists():
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
                return config.get("agents", {}).get("email_agent", {})
        return {"enabled": True, "auto_respond": True, "confidence_threshold": 0.85}

    def analyze_email(self, email_content: str, metadata: Dict[str, Any] = None) -> Dict[str, Any]:
        """Analyze email for sentiment, urgency, and intent."""
        prompt = f"""Analyze this email and provide a structured response.

Email Content:
{email_content}

Return JSON with:
{{
    "sentiment": "positive|neutral|negative",
    "urgency": "urgent|high|normal|low",
    "intent": "request|question|information|complaint|followup|other",
    "intent_details": "brief description of what sender wants",
    "key_topics": ["topic1", "topic2"],
    "action_required": true/false,
    "suggested_priority": "urgent|high|normal|low",
    "confidence": 0.0-1.0
}}"""

        response = self.call_claude(prompt, system="You are an email analysis expert. Return only valid JSON.")

        try:
            # Extract JSON from response
            json_match = re.search(r'\{[\s\S]*\}', response)
            if json_match:
                result = json.loads(json_match.group())
            else:
                result = json.loads(response)
        except json.JSONDecodeError:
            result = {
                "sentiment": "neutral",
                "urgency": "normal",
                "intent": "other",
                "confidence": 0.5,
                "error": "Failed to parse response"
            }

        result["analyzed_at"] = datetime.now().isoformat()
        result["metadata"] = metadata or {}
        return result

    def extract_action_items(self, email_content: str) -> List[Dict[str, str]]:
        """Extract action items from email content."""
        prompt = f"""Extract all action items, requests, and deadlines from this email.

Email:
{email_content}

Return JSON array:
[
    {{
        "action": "description of what needs to be done",
        "deadline": "deadline if mentioned, or null",
        "priority": "urgent|high|normal|low",
        "assigned_to": "who should do it, or 'me' if unclear"
    }}
]

If no action items found, return empty array: []"""

        response = self.call_claude(prompt, system="You are a task extraction expert. Return only valid JSON.")

        try:
            json_match = re.search(r'\[[\s\S]*\]', response)
            if json_match:
                return json.loads(json_match.group())
            return json.loads(response)
        except json.JSONDecodeError:
            return []

    def draft_responses(self, email_content: str, analysis: Dict[str, Any],
                        context: str = "") -> List[Dict[str, str]]:
        """Generate 3 response options for the email."""
        prompt = f"""Draft 3 professional email response options.

Original Email:
{email_content}

Analysis:
- Sentiment: {analysis.get('sentiment')}
- Intent: {analysis.get('intent')}
- Urgency: {analysis.get('urgency')}

Additional Context: {context or 'None'}

Return JSON array with 3 options:
[
    {{
        "tone": "formal|professional|casual",
        "subject": "Re: original subject",
        "body": "full email body text",
        "rationale": "why this response is appropriate"
    }}
]"""

        response = self.call_claude(prompt, system="You are a professional email writer. Return only valid JSON.")

        try:
            json_match = re.search(r'\[[\s\S]*\]', response)
            if json_match:
                return json.loads(json_match.group())
            return json.loads(response)
        except json.JSONDecodeError:
            return [{
                "tone": "professional",
                "subject": "Re: Your email",
                "body": "Thank you for your email. I will review and respond shortly.",
                "rationale": "Default response when generation fails"
            }]

    def should_auto_respond(self, analysis: Dict[str, Any],
                            responses: List[Dict[str, str]]) -> Dict[str, Any]:
        """Determine if email should receive an automatic response."""
        threshold = self.agent_config.get("confidence_threshold", 0.85)
        max_responses = self.agent_config.get("max_daily_auto_responses", 20)

        # Check daily limit
        if self.daily_responses >= max_responses:
            return {
                "auto_respond": False,
                "reason": "Daily auto-response limit reached"
            }

        # Check confidence
        confidence = analysis.get("confidence", 0)
        if confidence < threshold:
            return {
                "auto_respond": False,
                "reason": f"Confidence {confidence} below threshold {threshold}"
            }

        # Check intent - don't auto-respond to complex requests
        intent = analysis.get("intent")
        if intent in ["complaint", "request"]:
            return {
                "auto_respond": False,
                "reason": "Complex intent requires human review"
            }

        # Safe to auto-respond
        return {
            "auto_respond": True,
            "reason": "Meets auto-response criteria",
            "recommended_response": responses[0] if responses else None
        }

    def process_inbox_emails(self, max_emails: int = None) -> List[Dict[str, Any]]:
        """Process emails in the Needs_Action folder.

        Args:
            max_emails: Maximum number of emails to process. None or 0 means all.
        """
        needs_action = self.vault_path / "Needs_Action"
        processed = []

        if not needs_action.exists():
            return processed

        # Get all email files
        email_files = list(needs_action.glob("EMAIL_*.md"))

        # Limit to max_emails if specified
        if max_emails and max_emails > 0:
            email_files = email_files[:max_emails]

        for email_file in email_files:
            try:
                content = email_file.read_text()

                # Analyze email
                analysis = self.analyze_email(content, {"file": str(email_file)})

                # Extract action items
                actions = self.extract_action_items(content)

                # Draft responses
                responses = self.draft_responses(content, analysis)

                # Check auto-response
                auto_check = self.should_auto_respond(analysis, responses)

                result = {
                    "file": str(email_file),
                    "analysis": analysis,
                    "action_items": actions,
                    "responses": responses,
                    "auto_respond": auto_check,
                    "processed_at": datetime.now().isoformat()
                }

                processed.append(result)

                # Save result
                self.save_output(result, f"{email_file.stem}_analysis.json")

                # Log action
                self.log_action("process_email", {
                    "file": str(email_file),
                    "intent": analysis.get("intent"),
                    "urgency": analysis.get("urgency"),
                    "auto_respond": auto_check.get("auto_respond")
                })

            except Exception as e:
                self.logger.error(f"Error processing {email_file}: {e}")

        return processed

    def execute(self, action: str = "process_inbox", **kwargs) -> Dict[str, Any]:
        """Main execution method."""
        if action == "process_inbox":
            max_emails = kwargs.get("max_emails")
            return {
                "status": "success",
                "max_emails": max_emails if max_emails else "all",
                "processed_count": 0,  # Will be updated
                "processed_emails": self.process_inbox_emails(max_emails),
                "timestamp": datetime.now().isoformat()
            }
        elif action == "analyze":
            return self.analyze_email(kwargs.get("content", ""), kwargs.get("metadata"))
        elif action == "draft":
            return {
                "responses": self.draft_responses(
                    kwargs.get("content", ""),
                    kwargs.get("analysis", {}),
                    kwargs.get("context", "")
                )
            }
        else:
            return {"status": "error", "message": f"Unknown action: {action}"}


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Email Intelligence Agent")
    parser.add_argument("count", nargs="?", default="all",
                        help="Number of emails to process (number or 'all')")
    args = parser.parse_args()

    agent = EmailAgent()

    # Parse count argument
    if args.count.lower() == "all":
        max_emails = None
    else:
        try:
            max_emails = int(args.count)
        except ValueError:
            print(f"Invalid count '{args.count}'. Use a number or 'all'.")
            exit(1)

    result = agent.execute("process_inbox", max_emails=max_emails)
    result["processed_count"] = len(result.get("processed_emails", []))
    print(json.dumps(result, indent=2, default=str))
