from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path


def _tokenize(text: str) -> set[str]:
    text = text.lower()
    cleaned = "".join(ch if ch.isalnum() or ch.isspace() else " " for ch in text)
    return {t for t in cleaned.split() if t}


class SemanticMemory:
    def __init__(self, file_path: Path):
        self.file_path = file_path
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.file_path.exists():
            self.file_path.write_text("", encoding="utf-8")

    def _read_all(self) -> list[dict]:
        memories: list[dict] = []
        for line in self.file_path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            try:
                memories.append(json.loads(line))
            except json.JSONDecodeError:
                continue
        return memories

    def _write_all(self, memories: list[dict]) -> None:
        content = "\n".join(json.dumps(item, ensure_ascii=False) for item in memories)
        if content:
            content += "\n"
        self.file_path.write_text(content, encoding="utf-8")

    def add_memory(self, user_id: str, text: str, metadata: dict | None = None) -> None:
        item = {
            "user_id": user_id,
            "text": text,
            "metadata": metadata or {},
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        with self.file_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")

    def search_memory(self, user_id: str, query: str, limit: int = 5) -> list[dict]:
        query_tokens = _tokenize(query)
        scored: list[tuple[int, dict]] = []

        for item in self._read_all():
            if item.get("user_id") != user_id:
                continue
            text = item.get("text", "")
            score = len(query_tokens.intersection(_tokenize(text)))
            if query.lower() in text.lower():
                score += 2
            if score > 0:
                scored.append((score, item))

        scored.sort(key=lambda x: x[0], reverse=True)
        if scored:
            return [x[1] for x in scored[:limit]]

        recent = [item for item in self._read_all() if item.get("user_id") == user_id]
        return recent[-limit:][::-1]

    def clear_user_memory(self, user_id: str) -> None:
        data = [item for item in self._read_all() if item.get("user_id") != user_id]
        self._write_all(data)
