# Slack Integration (Platinum)
**Mode: MANUAL-TRIGGER (requires configuration)**

## Purpose
Real-time AI assistant in Slack with slash commands and intelligent responses.

## Features
- Auto-respond to @mentions with AI
- Monitor specific channels for keywords
- Interactive slash commands
- Scheduled status updates
- Rich message formatting

## Slash Commands
| Command | Description |
|---------|-------------|
| `/briefing` | Morning intelligence briefing |
| `/tasks` | Prioritized task list |
| `/research <topic>` | Conduct research on topic |
| `/analytics` | Performance metrics |
| `/predict` | Workload forecast |

## Setup Required
1. Create Slack app at https://api.slack.com/apps
2. Enable Socket Mode
3. Get credentials:
   - Bot User OAuth Token (xoxb-...)
   - Signing Secret
   - App-Level Token (xapp-...)
4. Update `Platinum_Tier/Configs/platinum_config.yaml`:

```yaml
integrations:
  slack:
    enabled: true
    workspace: "Your Workspace"
    bot_token: "xoxb-your-token"
    signing_secret: "your-secret"
    app_token: "xapp-your-token"
    channels:
      notifications: "CXXXXXXXX"
      commands: "CXXXXXXXX"
```

## Execution
```bash
bash run_ai_employee.sh slack_bot
```

Or directly:
```python
from Platinum_Tier.Integrations.slack.slack_bot import PlatinumSlackBot
bot = PlatinumSlackBot('/mnt/c/Users/Admin/AI_Employee_Vault')
bot.start()
```

## Security Notes
- Never commit tokens to version control
- Use environment variables for production
- Rotate tokens periodically
