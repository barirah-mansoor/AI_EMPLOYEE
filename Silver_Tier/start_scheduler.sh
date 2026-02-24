#!/bin/bash
# Start AI Employee Scheduler as background service

VAULT="$HOME/AI_Employee_Vault"
cd "$VAULT"

echo "🚀 Starting AI Employee Scheduler..."

# Kill existing scheduler if running
if [ -f "$VAULT/.scheduler.pid" ]; then
    OLD_PID=$(cat "$VAULT/.scheduler.pid")
    if kill -0 "$OLD_PID" 2>/dev/null; then
        echo "⚠️  Stopping existing scheduler (PID: $OLD_PID)"
        kill "$OLD_PID"
        sleep 3
    fi
    rm -f "$VAULT/.scheduler.pid"
fi

# Ensure log directory exists
mkdir -p "$VAULT/Silver_Tier/Automation/Logs"

# Start new scheduler in background
nohup python3 Silver_Tier/Automation/scheduler.py \
    > Silver_Tier/Automation/Logs/scheduler_output.log 2>&1 &

SCHEDULER_PID=$!
echo $SCHEDULER_PID > "$VAULT/.scheduler.pid"

# Wait a moment to check if it started successfully
sleep 2
if kill -0 "$SCHEDULER_PID" 2>/dev/null; then
    echo "✅ Scheduler started successfully with PID: $SCHEDULER_PID"
    echo "📋 Log file: Silver_Tier/Automation/Logs/scheduler_output.log"
    echo "⏹️  To stop: bash Silver_Tier/stop_scheduler.sh"
else
    echo "❌ Scheduler failed to start"
    rm -f "$VAULT/.scheduler.pid"
    exit 1
fi
