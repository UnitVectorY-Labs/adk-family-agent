 
from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Dict, List

from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm


@dataclass
class ShoppingItem:
    id: int
    name: str
    added_at: datetime

    def to_dict(self) -> Dict[str, str]:
        d = asdict(self)
        d["added_at"] = self.added_at.isoformat()
        return d


# In-memory store
_SHOPPING_ITEMS: Dict[int, ShoppingItem] = {}
_NEXT_ID: int = 1


def _next_id() -> int:
    global _NEXT_ID
    nid = _NEXT_ID
    _NEXT_ID += 1
    return nid


def get_shopping_list() -> dict:
    """Tool: Return current shopping list items."""
    data = [item.to_dict() for item in _SHOPPING_ITEMS.values()]
    if not data:
        return {"status": "success", "report": "Shopping list is empty.", "data": []}
    bullet = "\n".join(f"- ({i['id']}) {i['name']} added {i['added_at']}" for i in data)
    return {"status": "success", "report": f"Current shopping list:\n{bullet}", "data": data}


def add_item_to_shopping_list(item_name: str) -> dict:
    """Tool: Add a new item to the shopping list.

    Args:
        item_name: Name of the item to add.
    """
    if not item_name.strip():
        return {"status": "error", "report": "Item name cannot be empty."}
    item = ShoppingItem(id=_next_id(), name=item_name.strip(), added_at=datetime.utcnow())
    _SHOPPING_ITEMS[item.id] = item
    return {"status": "success", "report": f"Added item '{item.name}' with id {item.id}.", "data": item.to_dict()}


def remove_item_from_shopping_list(item_id: int) -> dict:
    """Tool: Remove an item by id.

    Args:
        item_id: Identifier of the item to remove.
    """
    item = _SHOPPING_ITEMS.pop(item_id, None)
    if not item:
        return {"status": "error", "report": f"No item found with id {item_id}."}
    return {"status": "success", "report": f"Removed item '{item.name}' (id {item.id})."}


shopping_list_agent = Agent(
    name="shopping_list",
    model=LiteLlm(model="ollama_chat/gpt-oss:20b"),
    description="Handles family shopping list operations as a tool for a parent agent. Use this agent as a tool to manage the shared shopping list.",
    instruction=(
        "Maintain an in-memory shopping list. Use tools to show, add, or remove items. "
        "Always show ids when listing so user can remove by id."
    ),
    tools=[get_shopping_list, add_item_to_shopping_list, remove_item_from_shopping_list],
)

__all__ = [
    "shopping_list_agent",
    "get_shopping_list",
    "add_item_to_shopping_list",
    "remove_item_from_shopping_list",
]
