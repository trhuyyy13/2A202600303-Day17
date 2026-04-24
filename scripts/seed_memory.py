from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from config import get_settings
from graph import MultiMemoryAgent


def main() -> None:
    parser = argparse.ArgumentParser(description="Seed memory for demo")
    parser.add_argument("--user-id", default=get_settings().user_id)
    args = parser.parse_args()

    settings = get_settings()
    agent = MultiMemoryAgent(settings)
    user_id = args.user_id

    agent.profile_memory.update_fact(user_id, "name", "Huy")
    agent.profile_memory.update_fact(user_id, "preferred_language", "Python")
    agent.profile_memory.update_fact(user_id, "disliked_language", "Java")
    agent.profile_memory.update_fact(user_id, "allergy", "đậu nành")
    agent.profile_memory.update_fact(user_id, "explanation_style", "ngắn gọn, có ví dụ code")

    agent.episodic_memory.add_episode(
        user_id=user_id,
        event="User had Docker networking issue and learned to use Docker service name instead of localhost.",
        tags=["docker", "networking", "debug"],
        metadata={"source": "seed", "outcome": "resolved"},
    )

    agent.semantic_memory.add_memory(
        user_id=user_id,
        text="User was confused about async/await and Celery.",
        metadata={"source": "seed", "memory_type": "semantic"},
    )

    print(f"Seed memory done for user_id={user_id}")


if __name__ == "__main__":
    main()
