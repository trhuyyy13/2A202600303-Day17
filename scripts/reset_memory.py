from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from config import get_settings
from graph import MultiMemoryAgent


def main() -> None:
    parser = argparse.ArgumentParser(description="Reset memory for a user")
    parser.add_argument("--user-id", default=get_settings().user_id)
    args = parser.parse_args()

    settings = get_settings()
    agent = MultiMemoryAgent(settings)
    agent.reset_user_memory(args.user_id)
    print(f"Reset memory done for user_id={args.user_id}")


if __name__ == "__main__":
    main()
