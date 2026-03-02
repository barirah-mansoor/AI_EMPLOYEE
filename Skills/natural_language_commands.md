# Natural Language Commands (Platinum)
**Mode: INTERACTIVE**

## Purpose
Execute any command using plain English - no need to remember specific syntax.

## How It Works
1. User types natural language command
2. AI analyzes intent and extracts parameters
3. System executes appropriate action
4. Results displayed in conversational format

## Example Commands

### Email
- "check my emails"
- "process my inbox"
- "send pending emails"
- "show me important emails"

### Research
- "research AI automation trends"
- "find info about machine learning"
- "look up competitive analysis best practices"

### Tasks
- "what are my top tasks"
- "prioritize my work"
- "show me my todo list"
- "what should I focus on today"

### Meetings
- "prepare for my meetings"
- "check my schedule"
- "what meetings do I have today"

### Analytics
- "show me analytics"
- "how am I doing"
- "give me a performance report"

### Predictions
- "predict my workload"
- "what's coming up this week"
- "forecast my tasks"

### Help
- "help"
- "what can you do"
- "show commands"

## Usage

### Interactive Chat
```bash
bash run_ai_employee.sh chat
```

### Programmatic
```python
from Platinum_Tier.NLP.command_processor import NLPCommandProcessor
processor = NLPCommandProcessor('/mnt/c/Users/Admin/AI_Employee_Vault')

# Process single command
result = processor.process_command("research AI trends")
execution = processor.execute_command(result)

# Interactive chat
processor.chat_interface()
```

## Conversation Memory
- Remembers context within session
- Can reference previous commands
- Maintains conversation history

## Tips
- Be specific for better results
- Use natural language
- Ask follow-up questions
- Request clarification when needed
