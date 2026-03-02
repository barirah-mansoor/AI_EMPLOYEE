#!/usr/bin/env python3
"""
Social Media MCP Server - Provides social media posting operations
Tools: post_twitter, post_linkedin, post_facebook, post_instagram, get_social_summary, schedule_post
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

# Configuration
DEV_MODE = os.environ.get("DEV_MODE", "false").lower() == "true"
VAULT_PATH = Path(os.environ.get("VAULT_PATH", "/mnt/c/Users/Admin/AI_Employee_Vault"))
LOG_FILE = VAULT_PATH / "Logs" / "social_mcp_dev.log"

# HITL Approval directory
PENDING_APPROVAL = VAULT_PATH / "Pending_Approval"
APPROVED = VAULT_PATH / "Approved"


def log(message: str):
    """Log to file."""
    timestamp = datetime.now().isoformat()
    log_line = f"[{timestamp}] {message}\n"
    try:
        LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(LOG_FILE, "a") as f:
            f.write(log_line)
    except Exception:
        pass
    print(log_line, file=sys.stderr)


def check_hitl_approval(platform: str, timestamp: str) -> bool:
    """Check if a social media post has HITL approval."""
    pending_file = PENDING_APPROVAL / f"SOCIAL_{platform}_{timestamp}.md"
    approved_file = APPROVED / f"SOCIAL_{platform}_{timestamp}.md"

    # First check Approved folder
    if approved_file.exists():
        return True

    # Then check if moved from Pending to Approved
    return False


def create_hitl_file(platform: str, text: str, image_url: str = None) -> str:
    """Create a Pending_Approval file for HITL."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    content = f"""---
type: social_media_post
platform: "{platform}"
text: "{text}"
image_url: "{image_url or 'none'}"
status: pending_approval
created: "{datetime.now().isoformat()}"
---

# Social Media Post - {platform}

## Post Content

{text}

## Image URL

{image_url or 'No image'}

## Approval Required

This post requires human approval before publishing.

