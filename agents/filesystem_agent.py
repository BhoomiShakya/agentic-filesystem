from tools.file_tools import read_file, write_file, create_file, delete_file

def filesystem_agent(state: dict):
    action = state.get("action")
    path = state.get("path")
    content = state.get("content", "")

    if action == "read":
        result = read_file(path)
    elif action == "write":
        # write_agent will handle this
        return state  # Pass state to write_agent via conditional edge
    elif action == "create":
        result = create_file(path)
    elif action == "delete":
        result = delete_file(path)
    else:
        result = f"Unknown action: {action}"

    return {**state, "result": result}
