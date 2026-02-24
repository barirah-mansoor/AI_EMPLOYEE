#!/usr/bin/env python3
"""
Base Agent - Foundation class for all Gold Tier AI agents
Uses OpenRouter API with OpenAI-compatible interface
"""
from __future__ import annotations

import os
import json
import yaml
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any

# Try to import openai for OpenRouter compatibility
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False


class BaseAgent:
    """Foundation class for Gold Tier AI agents using OpenRouter API."""

    # OpenRouter configuration
    OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
    DEFAULT_MODEL = "arcee-ai/trinity-large-preview:free"

    def __init__(self, agent_name: str, config_path: Optional[str] = None):
        self.agent_name = agent_name
        self.vault_path = Path(__file__).parent.parent.parent
        self.config = self.load_config(config_path)
        self.setup_logging()
        self.client = self.setup_openrouter_client()
        self.model = self._get_model()

    def _get_model(self) -> str:
        """Get the model name from config or use default."""
        return self.config.get("llm", {}).get("model", self.DEFAULT_MODEL)

    def load_config(self, config_path: Optional[str] = None) -> Dict[str, Any]:
        """Load configuration from YAML file."""
        if config_path is None:
            config_path = self.vault_path / "Gold_Tier" / "Configs" / "gold_config.yaml"

        config_path = Path(config_path)
        if config_path.exists():
            with open(config_path, 'r') as f:
                return yaml.safe_load(f) or {}
        return {"version": "1.0.0", "agents": {}}

    def setup_logging(self) -> logging.Logger:
        """Set up logging for the agent."""
        log_dir = self.vault_path / "Gold_Tier" / "Logs" / "agent_logs"
        log_dir.mkdir(parents=True, exist_ok=True)

        self.logger = logging.getLogger(self.agent_name)
        self.logger.setLevel(logging.INFO)

        # Avoid duplicate handlers
        if not self.logger.handlers:
            log_file = log_dir / f"{self.agent_name}.log"
            handler = logging.FileHandler(log_file)
            handler.setFormatter(
                logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            )
            self.logger.addHandler(handler)

        return self.logger

    def setup_openrouter_client(self) -> Optional[OpenAI]:
        """Set up OpenRouter client using OpenAI-compatible API."""
        if not OPENAI_AVAILABLE:
            self.logger.warning("OpenAI library not available - install with: pip install openai")
            return None

        # Get API key from environment or .env file
        api_key = os.environ.get("OPENROUTER_API_KEY")
        if not api_key:
            # Try to load from .env file
            env_path = self.vault_path / ".env"
            if env_path.exists():
                with open(env_path, 'r') as f:
                    for line in f:
                        line = line.strip()
                        if line.startswith("OPENROUTER_API_KEY="):
                            api_key = line.split("=", 1)[1].strip().strip('"\'')
                            if api_key:
                                break

        if api_key:
            client = OpenAI(
                api_key=api_key,
                base_url=self.OPENROUTER_BASE_URL
            )
            self.logger.info(f"OpenRouter client initialized for {self.agent_name}")
            return client
        else:
            self.logger.warning("No OPENROUTER_API_KEY found in environment or .env file")
            return None

    def call_llm(self, prompt: str, system: str = "", model: str = None,
                 max_tokens: int = 4096, temperature: float = 0.7) -> str:
        """Call OpenRouter API (OpenAI-compatible) with the given prompt."""
        if self.client is None:
            return self._mock_response(prompt)

        model = model or self.model

        try:
            messages = []
            if system:
                messages.append({"role": "system", "content": system})
            messages.append({"role": "user", "content": prompt})

            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature
            )
            return response.choices[0].message.content
        except Exception as e:
            self.logger.error(f"OpenRouter API error: {e}")
            return self._handle_llm_failure(prompt, str(e))

    # Graceful Degradation Methods
    def _handle_llm_failure(self, prompt: str, error: str) -> str:
        """Handle LLM API failure with graceful degradation."""
        # If LLM unavailable, write task to deferred
        if "API" in error or "connection" in error.lower() or "timeout" in error.lower():
            self._defer_task(prompt, error)
            return json.dumps({
                "status": "deferred",
                "message": "LLM unavailable - task deferred for later",
                "error": error
            })
        return json.dumps({"error": error})

    def _defer_task(self, prompt: str, reason: str):
        """Write deferred task to Needs_Action for later processing."""
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        deferred_file = self.vault_path / "Needs_Action" / f"DEFERRED_{timestamp}.md"

        content = f"""---
type: deferred_task
reason: "{reason}"
original_prompt: "{prompt[:200]}..."
status: pending
created: "{datetime.now().isoformat()}"
---

# Deferred Task

**Reason:** {reason}

**Original Prompt:**
{prompt}

## Resolution Needed

- [ ] Retry when service is available
- [ ] Manually process if needed
"""
        deferred_file.parent.mkdir(parents=True, exist_ok=True)
        deferred_file.write_text(content)
        self.logger.warning(f"Task deferred to {deferred_file.name}")

    def _queue_email(self, email_data: dict):
        """Queue email for later sending when Gmail is unavailable."""
        from datetime import datetime
        outbox_file = self.vault_path / "Silver_Tier" / "Gmail" / ".outbox_queue.json"

        outbox_file.parent.mkdir(parents=True, exist_ok=True)

        # Load existing queue
        queue = []
        if outbox_file.exists():
            try:
                import json
                queue = json.loads(outbox_file.read_text())
            except:
                pass

        queue.append({
            **email_data,
            "queued_at": datetime.now().isoformat()
        })

        outbox_file.write_text(json.dumps(queue, indent=2))
        self.logger.warning(f"Email queued to outbox: {len(queue)} pending")

    def sync_deferred_tasks(self):
        """Sync deferred tasks when service becomes available."""
        deferred_dir = self.vault_path / "Needs_Action"
        if not deferred_dir.exists():
            return []

        synced = []
        for deferred_file in deferred_dir.glob("DEFERRED_*.md"):
            # Move back to processing
            content = deferred_file.read_text()
            # Process deferred task
            synced.append(deferred_file.name)
            # Remove deferred file
            deferred_file.unlink()

        return synced

    # Alias for backward compatibility
    def call_claude(self, prompt: str, system: str = "", model: str = None,
                    max_tokens: int = 4096) -> str:
        """Alias for call_llm - backward compatibility."""
        return self.call_llm(prompt, system, model, max_tokens)

    def _mock_response(self, prompt: str) -> str:
        """Generate mock response when API is unavailable."""
        return json.dumps({
            "status": "mock",
            "message": "OpenRouter API unavailable - check OPENROUTER_API_KEY in .env",
            "prompt_preview": prompt[:200]
        })

    def save_output(self, data: Dict[str, Any], filename: str,
                    subdir: str = "agent_logs") -> Path:
        """Save output to a file."""
        output_dir = self.vault_path / "Gold_Tier" / "Logs" / subdir
        output_dir.mkdir(parents=True, exist_ok=True)

        output_path = output_dir / filename
        with open(output_path, 'w') as f:
            json.dump(data, f, indent=2, default=str)

        self.logger.info(f"Output saved to {output_path}")
        return output_path

    def log_action(self, action: str, details: Dict[str, Any] = None) -> None:
        """Log an action to the audit log."""
        log_dir = self.vault_path / "Gold_Tier" / "Logs" / "audit_logs"
        log_dir.mkdir(parents=True, exist_ok=True)

        today = datetime.now().strftime("%Y-%m-%d")
        log_file = log_dir / f"{today}.json"

        entry = {
            "timestamp": datetime.now().isoformat(),
            "agent": self.agent_name,
            "action": action,
            "details": details or {}
        }

        # Append to log file
        logs = []
        if log_file.exists():
            with open(log_file, 'r') as f:
                try:
                    logs = json.load(f)
                except json.JSONDecodeError:
                    logs = []

        logs.append(entry)
        with open(log_file, 'w') as f:
            json.dump(logs, f, indent=2, default=str)

        self.logger.info(f"Action logged: {action}")

    def execute(self, *args, **kwargs) -> Dict[str, Any]:
        """Main execution method - override in subclasses."""
        raise NotImplementedError("Subclasses must implement execute()")


if __name__ == "__main__":
    # Test the base agent
    agent = BaseAgent("test_agent")
    print(f"Agent: {agent.agent_name}")
    print(f"Config loaded: {bool(agent.config)}")
    print(f"OpenRouter client: {agent.client is not None}")
    print(f"Model: {agent.model}")
