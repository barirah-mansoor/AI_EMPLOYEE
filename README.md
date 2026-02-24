# 🤖 AI Employee Vault - GOLD TIER

> Your Personal Autonomous AI Agent System | Version 2.0

Welcome to **AI Employee Vault** - a Gold Tier autonomous AI system that works for you 24/7. This is a **Digital FTE (Full-Time Employee)** that handles tasks, communications, finances, research, meetings, and more - completely autonomously.

---

## ✨ The "Aha Moment"

This system operates as a **true autonomous employee**:

| Metric | Traditional Employee | AI Employee |
|--------|---------------------|-------------|
| **Cost/month** | $5,000+ | ~$50 (API costs) |
| **Hours** | 40/week | 168/week (24/7) |
| **Response Time** | Hours | Seconds |
| **Consistency** | Varies | Always same quality |
| **Scalability** | 1x | 10x (parallel tasks) |

**Bottom Line:** You get a full-time employee for 1% of the cost.

---

## 🏗️ Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         PERCEPTION LAYER (Inputs)                           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐      │
│  │  WhatsApp        │  │  Finance         │  │  Filesystem      │      │
│  │  Watcher         │  │  Watcher         │  │  Watcher         │      │
│  │                  │  │                  │  │                  │      │
│  │  - Poll 30s     │  │  - Poll 5min     │  │  - Inotify       │      │
│  │  - Keywords     │  │  - CSV parsing   │  │  - File events   │      │
│  │  - Create task  │  │  - Subscription   │  │  - Auto-process  │      │
│  └────────┬─────────┘  └────────┬─────────┘  └────────┬─────────┘      │
│           │                      │                      │                 │
│           ▼                      ▼                      ▼                 │
│  ┌─────────────────────────────────────────────────────────────────┐      │
│  │                     NEEDS_ACTION FOLDER                         │      │
│  │   WHATSAPP_*.md | FINANCE_*.md | EMAIL_*.md | *.md          │      │
│  └─────────────────────────────────────────────────────────────────┘      │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           VAULT (Memory)                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                         VAULT STRUCTURE                              │   │
│  ├───────────────┬───────────────┬───────────────┬───────────────────┤   │
│  │  Inbox/       │  Needs_Action│  Plans/       │  Pending_Approval│   │
│  │               │               │               │                   │   │
│  │  Drop tasks   │  AI reviews  │  AI creates  │  Human approval  │   │
│  │  here         │  this        │  plans here  │  required        │   │
│  └───────────────┴───────────────┴───────────────┴───────────────────┘   │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  ├───────────────┬───────────────┬───────────────┬───────────────────┤   │
│  │  Approved/    │  Done/       │  Briefings/  │  Accounting/      │   │
│  │               │               │               │                   │   │
│  │  Ready to    │  Completed   │  Daily/Weekly │  Financial        │   │
│  │  execute     │  tasks      │  reports      │  records          │   │
│  └───────────────┴───────────────┴───────────────┴───────────────────┘   │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  ├───────────────┬───────────────┬───────────────┬───────────────────┤   │
│  │  Logs/        │  Skills/     │  Knowledge_Base│ Gold_Tier/      │   │
│  │               │               │                │                   │   │
│  │  Audit trail │  Agent        │  Research     │  AI Agents       │   │
│  │  JSON logs   │  capabilities │  documents    │  & Orchestrator  │   │
│  └───────────────┴───────────────┴───────────────┴───────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                      REASONING LAYER (LLM)                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌───────────────────────────────────────────────────────────────────────┐ │
│  │                     OPENROUTER (Gateway)                             │ │
│  │                                                                       │ │
│  │   ┌─────────────────────────────────────────────────────────────┐   │ │
│  │   │  Model: arcee-ai/trinity-large-preview:free              │   │ │
│  │   │  Fallback: Multiple free models available                  │   │ │
│  │   │  Rate Limit: None (free tier)                               │   │ │
│  │   └─────────────────────────────────────────────────────────────┘   │ │
│  │                                                                       │ │
│  └───────────────────────────────────────────────────────────────────────┘ │
│                                    │                                        │
│           ┌────────────────────────┼────────────────────────┐              │
│           ▼                        ▼                        ▼              │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐           │
│  │ Email Agent     │  │ Task Optimizer  │  │ Research Agent │           │
│  │                 │  │                 │  │                 │           │
│  │ - Analyze       │  │ - Eisenhower   │  │ - Web search   │           │
│  │ - Sentiment     │  │ - Prioritize   │  │ - Source check │           │
│  │ - Auto-respond  │  │ - Schedule     │  │ - Summarize    │           │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘           │
│           │                        │                        │              │
│           └────────────────────────┼────────────────────────┘              │
│                                    ▼                                        │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐           │
│  │ Meeting Agent   │  │ Orchestrator     │  │ Base Agent     │           │
│  │                 │  │                 │  │                 │           │
│  │ - Prep         │  │ - Schedule      │  │ - LLM wrapper  │           │
│  │ - Attendees     │  │ - Workflows     │  │ - Retry logic │           │
│  │ - Follow-up     │  │ - Alerts       │  │ - Logging     │           │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘           │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                     HITL (Human in the Loop)                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌───────────────────────────────────────────────────────────────────────┐ │
│  │                     APPROVAL WORKFLOW                                 │ │
│  │                                                                       │ │
│  │   ┌──────────────┐      ┌──────────────┐      ┌──────────────┐    │ │
│  │   │ Pending_     │ ───► │   Human      │ ───► │  Approved/   │    │ │
│  │   │ Approval/    │      │   Reviews    │      │              │    │ │
│  │   │              │      │              │      │  Execute    │    │ │
│  │   └──────────────┘      └──────────────┘      └──────────────┘    │ │
│  │                                                                       │ │
│  │   Triggers: Payments, Emails, Social Posts, External Actions       │ │
│  └───────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                        ACTION LAYER (MCP)                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐  ┌────────────┐          │
│  │   Email    │  │  Calendar  │  │   Odoo     │  │  Social    │          │
│  │    MCP     │  │    MCP      │  │    MCP     │  │   MCP      │          │
│  │            │  │            │  │            │  │            │          │
│  │ send_     │  │ create_    │  │ create_    │  │ post_      │          │
│  │ email()    │  │ event()    │  │ invoice()  │  │ twitter()  │          │
│  │ draft_     │  │ list_      │  │ list_      │  │ post_      │          │
│  │ email()    │  │ events()   │  │ invoices() │  │ linkedin() │          │
│  │ search_    │  │ update_    │  │ post_      │  │ post_      │          │
│  │ emails()   │  │ event()    │  │ invoice()  │  │ facebook() │          │
│  └────────────┘  └────────────┘  └────────────┘  └────────────┘          │
│                                                                             │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐  ┌────────────┐          │
│  │ Gmail API  │  │ Google     │  │ XML-RPC    │  │  Twitter   │          │
│  │            │  │ Calendar   │  │   Odoo     │  │  LinkedIn  │          │
│  └────────────┘  └────────────┘  └────────────┘  └────────────┘          │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start

