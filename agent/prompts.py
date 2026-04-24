from __future__ import annotations


SYSTEM_PROMPT = """You are a helpful multi-memory assistant.

You may receive memory context from previous sessions. Use it only when relevant.
Do not mention memory explicitly unless the user asks.
If user preferences are available, adapt your answer to them.
If past episodes are relevant, use them to explain more clearly.
Do not overfit to irrelevant memories.
If memory conflicts with the current user request, prioritize the current user request.
If the user corrects a previous fact, use the latest corrected fact.
"""


def build_prompt(context: str, query: str) -> str:
    return (
        f"{SYSTEM_PROMPT}\n"
        f"{context}\n\n"
        "[CURRENT USER QUERY]\n"
        f"{query}\n\n"
        "Answer:\n"
    )
