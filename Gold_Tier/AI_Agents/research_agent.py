#!/usr/bin/env python3
"""
Research Agent - Deep research and knowledge base management
"""

import os
import json
import re
import yaml
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional

# Import base agent
import sys
sys.path.insert(0, str(Path(__file__).parent))
from base_agent import BaseAgent

# Try to import ChromaDB
try:
    import chromadb
    from chromadb.config import Settings
    CHROMADB_AVAILABLE = True
except ImportError:
    CHROMADB_AVAILABLE = False


class ResearchAgent(BaseAgent):
    """AI-powered research agent with knowledge base integration."""

    def __init__(self):
        super().__init__("research_agent")
        self.agent_config = self._load_agent_config()
        self.chroma_client = self._setup_chroma()

    def _load_agent_config(self) -> Dict[str, Any]:
        """Load agent-specific configuration."""
        config_path = self.vault_path / "Gold_Tier" / "Configs" / "agents_config.yaml"
        if config_path.exists():
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
                return config.get("agents", {}).get("research_agent", {})
        return {"enabled": True, "max_sources": 10}

    def _setup_chroma(self):
        """Set up ChromaDB client."""
        if not CHROMADB_AVAILABLE:
            self.logger.warning("ChromaDB not available")
            return None

        db_path = self.vault_path / "Gold_Tier" / "Knowledge_Base" / "vector_db"
        db_path.mkdir(parents=True, exist_ok=True)

        try:
            return chromadb.PersistentClient(path=str(db_path))
        except Exception as e:
            self.logger.error(f"ChromaDB setup failed: {e}")
            return None

    def web_search(self, query: str, num_results: int = 5) -> List[Dict[str, str]]:
        """Perform web search (simulated - replace with actual API)."""
        # Note: This is a placeholder. In production, integrate with:
        # - SerperAPI, Tavily, or similar search APIs
        # - WebFetch tool for actual content retrieval

        prompt = f"""Based on your knowledge, provide {num_results} relevant research results for:

Query: {query}

Return JSON array of results:
[
    {{
        "title": "Result title",
        "summary": "Brief summary of key information",
        "source": "Likely source type (e.g., academic, news, official)",
        "relevance": "How this relates to the query",
        "key_facts": ["fact1", "fact2"]
    }}
]"""

        response = self.call_claude(prompt, system="You are a research assistant. Return only valid JSON.")

        try:
            json_match = re.search(r'\[[\s\S]*\]', response)
            if json_match:
                return json.loads(json_match.group())
            return json.loads(response)
        except json.JSONDecodeError:
            return []

    def analyze_sources(self, sources: List[Dict[str, str]]) -> Dict[str, Any]:
        """Analyze credibility and quality of sources."""
        prompt = f"""Analyze these research sources for credibility and quality.

Sources:
{json.dumps(sources, indent=2)}

Return JSON:
{{
    "overall_credibility": "high|medium|low",
    "source_ratings": [
        {{
            "source": "source title",
            "credibility_score": 0.0-1.0,
            "bias": "neutral|biased|unknown",
            "reliability": "high|medium|low"
        }}
    ],
    "recommendations": "Advice on using these sources"
}}"""

        response = self.call_claude(prompt, system="You are a source analysis expert. Return only valid JSON.")

        try:
            json_match = re.search(r'\{[\s\S]*\}', response)
            if json_match:
                return json.loads(json_match.group())
            return json.loads(response)
        except json.JSONDecodeError:
            return {"overall_credibility": "unknown", "error": "Failed to analyze"}

    def synthesize_research(self, query: str, sources: List[Dict[str, str]],
                           analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Synthesize research into comprehensive summary."""
        prompt = f"""Synthesize research findings into a comprehensive summary.

Original Query: {query}

Sources:
{json.dumps(sources, indent=2)}

Source Analysis:
{json.dumps(analysis, indent=2)}

Return JSON:
{{
    "summary": "Executive summary of findings",
    "key_findings": ["finding1", "finding2", "finding3"],
    "detailed_analysis": "In-depth analysis with citations",
    "gaps": "What information is still missing",
    "recommendations": ["recommendation1", "recommendation2"],
    "further_research": "Suggested areas for deeper investigation"
}}"""

        response = self.call_claude(prompt, system="You are a research synthesis expert. Return only valid JSON.")

        try:
            json_match = re.search(r'\{[\s\S]*\}', response)
            if json_match:
                result = json.loads(json_match.group())
            else:
                result = json.loads(response)
        except json.JSONDecodeError:
            result = {
                "summary": "Failed to synthesize research",
                "key_findings": [],
                "error": "JSON parsing failed"
            }

        result["query"] = query
        result["sources_count"] = len(sources)
        result["synthesized_at"] = datetime.now().isoformat()
        return result

    def save_to_knowledge_base(self, research: Dict[str, Any],
                               doc_id: str = None) -> bool:
        """Save research to knowledge base."""
        if self.chroma_client is None:
            # Save to file instead
            return self._save_to_file(research, doc_id)

        try:
            collection = self.chroma_client.get_or_create_collection("knowledge")

            doc_id = doc_id or f"research_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            content = json.dumps(research, default=str)

            collection.add(
                documents=[content],
                metadatas=[{"type": "research", "query": research.get("query", "")}],
                ids=[doc_id]
            )

            self.logger.info(f"Saved research to knowledge base: {doc_id}")
            return True

        except Exception as e:
            self.logger.error(f"Failed to save to knowledge base: {e}")
            return self._save_to_file(research, doc_id)

    def _save_to_file(self, research: Dict[str, Any], doc_id: str = None) -> bool:
        """Fallback: Save research to file."""
        docs_dir = self.vault_path / "Gold_Tier" / "Knowledge_Base" / "documents"
        docs_dir.mkdir(parents=True, exist_ok=True)

        doc_id = doc_id or f"research_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        file_path = docs_dir / f"{doc_id}.json"

        with open(file_path, 'w') as f:
            json.dump(research, f, indent=2, default=str)

        self.logger.info(f"Saved research to file: {file_path}")
        return True

    def execute(self, action: str = "research", query: str = None,
                **kwargs) -> Dict[str, Any]:
        """Main execution method."""
        if action == "research":
            if not query:
                return {"status": "error", "message": "Query required for research"}

            # Perform research pipeline
            num_sources = kwargs.get("num_sources", self.agent_config.get("max_sources", 5))

            sources = self.web_search(query, num_sources)
            analysis = self.analyze_sources(sources)
            synthesis = self.synthesize_research(query, sources, analysis)

            # Save to knowledge base
            self.save_to_knowledge_base(synthesis)

            # Log action
            self.log_action("deep_research", {
                "query": query,
                "sources_found": len(sources),
                "credibility": analysis.get("overall_credibility")
            })

            # Save output
            self.save_output(synthesis, f"research_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                           "workflow_logs")

            return {
                "status": "success",
                "query": query,
                "sources": sources,
                "analysis": analysis,
                "synthesis": synthesis,
                "timestamp": datetime.now().isoformat()
            }

        elif action == "search":
            return {
                "status": "success",
                "results": self.web_search(kwargs.get("query", ""), kwargs.get("num_results", 5))
            }

        else:
            return {"status": "error", "message": f"Unknown action: {action}"}


if __name__ == "__main__":
    import yaml  # Ensure yaml is imported

    agent = ResearchAgent()

    # Run research with provided query or default
    query = sys.argv[1] if len(sys.argv) > 1 else "AI trends 2026"
    result = agent.execute("research", query=query)

    print(json.dumps(result, indent=2, default=str))
