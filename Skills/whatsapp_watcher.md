# WhatsApp Watcher Skill

**Mode:** AUTO-EXECUTE
**Trigger:** Continuous polling (30 seconds)
**Status:** Active (DEV_MODE)

## Purpose

Monitors WhatsApp Web for urgent messages and automatically creates action items.

## How It Works

1. Polls WhatsApp Web every 30 seconds
2. Scans for urgent keywords: `urgent`, `asap`, `invoice`, `payment`, `help`, `deadline`, `important`
3. Creates `Needs_Action/WHATSAPP_{contact}_{timestamp}.md` files
4. Logs all detections to audit log

## Usage

```bash
# Start watcher (continuous)
python3 whatsapp_watcher.py

# Run once
python3 whatsapp_watcher.py --once
```

## DEV_MODE

When `DEV_MODE=true`, uses synthetic test messages from `Silver_Tier/Templates/whatsapp_test_messages.json` instead of connecting to real WhatsApp Web.

## Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| DEV_MODE | false | Use synthetic messages |
| POLL_INTERVAL | 30 | Seconds between checks |

## Keywords Triggering Action

- urgent
- asap
- invoice
- payment
- help
- deadline
- important

## Output Files

Created files have YAML frontmatter:
```yaml
---
type: whatsapp_message
from: "Contact Name"
text: "Message preview"
received: "ISO timestamp"
priority: 🔴 URGENT | 🟡 HIGH | 🟢 NORMAL
status: pending
---
```

## Integration

Added to `run_ai_employee.sh`:
```bash
bash run_ai_employee.sh whatsapp_watcher
```
