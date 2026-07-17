"""Memory-loading workflow node."""

from ...memory.short_term import get_memory
from ..state import AgentState


def memory_node(state: AgentState) -> dict:
    print("➡️ Memory")
    memory = get_memory()
    trace = [*state.get("trace", []), f"🧠 Loaded {len(memory)} memory items"]
    return {"memory": memory, "trace": trace}
