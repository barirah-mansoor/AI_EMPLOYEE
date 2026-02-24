# Finance Watcher Skill

**Mode:** AUTO-EXECUTE
**Trigger:** Continuous polling (5 minutes)
**Status:** Active (DEV_MODE)

## Purpose

Monitors bank transactions for subscriptions, suspicious activity, and updates accounting records.

## How It Works

1. Polls `Accounting/bank_transactions.csv` every 5 minutes
2. Detects subscriptions from 15+ services (Netflix, AWS, GitHub, etc.)
3. Flags suspicious transactions (>$500) for human review
4. Updates `Accounting/Current_Month.md`
5. Creates review files in `Needs_Action/` and `Pending_Approval/`

## Usage

```bash
# Start watcher (continuous)
python3 finance_watcher.py

# Run once
python3 finance_watcher.py --once
```

## DEV_MODE

When `DEV_MODE=true`, uses synthetic transactions instead of reading bank CSV.

## Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| DEV_MODE | false | Use synthetic transactions |
| POLL_INTERVAL | 300 | Seconds between checks (5 min) |

## Subscriptions Detected

- Netflix, Spotify, Adobe, Notion, Slack
- GitHub, AWS, Google Cloud, OpenAI, Anthropic
- Zoom, Dropbox, Microsoft 365, Apple, Figma
- Atlassian (Jira, Confluence), Heroku, DigitalOcean

## Suspicious Transaction Handling

Transactions > $500 are flagged and create:
1. `Needs_Action/FINANCE_review_{id}.md`
2. `Pending_Approval/PAYMENT_review_{id}.md`

## Commands

```bash
bash run_ai_employee.sh finance_watcher
bash run_ai_employee.sh finance_once
```
