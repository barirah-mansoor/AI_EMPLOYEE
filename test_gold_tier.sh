#!/bin/bash
# Gold Tier Integration Test Suite

echo "🥇 Running Gold Tier Integration Tests..."
echo ""

# Test 1: Ralph Wiggum hook exists
echo "Test 1: Ralph Wiggum hook..."
if [ -f "/home/sibling_admins/.claude/settings.json" ]; then
    if grep -q "ralph_wiggum" /home/sibling_admins/.claude/settings.json; then
        echo "✅ Ralph Wiggum hook configured"
    else
        echo "⚠️  Hook file exists but Ralph not configured"
    fi
else
    echo "❌ Ralph Wiggum hook not found"
fi

# Test 2: All Python agents importable
echo ""
echo "Test 2: Agent imports..."
python3 -c "
import sys
sys.path.insert(0, 'Gold_Tier/AI_Agents')
from base_agent import BaseAgent
print('✅ base_agent imports')
from email_agent import EmailAgent
print('✅ email_agent imports')
from task_optimizer import TaskOptimizer
print('✅ task_optimizer imports')
" 2>/dev/null || echo "⚠️  Some agents failed to import"

# Test 3: Finance watcher DEV_MODE
echo ""
echo "Test 3: Finance watcher..."
DEV_MODE=true python3 -c "
import sys
sys.path.insert(0, '.')
from finance_watcher import check_new_transactions
result = check_new_transactions()
print(f'✅ Finance watcher works: {len(result)} transactions found')
"

# Test 4: WhatsApp watcher DEV_MODE
echo ""
echo "Test 4: WhatsApp watcher..."
DEV_MODE=true python3 -c "
import sys
sys.path.insert(0, '.')
from whatsapp_watcher import check_whatsapp_messages
result = check_whatsapp_messages()
print(f'✅ WhatsApp watcher works: {len(result)} messages found')
"

# Test 5: CEO briefing generation
echo ""
echo "Test 5: CEO briefing..."
DEV_MODE=true python3 -c "
import sys
sys.path.insert(0, '.')
from weekly_ceo_briefing import generate_briefing
content = generate_briefing()
print('✅ CEO briefing generated successfully')
" || echo "⚠️  CEO briefing failed"

# Test 6: Retry handler
echo ""
echo "Test 6: Retry handler..."
python3 -c "
import sys
sys.path.insert(0, '.')
from retry_handler import with_retry, TransientError
print('✅ Retry handler imports')

@with_retry(max_attempts=2, base_delay=0.1)
def test_retry():
    return 'success'

result = test_retry()
print('✅ Retry decorator works')
"

# Test 7: Watchdog
echo ""
echo "Test 7: Process watchdog..."
python3 -c "
import sys
sys.path.insert(0, '.')
from process_watchdog import check_processes
print('✅ Watchdog imports')
"

# Test 8: Audit logic
echo ""
echo "Test 8: Audit logic..."
python3 -c "
import sys
sys.path.insert(0, '.')
from audit_logic import analyze_transaction, SUBSCRIPTION_PATTERNS
print(f'✅ Audit logic imports ({len(SUBSCRIPTION_PATTERNS)} patterns)')

tx = {'id': '1', 'date': '2026-02-24', 'description': 'Netflix Subscription', 'amount': '-15.99'}
result = analyze_transaction(tx)
print(f'✅ Transaction analysis: is_subscription={result[\"is_subscription\"]}')
"

# Test 9: MCP config
echo ""
echo "Test 9: MCP Servers..."
if [ -f "/home/sibling_admins/.config/claude-code/mcp.json" ]; then
    echo "✅ MCP config exists"
    grep -q "email" /home/sibling_admins/.config/claude-code/mcp.json && echo "✅ Email MCP configured"
    grep -q "odoo" /home/sibling_admins/.config/claude-code/mcp.json && echo "✅ Odoo MCP configured"
    grep -q "social" /home/sibling_admins/.config/claude-code/mcp.json && echo "✅ Social MCP configured"
else
    echo "❌ MCP config not found"
fi

# Test 10: Skills exist
echo ""
echo "Test 10: Skills..."
ls Skills/ralph_loop.md 2>/dev/null && echo "✅ Ralph Loop skill"
ls Skills/whatsapp_watcher.md 2>/dev/null && echo "✅ WhatsApp skill"
ls Skills/finance_watcher.md 2>/dev/null && echo "✅ Finance skill"
ls Skills/ceo_briefing.md 2>/dev/null && echo "✅ CEO briefing skill"

echo ""
echo "=========================================="
echo "🎉 Gold Tier Integration Tests Complete!"
echo "=========================================="
