from typing import TypedDict
from langgraph.graph import StateGraph
from agents.filesystem_agent import filesystem_agent
from agents.write_agent import write_agent

class AgentState(TypedDict):
    action: str
    path: str
    content: str
    result: str  # Optional: to store final output

builder = StateGraph(AgentState)

builder.add_node("filesystem_agent", filesystem_agent)
builder.add_node("write_agent", write_agent)

def end_node(state: dict) -> dict:
    return state

builder.add_node("end_node", end_node)

builder.set_entry_point("filesystem_agent")
builder.add_conditional_edges(
    "filesystem_agent",
    lambda state: "write_agent" if state["action"] == "write" else "end_node",
    {
        "write_agent": "write_agent",
        "end_node": "end_node"  # virtual terminator node
    }
)

builder.set_finish_point("write_agent")
builder.set_finish_point("end_node")  # finish path for read/delete/create
graph = builder.compile()
