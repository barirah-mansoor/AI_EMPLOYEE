# GOLD TIER BUILD MISSION — Claude Code Execution Prompt

> Copy everything below the horizontal rule and paste it into your Claude Code terminal session.
> Run from: `~/AI_Employee_Vault`

---

## HOW TO USE

```bash
cd ~/AI_Employee_Vault
claude
```

Then paste the prompt below.

---

---
---

## THE PROMPT (paste into Claude Code)

You are my Personal AI Employee operating at **Gold Tier** level. Your mission is to build all missing components that upgrade this vault from its current Silver-adjacent state to a fully compliant Gold Tier system, as defined in the hackathon spec at:
`~/AI_Employee_Vault/Personal AI Employee Hackathon 0_ Building Autonomous FTEs in 2026.md`

The vault root is: `~/AI_Employee_Vault`

Read `CLAUDE.md` first to understand the system. Then read the hackathon spec file. Then execute the following build plan in order. After each major component is complete, log a completion entry to `Logs/YYYY-MM-DD.json` and update `Dashboard.md`.

**IMPORTANT RULES:**
- Never stop mid-task. Use the Ralph Wiggum pattern on yourself if needed.
- All new Python files must have `if __name__ == "__main__"` test blocks.
- All new Skills must be created as `.md` files in `~/AI_Employee_Vault/Skills/`
- All credentials go in `.env` — never hardcoded.
- Every action must be logged to the audit log before executing.
- Where real API credentials are missing, implement a full `DEV_MODE=true` dry-run fallback that simulates the action and logs it.

---

## PHASE 1: Ralph Wiggum Loop (Autonomous Task Completion)

**Goal:** Implement the Stop hook pattern so Claude Code keeps working until a task is truly complete.