### 1. Prerequisites

```bash
# Python 3.8+
python --version
# Should show: Python 3.8.x or higher

# Claude Code CLI
npm install -g @anthropic/claude-code
# Verify: claude --version

# Git (for cloning)
git --version

# Node.js (for MCP servers)
node --version
# Should show: Node 18+
```

### 2. Clone & Install

```bash
# Clone the repository
git clone <your-repo-url> ~/AI_Employee_Vault
cd ~/AI_Employee_Vault

# Install Python dependencies
pip install -r requirements.txt

# For Gold Tier (additional)
pip install openai pyyaml schedule

# Install Node.js dependencies for MCP servers
cd Silver_Tier/MCP_Servers/email_mcp && npm install
cd ../../calendar_mcp && npm install
```

### 3. Configure Environment

Create `.env` file in vault root:

```bash
# ============================================
# REQUIRED - LLM Provider
# ============================================

# Get free API key at https://openrouter.ai
OPENROUTER_API_KEY=sk-or-v1-xxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# ============================================
# OPTIONAL - Gmail API (for email sending)
# ============================================
GMAIL_CLIENT_ID=your-client-id.apps.googleusercontent.com
GMAIL_CLIENT_SECRET=your-client-secret
GMAIL_REFRESH_TOKEN=your-refresh-token

# ============================================
# OPTIONAL - Odoo ERP (for accounting)
# ============================================
ODOO_URL=http://localhost:8069
ODOO_DB=odoo
ODOO_USER=admin
ODOO_PASSWORD=your-password

# ============================================
# OPTIONAL - Social Media
# ============================================
TWITTER_API_KEY=xxx
TWITTER_API_SECRET=xxx
TWITTER_ACCESS_TOKEN=xxx
TWITTER_ACCESS_SECRET=xxx
LINKEDIN_ACCESS_TOKEN=xxx
FACEBOOK_ACCESS_TOKEN=xxx
INSTAGRAM_ACCESS_TOKEN=xxx

# ============================================
# OPTIONAL - Development
# ============================================
DEV_MODE=true              # Use synthetic data (no real APIs)
MAX_ITERATIONS=10          # Ralph Wiggum max loops
```

