
from __future__ import annotations

from datetime import date, datetime
from typing import Dict, List

from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

# ---- In-memory mock schedule store ---------------------------------------
# Map ISO date string -> list of event strings
_SCHEDULE_DATA: Dict[str, List[str]] = {
    date.today().isoformat(): [
        "Breakfast with family at 8:00 AM",
        "Team stand-up at 9:30 AM",
        "Grocery pickup at 5:00 PM",
    ]
}


def get_schedule_for_day(day: str) -> dict:
    """Tool: Return scheduled items for an ISO day (YYYY-MM-DD).

    Args:
        day: ISO 8601 date string.

    Returns:
        dict: status + report (human text) + data (list of events)
    """
    try:
        # Validate date format
        _ = datetime.fromisoformat(day).date()
    except ValueError:
        return {"status": "error", "report": "Invalid date format. Use YYYY-MM-DD."}

    events = _SCHEDULE_DATA.get(day, [])
    if not events:
        return {"status": "success", "report": f"No events scheduled for {day}.", "data": []}
    bullet = "\n".join(f"- {e}" for e in events)
    return {
        "status": "success",
        "report": f"Schedule for {day}:\n{bullet}",
        "data": events,
    }


schedule_manager_agent = Agent(
    name="schedule_manager",
    model=LiteLlm(model="ollama_chat/gpt-oss:20b"),
    description="Handles family schedule operations as a tool for a parent agent. Use this agent as a tool to manage and report schedule entries.",
    instruction=(
        "Provide the schedule for a requested date using the get_schedule_for_day tool. "
        "If the user supplies a date, call the tool with that date. If not, ask for the date "
        "in YYYY-MM-DD format."
    ),
    tools=[get_schedule_for_day],
)

__all__ = ["schedule_manager_agent", "get_schedule_for_day"]
