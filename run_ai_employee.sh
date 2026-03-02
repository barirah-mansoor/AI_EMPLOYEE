#!/bin/bash
# AI Employee Runner Script - Bronze, Silver & Gold Tier
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
    "whatsapp_watcher")
        echo "📱 Starting WhatsApp Watcher..."
        python3 whatsapp_watcher.py
        ;;
    "whatsapp_once")
        echo "📱 Running WhatsApp Watcher once..."
        python3 whatsapp_watcher.py --once
        ;;
    "finance_watcher")
        echo "💰 Starting Finance Watcher..."
        python3 finance_watcher.py
        ;;
    "finance_once")
        echo "💰 Running Finance Watcher once..."
        python3 finance_watcher.py --once
        ;;

    # Gold Tier Commands
    "email_intelligence")
        count="${2:-all}"
        echo "📧 Running Email Intelligence Agent (processing: $count emails)..."
        python3 Gold_Tier/AI_Agents/email_agent.py "$count"
        ;;
    "deep_research")
        echo "🔍 Running Deep Research Agent..."
        query="${2:-AI trends 2026}"
        python3 Gold_Tier/AI_Agents/research_agent.py "$query"
        ;;
    "meeting_maestro")
        echo "📅 Running Meeting Maestro Agent..."
        python3 Gold_Tier/AI_Agents/meeting_agent.py
        ;;
    "task_optimizer")
        echo "📊 Running Task Optimizer Agent..."
        python3 Gold_Tier/AI_Agents/task_optimizer.py
        ;;
    "gold_briefing")
        echo "🥇 Generating Gold Tier Briefing..."
        python3 Gold_Tier/AI_Agents/email_agent.py 2>/dev/null
        python3 Gold_Tier/AI_Agents/task_optimizer.py 2>/dev/null
        python3 -c "
import sys
sys.path.insert(0, 'Gold_Tier/Automation')
from orchestrator import GoldOrchestrator
orch = GoldOrchestrator()
result = orch._generate_briefing()
print('Briefing generated:', result.get('briefing_file', 'N/A'))
"
        ;;
    "weekly_briefing")
        echo "📊 Generating Weekly CEO Briefing..."
        python3 weekly_ceo_briefing.py
        ;;
    "start_gold")
        echo "🥇 Starting Gold Tier Orchestrator..."
        python3 Gold_Tier/Automation/orchestrator.py &
        echo "Gold Tier Orchestrator started in background"
        ;;
    "stop_gold")
        echo "🛑 Stopping Gold Tier Orchestrator..."
        pkill -f "orchestrator.py" 2>/dev/null || echo "No orchestrator process found"
        ;;
    "start_watchdog")
        echo "🐕 Starting Process Watchdog..."
        python3 process_watchdog.py &
        echo "Watchdog started in background"
        ;;
    "stop_watchdog")
        echo "🛑 Stopping Process Watchdog..."
        python3 process_watchdog.py --stop 2>/dev/null || pkill -f "process_watchdog.py" 2>/dev/null || echo "No watchdog process found"
        ;;
    "test_gold")
        echo "🧪 Testing Gold Tier Setup..."
        echo ""
        echo "Testing imports..."
        python3 -c "
import sys
sys.path.insert(0, 'Gold_Tier/AI_Agents')
from base_agent import BaseAgent
print('✅ base_agent imported')
try:
    from email_agent import EmailAgent
    print('✅ email_agent imported')
except Exception as e:
    print('⚠️  email_agent:', e)
try:
    from research_agent import ResearchAgent
    print('✅ research_agent imported')
except Exception as e:
    print('⚠️  research_agent:', e)
try:
    from meeting_agent import MeetingAgent
    print('✅ meeting_agent imported')
except Exception as e:
    print('⚠️  meeting_agent:', e)
try:
    from task_optimizer import TaskOptimizer
    print('✅ task_optimizer imported')
