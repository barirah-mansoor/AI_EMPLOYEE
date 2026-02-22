#!/bin/bash
# AI Employee Runner Script - Bronze & Silver Tier
# Usage: bash run_ai_employee.sh [command]

VAULT="$HOME/AI_Employee_Vault"
cd "$VAULT"

# Source any environment variables
if [ -f ".env" ]; then
    source .env
fi

# Function to run a skill
run_skill() {
    local skill_name="$1"
    local skill_file="Skills/${skill_name}.md"
    local log_file="Logs/${skill_name}.log"

    if [ -f "$skill_file" ]; then
        echo "📋 Running skill: $skill_name"
        echo "📖 Executing: $skill_file"
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        
        # Actually execute the skill with Claude
        claude -p "$skill_file" 2>&1 | tee -a "$log_file"
        
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo "✅ Skill '$skill_name' completed"
        echo "📝 Log saved to: $log_file"
    else
        echo "❌ Skill not found: $skill_file"
        exit 1
    fi
}

# Main command handler
case "$1" in
    "start")
        echo "🚀 Starting AI Employee..."
        bash start.sh
        ;;
    "process_inbox")
        echo "📥 Processing inbox..."
        python3 Silver_Tier/silver_process_inbox.py
        ;;
    "daily_briefing")
        echo "📊 Generating daily briefing..."
        python3 Silver_Tier/silver_briefing.py
        ;;
    "vault_health")
        echo "🔍 Checking vault health..."
        run_skill "vault_health"
        ;;
    "audit_week")
        echo "📈 Running weekly audit..."
        run_skill "audit_week"
        ;;

    # Silver Tier Commands
    "process_gmail")
        echo "📧 Processing Gmail..."
        python3 Silver_Tier/silver_process_gmail.py
        ;;
    "process_emails")
        echo "📤 Processing email tasks..."
        python3 Silver_Tier/silver_process_emails.py
        ;;
    "send_emails")
        echo "📤 Sending approved emails..."
        python3 Silver_Tier/silver_send_emails.py 2>/dev/null || echo "⚠️  send_emails not implemented yet"
        ;;
    "silver_briefing")
        echo "🥈 Generating Silver Tier briefing..."
        python3 Silver_Tier/silver_briefing.py
        ;;
    "system_monitor")
        echo "🔍 Running system health check..."
        python3 Silver_Tier/silver_system_monitor.py
        ;;
    "start_scheduler")
        bash Silver_Tier/start_scheduler.sh
        ;;
    "stop_scheduler")
        bash Silver_Tier/stop_scheduler.sh
        ;;

    *)
        echo "🤖 AI Employee Runner"
        echo "====================="
        echo ""
        echo "Usage: bash run_ai_employee.sh [command]"
        echo ""
        echo "Bronze Tier Commands:"
        echo "  start           - Start the AI Employee (file watcher)"
        echo "  process_inbox  - Triage Needs_Action folder"
        echo "  daily_briefing - Generate daily summary"
        echo "  vault_health   - Audit all folders"
        echo "  audit_week     - Weekly summary report"
        echo ""
        echo "Silver Tier Commands:"
        echo "  process_gmail    - Sync Gmail, create EMAIL_ files in Needs_Action"
        echo "  process_emails   - Categorize EMAIL_ files, archive to Done"
        echo "  send_emails     - Send approved email responses"
        echo "  silver_briefing - Enhanced daily briefing with email/calendar data"
        echo "  system_monitor  - Check Silver Tier system health and performance"
        echo "  start_scheduler - Start automated task scheduler service"
        echo "  stop_scheduler  - Stop automated task scheduler service"
        echo ""
        echo "Examples:"
        echo "  bash run_ai_employee.sh start"
        echo "  bash run_ai_employee.sh process_gmail"
        echo "  bash run_ai_employee.sh daily_briefing"
        ;;
esac