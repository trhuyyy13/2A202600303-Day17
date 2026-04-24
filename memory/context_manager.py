from __future__ import annotations


def approximate_tokens(text: str) -> int:
    return max(1, len(text.split()))


class ContextManager:
    def __init__(self, default_max_tokens: int = 1500):
        self.default_max_tokens = default_max_tokens

    def _format_profile(self, profile: dict) -> str:
        if not profile:
            return "(empty)"
        return "\n".join(f"- {k}: {v}" for k, v in profile.items())

    def _format_episodes(self, episodes: list[dict]) -> str:
        if not episodes:
            return "(empty)"
        return "\n".join(f"- {e.get('event', '')}" for e in episodes[:5])

    def _format_semantic(self, semantic_hits: list[dict]) -> str:
        if not semantic_hits:
            return "(empty)"
        return "\n".join(f"- {item.get('text', '')}" for item in semantic_hits[:5])

    def _format_recent(self, recent_conversation: list[dict]) -> str:
        if not recent_conversation:
            return "(empty)"
        return "\n".join(
            f"{m.get('role', 'unknown').title()}: {m.get('content', '')}" for m in recent_conversation[-8:]
        )

    def build_context(
        self,
        query: str,
        profile: dict,
        episodes: list[dict],
        semantic_hits: list[dict],
        recent_conversation: list[dict],
        max_tokens: int = 1500,
    ) -> str:
        budget = max_tokens or self.default_max_tokens
        sections: list[tuple[str, str]] = [
            ("USER PROFILE", self._format_profile(profile)),
            ("RECENT CONVERSATION", self._format_recent(recent_conversation)),
            ("SEMANTIC MEMORY", self._format_semantic(semantic_hits)),
            ("EPISODIC MEMORY", self._format_episodes(episodes)),
        ]

        final: list[str] = []
        used = 0
        _ = query
        for title, content in sections:
            block = f"[{title}]\n{content}\n"
            cost = approximate_tokens(block)
            if used + cost <= budget:
                final.append(block)
                used += cost

        return "\n".join(final).strip()
