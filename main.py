from __future__ import annotations

import argparse

from config import get_settings
from graph import MultiMemoryAgent


def run_chat(user_id: str) -> None:
    settings = get_settings()
    agent = MultiMemoryAgent(settings)

    print("Multi-Memory Agent chat started. Gõ 'exit' để thoát.")
    while True:
        user_query = input("You: ").strip()
        if not user_query:
            continue
        if user_query.lower() in {"exit", "quit"}:
            break
        response = agent.ask(query=user_query, user_id=user_id, with_memory=True)
        print(f"Agent: {response}")


def run_single_query(user_id: str, query: str, no_memory: bool) -> None:
    settings = get_settings()
    agent = MultiMemoryAgent(settings)
    response = agent.ask(query=query, user_id=user_id, with_memory=not no_memory)
    print(response)


def main() -> None:
    parser = argparse.ArgumentParser(description="Lab 17 Multi-Memory Agent")
    subparsers = parser.add_subparsers(dest="command", required=True)

    chat_parser = subparsers.add_parser("chat", help="Start interactive chat")
    chat_parser.add_argument("--user-id", default=get_settings().user_id)

    ask_parser = subparsers.add_parser("ask", help="Ask one query")
    ask_parser.add_argument("query")
    ask_parser.add_argument("--user-id", default=get_settings().user_id)
    ask_parser.add_argument("--no-memory", action="store_true")

    args = parser.parse_args()
    if args.command == "chat":
        run_chat(user_id=args.user_id)
    elif args.command == "ask":
        run_single_query(user_id=args.user_id, query=args.query, no_memory=args.no_memory)


if __name__ == "__main__":
    main()
