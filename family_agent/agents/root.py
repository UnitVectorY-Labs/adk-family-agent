
from __future__ import annotations

from typing import List, Callable

from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

from .schedule_manager import schedule_manager_agent
from .shopping_list import shopping_list_agent

from google.adk.tools import agent_tool


# NOTE: We keep tool signatures simple (no *args/*kwargs) for clarity.
root_agent = Agent(
    name="family_root",
    model=LiteLlm(model="ollama_chat/gpt-oss:20b"),
    description="Family orchestrator agent that can help with schedule and shopping list.",
    instruction=(
        "You are the family root agent. Provide concise help. When the user asks about the "
        "schedule for a date, use the schedule_manager_agent as a tool to handle the request. "
        "For shopping list operations, use the shopping_list_agent as a tool to perform the work. "
        "If unsure, list capabilities. Do not delegate; invoke these agents as tools so they process the request themselves."
    ),
    tools=[
        agent_tool.AgentTool(agent=schedule_manager_agent),
        agent_tool.AgentTool(agent=shopping_list_agent),
    ],
)

__all__: List[str] = ["root_agent"]