### 4. First Run

```bash
# Make scripts executable
chmod +x *.sh
chmod +x Gold_Tier/AI_Agents/*.py

# Test the setup
bash test_gold_tier.sh

# Start the system
bash run_ai_employee.sh start_gold

# Check dashboard
cat Dashboard.md
```

---

## 📋 Features by Tier

### 🥉 Bronze Tier (Foundation)

| Feature | Command | Description |
|---------|---------|-------------|
| **File Watcher** | `bash run_ai_employee.sh start` | Monitors Inbox folder |
| **Task Processing** | `process_inbox` | Creates plans from files |
| **Priority Sorting** | Auto | URGENT/HIGH/NORMAL/LOW |
| **Dashboard** | `vault_health` | Real-time status |
| **Audit Logging** | Auto | Every action in JSON |
| **Briefing** | `daily_briefing` | Daily summary |

### 🥈 Silver Tier (Advanced)

| Feature | Command | Description |
|---------|---------|-------------|
| **Gmail Sync** | `process_gmail` | Sync emails to files |
| **Email Processing** | `process_emails` | Categorize & analyze |
| **Email Sending** | `send_emails` | Send approved responses |
| **System Monitor** | `system_monitor` | Health & performance |
| **Scheduler** | `start_scheduler` | Automated cron |
| **Enhanced Briefing** | `silver_briefing` | With email data |

### 🥇 Gold Tier (Autonomous)

| Feature | Command | Description |
|---------|---------|-------------|
| **Email Intelligence** | `email_intelligence [n]` | AI analysis, sentiment, auto-response |
| **Deep Research** | `deep_research "topic"` | Multi-source research |
| **Meeting Maestro** | `meeting_maestro` | Auto prep & follow-up |
| **Task Optimizer** | `task_optimizer` | Eisenhower Matrix |
| **Gold Briefing** | `gold_briefing` | Morning intelligence |
| **Weekly CEO Briefing** | `weekly_briefing` | Business audit |
| **WhatsApp Watcher** | `whatsapp_watcher` | Urgent messages |
| **Finance Watcher** | `finance_watcher` | Transaction monitoring |
| **Process Watchdog** | `start_watchdog` | Auto-restart |
| **Ralph Wiggum** | Auto | Autonomous completion |
| **Error Recovery** | Auto | Graceful degradation |
| **MCP Servers** | Auto | Email, Calendar, Odoo, Social |

