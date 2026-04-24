# Multi Memory Agent (Lab 17)

Project này triển khai **Multi-Memory Agent** theo yêu cầu Lab #17 với 4 lớp memory:

- Short-term memory (conversation buffer)
- Long-term profile memory (JSON KV)
- Episodic memory (JSONL event log)
- Semantic memory (keyword-search fallback)

## Cấu trúc chính

- `main.py`: CLI chat và hỏi một câu
- `graph.py`: orchestrator flow classify → retrieve → build context → answer → write
- `agent/`: state, prompts, nodes
- `memory/`: 4 memory backend + router + context manager
- `benchmark/`: 10 multi-turn test cases + benchmark runner
- `scripts/`: seed/reset memory

## Cài đặt

```bash
pip install -r requirements.txt
cp .env.example .env
```

Sau đó cập nhật `.env`:

```env
LLM_PROVIDER=openai
OPENAI_API_KEY=your_real_openai_key
OPENAI_MODEL=gpt-4o-mini
```

## Chạy demo chat

```bash
python main.py chat --user-id demo_user
```

## Hỏi một câu

```bash
python main.py ask "Tôi tên gì?" --user-id demo_user
python main.py ask "Tôi tên gì?" --user-id demo_user --no-memory
```

## Seed / Reset memory

```bash
python scripts/seed_memory.py --user-id demo_user
python scripts/reset_memory.py --user-id demo_user
```

## Benchmark

```bash
python benchmark/run_benchmark.py
```

Nếu chạy bằng OpenAI thật, benchmark sẽ tốn token/cost tùy số lượng case.

Kết quả sẽ được ghi vào:

- `benchmark/results.json`
- `BENCHMARK.md`

## Reflection privacy/limitations

- Profile memory nhạy cảm nhất vì chứa dữ liệu trực tiếp của user.
- User có quyền yêu cầu xóa dữ liệu trên toàn bộ backend (`profile`, `episodic`, `semantic`, `short-term`).
- TTL đề xuất: short-term theo session, episodic 30-90 ngày, profile theo consent.
- Limitation hiện tại: router rule-based và semantic keyword fallback có thể bỏ sót ngữ nghĩa phức tạp.
# 2A202600303-Day17
