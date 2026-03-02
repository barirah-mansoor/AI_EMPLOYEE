#!/usr/bin/env python3
"""
Platinum Orchestrator
Central hub that coordinates all Platinum Tier features
"""

import os
import sys
import json
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime
import time
import threading

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

try:
    import anthropic
    import yaml
    DEPENDENCIES_OK = True
except ImportError:
    DEPENDENCIES_OK = False


class PlatinumOrchestrator:
    """
    Central orchestrator for all Platinum Tier systems:
    - Multi-agent coordination
    - Predictive analytics
    - Natural language processing
    - Integration management
    """

    def __init__(self, vault_path: str = None):
        self.vault = Path(vault_path) if vault_path else Path("/mnt/c/Users/Admin/AI_Employee_Vault")
        self.config = self.load_config()
        self.client = anthropic.Anthropic() if DEPENDENCIES_OK else None

        # Initialize subsystems
        self.agent_coordinator = None
        self.predictive_engine = None
        self.nlp_processor = None

        # State
        self.running = False
        self.scheduler_thread = None

    def load_config(self) -> Dict:
        """Load configuration"""
        config_file = self.vault / "Platinum_Tier/Configs/platinum_config.yaml"
        if config_file.exists():
            try:
                import yaml
                with open(config_file) as f:
                    return yaml.safe_load(f)
            except:
                pass
        return {}

    def initialize(self) -> Dict:
        """Initialize all Platinum subsystems"""
        results = {
            'timestamp': datetime.now().isoformat(),
            'initialized': [],
            'failed': [],
            'warnings': []
        }

        # Initialize Multi-Agent Coordinator
        try:
            from Platinum_Tier.Multi_Agent_System.agent_coordinator import AgentCoordinator
            self.agent_coordinator = AgentCoordinator(str(self.vault))
            results['initialized'].append('multi_agent_coordinator')
        except Exception as e:
            results['failed'].append(f'multi_agent_coordinator: {str(e)}')

        # Initialize Predictive Engine
        try:
            import sys
            sys.path.insert(0, str(self.vault))
            from Platinum_Tier.Predictive.forecasting_engine import PredictiveEngine
            self.predictive_engine = PredictiveEngine(str(self.vault))
            results['initialized'].append('predictive_engine')
        except Exception as e:
            results['failed'].append(f'predictive_engine: {str(e)}')
            print(f"⚠️ Predictive engine failed to initialize: {e}")

        # Initialize NLP Processor
        try:
            from Platinum_Tier.NLP.command_processor import NLPCommandProcessor
            self.nlp_processor = NLPCommandProcessor(str(self.vault))
            results['initialized'].append('nlp_processor')
        except Exception as e:
            results['failed'].append(f'nlp_processor: {str(e)}')

        # Log initialization
        self.log_action('initialize', results)

        return results

    def start(self) -> Dict:
        """Start all Platinum services"""
        if self.running:
            return {'status': 'already_running'}

        print("💎 Starting Platinum Tier Orchestrator...")

        # Initialize first
        init_results = self.initialize()
        print(f"  Initialized: {len(init_results['initialized'])} components")
        if init_results['failed']:
            print(f"  Failed: {init_results['failed']}")

        self.running = True

        # Start background scheduler
        self.scheduler_thread = threading.Thread(target=self._scheduler_loop, daemon=True)
        self.scheduler_thread.start()

        # Log start
        self.log_action('start', {'status': 'started'})

        return {
            'status': 'started',
            'initialization': init_results
        }

    def stop(self) -> Dict:
        """Stop all Platinum services"""
        if not self.running:
            return {'status': 'already_stopped'}

        print("💎 Stopping Platinum Tier Orchestrator...")
        self.running = False

        # Log stop
        self.log_action('stop', {'status': 'stopped'})

        return {'status': 'stopped'}

    def _scheduler_loop(self):
        """Background scheduler for periodic tasks"""
        check_interval = 300  # 5 minutes

        while self.running:
            try:
                # Check for tasks to process
                self._check_task_queue()

                # Update predictions if needed
                self._update_predictions()

                # Sleep until next check
                time.sleep(check_interval)

            except Exception as e:
                print(f"Scheduler error: {e}")
                time.sleep(60)

    def _check_task_queue(self):
        """Check and process task queue"""
        needs_action = self.vault / "Needs_Action"
        pending_count = len(list(needs_action.glob("*.md")))

        if pending_count > 10 and self.agent_coordinator:
            # Delegate overflow to agents
            print(f"📊 High task count detected: {pending_count} tasks")

    def _update_predictions(self):
        """Update predictive models"""
        # Run prediction updates daily
        pass

    def process_command(self, command: str) -> Dict:
        """Process a natural language command"""
        if not self.nlp_processor:
            return {'error': 'NLP processor not initialized'}

        parsed = self.nlp_processor.process_command(command)
        result = self.nlp_processor.execute_command(parsed)

        # Log command
        self.log_action('command', {
            'input': command,
            'parsed': parsed,
            'result': result
        })

        return result

    def delegate_task(self, task: Dict) -> Dict:
        """Delegate task to agent pool"""
        if not self.agent_coordinator:
            return {'error': 'Agent coordinator not initialized'}

        return self.agent_coordinator.delegate_task(task)

    def get_forecast(self, days: int = 7) -> Dict:
        """Get workload forecast"""
        if not self.predictive_engine:
            return {'error': 'Predictive engine not initialized'}

        return self.predictive_engine.forecast_workload(days)

    def get_status(self) -> Dict:
        """Get current system status"""
        status = {
            'running': self.running,
            'timestamp': datetime.now().isoformat(),
            'components': {
                'agent_coordinator': self.agent_coordinator is not None,
                'predictive_engine': self.predictive_engine is not None,
                'nlp_processor': self.nlp_processor is not None
            }
        }

        if self.agent_coordinator:
            status['agent_pool'] = self.agent_coordinator.get_agent_status()

        # Task counts
        needs_action = self.vault / "Needs_Action"
        done = self.vault / "Done"

        status['tasks'] = {
            'pending': len(list(needs_action.glob("*.md"))),
            'completed': len(list(done.glob("*.md")))
        }

        return status

    def generate_executive_report(self) -> str:
        """Generate executive analytics report"""
        if not self.predictive_engine:
            # Try to initialize it on demand
            try:
                import sys
                sys.path.insert(0, str(self.vault))
                from Platinum_Tier.Predictive.forecasting_engine import PredictiveEngine
                self.predictive_engine = PredictiveEngine(str(self.vault))
            except Exception as e:
                return f"Predictive engine not initialized: {str(e)}"

        return self.predictive_engine.generate_executive_report()

    def log_action(self, action: str, data: Dict):
        """Log action to Platinum logs"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "data": data
        }

        log_file = self.vault / "Platinum_Tier/Logs/orchestrator.json"
        log_file.parent.mkdir(parents=True, exist_ok=True)

        logs = []
        if log_file.exists():
            try:
                with open(log_file) as f:
                    logs = json.load(f)
            except:
                logs = []

        logs.append(log_entry)

        with open(log_file, 'w') as f:
            json.dump(logs[-100:], f, indent=2)


def main():
    """Main entry point for Platinum Orchestrator"""
    vault_path = os.environ.get('VAULT_PATH', '/mnt/c/Users/Admin/AI_Employee_Vault')

    import argparse
    parser = argparse.ArgumentParser(description='Platinum Tier Orchestrator')
    parser.add_argument('command', nargs='?', default='status',
                        choices=['start', 'stop', 'status', 'test', 'report', 'chat'],
                        help='Command to execute')
    parser.add_argument('--days', type=int, default=7, help='Days to forecast')
    args = parser.parse_args()

    orchestrator = PlatinumOrchestrator(vault_path)

    if args.command == 'start':
        result = orchestrator.start()
        print(json.dumps(result, indent=2))

        if result.get('status') == 'started':
            print("\n💎 Platinum Tier is running!")
            print("Press Ctrl+C to stop...")

            try:
                while orchestrator.running:
                    time.sleep(1)
            except KeyboardInterrupt:
                orchestrator.stop()

    elif args.command == 'stop':
        result = orchestrator.stop()
        print(json.dumps(result, indent=2))

    elif args.command == 'status':
        orchestrator.initialize()
        status = orchestrator.get_status()
        print(json.dumps(status, indent=2))

    elif args.command == 'test':
        print("💎 Testing Platinum Tier components...")
        results = orchestrator.initialize()
        print(f"\n✅ Initialized: {results['initialized']}")
        if results['failed']:
            print(f"❌ Failed: {results['failed']}")

        # Test delegation
        if orchestrator.agent_coordinator:
            test_result = orchestrator.delegate_task({
                'type': 'research',
                'description': 'Test task'
            })
            print(f"\n📊 Delegation test: {test_result.get('status')}")

        # Test prediction
        if orchestrator.predictive_engine:
            forecast = orchestrator.get_forecast(3)
            print(f"\n🔮 Forecast test: {len(forecast.get('daily_forecast', []))} days")

    elif args.command == 'report':
        orchestrator.initialize()
        report_file = orchestrator.generate_executive_report()
        print(f"📄 Executive report generated: {report_file}")

    elif args.command == 'chat':
        orchestrator.initialize()
        if orchestrator.nlp_processor:
            orchestrator.nlp_processor.chat_interface()
        else:
            print("❌ NLP processor not available")


if __name__ == "__main__":
    main()
