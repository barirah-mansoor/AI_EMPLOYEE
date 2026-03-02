# Deep Research Skill

**Mode:** AUTO-EXECUTE
**Trigger:** Manual with query parameter
**Agent:** research_agent.py

## Purpose
Conduct comprehensive research on any topic with multi-source analysis, credibility assessment, and knowledge base storage.

## Execution

```bash
# Default research
python3 Gold_Tier/AI_Agents/research_agent.py "your research query"

# Or with specific parameters
python3 -c "from Gold_Tier.AI_Agents.research_agent import ResearchAgent; agent = ResearchAgent(); agent.execute('research', query='AI trends 2026')"
```

## Capabilities

1. **Web Search**
   - Multi-source search (simulated, can integrate APIs)
   - Configurable result count
   - Relevance ranking

2. **Source Analysis**
   - Credibility scoring
   - Bias detection
   - Reliability assessment

3. **Research Synthesis**
   - Executive summary generation
   - Key findings extraction
   - Gap identification
   - Further research suggestions

4. **Knowledge Base Storage**
   - ChromaDB vector storage (when available)
   - JSON file fallback
   - Metadata preservation

## Output Files

- `Gold_Tier/Knowledge_Base/documents/*.json` - Research documents
- `Gold_Tier/Knowledge_Base/vector_db/` - Vector embeddings
- `Gold_Tier/Logs/workflow_logs/research_*.json` - Research results

## Configuration

Settings in `Gold_Tier/Configs/agents_config.yaml`:
- `max_sources`: Maximum sources to analyze
- `enabled`: Enable/disable agent

## Example Usage

```bash
# Research a topic
bash run_ai_employee.sh deep_research "market trends in AI automation"

# Results stored in Knowledge Base
ls Gold_Tier/Knowledge_Base/documents/
```

## Integration

Works with:
- Task Optimizer (provides context)
- Meeting Agent (attendee research)
- Knowledge Base (vector storage)
