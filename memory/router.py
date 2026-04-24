from __future__ import annotations


class MemoryRouter:
    def route(self, query: str) -> dict:
        q = query.lower()

        if any(x in q for x in ["tôi thích", "tôi không thích", "tôi dị ứng", "tên tôi là"]):
            return {
                "intent": "profile_update",
                "selected_backends": ["profile", "short_term"],
                "should_write_memory": True,
            }

        if any(x in q for x in ["à nhầm", "không phải", "sửa lại", "thay đổi"]):
            return {
                "intent": "profile_update",
                "selected_backends": ["profile", "episodic", "short_term"],
                "should_write_memory": True,
            }

        if any(x in q for x in ["lần trước", "hôm trước", "từng", "trước đó"]):
            return {
                "intent": "episodic_recall",
                "selected_backends": ["episodic", "semantic", "short_term"],
                "should_write_memory": False,
            }

        if any(x in q for x in ["gợi ý", "nên dùng", "recommend", "đề xuất"]):
            return {
                "intent": "profile_recall",
                "selected_backends": ["profile", "semantic", "short_term"],
                "should_write_memory": False,
            }

        if any(x in q for x in ["giải thích", "explain", "là gì"]):
            return {
                "intent": "general_query",
                "selected_backends": ["profile", "semantic", "short_term"],
                "should_write_memory": False,
            }

        if any(x in q for x in ["quên", "xóa memory", "xóa thông tin", "xóa tên"]):
            return {
                "intent": "forget_request",
                "selected_backends": ["profile", "episodic", "semantic", "short_term"],
                "should_write_memory": False,
            }

        if any(x in q for x in ["tôi bị lỗi", "tôi bị rối", "docker", "celery", "async"]):
            return {
                "intent": "semantic_recall",
                "selected_backends": ["semantic", "episodic", "short_term"],
                "should_write_memory": True,
            }

        return {
            "intent": "general_query",
            "selected_backends": ["short_term", "semantic"],
            "should_write_memory": False,
        }
