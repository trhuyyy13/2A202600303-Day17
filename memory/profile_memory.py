from __future__ import annotations

import json
from pathlib import Path


class ProfileMemory:
    def __init__(self, file_path: Path):
        self.file_path = file_path
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.file_path.exists():
            self.file_path.write_text("{}", encoding="utf-8")

    def _read(self) -> dict:
        try:
            return json.loads(self.file_path.read_text(encoding="utf-8") or "{}")
        except json.JSONDecodeError:
            return {}

    def _write(self, data: dict) -> None:
        self.file_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    def get_profile(self, user_id: str) -> dict:
        return self._read().get(user_id, {})

    def update_fact(self, user_id: str, key: str, value: str) -> None:
        data = self._read()
        profile = data.get(user_id, {})
        profile[key] = value
        data[user_id] = profile
        self._write(data)

    def delete_fact(self, user_id: str, key: str) -> None:
        data = self._read()
        profile = data.get(user_id, {})
        if key in profile:
            del profile[key]
        data[user_id] = profile
        self._write(data)

    def clear_profile(self, user_id: str) -> None:
        data = self._read()
        if user_id in data:
            del data[user_id]
        self._write(data)
