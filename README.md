
# 🧠 Agentic Filesystem with LangGraph

A modular, agentic AI-powered filesystem built using [LangGraph](https://docs.langgraph.dev/). This project demonstrates how intelligent agents can be orchestrated using a graph structure to perform file operations such as **create**, **write**, **read**, and **delete**, with reusable tools and autonomous flow control.

---

## 🚀 Features

- ✅ **Agent-based architecture** using LangGraph
- 📂 Intelligent handling of file operations (`create`, `write`, `read`, `delete`)
- ♻️ Reusable tools — file utilities are not tightly coupled to any agent
- 📈 Conditional routing and execution using LangGraph’s `StateGraph`
- ✅ Final state termination node to prevent infinite recursion

---

## 📁 Project Structure

```
filesystem-agent/
│
├── agents/
│   ├── filesystem_agent.py     # Main decision-maker (routes to tool based on action)
│   └── write_agent.py          # Write-specific logic
│
├── tools/
│   └── file_tools.py           # Reusable file operation tools
│
├── graph/
│   └── builder.py              # LangGraph graph setup with conditional edges
│
├── main.py                     # Entry point with sample invocation
├── README.md                   # This file
```

---

## 🧩 Agents

### `filesystem_agent.py`
The router agent. Determines which tool or agent should handle the operation based on the `action` field.

```python
def filesystem_agent(state: dict) -> dict:
    action = state.get("action")
    
    if action == "create":
        result = create_file(state["path"])
    elif action == "read":
        result = read_file(state["path"])
    elif action == "delete":
        result = delete_file(state["path"])
    elif action == "write":
        return state  # Let write_agent handle it
    else:
        result = f"Unknown action: {action}"

    return {**state, "result": result}
```

### `write_agent.py`
Handles writing content to a file and creates the file if it does not exist.

```python
def write_agent(state: dict) -> dict:
    path = state.get("path")
    content = state.get("content")

    if not os.path.exists(path):
        create_file(path)

    result = write_file(path, content)
    return {**state, "result": result}
```

---

## 🛠 Tools (`tools/file_tools.py`)

These are simple, reusable Python functions:

```python
def create_file(path: str) -> str:
    open(path, 'a').close()
    return f"File created at {path}"

def delete_file(path: str) -> str:
    if os.path.exists(path):
        os.remove(path)
        return f"File deleted: {path}"
    return f"File does not exist: {path}"

def read_file(path: str) -> str:
    if not os.path.exists(path):
        return f"File not found: {path}"
    with open(path, 'r') as file:
        return file.read()

def write_file(path: str, content: str) -> str:
    with open(path, 'w') as file:
        file.write(content)
    return f"Content written to {path}"
```

---

## 🔁 Graph Setup (`graph/builder.py`)

Using `LangGraph` to define the state and conditional transitions.

```python
from langgraph.graph import StateGraph
from agents.filesystem_agent import filesystem_agent
from agents.write_agent import write_agent

class AgentState(TypedDict):
    action: str
    path: str
    content: str

builder = StateGraph(AgentState)

builder.add_node("filesystem_agent", filesystem_agent)
builder.add_node("write_agent", write_agent)
builder.add_node("end_node", lambda state: state)

builder.set_entry_point("filesystem_agent")

builder.add_conditional_edges(
    "filesystem_agent",
    lambda state: "write_agent" if state.get("action") == "write" else "end_node",
    {
        "write_agent": "write_agent",
        "end_node": "end_node"
    }
)

builder.add_edge("write_agent", "end_node")

graph = builder.compile()
```

---

## ▶️ How to Run

### 1. Create Virtual Environment

```bash
python -m venv filesystemagent
source filesystemagent/bin/activate  # On Windows use: .\filesystemagent\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install langgraph
```

### 3. Run Main

Modify `main.py` with any action you want to test:

```python
from graph.builder import graph

if __name__ == "__main__":
    input_data = {
        "action": "read",  # "write", "create", "delete"
        "path": "test.txt"
    }

    result = graph.invoke(input_data)
    print("Result:", result.get("result", "<no result>"))
```

Then run:

```bash
python main.py
```

---

## ✅ Example Actions

### ➕ Create File

```python
{ "action": "create", "path": "test.txt" }
```

### 📝 Write to File

```python
{ "action": "write", "path": "test.txt", "content": "Hello from LangGraph!" }
```

### 📖 Read File

```python
{ "action": "read", "path": "test.txt" }
```

### ❌ Delete File

```python
{ "action": "delete", "path": "test.txt" }
```

---

## 📌 TODOs

- [ ] Add logging or tracing
- [ ] Add support for append operation
- [ ] Add web or CLI interface

---

## 🤝 Contributions

Pull requests welcome. For major changes, please open an issue first to discuss what you would like to change.

---