except Exception as e:
    print('⚠️  task_optimizer:', e)
"
        echo ""
        echo "Testing config files..."
        test -f Gold_Tier/Configs/gold_config.yaml && echo "✅ gold_config.yaml exists" || echo "❌ gold_config.yaml missing"
        test -f Gold_Tier/Configs/agents_config.yaml && echo "✅ agents_config.yaml exists" || echo "❌ agents_config.yaml missing"
        test -f Gold_Tier/Configs/workflows_config.yaml && echo "✅ workflows_config.yaml exists" || echo "❌ workflows_config.yaml missing"
        echo ""
        echo "Testing directories..."
        test -d Gold_Tier/AI_Agents && echo "✅ AI_Agents dir exists" || echo "❌ AI_Agents dir missing"
        test -d Gold_Tier/Knowledge_Base && echo "✅ Knowledge_Base dir exists" || echo "❌ Knowledge_Base dir missing"
        test -d Gold_Tier/Analytics/Reports/Daily && echo "✅ Analytics/Reports/Daily dir exists" || echo "❌ Analytics/Reports/Daily dir missing"
        echo ""
        echo "✅ Gold Tier test complete!"
        ;;

    # Platinum Tier Commands
    "multi_agent")
        echo "🤖 Running Multi-Agent Coordinator..."
        python3 Platinum_Tier/Multi_Agent_System/agent_coordinator.py
        ;;
    "predict")
        days="${2:-7}"
        echo "🔮 Running Predictive Analytics ($days-day forecast)..."
        python3 Platinum_Tier/Predictive/forecasting_engine.py
        ;;
    "slack_bot")
        echo "💬 Starting Slack Bot Integration..."
        python3 Platinum_Tier/Integrations/slack/slack_bot.py
        ;;
    "chat")
        echo "💬 Starting Natural Language Chat Interface..."
        python3 Platinum_Tier/NLP/command_processor.py
        ;;
    "executive_report")
        echo "📊 Generating Executive Analytics Report..."
        python3 Platinum_Tier/orchestrator.py report
        ;;
    "start_platinum")
        echo "💎 Starting Platinum Tier Orchestrator..."
        bash run_ai_employee.sh start_gold
        python3 Platinum_Tier/orchestrator.py start &
        echo "Platinum Tier started in background"
        ;;
    "stop_platinum")
        echo "🛑 Stopping Platinum Tier..."
        python3 Platinum_Tier/orchestrator.py stop 2>/dev/null
        pkill -f "Platinum_Tier/orchestrator" 2>/dev/null
        echo "Platinum Tier stopped"
        ;;
    "test_platinum")
        echo "💎 Testing Platinum Tier Setup..."
        echo ""
        echo "Testing imports..."
        python3 -c "
import sys
sys.path.insert(0, 'Platinum_Tier')
try:
    from Multi_Agent_System.agent_coordinator import AgentCoordinator
    print('✅ agent_coordinator imported')
except Exception as e:
    print('⚠️  agent_coordinator:', e)
try:
    from Predictive.forecasting_engine import PredictiveEngine
    print('✅ forecasting_engine imported')
except Exception as e:
    print('⚠️  forecasting_engine:', e)
try:
    from NLP.command_processor import NLPCommandProcessor
    print('✅ command_processor imported')
except Exception as e:
    print('⚠️  command_processor:', e)
try:
    from Learning.learning_system import LearningSystem
    print('✅ learning_system imported')
except Exception as e:
    print('⚠️  learning_system:', e)
