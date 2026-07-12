from langchain_core.messages import HumanMessage
from graph import graph

result = graph.invoke(
    {
        "messages": [
            HumanMessage(
                content="Show  5 Point summary of sales and outlier in next responce"
            )
        ],
        "trace": []
    }
)

print("\n===== AGENT TRACE =====")

for step in result["trace"]:
    print(step)


print("\n========== ANSWER ==========")
print(result["messages"][-1].content)