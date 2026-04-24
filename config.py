from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


@dataclass
class Settings:
    root_dir: Path
    llm_provider: str
    openai_api_key: str
    openai_model: str
    user_id: str
    max_context_tokens: int
    memory_budget: int
    profile_memory_path: Path
    episodic_memory_path: Path
    semantic_memory_path: Path
    chroma_persist_dir: Path


def get_settings() -> Settings:
    load_dotenv()
    root = Path(__file__).resolve().parent

    profile_path = (root / os.getenv("PROFILE_MEMORY_PATH", "./data/profile.json")).resolve()
    episodic_path = (root / os.getenv("EPISODIC_MEMORY_PATH", "./data/episodes.jsonl")).resolve()
    semantic_path = (root / os.getenv("SEMANTIC_MEMORY_PATH", "./data/semantic.jsonl")).resolve()
    chroma_dir = (root / os.getenv("CHROMA_PERSIST_DIR", "./data/chroma_db")).resolve()

    profile_path.parent.mkdir(parents=True, exist_ok=True)
    episodic_path.parent.mkdir(parents=True, exist_ok=True)
    semantic_path.parent.mkdir(parents=True, exist_ok=True)
    chroma_dir.mkdir(parents=True, exist_ok=True)

    if not profile_path.exists():
        profile_path.write_text("{}", encoding="utf-8")
    if not episodic_path.exists():
        episodic_path.write_text("", encoding="utf-8")
    if not semantic_path.exists():
        semantic_path.write_text("", encoding="utf-8")

    return Settings(
        root_dir=root,
        llm_provider=os.getenv("LLM_PROVIDER", "mock"),
        openai_api_key=os.getenv("OPENAI_API_KEY", ""),
        openai_model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        user_id=os.getenv("USER_ID", "demo_user"),
        max_context_tokens=int(os.getenv("MAX_CONTEXT_TOKENS", "3000")),
        memory_budget=int(os.getenv("MEMORY_BUDGET", "1500")),
        profile_memory_path=profile_path,
        episodic_memory_path=episodic_path,
        semantic_memory_path=semantic_path,
        chroma_persist_dir=chroma_dir,
    )
