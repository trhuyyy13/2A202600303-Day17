from __future__ import annotations


def _contains_all(text: str, expected: list[str]) -> bool:
    lower = text.lower()
    return all(item.lower() in lower for item in expected)


def evaluate_case(case: dict, with_memory_answer: str, no_memory_answer: str) -> dict:
    checks = case.get("checks", {})
    with_expected = checks.get("with_memory_contains", [])
    no_memory_expected = checks.get("no_memory_contains", [])

    with_pass = _contains_all(with_memory_answer, with_expected) if with_expected else True
    no_memory_pass = _contains_all(no_memory_answer, no_memory_expected) if no_memory_expected else True

    return {
        "with_memory_pass": with_pass,
        "no_memory_pass": no_memory_pass,
        "pass": with_pass,
    }
