from dataclasses import dataclass, asdict
from typing import List, Any, Dict


@dataclass
class Task:
    id: str
    description: str
    assigned_to: str = None
    status: str = "pending"
    result: Any = None
    dependencies: List[str] = None

    def __post_init__(self):
        if self.dependencies is None:
            self.dependencies = []


@dataclass
class Agent:
    name: str
    role: str
    expertise: str
    system_prompt: str


AGENT_REGISTRY: Dict[str, Agent] = {
    "researcher": Agent(
        name="researcher",
        role="Research Specialist",
        expertise="Information gathering, analysis, and synthesis",
        system_prompt="You are a research specialist. Provide thorough research on topics."
    ),
    "coder": Agent(
        name="coder",
        role="Software Engineer",
        expertise="Writing clean, efficient code with best practices",
        system_prompt="You are an expert programmer. Write clean, well-documented code."
    ),
    "writer": Agent(
        name="writer",
        role="Content Writer",
        expertise="Clear communication and documentation",
        system_prompt="You are a professional writer. Create clear, engaging content."
    ),
    "analyst": Agent(
        name="analyst",
        role="Data Analyst",
        expertise="Data interpretation and insights",
        system_prompt="You are a data analyst. Provide clear insights from data."
    )
}


__all__ = ["Task", "Agent", "AGENT_REGISTRY", "asdict"]
