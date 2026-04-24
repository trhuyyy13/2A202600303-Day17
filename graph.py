from __future__ import annotations

from typing import Any

from agent.nodes import MemoryAgentNodes, SimpleLLM
from config import Settings
from memory.context_manager import ContextManager
from memory.episodic_memory import EpisodicMemory
from memory.profile_memory import ProfileMemory
from memory.router import MemoryRouter
from memory.semantic_memory import SemanticMemory
from memory.short_term import ShortTermMemoryStore


class MultiMemoryAgent:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.short_term_store = ShortTermMemoryStore(max_messages=10)
        self.profile_memory = ProfileMemory(settings.profile_memory_path)
        self.episodic_memory = EpisodicMemory(settings.episodic_memory_path)
        self.semantic_memory = SemanticMemory(settings.semantic_memory_path)
        self.router = MemoryRouter()
        self.context_manager = ContextManager(default_max_tokens=settings.memory_budget)
        self.llm = SimpleLLM(
            provider=settings.llm_provider,
            openai_api_key=settings.openai_api_key,
            openai_model=settings.openai_model,
        )
        self.nodes = MemoryAgentNodes(
            short_term_store=self.short_term_store,
            profile_memory=self.profile_memory,
            episodic_memory=self.episodic_memory,
            semantic_memory=self.semantic_memory,
            router=self.router,
            context_manager=self.context_manager,
            llm=self.llm,
        )

    def _base_state(self, user_id: str, query: str) -> dict[str, Any]:
        return {
            "user_id": user_id,
            "messages": [],
            "query": query,
            "intent": "general_query",
            "selected_backends": [],
            "user_profile": {},
            "episodes": [],
            "semantic_hits": [],
            "recent_conversation": [],
            "memory_budget": self.settings.memory_budget,
            "context": "",
            "response": "",
            "should_write_memory": False,
            "memory_write_payload": {},
        }

    def ask(self, query: str, user_id: str, with_memory: bool = True) -> str:
        if with_memory:
            return self._ask_with_memory(query=query, user_id=user_id)
        return self._ask_no_memory(query=query, user_id=user_id)

    def _ask_with_memory(self, query: str, user_id: str) -> str:
        state = self._base_state(user_id=user_id, query=query)
        state = self.nodes.classify_intent_node(state)
        state = self.nodes.retrieve_memory_node(state)
        state = self.nodes.build_context_node(state)
        state = self.nodes.generate_answer_node(state)
        state = self.nodes.write_memory_node(state)

        buffer = self.short_term_store.get_buffer(user_id)
        buffer.add_message("user", query)
        buffer.add_message("assistant", state["response"])
        return state["response"]

    def _ask_no_memory(self, query: str, user_id: str) -> str:
        state = self._base_state(user_id=user_id, query=query)
        state["response"] = self.llm.generate(state=state, use_memory=False)
        return state["response"]

    def reset_user_memory(self, user_id: str) -> None:
        self.short_term_store.clear(user_id)
        self.profile_memory.clear_profile(user_id)
        self.episodic_memory.clear_user(user_id)
        self.semantic_memory.clear_user_memory(user_id)
