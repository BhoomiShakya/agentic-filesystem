from tools.file_tools import write_file, create_file
import os

def write_agent(state: dict):
    path = state.get("path")
    content = state.get("content")

    if not os.path.exists(path):
        create_file(path)

    result = write_file(path, content)
    return {**state, "result": result}