---

## 💻 Complete Command Reference

### Basic Operations

```bash
# Start/Stop
bash run_ai_employee.sh start              # Start filesystem watcher
bash run_ai_employee.sh stop                # Stop all watchers

# Processing
bash run_ai_employee.sh process_inbox       # Process Inbox folder
bash run_ai_employee.sh vault_health        # Check system health
bash run_ai_employee.sh audit_week          # Weekly audit
```

### Silver Tier

```bash
# Email
bash run_ai_employee.sh process_gmail      # Sync Gmail
bash run_ai_employee.sh process_emails      # Categorize emails
bash run_ai_employee.sh send_emails        # Send approved emails

# System
bash run_ai_employee.sh silver_briefing     # Daily briefing
bash run_ai_employee.sh system_monitor      # Health check
bash run_ai_employee.sh start_scheduler     # Start scheduler
bash run_ai_employee.sh stop_scheduler      # Stop scheduler
```

### Gold Tier - AI Agents

```bash
# Email Intelligence
bash run_ai_employee.sh email_intelligence 5    # Process 5 emails
bash run_ai_employee.sh email_intelligence 20   # Process 20 emails
bash run_ai_employee.sh email_intelligence all   # Process all emails

# Research
bash run_ai_employee.sh deep_research "AI trends 2026"
bash run_ai_employee.sh deep_research "best productivity tools"
bash run_ai_employee.sh deep_research "market analysis"

# Task Management
bash run_ai_employee.sh task_optimizer          # Eisenhower Matrix
bash run_ai_employee.sh meeting_maestro         # Meeting prep
bash run_ai_employee.sh meeting_maestro "team sync"

# Briefings
bash run_ai_employee.sh gold_briefing           # Daily briefing
bash run_ai_employee.sh weekly_briefing         # CEO briefing
```

### Gold Tier - Watchers & Monitors

```bash
# WhatsApp Watcher
bash run_ai_employee.sh whatsapp_watcher       # Start (continuous)
bash run_ai_employee.sh whatsapp_once          # Run once

# Finance Watcher
bash run_ai_employee.sh finance_watcher         # Start (continuous)
bash run_ai_employee.sh finance_once           # Run once
```

### Gold Tier - System

```bash
# Orchestrator
bash run_ai_employee.sh start_gold            # Start orchestrator
bash run_ai_employee.sh stop_gold             # Stop orchestrator

# Watchdog
bash run_ai_employee.sh start_watchdog        # Start watchdog
bash run_ai_employee.sh stop_watchdog         # Stop watchdog

# Testing
bash run_ai_employee.sh test_gold             # Test setup
bash test_gold_tier.sh                        # Full integration tests
```

---

## 📁 Complete Vault Structure

