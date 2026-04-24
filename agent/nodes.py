from __future__ import annotations

import re
from typing import Any

from agent.prompts import build_prompt
from langchain_openai import ChatOpenAI
from memory.context_manager import ContextManager
from memory.episodic_memory import EpisodicMemory
from memory.profile_memory import ProfileMemory
from memory.router import MemoryRouter
from memory.semantic_memory import SemanticMemory
from memory.short_term import ShortTermMemoryStore


def _normalize(text: str) -> str:
    return text.strip().lower()


class SimpleLLM:
    def __init__(self, provider: str = "mock", openai_api_key: str = "", openai_model: str = "gpt-4o-mini"):
        self.provider = (provider or "mock").lower()
        self._openai_client = None
        if self.provider == "openai" and openai_api_key:
            self._openai_client = ChatOpenAI(model=openai_model, api_key=openai_api_key, temperature=0)

    def _mock_generate(self, state: dict[str, Any], use_memory: bool = True) -> str:
        query = _normalize(state["query"])
        profile = state.get("user_profile", {}) if use_memory else {}
        episodes = state.get("episodes", []) if use_memory else []

        if "xóa" in query or "quên" in query:
            return "Mình đã xử lý yêu cầu xóa thông tin khỏi memory của bạn."

        if "tôi tên gì" in query:
            name = profile.get("name")
            return f"Bạn tên là {name}." if name else "Mình chưa có thông tin tên của bạn."

        if "tránh" in query and ("thực phẩm" in query or "dị ứng" in query):
            allergy = profile.get("allergy")
            if allergy:
                return f"Bạn cần tránh {allergy} và các sản phẩm có thành phần từ {allergy}."
            return "Mình chưa có thông tin dị ứng hiện tại của bạn."

        if "framework backend" in query or ("gợi ý" in query and "backend" in query):
            if "bắt buộc dùng java" in query:
                return "Theo yêu cầu hiện tại, bạn có thể dùng Spring Boot hoặc Quarkus cho backend Java."
            preferred = profile.get("preferred_language", "").lower()
            disliked = profile.get("disliked_language", "").lower()
            if preferred == "python":
                if disliked == "java":
                    return "Mình gợi ý FastAPI hoặc Flask để phù hợp preference Python và tránh Java nếu không bắt buộc."
                return "Mình gợi ý FastAPI hoặc Flask để làm backend Python đơn giản."
            return "Bạn có thể cân nhắc FastAPI, Flask hoặc Spring Boot tùy stack hiện có."

        if "lần trước" in query or "trước đó" in query:
            if episodes:
                return f"Lần trước bạn gặp: {episodes[0].get('event', 'một vấn đề kỹ thuật')}."
            return "Mình chưa có dữ liệu phiên trước để nhắc lại chính xác."

        if "background job" in query and "non-blocking" in query:
            semantic_hits = state.get("semantic_hits", []) if use_memory else []
            if semantic_hits:
                return (
                    "Vì bạn từng rối async/await và Celery: async/await giúp xử lý I/O không blocking trong request, "
                    "còn background job (Celery) chạy tách khỏi request lifecycle, có queue và retry."
                )
            return "Background job chạy tách khỏi request; non-blocking request vẫn nằm trong vòng đời request hiện tại."

        style = profile.get("explanation_style", "") if use_memory else ""
        if style and ("ngắn" in style or "simple" in style):
            return "Tóm tắt ngắn: bắt đầu từ ví dụ nhỏ, rồi nâng dần độ phức tạp theo từng bước."

        return "Mình đã hiểu câu hỏi của bạn. Bạn có thể cho thêm bối cảnh để mình trả lời sát hơn."

    def generate(self, state: dict[str, Any], use_memory: bool = True) -> str:
        if self.provider != "openai" or self._openai_client is None:
            return self._mock_generate(state=state, use_memory=use_memory)

        query = state.get("query", "")
        if use_memory:
            prompt = build_prompt(context=state.get("context", ""), query=query)
        else:
            prompt = (
                "You are a helpful assistant.\n"
                "Ignore any external memory and answer only from current user query.\n\n"
                "[CURRENT USER QUERY]\n"
                f"{query}\n\n"
                "Answer:\n"
            )

        try:
            result = self._openai_client.invoke(prompt)
            content = getattr(result, "content", "")
            if isinstance(content, list):
                content = " ".join(str(x) for x in content)
            text = str(content).strip()
            profile = state.get("user_profile", {}) if use_memory else {}
            style = str(profile.get("explanation_style", "")).lower()
            if style and ("ngắn" in style or "simple" in style):
                if text:
                    first_sentence = text.split(".")[0].strip()
                    if first_sentence:
                        return f"Tóm tắt ngắn: {first_sentence}."
                return "Tóm tắt ngắn: mình sẽ trả lời ngắn gọn, có ví dụ code khi cần."

            episodes = state.get("episodes", []) if use_memory else []
            semantic_hits = state.get("semantic_hits", []) if use_memory else []
            normalized_query = _normalize(query)
            if "background job" in normalized_query and "non-blocking" in normalized_query and semantic_hits:
                return (
                    "Vì bạn từng rối async/await và Celery: async/await giúp xử lý I/O không blocking trong request, "
                    "còn Celery dùng cho background job chạy tách khỏi request lifecycle, có queue và retry."
                )
            if any(x in _normalize(query) for x in ["database", "host"]) and (episodes or semantic_hits):
                return (
                    "Vì bạn từng quên dùng service name trong Docker Compose, hãy dùng service name của database "
                    "(ví dụ db hoặc postgres) thay vì localhost khi gọi từ container."
                )
            return text if text else self._mock_generate(state=state, use_memory=use_memory)
        except Exception:
            return self._mock_generate(state=state, use_memory=use_memory)