"
        echo ""
        echo "Testing config files..."
        test -f Platinum_Tier/Configs/platinum_config.yaml && echo "✅ platinum_config.yaml exists" || echo "❌ platinum_config.yaml missing"
        test -f Platinum_Tier/Configs/agent_pool_config.yaml && echo "✅ agent_pool_config.yaml exists" || echo "❌ agent_pool_config.yaml missing"
        test -f Platinum_Tier/Configs/integrations_config.yaml && echo "✅ integrations_config.yaml exists" || echo "❌ integrations_config.yaml missing"
        echo ""
        echo "Testing directories..."
        test -d Platinum_Tier/Multi_Agent_System && echo "✅ Multi_Agent_System dir exists" || echo "❌ Multi_Agent_System dir missing"
        test -d Platinum_Tier/Predictive && echo "✅ Predictive dir exists" || echo "❌ Predictive dir missing"
        test -d Platinum_Tier/NLP && echo "✅ NLP dir exists" || echo "❌ NLP dir missing"
        test -d Platinum_Tier/Integrations && echo "✅ Integrations dir exists" || echo "❌ Integrations dir missing"
        test -d Platinum_Tier/Reports/Executive && echo "✅ Reports/Executive dir exists" || echo "❌ Reports/Executive dir missing"
        echo ""
        echo "✅ Platinum Tier test complete!"
        ;;
    "learning_report")
        echo "🧠 Generating Learning System Report..."
        python3 Platinum_Tier/Learning/learning_system.py
        ;;

    *)
        echo "🤖 AI Employee Runner"
        echo "====================="
        echo ""
        echo "Usage: bash run_ai_employee.sh [command]"
        echo ""
        echo "Bronze Tier Commands:"
        echo "  start           - Start the AI Employee (file watcher)"
        echo "  process_inbox   - Triage Needs_Action folder"
        echo "  daily_briefing  - Generate daily summary"
        echo "  vault_health    - Audit all folders"
        echo "  audit_week      - Weekly summary report"
        echo ""
        echo "Silver Tier Commands:"
        echo "  process_gmail    - Sync Gmail, create EMAIL_ files in Needs_Action"
        echo "  process_emails   - Categorize EMAIL_ files, archive to Done"
        echo "  send_emails      - Send approved email responses"
        echo "  silver_briefing  - Enhanced daily briefing with email/calendar data"
        echo "  system_monitor   - Check Silver Tier system health and performance"
        echo "  start_scheduler  - Start automated task scheduler service"
        echo "  stop_scheduler   - Stop automated task scheduler service"
        echo ""
        echo "Gold Tier Commands:"
        echo "  email_intelligence [count] - AI email analysis (count: number or 'all')"
        echo "  deep_research [query]      - Multi-source research with knowledge base"
        echo "  meeting_maestro            - Automated meeting preparation and follow-up"
        echo "  task_optimizer             - Eisenhower Matrix prioritization and scheduling"
        echo "  gold_briefing              - Comprehensive morning intelligence briefing"
        echo "  start_gold                 - Start Gold Tier Orchestrator (automated workflows)"
        echo "  stop_gold                  - Stop Gold Tier Orchestrator"
        echo "  test_gold                  - Test Gold Tier setup and imports"
        echo ""
        echo "Platinum Tier Commands:"
        echo "  multi_agent           - Multi-agent coordination and delegation"
        echo "  predict [days]        - Predictive analytics and workload forecast"
        echo "  slack_bot             - Start Slack integration bot"
        echo "  chat                  - Natural language command interface"
        echo "  executive_report      - Generate executive analytics report"
        echo "  start_platinum        - Start Platinum Tier Orchestrator"
        echo "  stop_platinum         - Stop Platinum Tier"
        echo "  test_platinum         - Test Platinum Tier setup"
        echo "  learning_report       - Generate learning system report"
        echo ""
        echo "Examples:"
        echo "  bash run_ai_employee.sh start"
        echo "  bash run_ai_employee.sh process_gmail"
        echo "  bash run_ai_employee.sh email_intelligence 10    # Process 10 emails"
        echo "  bash run_ai_employee.sh email_intelligence all   # Process all emails"
        echo "  bash run_ai_employee.sh gold_briefing"
        echo "  bash run_ai_employee.sh deep_research 'market trends'"
        ;;
esac
