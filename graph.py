from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode

from state import AgentState
from nodes import planner_node, chatbot
from tools import TOOLS
from router import route_tools

builder = StateGraph(AgentState)

# Nodes
builder.add_node("planner", planner_node)
builder.add_node("chatbot", chatbot)
builder.add_node("tool", ToolNode(TOOLS))

# Start
builder.add_edge(START, "planner")

# Planner runs only once
builder.add_edge("planner", "chatbot")

# Chatbot decides
builder.add_conditional_edges(
    "chatbot",
    route_tools,
    {
        "tool": "tool",
        "end": END,
    },
)

# Tool returns to chatbot
builder.add_edge("tool", "chatbot")

graph = builder.compile()