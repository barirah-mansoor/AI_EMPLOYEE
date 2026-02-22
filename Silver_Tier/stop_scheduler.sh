#!/bin/bash
# Stop AI Employee Scheduler

VAULT="$HOME/AI_Employee_Vault"

if [ -f "$VAULT/.scheduler.pid" ]; then
    PID=$(cat "$VAULT/.scheduler.pid")
    if kill -0 "$PID" 2>/dev/null; then
        echo "⏹️  Stopping AI Employee Scheduler (PID: $PID)"
        kill "$PID"

        # Wait for graceful shutdown
        for i in {1..10}; do
            if ! kill -0 "$PID" 2>/dev/null; then
                echo "✅ Scheduler stopped gracefully"
                rm -f "$VAULT/.scheduler.pid"
                exit 0
            fi
            sleep 1
        done

        # Force kill if still running
        echo "⚠️  Force killing scheduler..."
        kill -9 "$PID" 2>/dev/null
        rm -f "$VAULT/.scheduler.pid"
        echo "✅ Scheduler force stopped"
    else
        echo "⚠️  Scheduler not running (stale PID file)"
        rm -f "$VAULT/.scheduler.pid"
    fi
else
    echo "❌ Scheduler PID file not found - not running?"
fi
