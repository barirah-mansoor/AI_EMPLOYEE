# AI Employee Vault - Your Personal AI Assistant

Welcome! This is your **Personal AI Employee** system that works for you 24/7. It's designed to handle tasks, manage files, and keep you informed — all through simple file-based interactions. This guide will help you understand how it works and get it running on your system.

## What Does It Do?

Your AI Employee is like having a helpful assistant that:
- **Monitors your inbox** - Automatically detects when you add files to the system
- **Processes tasks** - Reads your files and creates action plans
- **Manages your workflow** - Sorts tasks by priority and handles follow-ups
- **Keeps you informed** - Creates daily summaries and logs everything
- **Asks for approval** - For important decisions, it checks with you first

---

## Quick Setup Guide

### 1. Prerequisites
Before starting, make sure you have:
- **Python 3.8 or higher** (check with `python --version`)
- **Claude Code CLI** installed (install with `npm install -g @anthropic/claude-code`)
- **Git** (if you're cloning the repository)

### 2. Installation Steps

1. **Open your terminal** (command prompt on Windows, Terminal on Mac/Linux)

2. **Navigate to your AI Employee folder** (usually `~/AI_Employee_Vault`)

3. **Install required packages:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Start your AI Employee:**
   ```bash
   bash start.sh
   ```

   You should see something like:
   ```
   🤖 AI Employee — Filesystem Watcher
   ==================================
   Vault Path : /home/username/AI_Employee_Vault
   Watching   : /home/username/AI_Employee_Vault/Inbox
   Started    : 2026-02-18 14:30:00 UTC
   ==================================
   Drop files into Inbox/ to trigger processing.
   Press Ctrl+C to stop.
   ```

5. **Your AI Employee is now running!** It's watching the `Inbox` folder for new files.

---

## How to Use It - Step by Step

### Step 1: Give Your AI a Task
Simply put a file in the `Inbox` folder:
```bash
# Create a simple task
echo "Please organize my weekly schedule" > ~/AI_Employee_Vault/Inbox/my_task.txt
```

### Step 2: Let the AI Process It
The system automatically:
- Moves your file to the `Needs_Action` folder
- Creates a plan in the `Plans` folder
- Updates the dashboard with current status

### Step 3: Check Your Dashboard
Open `Dashboard.md` to see what's happening:
```bash
cat ~/AI_Employee_Vault/Dashboard.md
```

### Step 4: Review and Approve (if needed)
- If a task needs your approval, check the `Pending_Approval` folder
- If everything looks good, move the file to `Approved` folder
- Completed tasks go to the `Done` folder

---

## Your AI Employee's Folder Structure

Here's what each folder does:

| Folder | What It Does | Example |
|--------|--------------|---------|
| `Inbox` | Drop files here to give tasks to your AI | "schedule_meeting.txt" |
| `Needs_Action` | Files waiting for AI to review | Your file gets copied here automatically |
| `Plans` | AI creates action plans here | "PLAN_schedule_meeting.md" |
| `Pending_Approval` | Important tasks needing your approval | Payment requests |
| `Approved` | You've approved these, AI will act on them | After you review them |
| `Done` | Completed tasks (archived) | Finished work |
| `Logs` | Daily records of all actions | "2026-02-18.json" |
| `Briefings` | Daily summaries from your AI | "Briefing_2026-02-18.md" |
| `Skills` | AI's capabilities and instructions | How your AI knows what to do |

---

## How to Give Tasks to Your AI

### Method 1: Simple Text Files
Create a text file with your request:
```bash
echo "Please review the quarterly report and summarize the key points" > ~/AI_Employee_Vault/Inbox/review_report.txt
```

### Method 2: Other File Types
You can also drop other files:
- PDFs, Word documents, spreadsheets
- Images with written instructions
- Email files (.eml, .msg)

### Method 3: Using the System Commands
Once your AI Employee is running, you can use these commands:
```bash
# Get a daily summary
bash run_ai_employee.sh daily_briefing

# Process any waiting tasks
bash run_ai_employee.sh process_inbox

# Check overall health of the system
bash run_ai_employee.sh vault_health
```

---

## Understanding Priorities

Your AI sorts tasks into different priority levels:

- 🔴 **URGENT** (Red) - Emergency issues, security alerts, immediate deadlines
- 🟡 **HIGH** (Yellow) - Important deadlines, client communications
- 🟢 **NORMAL** (Green) - Regular tasks, general organization
- ⚪ **LOW** (White) - Archiving, scheduling, non-urgent tasks

---

## Silver Tier Features (Advanced)

This system has additional capabilities for power users:

| Feature | What It Does |
|---------|--------------|
| `process_gmail` | Automatically processes your emails |
| `send_emails` | Sends pre-approved email responses |
| `system_monitor` | Checks system health and performance |
| `silver_briefing` | Enhanced daily summaries with email data |
| `start_scheduler` | Automated task scheduling |

To use these features, you'll need to run additional setup as mentioned in the Silver Tier documentation.

---

## Safety & Security

Your AI Employee follows strict rules:
- **Everything is logged** - Every action is recorded in your Logs folder
- **Financial actions require approval** - Your AI never makes purchases
- **No deletion without permission** - Files are moved, not deleted
- **Communication approval needed** - Your AI won't send emails without your OK

---

## Troubleshooting

### Common Issues

**"Command not found" error:**
- Make sure you're in the AI_Employee_Vault folder
- Check if Python and Claude Code are properly installed

**AI Employee won't start:**
- Verify you have Python 3.8+ installed
- Run `pip install -r requirements.txt` again
- Make sure your terminal is in the correct directory

**File isn't being processed:**
- Check if the filesystem watcher is running
- Ensure the file was placed in the `Inbox` folder
- Look at `Dashboard.md` for status updates

### Restarting Your AI Employee
If the system stops working, simply stop it (Ctrl+C) and restart with:
```bash
bash start.sh
```

---

## Example Workflow

Let's say you want your AI to help organize your week:

1. **Create a task:** Put "weekly_schedule.txt" in the Inbox folder
2. **Automatic processing:** The AI detects your file and moves it to Needs_Action
3. **Plan creation:** The AI creates a plan in the Plans folder
4. **Dashboard update:** Your Dashboard shows the current status
5. **Review & approval:** If needed, you review and approve the plan in Pending_Approval
6. **Task completion:** The AI executes the plan, and moves completed tasks to Done

---

## Daily Use Tips

- Check your `Dashboard.md` each morning to see pending tasks
- Look at `Briefings/` for daily summaries from your AI
- Use `Logs/` to review what your AI employee has done
- Place new tasks in the `Inbox` folder anytime
- For sensitive tasks, check `Pending_Approval` before they're processed

---

## Getting Help

- Check `CLAUDE.md` for detailed system instructions
- Look at `Skills/` folder to see what your AI can do
- Review logged actions in `Logs/` for detailed records
- Your `Dashboard.md` shows real-time system status

---

## Next Steps

Once you're comfortable with the basic system, you can explore:
- Silver Tier features for advanced capabilities
- Email integration for automated communication
- Task scheduling for routine operations
- Custom skill creation for specialized tasks

---

*Your Personal AI Employee - Working for you 24/7*