```
AI_Employee_Vault/
├── .env                           # API keys (NEVER commit)
├── .gitignore                     # Ignore .env, logs, etc.
├── README.md                      # This file
├── CLAUDE.md                      # AI instructions
├── Dashboard.md                   # Real-time status
│
├── Inbox/                         # Drop tasks here
│   └── *.txt, *.md, *.pdf        # Task files
│
├── Needs_Action/                  # Files awaiting AI review
│   ├── EMAIL_*.md                # From Gmail
│   ├── WHATSAPP_*.md             # From WhatsApp
│   ├── FINANCE_*.md              # From Finance Watcher
│   └── *.md                      # From Inbox
│
├── Plans/                         # AI-generated plans
│   ├── CURRENT_TASK.md           # Ralph Wiggum tracking
│   └── PLAN_*.md                # Task plans
│
├── Pending_Approval/              # Human review required
│   ├── PAYMENT_*.md              # Financial approvals
│   ├── SOCIAL_*.md              # Social media posts
│   └── *.md                      # Other approvals
│
├── Approved/                      # Ready to execute
│   └── *.md                      # Approved actions
│
├── Done/                          # Completed tasks
│   └── *.md                      # Archived tasks
│
├── Briefings/                     # AI-generated reports
│   ├── gold_briefing_*.md       # Daily briefings
│   ├── *_Monday_CEO_Briefing.md # Weekly briefings
│   └── social_summary_*.md      # Social reports
│
├── Accounting/                    # Financial records
│   ├── Current_Month.md          # This month's transactions
│   ├── bank_transactions.csv    # Bank feed (edit this)
│   └── Rates.md                  # Client billing rates
│
├── Logs/                          # Audit logs
│   ├── YYYY-MM-DD.json          # Daily action logs
│   ├── ralph_wiggum.json        # Ralph loop logs
│   ├── watchdog.log             # Process monitor logs
│   └── *.log                    # Various logs
│
├── Skills/                        # Agent capabilities (markdown)
│   ├── ralph_loop.md            # Ralph Wiggum skill
│   ├── whatsapp_watcher.md      # WhatsApp skill
│   ├── finance_watcher.md       # Finance skill
│   ├── linkedin_post.md         # LinkedIn skill
│   ├── twitter_post.md           # Twitter skill
│   └── *.md                     # Other skills
│
├── Knowledge_Base/                # Research storage
│   ├── documents/               # Saved research
│   ├── embeddings/              # Vector embeddings
│   └── summaries/               # Research summaries
│
├── Gold_Tier/                     # Gold Tier components
│   ├── AI_Agents/              # AI agent implementations
│   │   ├── base_agent.py       # Foundation class
│   │   ├── email_agent.py      # Email intelligence
│   │   ├── research_agent.py    # Deep research
│   │   ├── meeting_agent.py     # Meeting automation
│   │   └── task_optimizer.py    # Task prioritization
│   │
│   ├── Automation/              # Workflow orchestration
│   │   ├── orchestrator.py     # Main scheduler
│   │   ├── workflows/          # Workflow definitions
│   │   ├── schedules/          # Schedule configs
│   │   └── triggers/           # Event triggers
│   │
│   ├── Configs/                 # Configuration
│   │   ├── gold_config.yaml   # Main config
│   │   ├── agents_config.yaml # Agent settings
│   │   └── workflows_config.yaml # Workflows
│   │
│   ├── Analytics/               # Reports
│   │   └── Reports/
│   │       ├── Daily/          # Daily reports
│   │       ├── Weekly/         # Weekly reports
│   │       └── Monthly/        # Monthly reports
│   │
│   └── Logs/                    # Gold Tier logs
│       ├── agent_logs/         # Agent-specific logs
│       ├── workflow_logs/      # Workflow logs
│       └── audit_logs/         # Audit trail
│
├── Silver_Tier/                   # Silver Tier components
│   ├── *.py                     # Silver scripts
│   ├── MCP_Servers/            # MCP implementations
│   │   ├── email_mcp/          # Email MCP server
│   │   ├── calendar_mcp/       # Calendar MCP server
│   │   ├── odoo_mcp/           # Odoo MCP server
│   │   └── social_mcp/         # Social MCP server
│   └── Templates/              # Test message templates
│
├── ralph_wiggum.py               # Ralph Wiggum hook
├── whatsapp_watcher.py          # WhatsApp monitor
├── finance_watcher.py            # Finance monitor
├── audit_logic.py                # Subscription detection
├── weekly_ceo_briefing.py       # CEO briefing generator
├── retry_handler.py              # Error recovery
├── process_watchdog.py           # Process monitor
├── test_gold_tier.sh            # Integration tests
└── run_ai_employee.sh           # Main CLI
```

---

## 🔧 MCP Servers Deep Dive

### 4 MCP Servers Included

#### 1. Email MCP (`email_mcp/`)

```javascript
// Tools available:
send_email(to, subject, body, attachment?)
draft_email(to, subject, body)
search_emails(query, maxResults?)
get_email(id)
```

**Setup:** Requires Gmail OAuth credentials in `.env`

