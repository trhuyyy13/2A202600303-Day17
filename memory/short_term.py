from __future__ import annotations


class ShortTermMemory:
    def __init__(self, max_messages: int = 10):
        self.messages: list[dict] = []
        self.max_messages = max_messages

    def add_message(self, role: str, content: str) -> None:
        self.messages.append({"role": role, "content": content})
        self.messages = self.messages[-self.max_messages :]

    def get_messages(self, limit: int = 10) -> list[dict]:
        return self.messages[-limit:]

    def clear(self) -> None:
        self.messages.clear()


class ShortTermMemoryStore:
    def __init__(self, max_messages: int = 10):
        self.max_messages = max_messages
        self._store: dict[str, ShortTermMemory] = {}

    def get_buffer(self, user_id: str) -> ShortTermMemory:
        if user_id not in self._store:
            self._store[user_id] = ShortTermMemory(max_messages=self.max_messages)
        return self._store[user_id]

    def clear(self, user_id: str) -> None:
        if user_id in self._store:
            self._store[user_id].clear()
