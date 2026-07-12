from llm import llm
from tools import TOOLS
from planner import create_plan

llm_with_tools = llm.bind_tools([*TOOLS])



def planner_node(state):

    question = state["messages"][-1].content

    plan = create_plan(question)

    trace = state.get("trace", [])

    trace.append("📋 Planner generated execution plan")

    print("\n===== PLAN =====")
    trace.append(f"📋 PLAN\n{plan}")

    return {
        "plan": plan,
        "trace": trace,
    }


def chatbot(state):
    trace = state.get("trace", [])

    trace.append("🧠 Chatbot node started")

    response = llm_with_tools.invoke(state["messages"])

    if response.tool_calls:
        tool_name = response.tool_calls[0]["name"]
        trace.append(f"🔧 Tool requested: {tool_name}")
    else:
        trace.append("💬 Generated final answer")

    return {
        "messages": [response],
        "trace": trace,
    }

def reflection_node(state):

    last_message = state["messages"][-1]

    if "ERROR:" in last_message.content:

        print("🔍 Reflection")

        print(last_message.content)

        return {
            "last_error": last_message.content,
            "retry_count": state.get("retry_count", 0) + 1
        }

    return {}