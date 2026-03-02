#!/usr/bin/env python3
"""
Platinum Multi-Agent Coordinator
Manages agent pool, task delegation, and collaboration
"""

import os
import sys
import json
from pathlib import Path
from typing import List, Dict, Optional, Any
from datetime import datetime

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

try:
    import anthropic
    DEPENDENCIES_OK = True
except ImportError:
    DEPENDENCIES_OK = False


class AgentCoordinator:
    """Coordinates multiple specialized agents for complex tasks"""

    def __init__(self, vault_path: str = None):
        self.vault = Path(vault_path) if vault_path else Path("/mnt/c/Users/Admin/AI_Employee_Vault")
        self.client = anthropic.Anthropic() if DEPENDENCIES_OK else None
        self.config = self.load_config()
        self.agent_pool = self.initialize_agent_pool()
        self.task_history = []

    def load_config(self) -> Dict:
        """Load agent pool configuration"""
        config_file = self.vault / "Platinum_Tier/Configs/agent_pool_config.yaml"
        if config_file.exists():
            try:
                import yaml
                with open(config_file) as f:
                    return yaml.safe_load(f)
            except:
                pass
        return {"agent_pool": {"specialist_agents": [], "collaboration_rules": []}}

    def initialize_agent_pool(self) -> Dict:
        """Initialize all specialist agents"""
        agents = {}
        for agent_config in self.config.get('agent_pool', {}).get('specialist_agents', []):
            agents[agent_config['name']] = {
                'type': agent_config['type'],
                'expertise': agent_config['expertise'],
                'capacity': agent_config['capacity'],
                'current_load': 0,
                'status': 'ready',
                'tasks_completed': 0,
                'last_task': None
            }
        return agents

    def get_agent_status(self) -> Dict:
        """Get status of all agents"""
        return {
            name: {
                'status': info['status'],
                'load': f"{info['current_load']}/{info['capacity']}",
                'tasks_completed': info['tasks_completed']
            }
            for name, info in self.agent_pool.items()
        }

    def delegate_task(self, task: Dict) -> Dict:
        """Intelligently delegate task to best agent(s)"""
        # Analyze task requirements
        requirements = self.analyze_task_requirements(task)

        # Log the delegation
        self.log_action("delegate_task", task, requirements)

        # Find best agent(s)
        if requirements.get('complexity') == 'high' or requirements.get('requires_collaboration'):
            assigned = self.assign_collaborative_task(task, requirements)
        else:
            assigned = self.assign_single_agent(task, requirements)

        if assigned:
            return {
                'status': 'delegated',
                'assigned_to': assigned,
                'requirements': requirements,
                'timestamp': datetime.now().isoformat()
            }
        else:
            return {
                'status': 'queued',
                'reason': 'No available agents with required capacity',
                'requirements': requirements,
                'timestamp': datetime.now().isoformat()
            }

    def analyze_task_requirements(self, task: Dict) -> Dict:
        """Analyze what the task needs using AI"""
        if not self.client:
            # Fallback to rule-based analysis
            return self._rule_based_analysis(task)

        prompt = f"""
Analyze this task and determine requirements:

Task: {json.dumps(task, indent=2)}

Return JSON with this exact structure:
{{
  "complexity": "low|medium|high",
  "required_expertise": ["expertise1"],
  "estimated_time_minutes": 30,
  "priority": 1,
  "requires_collaboration": false,
  "reasoning": "Brief explanation"
}}
"""

        try:
            response = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1000,
                messages=[{"role": "user", "content": prompt}]
            )

            result_text = response.content[0].text
            # Extract JSON from response
            if '```json' in result_text:
                result_text = result_text.split('```json')[1].split('```')[0]
            elif '```' in result_text:
                result_text = result_text.split('```')[1].split('```')[0]

            return json.loads(result_text.strip())
        except Exception as e:
            return self._rule_based_analysis(task)

    def _rule_based_analysis(self, task: Dict) -> Dict:
        """Fallback rule-based task analysis"""
        task_type = task.get('type', 'general')
        description = task.get('description', '').lower()

        expertise_map = {
            'email': 'email_processing',
            'research': 'deep_research',
            'meeting': 'meeting_management',
            'code': 'code_review',
            'analytics': 'data_analysis'
        }

        complexity = 'low'
        if any(word in description for word in ['complex', 'multiple', 'comprehensive', 'deep']):
            complexity = 'high'
        elif any(word in description for word in ['moderate', 'some', 'several']):
            complexity = 'medium'

        expertise = [expertise_map.get(task_type, 'general')]

        return {
            'complexity': complexity,
            'required_expertise': expertise,
            'estimated_time_minutes': 30,
            'priority': task.get('priority', 3),
            'requires_collaboration': complexity == 'high',
            'reasoning': 'Rule-based analysis'
        }

    def assign_single_agent(self, task: Dict, requirements: Dict) -> Optional[str]:
        """Assign to single best agent"""
        expertise_needed = requirements.get('required_expertise', ['general'])[0]

        # Find agent with matching expertise and capacity
        best_agent = None
        lowest_load = float('inf')

        for agent_name, agent_info in self.agent_pool.items():
            if (agent_info['expertise'] == expertise_needed and
                agent_info['current_load'] < agent_info['capacity']):

                if agent_info['current_load'] < lowest_load:
                    best_agent = agent_name
                    lowest_load = agent_info['current_load']

        if best_agent:
            self.agent_pool[best_agent]['current_load'] += 1
            self.agent_pool[best_agent]['last_task'] = task

        return best_agent

    def assign_collaborative_task(self, task: Dict, requirements: Dict) -> List[str]:
        """Assign to multiple agents for collaboration"""
        needed_expertise = requirements.get('required_expertise', [])
        assigned_agents = []

        for expertise in needed_expertise:
            agent = self.find_agent_by_expertise(expertise)
            if agent:
                assigned_agents.append(agent)
                self.agent_pool[agent]['current_load'] += 1

        # If no specific expertise matched, assign based on collaboration rules
        if not assigned_agents:
            assigned_agents = self.find_collaboration_team(task)

        return assigned_agents

    def find_agent_by_expertise(self, expertise: str) -> Optional[str]:
        """Find available agent with specific expertise"""
        for agent_name, agent_info in self.agent_pool.items():
            if (agent_info['expertise'] == expertise and
                agent_info['status'] == 'ready' and
                agent_info['current_load'] < agent_info['capacity']):
                return agent_name
        return None

    def find_collaboration_team(self, task: Dict) -> List[str]:
        """Find agents based on collaboration rules"""
        task_type = task.get('type', 'general')

        for rule in self.config.get('agent_pool', {}).get('collaboration_rules', []):
            if task_type in rule.get('trigger', ''):
                team = []
                for agent_name in rule.get('agents', []):
                    if agent_name in self.agent_pool:
                        if self.agent_pool[agent_name]['current_load'] < self.agent_pool[agent_name]['capacity']:
                            team.append(agent_name)
                return team if team else []

        # Default: return first available agent
        for agent_name, agent_info in self.agent_pool.items():
            if agent_info['current_load'] < agent_info['capacity']:
                return [agent_name]
        return []

    def coordinate_collaboration(self, agents: List[str], task: Dict) -> Dict:
        """Coordinate multiple agents on a task"""
        results = {}

        for agent in agents:
            agent_type = self.agent_pool[agent]['type']
            result = self.execute_agent_task(agent, agent_type, task)
            results[agent] = result

        # Synthesize results
        return self.synthesize_results(results, task)

    def execute_agent_task(self, agent_name: str, agent_type: str, task: Dict) -> Dict:
        """Execute task on specific agent"""
        self.agent_pool[agent_name]['status'] = 'busy'

        try:
            # Import and execute the appropriate agent
            if agent_type == 'email_agent':
                from Gold_Tier.AI_Agents.email_agent import EmailAgent
                agent = EmailAgent(str(self.vault))
                result = agent.execute()
            elif agent_type == 'research_agent':
                from Gold_Tier.AI_Agents.research_agent import ResearchAgent
                agent = ResearchAgent(str(self.vault))
                result = agent.execute(task.get('topic', 'general research'))
            elif agent_type == 'meeting_agent':
                from Gold_Tier.AI_Agents.meeting_agent import MeetingAgent
                agent = MeetingAgent(str(self.vault))
                result = agent.execute()
            elif agent_type == 'task_optimizer':
                from Gold_Tier.AI_Agents.task_optimizer import TaskOptimizer
                agent = TaskOptimizer(str(self.vault))
                result = agent.execute()
            else:
                result = {'status': 'completed', 'output': 'Generic task completion'}

            self.agent_pool[agent_name]['tasks_completed'] += 1
            return result

        except Exception as e:
            return {'status': 'error', 'error': str(e)}
        finally:
            self.agent_pool[agent_name]['status'] = 'ready'
            self.agent_pool[agent_name]['current_load'] = max(0, self.agent_pool[agent_name]['current_load'] - 1)

    def synthesize_results(self, results: Dict, task: Dict) -> Dict:
        """Combine results from multiple agents using AI"""
        if not self.client:
            return {
                'synthesis': 'Results collected from agents',
                'agent_results': results,
                'task': task
            }

        prompt = f"""
Synthesize these agent results into a comprehensive response:

Task: {json.dumps(task, indent=2)}
Agent Results: {json.dumps(results, indent=2)}

Provide:
1. Integrated findings
2. Key recommendations
3. Next actions
4. Confidence level (0-1)
"""

        try:
            response = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=3000,
                messages=[{"role": "user", "content": prompt}]
            )

            return {
                'synthesis': response.content[0].text,
                'agent_results': results,
                'task': task,
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            return {
                'synthesis': f'Error during synthesis: {e}',
                'agent_results': results,
                'task': task
            }

    def log_action(self, action: str, task: Dict, result: Dict):
        """Log action to Platinum logs"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "task": task,
            "result": result
        }

        log_file = self.vault / "Platinum_Tier/Logs/agent_collaboration/coordination.json"
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
            json.dump(logs[-100:], f, indent=2)  # Keep last 100 entries


def main():
    """Main entry point for testing"""
    vault_path = os.environ.get('VAULT_PATH', '/mnt/c/Users/Admin/AI_Employee_Vault')

    print("💎 Platinum Multi-Agent Coordinator")
    print("=" * 50)

    coordinator = AgentCoordinator(vault_path)

    # Show agent status
    print("\n📊 Agent Pool Status:")
    for name, status in coordinator.get_agent_status().items():
        print(f"  • {name}: {status['status']} (Load: {status['load']}, Completed: {status['tasks_completed']})")

    # Test delegation
    test_task = {
        'type': 'research',
        'description': 'Research AI automation trends for Q1 2026',
        'priority': 2
    }

    print(f"\n🚀 Testing task delegation...")
    result = coordinator.delegate_task(test_task)
    print(f"Result: {json.dumps(result, indent=2)}")


if __name__ == "__main__":
    main()
