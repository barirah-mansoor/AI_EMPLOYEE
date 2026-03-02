#!/bin/bash
# Gold Tier Setup Script
# Installs dependencies and initializes Gold Tier system

echo "🥇 Setting up Gold Tier..."

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip3 install --quiet anthropic langchain chromadb sentence-transformers \
    schedule redis pyyaml matplotlib pandas numpy 2>/dev/null || \
    pip install --quiet anthropic langchain chromadb sentence-transformers \
    schedule redis pyyaml matplotlib pandas numpy

# Install system dependencies (may require sudo)
echo "📦 Installing system dependencies..."
sudo apt-get update -qq 2>/dev/null
sudo apt-get install -y -qq redis-server sqlite3 2>/dev/null || echo "Note: System packages may need manual install"

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p Gold_Tier/Logs/{agent_logs,workflow_logs,audit_logs}
mkdir -p Gold_Tier/Knowledge_Base/{vector_db,documents,embeddings,summaries}
mkdir -p Gold_Tier/Analytics/Reports/{Daily,Weekly,Monthly}

# Initialize vector database
echo "🗄️ Initializing vector database..."
python3 -c "
import chromadb
from chromadb.config import Settings
client = chromadb.PersistentClient(path='Gold_Tier/Knowledge_Base/vector_db')
client.get_or_create_collection('knowledge')
print('Vector database initialized')
" 2>/dev/null || echo "Vector DB will be initialized on first use"

# Test imports
echo "🧪 Testing imports..."
python3 -c "
import anthropic
import yaml
import schedule
print('All imports successful')
"

echo "✅ Gold Tier setup complete!"
echo ""
echo "Available commands:"
echo "  bash run_ai_employee.sh email_intelligence"
echo "  bash run_ai_employee.sh deep_research"
echo "  bash run_ai_employee.sh task_optimizer"
echo "  bash run_ai_employee.sh gold_briefing"
echo "  bash run_ai_employee.sh start_gold"
echo "  bash run_ai_employee.sh test_gold"
