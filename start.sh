#!/bin/bash
echo "🤖 Starting AI Employee..."
echo "================================"
cd ~/AI_Employee_Vault

# Start watcher in background
python3 filesystem_watcher.py &
WATCHER_PID=$!
echo "✅ Watcher started (PID: $WATCHER_PID)"
echo $WATCHER_PID > .watcher.pid

# Run initial vault health check
echo ""
echo "🔍 Running startup health check..."
python3 Silver_Tier/silver_system_monitor.py

echo ""
echo "================================"
echo "✅ AI Employee is RUNNING"
echo "📁 Vault: ~/AI_Employee_Vault"
echo "👁️  Watching: ~/AI_Employee_Vault/Inbox"
echo ""
echo "Drop files into ~/AI_Employee_Vault/Inbox to trigger processing"
echo "Run 'claude' in this folder to interact with your AI Employee"
echo "================================"