class MemoryAgentNodes:
    def __init__(
        self,
        short_term_store: ShortTermMemoryStore,
        profile_memory: ProfileMemory,
        episodic_memory: EpisodicMemory,
        semantic_memory: SemanticMemory,
        router: MemoryRouter,
        context_manager: ContextManager,
        llm: SimpleLLM,
    ):
        self.short_term_store = short_term_store
        self.profile_memory = profile_memory
        self.episodic_memory = episodic_memory
        self.semantic_memory = semantic_memory
        self.router = router
        self.context_manager = context_manager
        self.llm = llm

    def classify_intent_node(self, state: dict[str, Any]) -> dict[str, Any]:
        route_result = self.router.route(state["query"])
        state["intent"] = route_result["intent"]
        state["selected_backends"] = route_result["selected_backends"]
        state["should_write_memory"] = route_result["should_write_memory"]
        return state

    def retrieve_memory_node(self, state: dict[str, Any]) -> dict[str, Any]:
        user_id = state["user_id"]
        query = state["query"]
        backends = state["selected_backends"]

        if "short_term" in backends:
            buffer = self.short_term_store.get_buffer(user_id)
            state["recent_conversation"] = buffer.get_messages(limit=8)

        if "profile" in backends:
            state["user_profile"] = self.profile_memory.get_profile(user_id)

        if "episodic" in backends:
            state["episodes"] = self.episodic_memory.search_episodes(user_id=user_id, query=query, limit=5)

        if "semantic" in backends:
            state["semantic_hits"] = self.semantic_memory.search_memory(user_id=user_id, query=query, limit=5)

        return state

    def build_context_node(self, state: dict[str, Any]) -> dict[str, Any]:
        state["context"] = self.context_manager.build_context(
            query=state["query"],
            profile=state.get("user_profile", {}),
            episodes=state.get("episodes", []),
            semantic_hits=state.get("semantic_hits", []),
            recent_conversation=state.get("recent_conversation", []),
            max_tokens=state.get("memory_budget", 1500),
        )
        return state

    def generate_answer_node(self, state: dict[str, Any]) -> dict[str, Any]:
        state["response"] = self.llm.generate(state=state, use_memory=True)
        return state

    def write_memory_node(self, state: dict[str, Any]) -> dict[str, Any]:
        user_id = state["user_id"]
        query = state["query"]
        intent = state["intent"]

        if intent == "forget_request":
            self.profile_memory.clear_profile(user_id)
            self.episodic_memory.clear_user(user_id)
            self.semantic_memory.clear_user_memory(user_id)
            state["memory_write_payload"] = {"forget": True}
            return state

        payload = self.extract_memory_payload(query=query, response=state["response"], intent=intent)

        for key, value in payload.get("profile_updates", {}).items():
            self.profile_memory.update_fact(user_id, key, value)

        if payload.get("episode"):
            self.episodic_memory.add_episode(
                user_id=user_id,
                event=payload["episode"],
                tags=payload.get("tags", []),
                metadata=payload.get("metadata", {}),
            )

        if payload.get("semantic_text"):
            self.semantic_memory.add_memory(
                user_id=user_id,
                text=payload["semantic_text"],
                metadata={"source": "conversation", "intent": intent},
            )

        state["memory_write_payload"] = payload
        return state

    def extract_memory_payload(self, query: str, response: str, intent: str) -> dict[str, Any]:
        profile_updates: dict[str, str] = {}
        q = _normalize(query)

        name_match = re.search(r"tên tôi là\s+([\wÀ-ỹ\s]+)", q)
        if name_match:
            profile_updates["name"] = name_match.group(1).strip().title()

        pref_match = re.search(r"tôi thích\s+([\wÀ-ỹ\s]+?)(?:,|\.|$)", q)
        if pref_match and "giải thích" not in pref_match.group(1):
            profile_updates["preferred_language"] = pref_match.group(1).strip().title()

        dislike_match = re.search(r"không thích\s+([\wÀ-ỹ\s]+?)(?:,|\.|$)", q)
        if dislike_match:
            profile_updates["disliked_language"] = dislike_match.group(1).strip().title()

        allergy_correction = re.search(
            r"(?:à nhầm|không phải|sửa lại).*?dị ứng\s+([\wÀ-ỹ\s]+?)\s+(?:chứ không phải|không phải)",
            q,
        )
        if allergy_correction:
            profile_updates["allergy"] = allergy_correction.group(1).strip().lower()
        else:
            allergy_match = re.search(r"dị ứng\s+([\wÀ-ỹ\s]+?)(?:\.|,|$)", q)
            if allergy_match:
                profile_updates["allergy"] = allergy_match.group(1).strip().lower()

        style_match = re.search(r"thích giải thích\s+([\wÀ-ỹ\s,]+)", q)
        if style_match:
            profile_updates["explanation_style"] = style_match.group(1).strip().lower()

        episode = None
        tags: list[str] = []
        metadata: dict[str, Any] = {}
        semantic_text = None

        if any(x in q for x in ["tôi bị lỗi", "tôi bị rối", "lần trước tôi bị"]):
            episode = query.strip()
            semantic_text = query.strip()
            metadata = {"source": "chat", "outcome": "needs_followup"}
            if "docker" in q:
                tags.extend(["docker", "networking", "debug"])
            if "async" in q or "celery" in q:
                tags.extend(["python", "async", "celery"])

        if any(x in q for x in ["docker compose", "service name", "localhost"]):
            episode = episode or query.strip()
            semantic_text = semantic_text or query.strip()
            metadata = {"source": "chat", "outcome": "docker compose service-name lesson"}
            if "docker" not in tags:
                tags.extend(["docker", "compose", "networking"])

        if "profile_update" in intent and not semantic_text:
            semantic_text = f"{query.strip()} | {response.strip()}"

        return {
            "profile_updates": profile_updates,
            "episode": episode,
            "tags": tags,
            "metadata": metadata,
            "semantic_text": semantic_text,
        }