1. Create the directory: `~/.claude/` (if it doesn't exist)

2. Create `~/.claude/settings.json` with this Stop hook configuration:
```json
{
  "hooks": {
    "Stop": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "python3 ~/AI_Employee_Vault/ralph_wiggum.py"
          }
        ]
      }
    ]
  }
}
```

3. Create `~/AI_Employee_Vault/ralph_wiggum.py`:
   - Read the current task state file from `~/AI_Employee_Vault/Plans/CURRENT_TASK.md`
   - If the file does NOT exist → allow exit (output: `{"decision": "block", "reason": "No active task"}` — actually allow)
   - If it exists AND contains `status: done` → delete it, allow exit
   - If it exists AND contains `status: in_progress` → block exit with a re-injection message telling Claude to keep working
   - Support `MAX_ITERATIONS=10` env var to prevent infinite loops (read iteration count from the task file frontmatter)
   - Log each iteration to `Logs/ralph_wiggum.json`
   - Output must go to stdout as JSON: `{"decision": "block", "reason": "..."}` or `{"decision": "allow"}`

4. Create `Skills/ralph_loop.md` Agent Skill explaining how to use the Ralph Wiggum pattern for multi-step tasks.

5. Create `Plans/CURRENT_TASK.md` template (with `status: idle`).

---

## PHASE 2: WhatsApp Watcher (Complete Silver Prerequisite)

**Goal:** Build a working WhatsApp Web watcher using Playwright.

1. Create `~/AI_Employee_Vault/whatsapp_watcher.py`:
   - Extend the existing `BaseWatcher` pattern used by `filesystem_watcher.py`
   - Use `playwright` to connect to WhatsApp Web (persistent browser context stored in `~/.whatsapp_session/`)
   - Poll every 30 seconds for unread messages
   - Detect keywords: `['urgent', 'asap', 'invoice', 'payment', 'help', 'deadline', 'important']`
   - For matching messages, create a file `Needs_Action/WHATSAPP_{contact}_{timestamp}.md` with proper YAML frontmatter (type, from, text, received, priority, status: pending)
   - Mark processed messages in a local `Silver_Tier/.whatsapp_processed.json` cache to avoid duplicates
   - Full DEV_MODE support: when `DEV_MODE=true`, generate synthetic WhatsApp messages from `Silver_Tier/Templates/whatsapp_test_messages.json` instead of connecting to real WhatsApp
   - Include exponential backoff retry on connection failures
   - Log all detections to `Logs/YYYY-MM-DD.json`

2. Create `Silver_Tier/Templates/whatsapp_test_messages.json` with 5 realistic test messages.

3. Create `Skills/whatsapp_watcher.md` Agent Skill.

4. Add `whatsapp_watcher` command to `run_ai_employee.sh`.

---

## PHASE 3: Finance Watcher + Accounting System

**Goal:** Build the financial perception layer and accounting records.

1. Create `~/AI_Employee_Vault/finance_watcher.py`:
   - Poll a local CSV file at `Accounting/bank_transactions.csv` every 5 minutes (this is the simulated bank feed)
   - Parse new rows and append them to `Accounting/Current_Month.md` in the format specified in the hackathon spec
   - Detect subscription patterns using a `SUBSCRIPTION_PATTERNS` dict (include Netflix, Spotify, Adobe, Notion, Slack, GitHub, AWS, Google, OpenAI, Anthropic, etc.)
   - Flag suspicious transactions: amounts > $500 → create `Needs_Action/FINANCE_review_{id}.md` + `Pending_Approval/PAYMENT_review_{id}.md`
   - Full DEV_MODE: generate synthetic transactions from a hardcoded list
   - Log all new transactions to `Gold_Tier/Logs/audit_logs/YYYY-MM-DD.json`

2. Create `Accounting/Current_Month.md` template with proper YAML frontmatter.

3. Create `Accounting/bank_transactions.csv` with 10 realistic sample transactions (mix of income + expenses + subscriptions).

4. Create `Accounting/Rates.md` — client billing rates reference file (used by the invoice flow example in the spec).

5. Create `audit_logic.py` at vault root:
   - `SUBSCRIPTION_PATTERNS` dict with 15+ common services
   - `analyze_transaction(transaction: dict) -> dict | None` function
   - `flag_unused_subscriptions(transactions: list, days_threshold=30) -> list` function
   - Full docstrings and type hints

6. Create `Skills/finance_watcher.md` Agent Skill.

7. Add `finance_watcher` command to `run_ai_employee.sh`.

---

## PHASE 4: Multiple MCP Servers

**Goal:** Build actual working MCP servers (currently the MCP_Servers dir is empty).

Create all MCP servers inside `~/AI_Employee_Vault/Silver_Tier/MCP_Servers/`. Each server must be a runnable Node.js or Python script that exposes tools via the MCP protocol.

### 4a. Email MCP Server
Create `Silver_Tier/MCP_Servers/email_mcp/`:
- `index.js` — MCP server using `@modelcontextprotocol/sdk`
- Tools exposed: `send_email(to, subject, body, attachment?)`, `draft_email(to, subject, body)`, `search_emails(query)`, `get_email(id)`
- Uses Gmail API credentials from `.env` (GMAIL_CLIENT_ID, GMAIL_CLIENT_SECRET, GMAIL_REFRESH_TOKEN)
- DEV_MODE: logs the email to `Logs/email_mcp_dev.log` instead of sending
- `package.json` with all dependencies

### 4b. Calendar MCP Server
Create `Silver_Tier/MCP_Servers/calendar_mcp/`:
- `index.js` — MCP server
- Tools: `create_event(title, start, end, attendees)`, `list_events(date_range)`, `update_event(id, changes)`, `delete_event(id)`
- Uses Google Calendar API (same OAuth as Gmail)
- DEV_MODE: writes to `Accounting/calendar_events.json` locally

### 4c. Odoo MCP Server
Create `Silver_Tier/MCP_Servers/odoo_mcp/`:
- `odoo_mcp.py` — Python MCP server using `mcp` library
- Connects to Odoo via JSON-RPC 2.0 at `ODOO_URL` from `.env`
- Tools: `create_invoice(partner, amount, description)`, `list_invoices(state?)`, `create_customer(name, email)`, `get_accounting_summary()`, `post_invoice(id)` (requires HITL approval)
- Authentication: `xmlrpc.client` with `ODOO_DB`, `ODOO_USER`, `ODOO_PASSWORD` from `.env`
- DEV_MODE: returns mock Odoo responses with realistic data
- `requirements.txt` for this server

### 4d. Social Media MCP Server
Create `Silver_Tier/MCP_Servers/social_mcp/`:
- `social_mcp.py` — Python MCP server
- Tools: 
  - `post_twitter(text, image_url?)` — uses `TWITTER_API_KEY`, `TWITTER_API_SECRET`, `TWITTER_ACCESS_TOKEN`, `TWITTER_ACCESS_SECRET` from `.env`
  - `post_linkedin(text, image_url?)` — uses `LINKEDIN_ACCESS_TOKEN` from `.env`  
  - `post_facebook(text, image_url?, page_id?)` — uses `FACEBOOK_ACCESS_TOKEN` from `.env`
  - `post_instagram(image_url, caption)` — uses `INSTAGRAM_ACCESS_TOKEN` from `.env`
  - `get_social_summary(platform, days=7)` — returns engagement stats
  - `schedule_post(platform, text, scheduled_time)` — queue post for later
- All posts MUST go through HITL: write `Pending_Approval/SOCIAL_{platform}_{timestamp}.md` first; only execute if a matching file exists in `/Approved/`
- DEV_MODE: log intended posts to `Logs/social_mcp_dev.log` with full post content
- `requirements.txt`: `tweepy`, `linkedin-api`, `facebook-sdk`

5. Create `~/.config/claude-code/mcp.json` (or the correct Claude Code MCP config path) registering all 4 servers:
```json
{
  "mcpServers": {
    "email": { "command": "node", "args": ["/home/{USER}/AI_Employee_Vault/Silver_Tier/MCP_Servers/email_mcp/index.js"] },
    "calendar": { "command": "node", "args": ["/home/{USER}/AI_Employee_Vault/Silver_Tier/MCP_Servers/calendar_mcp/index.js"] },
    "odoo": { "command": "python3", "args": ["/home/{USER}/AI_Employee_Vault/Silver_Tier/MCP_Servers/odoo_mcp/odoo_mcp.py"] },
    "social": { "command": "python3", "args": ["/home/{USER}/AI_Employee_Vault/Silver_Tier/MCP_Servers/social_mcp/social_mcp.py"] }
  }
}
```

---

## PHASE 5: Weekly CEO Briefing + Accounting Audit

**Goal:** Build the autonomous weekly business audit that reads from all domains.

1. Create `~/AI_Employee_Vault/weekly_ceo_briefing.py`:
   - Must be schedulable (called by orchestrator every Sunday at 11:00 PM)
   - Read: `Business_Goals.md`, `Done/` (tasks completed this week), `Accounting/Current_Month.md`, `Accounting/bank_transactions.csv`
   - Call `audit_logic.py` to detect subscriptions and flags
   - Call Odoo MCP (or DEV_MODE mock) to get revenue summary
   - Generate a briefing at `Briefings/{YYYY-MM-DD}_Monday_CEO_Briefing.md` following EXACTLY the template in the hackathon spec:
     - Executive Summary
     - Revenue (This Week, MTD, % of target, Trend)
     - Completed Tasks (checkbox list from Done/)
     - Bottlenecks (table: Task | Expected | Actual | Delay)
     - Proactive Suggestions (subscription audit, upcoming deadlines, cost optimization)
   - Update `Dashboard.md` with briefing link
   - Log generation to audit log

2. Add `weekly_ceo_briefing` to the Gold orchestrator's schedule:
   - In `Gold_Tier/Configs/workflows_config.yaml`, add:
     ```yaml
     weekly_ceo_briefing:
       enabled: true
       name: "Weekly CEO Briefing & Accounting Audit"
       trigger:
         type: "schedule"
         day: "sunday"
         time: "23:00"
       steps:
         - audit_accounting
         - analyze_completed_tasks
         - check_subscriptions
         - generate_ceo_briefing
         - notify_human
     ```
   - Add step handlers in `Gold_Tier/Automation/orchestrator.py`

3. Create `Skills/ceo_briefing.md` Agent Skill with full instructions.

---

## PHASE 6: Error Recovery & Graceful Degradation

**Goal:** Make the system production-grade with proper error handling.

1. Create `~/AI_Employee_Vault/retry_handler.py`:
   - `@with_retry(max_attempts=3, base_delay=1, max_delay=60)` decorator
   - Uses exponential backoff: `delay = min(base_delay * (2 ** attempt), max_delay)`
   - `TransientError` custom exception class
   - `AuthError` custom exception class (do NOT retry — alert human)
   - Full docstrings and type hints
   - `if __name__ == "__main__"` test demonstrating retry behavior

2. Create `~/AI_Employee_Vault/process_watchdog.py`:
   - Monitors PID files for: `orchestrator.py`, `filesystem_watcher.py`, `whatsapp_watcher.py`, `finance_watcher.py`
   - PID files stored in `~/.ai_employee_pids/`
   - If a process is dead → restart it + log to `Logs/watchdog.log` + create `Needs_Action/ALERT_process_restart_{name}.md`
   - Runs itself as a daemon (check every 60 seconds)
   - Sends desktop notification if available (`notify-send` on Linux)
   - `start_watchdog()` and `stop_watchdog()` helper functions

3. Update `Gold_Tier/Automation/orchestrator.py` to use `@with_retry` on all external API calls.

4. Add graceful degradation handling to `base_agent.py`:
   - Gmail API down → queue emails to `Silver_Tier/Gmail/.outbox_queue.json`
   - Claude/LLM unavailable → write task to `Needs_Action/DEFERRED_{timestamp}.md` for later
   - Vault locked → write to `/tmp/ai_employee_fallback/` with sync on next run

5. Add `start_watchdog` and `stop_watchdog` commands to `run_ai_employee.sh`.

---

## PHASE 7: Social Media Skill Wrappers + LinkedIn Auto-Post

**Goal:** Add Agent Skills for social media automation per hackathon spec.

1. Create `Skills/linkedin_post.md`:
   - Skill that generates a LinkedIn post from business context
   - Reads `Business_Goals.md` and recent `Done/` tasks for content
   - Suggests post based on week's achievements or insights
   - Routes DRAFT to `Pending_Approval/SOCIAL_linkedin_{timestamp}.md`
   - Only publishes when file moves to `/Approved/`

2. Create `Skills/twitter_post.md`:
   - Reads from `Business_Goals.md` and current research in `Knowledge_Base/`
   - Generates tweet thread (max 10 tweets)
   - HITL approval flow

3. Create `Skills/social_summary.md`:
   - Aggregates last 7 days of social activity from `Logs/social_mcp_dev.log` or real API
   - Generates markdown report of posts published, scheduled, and their performance
   - Outputs to `Briefings/social_summary_{date}.md`

4. Create `Skills/facebook_instagram_post.md`:
   - Handles Facebook Page + Instagram Business posting
   - Includes image path support
   - HITL required

---

## PHASE 8: Architecture Documentation (Submission-Ready)

**Goal:** Make the README submission-ready for the hackathon judges.

1. Rebuild `README.md` completely. It must include:

   **Section 1 — Project Overview**
   - What this is (Digital FTE concept)
   - Tier declaration: **GOLD TIER**
   - The "Aha moment" metric (hours worked, cost per task)

   **Section 2 — Architecture Diagram**
   - Full ASCII architecture diagram matching the hackathon spec's layout
   - Include all layers: Perception (Watchers), Obsidian Vault, Reasoning (Claude Code), HITL, Action (MCP Servers)

   **Section 3 — Setup Instructions**
   - Prerequisites (Python 3.13, Node.js v24+, Claude Code, Obsidian)
   - Step-by-step install: `git clone`, `pip install -r requirements.txt`, `.env` setup
   - Gold Tier setup: `bash Gold_Tier/setup_gold.sh`
   - MCP server registration: `bash setup_mcp_servers.sh`
   - Odoo setup instructions (Docker command to run Odoo 19 locally)

   **Section 4 — Credential Setup**
   - `.env` template with every key needed (OPENROUTER_API_KEY, GMAIL_CLIENT_ID, GMAIL_CLIENT_SECRET, ODOO_URL, ODOO_DB, TWITTER_API_KEY, LINKEDIN_ACCESS_TOKEN, FACEBOOK_ACCESS_TOKEN, INSTAGRAM_ACCESS_TOKEN)
   - Link to each API's developer portal for getting keys
   - Security disclosure: all credentials in `.env` (gitignored), never in vault markdown

   **Section 5 — Features by Tier**
   - Bronze, Silver, Gold features table

   **Section 6 — Running the System**
   - All commands from `run_ai_employee.sh` documented
   - Startup sequence: filesystem watcher → whatsapp watcher → finance watcher → orchestrator → watchdog

   **Section 7 — Lessons Learned**
   - At least 5 substantive lessons about building autonomous agents (file-based state, HITL importance, prompt engineering for agentic loops, error recovery patterns, etc.)

2. Create `setup_mcp_servers.sh` — script to `npm install` all MCP servers and register `mcp.json`:
   - Installs deps for `email_mcp`, `calendar_mcp`
   - `pip install` for `odoo_mcp`, `social_mcp`
   - Writes the MCP JSON config to the correct Claude Code config path
   - Prints a success summary

3. Update `.env` to include a template for ALL required keys (with placeholder values and comments explaining each one). Ensure `.gitignore` includes `.env`.

---

## PHASE 9: Final Integration Test

**Goal:** Verify the complete Gold Tier system works end-to-end.

1. Create `test_gold_tier.sh` — comprehensive test script:
   ```bash
   #!/bin/bash
   # Gold Tier Integration Test Suite
   echo "🥇 Running Gold Tier Integration Tests..."
   
   # Test 1: Ralph Wiggum hook exists
   # Test 2: All MCP servers importable / startable
   # Test 3: Finance watcher DEV_MODE run
   # Test 4: WhatsApp watcher DEV_MODE run  
   # Test 5: CEO briefing generation (DEV_MODE)
   # Test 6: Social media post (DEV_MODE — check Pending_Approval output)
   # Test 7: Retry handler import and decorator test
   # Test 8: Watchdog process monitor import
   # Test 9: audit_logic.py subscription detection
   # Test 10: Full Gold orchestrator workflow dry run
   ```

2. Run `bash test_gold_tier.sh` and fix any failures before declaring done.

3. After all tests pass:
   - Update `Dashboard.md` with "GOLD TIER COMPLETE" status
   - Create `Briefings/GOLD_TIER_COMPLETION_REPORT.md` with:
     - List of all components built in this session
     - Current system capabilities
     - Remaining optional enhancements
     - Submission checklist (GitHub repo link, demo video todo, form link)
   - Log the completion to `Gold_Tier/Logs/audit_logs/YYYY-MM-DD.json`

---

## COMPLETION SIGNAL

When ALL phases are done, output this exact string to signal the Ralph Wiggum hook:

```
<promise>GOLD_TIER_BUILD_COMPLETE</promise>
```

And move `Plans/CURRENT_TASK.md` status to `done`.

---

## CONTEXT FILES TO READ FIRST

Before starting any phase, read these files in order:
1. `CLAUDE.md` — your operating system
2. `Personal AI Employee Hackathon 0_ Building Autonomous FTEs in 2026.md` — the spec
3. `Gold_Tier/Configs/gold_config.yaml` — current Gold config
4. `Silver_Tier/SILVER_TIER_COMPLETE.md` — what Silver already provides
5. `run_ai_employee.sh` — current command registry
6. `.env` — what credentials already exist (use them, don't overwrite)
