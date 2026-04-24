from __future__ import annotations

from typing import Any, TypedDict


class MemoryState(TypedDict):
    user_id: str
    messages: list[dict]
    query: str
    intent: str
    selected_backends: list[str]
    user_profile: dict
    episodes: list[dict]
    semantic_hits: list[dict]
    recent_conversation: list[dict]
    memory_budget: int
    context: str
    response: str
    should_write_memory: bool
    memory_write_payload: dict[str, Any]