#### 2. Calendar MCP (`calendar_mcp/`)

```javascript
// Tools available:
create_event(title, start, end, attendees?, description?, location?)
list_events(date_range, max_results?)
update_event(id, changes)
delete_event(id)
```

**Setup:** Uses same credentials as Gmail

#### 3. Odoo MCP (`odoo_mcp/`)

```python
# Tools available:
create_invoice(partner, amount, description)
list_invoices(state?)  # draft, posted, paid
create_customer(name, email)
get_accounting_summary()
post_invoice(id)  # Requires HITL approval
```

**Setup:** Requires Odoo instance running

#### 4. Social MCP (`social_mcp/`)

```python
# Tools available:
post_twitter(text, image_url?)
post_linkedin(text, image_url?)
post_facebook(text, image_url?, page_id?)
post_instagram(image_url, caption)
get_social_summary(platform?, days?)
schedule_post(platform, text, scheduled_time)
```

**Setup:** Requires platform API credentials

---

## 🔐 Security Model

### Always Rules (Never Break)

1. **Log Everything** - Every action → `Logs/YYYY-MM-DD.json`
2. **No Financial Actions** - Always create `Pending_Approval/`
3. **No Deletion** - Always move to `Done/`
4. **Update Dashboard** - After any task batch
5. **No External Comms** - Without `Approved/` file
6. **Write Plans** - If uncertain, create plan first

### HITL (Human in the Loop)

Required for:
- 💸 Payments > $500
- 📧 External emails
- 🐦 Social media posts
- 📄 Invoice posting
- 🔓 Account changes

### Approval Workflow

```
AI detects action requiring approval
         │
         ▼
Create Pending_Approval/FILE.md
         │
         ▼
Human reviews file
         │
    ┌────┴────┐
    ▼         ▼
Reject     Move to
           Approved/
         │
         ▼
AI executes action
```

---

## 🌀 Ralph Wiggum Loop

The system prevents Claude from stopping mid-task.

### How It Works

1. **Start Task:** Update `Plans/CURRENT_TASK.md`
2. **Work:** Claude continues until done
3. **Stop Attempt:** Hook checks status
4. **If in_progress:** Block exit, keep working
5. **If done:** Allow exit

### Configuration

```yaml
# Plans/CURRENT_TASK.md
---
status: in_progress
task: "Build MCP Servers"
iterations: 0
created: "2026-02-24T10:00:00"
---
```

```bash
# Environment
MAX_ITERATIONS=10  # Prevent infinite loops
```

### Commands

```bash
# Check status
python3 ralph_wiggum.py

# Set custom max
MAX_ITERATIONS=20 python3 ralph_wiggum.py
```

---

## 🔄 Error Recovery

### Retry Handler

```python
from retry_handler import with_retry, TransientError

@with_retry(max_attempts=3, base_delay=1.0)
def call_api():
    # API call that might fail
    pass
```

**Features:**
- Exponential backoff
- Custom exceptions
- AuthError (no retry)
- TransientError (retry)

### Graceful Degradation

| Failure | Action |
|---------|--------|
| LLM unavailable | Write to `DEFERRED_*.md` |
| Gmail down | Queue to `.outbox_queue.json` |
| Vault locked | Write to `/tmp/` |

### Process Watchdog

Monitors and auto-restarts:
- `orchestrator.py`
- `filesystem_watcher.py`
- `whatsapp_watcher.py`
- `finance_watcher.py`

---

## 📊 DEV_MODE

All features work without real APIs!

```bash
# Enable
DEV_MODE=true

# Test components
DEV_MODE=true python3 whatsapp_watcher.py --once
DEV_MODE=true python3 finance_watcher.py --once
DEV_MODE=true python3 weekly_ceo_briefing.py
```

### Synthetic Data Sources

