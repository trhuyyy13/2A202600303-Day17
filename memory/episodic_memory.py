from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path


def _tokenize(text: str) -> set[str]:
    return {t for t in text.lower().split() if t}


class EpisodicMemory:
    def __init__(self, file_path: Path):
        self.file_path = file_path
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.file_path.exists():
            self.file_path.write_text("", encoding="utf-8")

    def _read_all(self) -> list[dict]:
        episodes: list[dict] = []
        for line in self.file_path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            try:
                episodes.append(json.loads(line))
            except json.JSONDecodeError:
                continue
        return episodes

    def _write_all(self, episodes: list[dict]) -> None:
        content = "\n".join(json.dumps(ep, ensure_ascii=False) for ep in episodes)
        if content:
            content += "\n"
        self.file_path.write_text(content, encoding="utf-8")

    def add_episode(
        self,
        user_id: str,
        event: str,
        tags: list[str] | None = None,
        metadata: dict | None = None,
    ) -> None:
        episode = {
            "user_id": user_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event": event,
            "tags": tags or [],
            "metadata": metadata or {},
        }
        with self.file_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(episode, ensure_ascii=False) + "\n")

    def get_recent_episodes(self, user_id: str, limit: int = 5) -> list[dict]:
        episodes = [e for e in self._read_all() if e.get("user_id") == user_id]
        return episodes[-limit:][::-1]

    def search_episodes(self, user_id: str, query: str, limit: int = 5) -> list[dict]:
        query_tokens = _tokenize(query)
        episodes = [e for e in self._read_all() if e.get("user_id") == user_id]

        scored: list[tuple[int, dict]] = []
        for episode in episodes:
            text = f"{episode.get('event', '')} {' '.join(episode.get('tags', []))}"
            score = len(query_tokens.intersection(_tokenize(text)))
            if score > 0:
                scored.append((score, episode))

        if not scored:
            return self.get_recent_episodes(user_id, limit=limit)

        scored.sort(key=lambda x: x[0], reverse=True)
        return [item[1] for item in scored[:limit]]

    def clear_user(self, user_id: str) -> None:
        episodes = [e for e in self._read_all() if e.get("user_id") != user_id]
        self._write_all(episodes)
