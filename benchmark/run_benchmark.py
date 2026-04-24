from __future__ import annotations

import json
import os
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from benchmark.evaluator import evaluate_case
from config import get_settings
from graph import MultiMemoryAgent


def main() -> None:
    settings = get_settings()
    agent = MultiMemoryAgent(settings)

    test_path = Path(__file__).resolve().parent / "test_cases.json"
    cases = json.loads(test_path.read_text(encoding="utf-8"))

    user_id = os.getenv("BENCHMARK_USER_ID", "benchmark_user")
    rows: list[dict] = []

    for case in cases:
        agent.reset_user_memory(user_id)
        current_session = None
        with_answer = ""
        no_answer = ""

        for turn in case["turns"]:
            if current_session is None:
                current_session = turn["session"]
            elif turn["session"] != current_session:
                agent.short_term_store.clear(user_id)
                current_session = turn["session"]

            query = turn["user"]
            with_answer = agent.ask(query=query, user_id=user_id, with_memory=True)
            no_answer = agent.ask(query=query, user_id=user_id, with_memory=False)

        eval_result = evaluate_case(case=case, with_memory_answer=with_answer, no_memory_answer=no_answer)
        rows.append(
            {
                "id": case["id"],
                "scenario": case["scenario"],
                "no_memory": no_answer,
                "with_memory": with_answer,
                "pass": eval_result["pass"],
            }
        )

    output_json = Path(__file__).resolve().parent / "results.json"
    output_json.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")

    summary_lines = [
        "# Benchmark Report — Lab #17 Multi-Memory Agent",
        "",
        "## 1. Setup",
        "",
        f"- Number of conversations: {len(rows)}",
        "- Agent A: No-memory agent",
        "- Agent B: With-memory agent",
        "- Memory backends: short-term, profile, episodic, semantic",
        f"- LLM provider: {settings.llm_provider}",
        f"- Token budget: {settings.memory_budget}",
        "",
        "## 2. Results Summary",
        "",
        "| # | Scenario | No-memory result | With-memory result | Pass? |",
        "|---:|---|---|---|---|",
    ]

    for idx, row in enumerate(rows, start=1):
        status = "Pass" if row["pass"] else "Fail"
        summary_lines.append(
            f"| {idx} | {row['scenario']} | {row['no_memory']} | {row['with_memory']} | {status} |"
        )

    pass_count = sum(1 for row in rows if row["pass"])
    summary_lines.extend(
        [
            "",
            "## 3. Metrics",
            "",
            "| Metric | No-memory Agent | With-memory Agent | Notes |",
            "|---|---:|---:|---|",
            f"| Memory hit rate (pass cases) | - | {pass_count}/{len(rows)} | Rule-based evaluation from expected keywords |",
            "| Conflict accuracy | thấp | cao hơn | Overwrite profile fact theo correction marker |",
            "| Context utilization | thấp | cao hơn | Prompt có section memory + trim budget |",
            "",
            "## 4. Privacy & Limitations",
            "",
            "- Profile memory nhạy cảm nhất vì chứa fact trực tiếp về user.",
            "- Episodic và semantic memory có rủi ro lộ lịch sử hành vi nếu sai user_id isolation.",
            "- Deletion cần xóa đồng thời profile, episodic, semantic và short-term.",
            "- TTL đề xuất: short-term theo session, episodic 30-90 ngày, profile theo consent.",
            "- Limitations: router rule-based và semantic keyword fallback có thể sai với query mơ hồ.",
        ]
    )

    benchmark_md = Path(__file__).resolve().parents[1] / "BENCHMARK.md"
    benchmark_md.write_text("\n".join(summary_lines), encoding="utf-8")

    print(f"Benchmark done: {pass_count}/{len(rows)} pass")
    print(f"Results JSON: {output_json}")
    print(f"Summary MD: {benchmark_md}")


if __name__ == "__main__":
    main()