| Component | Source |
|-----------|--------|
| WhatsApp | `Silver_Tier/Templates/whatsapp_test_messages.json` |
| Finance | Hardcoded transactions in `finance_watcher.py` |
| Email | Real Gmail (or mock if no credentials) |
| Odoo | Mock responses |

---

## 🧪 Testing

### Run All Tests

```bash
bash test_gold_tier.sh
```

### Test Individual Components

```bash
# Test imports
python3 -c "from Gold_Tier.AI_Agents.base_agent import BaseAgent"

# Test LLM
python3 Gold_Tier/AI_Agents/base_agent.py

# Test audit logic
python3 audit_logic.py

# Test retry handler
python3 retry_handler.py
```

### Expected Output

```
Test 1: Ralph Wiggum hook... ✅
Test 2: Agent imports... ✅
Test 3: Finance watcher... ✅
Test 4: WhatsApp watcher... ✅
Test 5: CEO briefing... ✅
Test 6: Retry handler... ✅
Test 7: Process watchdog... ✅
Test 8: Audit logic... ✅
Test 9: MCP Servers... ✅
Test 10: Skills... ✅

🎉 All tests passed!
```

---

## 🚦 Getting Started Checklist

- [ ] Clone repository
- [ ] Install Python dependencies
- [ ] Create `.env` with OPENROUTER_API_KEY
- [ ] Run `bash test_gold_tier.sh`
- [ ] Start orchestrator: `bash run_ai_employee.sh start_gold`
- [ ] Process emails: `bash run_ai_employee.sh email_intelligence 5`
- [ ] Check dashboard: `cat Dashboard.md`

---

## 📈 Metrics & Analytics

### What Gets Tracked

- Emails processed
- Tasks completed
- Time saved
- Revenue tracked
- Subscriptions detected
- Social posts published

### Where

- `Gold_Tier/Analytics/Reports/Daily/`
- `Gold_Tier/Analytics/Reports/Weekly/`
- `Briefings/`

---

## 🔗 External Integrations

### Getting API Keys

| Service | URL | Purpose |
|---------|-----|---------|
| OpenRouter | https://openrouter.ai | LLM (free tier) |
| Google Cloud | https://console.cloud.google.com | Gmail + Calendar |
| Odoo | https://www.odoo.com | ERP/Accounting |
| Twitter Dev | https://developer.twitter.com | Twitter/X |
| LinkedIn Dev | https://developer.linkedin.com | LinkedIn |
| Meta Dev | https://developers.facebook.com | Facebook/Instagram |

---

## 🤝 Contributing

1. Fork the repo
2. Create feature branch
3. Make changes
4. Add tests
5. Submit PR

---

## 📝 License

MIT License - Use freely!

---

## 🙏 Acknowledgments

- Claude Code (Anthropic)
- OpenRouter
- Model Context Protocol
- Open Source Community

---

## ❓ FAQ

### Q: Does it really work without any API keys?
**A:** Yes! Set `DEV_MODE=true` in `.env` and everything works with synthetic data.

### Q: How much does it cost?
**A:** ~$0-50/month depending on usage. OpenRouter free tier covers most use cases.

### Q: Is it safe?
**A:** Yes! Multiple safety layers: audit logging, HITL approval, no deletion, financial controls.

### Q: Can I customize it?
**A:** Absolutely! Edit skills in `Skills/`, agents in `Gold_Tier/AI_Agents/`, or add new MCP servers.

### Q: How do I get help?
**A:** Check `CLAUDE.md`, review logs in `Logs/`, or open an issue on GitHub.

---

## 📚 Additional Resources

- [CLAUDE.md](CLAUDE.md) - Detailed AI instructions
- [Skills/](Skills/) - Agent capabilities
- [Gold_Tier/](Gold_Tier/) - AI agent source code
- [Logs/](Logs/) - Audit trail

---

*Your Personal AI Employee - Working 24/7 for you*

**Tier: 🥇 GOLD | Version: 2.0 | Status: OPERATIONAL**