- [ ] Review post content
- [ ] Approve or reject
- [ ] If approved, move to /Approved/ folder to publish
"""

    PENDING_APPROVAL.mkdir(parents=True, exist_ok=True)
    file_path = PENDING_APPROVAL / f"SOCIAL_{platform}_{timestamp}.md"
    file_path.write_text(content)

    return str(file_path)


def post_twitter(text: str, image_url: str = None) -> dict:
    """Post to Twitter/X."""
    if DEV_MODE:
        log(f"TWITTER (DEV): {text[:50]}...")
        # Check for HITL approval
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        if not check_hitl_approval("twitter", timestamp):
            file_path = create_hitl_file("twitter", text, image_url)
            return {
                "success": True,
                "dev_mode": True,
                "status": "pending_approval",
                "message": f"HITL required. Created {file_path}",
                "approval_file": str(file_path)
            }

        return {
            "success": True,
            "dev_mode": True,
            "post_id": f"dev_tweet_{timestamp}",
            "text": text,
            "image_url": image_url,
            "message": "DEV_MODE: Tweet posted (mock)"
        }

    # Real Twitter API would go here
    return {"error": "Twitter API not configured. Set TWITTER_API_KEY and related env vars."}


def post_linkedin(text: str, image_url: str = None) -> dict:
    """Post to LinkedIn."""
    if DEV_MODE:
        log(f"LINKEDIN (DEV): {text[:50]}...")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        if not check_hitl_approval("linkedin", timestamp):
            file_path = create_hitl_file("linkedin", text, image_url)
            return {
                "success": True,
                "dev_mode": True,
                "status": "pending_approval",
                "message": f"HITL required. Created {file_path}",
                "approval_file": str(file_path)
            }

        return {
            "success": True,
            "dev_mode": True,
            "post_id": f"dev_linkedin_{timestamp}",
            "text": text,
            "image_url": image_url,
            "message": "DEV_MODE: LinkedIn post published (mock)"
        }

    return {"error": "LinkedIn API not configured"}


def post_facebook(text: str, image_url: str = None, page_id: str = None) -> dict:
    """Post to Facebook."""
    if DEV_MODE:
        log(f"FACEBOOK (DEV): {text[:50]}...")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        if not check_hitl_approval("facebook", timestamp):
            file_path = create_hitl_file("facebook", text, image_url)
            return {
                "success": True,
                "dev_mode": True,
                "status": "pending_approval",
                "message": f"HITL required. Created {file_path}",
                "approval_file": str(file_path)
            }

        return {
            "success": True,
            "dev_mode": True,
            "post_id": f"dev_fb_{timestamp}",
            "text": text,
            "page_id": page_id,
            "message": "DEV_MODE: Facebook post published (mock)"
        }

    return {"error": "Facebook API not configured"}


def post_instagram(image_url: str, caption: str) -> dict:
    """Post to Instagram."""
    if DEV_MODE:
        log(f"INSTAGRAM (DEV): {caption[:50]}...")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        if not check_hitl_approval("instagram", timestamp):
            file_path = create_hitl_file("instagram", caption, image_url)
            return {
                "success": True,
                "dev_mode": True,
                "status": "pending_approval",
                "message": f"HITL required. Created {file_path}",
                "approval_file": str(file_path)
            }

        return {
            "success": True,
            "dev_mode": True,
            "post_id": f"dev_ig_{timestamp}",
            "image_url": image_url,
            "caption": caption,
            "message": "DEV_MODE: Instagram post published (mock)"
        }

    return {"error": "Instagram API not configured"}


def get_social_summary(platform: str = None, days: int = 7) -> dict:
    """Get social media engagement summary."""
    if DEV_MODE:
        # Read from log file
        summary = {
            "period_days": days,
            "posts_published": 0,
            "posts_scheduled": 0,
            "posts_pending": 0,
            "total_impressions": 0,
            "total_engagement": 0,
            "top_post": None
        }

        if LOG_FILE.exists():
            content = LOG_FILE.read_text()
            posts = [line for line in content.split("\n") if "DEV:" in line]

            summary["posts_published"] = len([p for p in posts if "posted" in p])
            summary["posts_pending"] = len([p for p in posts if "pending_approval" in p])

        return {
            "success": True,
            "dev_mode": True,
            "summary": summary,
            "message": "DEV_MODE: Summary from log file"
        }

    return {"error": "Cannot get real stats without API credentials"}


def schedule_post(platform: str, text: str, scheduled_time: str) -> dict:
    """Schedule a post for later."""
    if DEV_MODE:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = create_hitl_file(f"{platform}_scheduled", text)
        return {
            "success": True,
            "dev_mode": True,
            "status": "scheduled",
            "scheduled_time": scheduled_time,
            "message": f"DEV_MODE: Post scheduled for {scheduled_time}",
            "approval_file": str(file_path)
        }

    return {"error": "Scheduling requires HITL approval first"}


# MCP Server Protocol
def handle_tool(name: str, args: dict) -> dict:
    """Route tool calls to appropriate functions."""
    tools = {
        "post_twitter": lambda: post_twitter(
            args.get("text", ""),
            args.get("image_url")
        ),
        "post_linkedin": lambda: post_linkedin(
            args.get("text", ""),
            args.get("image_url")
        ),
        "post_facebook": lambda: post_facebook(
            args.get("text", ""),
            args.get("image_url"),
            args.get("page_id")
        ),
        "post_instagram": lambda: post_instagram(
            args.get("image_url", ""),
            args.get("caption", "")
        ),
        "get_social_summary": lambda: get_social_summary(
            args.get("platform"),
            args.get("days", 7)
        ),
        "schedule_post": lambda: schedule_post(
            args.get("platform", ""),
            args.get("text", ""),
            args.get("scheduled_time", "")
        ),
    }

    if name not in tools:
        return {"error": f"Unknown tool: {name}"}

    return tools[name]()


def send_json_response(data):
    print(json.dumps(data))
    sys.stdout.flush()


def send_error(error):
    print(json.dumps({"error": str(error)}))
    sys.stdout.flush()


# Main loop
if __name__ == "__main__":
    log(f"Social MCP Server starting... DEV_MODE={DEV_MODE}")

    while True:
        try:
            line = sys.stdin.readline()
            if not line:
                break

            request = json.loads(line.strip())

            if request.get("method") == "tools/list":
                send_json_response({
                    "tools": [
                        {
                            "name": "post_twitter",
                            "description": "Post to Twitter/X",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "text": {"type": "string", "description": "Tweet text"},
                                    "image_url": {"type": "string", "description": "Optional image URL"}
                                },
                                "required": ["text"]
                            }
                        },
                        {
                            "name": "post_linkedin",
                            "description": "Post to LinkedIn",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "text": {"type": "string", "description": "Post text"},
                                    "image_url": {"type": "string", "description": "Optional image URL"}
                                },
                                "required": ["text"]
                            }
                        },
                        {
                            "name": "post_facebook",
                            "description": "Post to Facebook Page",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "text": {"type": "string", "description": "Post text"},
                                    "image_url": {"type": "string", "description": "Optional image URL"},
                                    "page_id": {"type": "string", "description": "Facebook Page ID"}
                                },
                                "required": ["text"]
                            }
                        },
                        {
                            "name": "post_instagram",
                            "description": "Post to Instagram",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "image_url": {"type": "string", "description": "Image URL"},
                                    "caption": {"type": "string", "description": "Post caption"}
                                },
                                "required": ["image_url", "caption"]
                            }
                        },
                        {
                            "name": "get_social_summary",
                            "description": "Get social media engagement summary",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "platform": {"type": "string", "description": "Platform (twitter, linkedin, facebook, instagram)"},
                                    "days": {"type": "number", "description": "Days to analyze", "default": 7}
                                }
                            }
                        },
                        {
                            "name": "schedule_post",
                            "description": "Schedule a post for later",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "platform": {"type": "string", "description": "Platform"},
                                    "text": {"type": "string", "description": "Post text"},
                                    "scheduled_time": {"type": "string", "description": "ISO timestamp"}
                                },
                                "required": ["platform", "text", "scheduled_time"]
                            }
                        }
                    ]
                })

            elif request.get("method") == "tools/call":
                tool_name = request.get("params", {}).get("name")
                tool_args = request.get("params", {}).get("arguments", {})
                result = handle_tool(tool_name, tool_args)
                send_json_response({"content": [{"type": "text", "text": json.dumps(result)}]})

        except Exception as e:
            send_error(str(e))
