"""Reflection workflow node."""

from ..state import AgentState


def reflection_node(state: AgentState) -> dict:
    print("➡️ Reflection")
    tool_results = state.get("tool_results", [])

    if not tool_results:
        return {}

    latest = tool_results[-1]
    if latest.status == "success":
        return {"last_error": None}

    return {
        "retry_count": state.get("retry_count", 0) + 1,
        "last_error": latest.message,
    }
