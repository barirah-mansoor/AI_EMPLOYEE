#!/bin/bash
echo "🧪 Silver Tier Validation Suite"
echo "=================================="

cd ~/AI_Employee_Vault

# Test 1: Directory structure
echo "📁 Testing directory structure..."
REQUIRED_DIRS=(
    "Silver_Tier/Gmail"
    "Silver_Tier/Automation"
    "Silver_Tier/Analytics"
    "Silver_Tier/Credentials"
    ".vscode"
)

for dir in "${REQUIRED_DIRS[@]}"; do
    if [ -d "$dir" ]; then
        echo "  ✅ $dir"
    else
        echo "  ❌ $dir MISSING"
    fi
done

# Test 2: Required files
echo "📄 Testing required files..."
REQUIRED_FILES=(
    "Silver_Tier/gmail_authenticator.py"
    "Silver_Tier/gmail_processor.py"
    "Silver_Tier/start_scheduler.sh"
    "Skills/process_gmail.md"
    "Skills/silver_briefing.md"
    "AI_Employee.code-workspace"
)

for file in "${REQUIRED_FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "  ✅ $file"
    else
        echo "  ❌ $file MISSING"
    fi
done

# Test 3: Python dependencies
echo "🐍 Testing Python dependencies..."
python3 -c "
import sys
modules = ['google.auth', 'googleapiclient', 'schedule', 'pandas', 'requests']
for module in modules:
    try:
        __import__(module)
        print(f'  ✅ {module}')
    except ImportError:
        print(f'  ❌ {module} MISSING')
"

# Test 4: Executable permissions
echo "⚡ Testing executable permissions..."
EXECUTABLES=(
    "Silver_Tier/gmail_authenticator.py"
    "Silver_Tier/gmail_processor.py"
    "Silver_Tier/start_scheduler.sh"
    "Silver_Tier/stop_scheduler.sh"
)

for file in "${EXECUTABLES[@]}"; do
    if [ -x "$file" ]; then
        echo "  ✅ $file executable"
    else
        echo "  ❌ $file not executable"
    fi
done

echo "=================================="
echo "🎯 Silver Tier validation complete!"
echo ""
echo "Next steps:"
echo "1. Set up Gmail API credentials"
echo "2. Run: bash run_ai_employee.sh process_gmail"
echo "3. Run: bash run_ai_employee.sh start_scheduler"
