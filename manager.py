from typing import List, Dict, Any, Optional
import re
import json

from models import Task, AGENT_REGISTRY
from llm import LocalLLM
from utils import timestamped_log, safe_extract_json


class ManagerAgent:
    def __init__(self, model_name: str = "TinyLlama/TinyLlama-1.1B-Chat-v1.0", llm: Optional[LocalLLM] = None):
        self.llm = llm or LocalLLM(model_name)
        self.agents = AGENT_REGISTRY
        self.tasks: Dict[str, Task] = {}
        self.execution_log: List[str] = []

    def log(self, message: str):
        entry = timestamped_log(message)
        self.execution_log.append(entry)

    def decompose_goal(self, goal: str) -> List[Task]:
        self.log(f"🎯 Decomposing goal: {goal}")
        agent_info = "\n".join([f"- {name}: {agent.expertise}" for name, agent in self.agents.items()])
        prompt = f"""Break down this goal into 3 specific subtasks. Assign each to the best agent.

Goal: {goal}

Available agents:
{agent_info}

Respond ONLY with a JSON array."""
        response = self.llm.generate(prompt, max_tokens=250)
        tasks_data = safe_extract_json(response)
        if tasks_data is None:
            tasks_data = self._create_default_tasks(goal)

        tasks: List[Task] = []
        for i, task_data in enumerate(tasks_data[:3]):
            tid = task_data.get('id', f'task_{i+1}')
            task = Task(
                id=tid,
                description=task_data.get('description', f'Work on: {goal}'),
                assigned_to=task_data.get('assigned_to', list(self.agents.keys())[i % len(self.agents)]),
                dependencies=task_data.get('dependencies', [] if i == 0 else [f'task_{i}'])
            )
            self.tasks[task.id] = task
            tasks.append(task)
            self.log(f"  ✓ {task.id}: {task.description[:50]}... → {task.assigned_to}")

        return tasks

    def _create_default_tasks(self, goal: str) -> List[Dict[str, Any]]:
        if any(word in goal.lower() for word in ['code', 'program', 'implement', 'algorithm']):
            return [
                {"id": "task_1", "description": f"Research and explain the concept: {goal}", "assigned_to": "researcher", "dependencies": []},
                {"id": "task_2", "description": f"Write code implementation for: {goal}", "assigned_to": "coder", "dependencies": ["task_1"]},
                {"id": "task_3", "description": f"Create documentation and examples", "assigned_to": "writer", "dependencies": ["task_2"]}
            ]
        return [
            {"id": "task_1", "description": f"Research: {goal}", "assigned_to": "researcher", "dependencies": []},
            {"id": "task_2", "description": f"Analyze findings and structure content", "assigned_to": "analyst", "dependencies": ["task_1"]},
            {"id": "task_3", "description": f"Write comprehensive response", "assigned_to": "writer", "dependencies": ["task_2"]}
        ]

    def execute_task(self, task: Task, context: Dict[str, Any] = None) -> str:
        self.log(f"🤖 Executing {task.id} with {task.assigned_to}")
        task.status = "in_progress"
        agent = self.agents.get(task.assigned_to)
        context_str = ""
        if context and task.dependencies:
            context_str = "\n\nContext from previous tasks:\n"
            for dep_id in task.dependencies:
                if dep_id in context:
                    context_str += f"- {context[dep_id][:150]}...\n"

        prompt = f"""{agent.system_prompt if agent else ''}

Task: {task.description}{context_str}

Provide a clear, concise response:"""
        result = self.llm.generate(prompt, max_tokens=250)
        task.result = result
        task.status = "completed"
        self.log(f"  ✓ Completed {task.id}")
        return result

    def synthesize_results(self, goal: str, results: Dict[str, str]) -> str:
        self.log("🔄 Synthesizing final results")
        results_text = "\n\n".join([f"Task {tid}:\n{res[:200]}" for tid, res in results.items()])
        prompt = f"""Combine these task results into one final coherent answer.

Original Goal: {goal}

Task Results:
{results_text}

Final comprehensive answer:"""
        return self.llm.generate(prompt, max_tokens=350)

    def execute_goal(self, goal: str) -> Dict[str, Any]:
        self.log(f"\n{'='*60}\n🎬 Starting Manager Agent\n{'='*60}")
        tasks = self.decompose_goal(goal)
        results: Dict[str, str] = {}
        completed = set()
        max_iterations = len(tasks) * 2
        iteration = 0

        while len(completed) < len(tasks) and iteration < max_iterations:
            iteration += 1
            for task in tasks:
                if task.id in completed:
                    continue
                deps_met = all(dep in completed for dep in task.dependencies)
                if deps_met:
                    result = self.execute_task(task, results)
                    results[task.id] = result
                    completed.add(task.id)

        final_output = self.synthesize_results(goal, results)
        self.log(f"\n{'='*60}\n✅ Execution Complete!\n{'='*60}\n")

        return {
            "goal": goal,
            "tasks": [task.__dict__ for task in tasks],
            "final_output": final_output,
            "execution_log": self.execution_log
        }


__all__ = ["ManagerAgent"]
