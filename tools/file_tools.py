import os

def read_file(path: str) -> str:
    if not os.path.exists(path):
        return f"File not found: {path}"
    with open(path, 'r') as file:
        return file.read()

def create_file(path: str) -> str:
    open(path, 'a').close()
    return f"File created at {path}"

def delete_file(path: str) -> str:
    if os.path.exists(path):
        os.remove(path)
        return f"File deleted: {path}"
    return f"File does not exist: {path}"

def write_file(path: str, content: str) -> str:
    with open(path, 'w') as file:
        file.write(content)
    return f"Content written to {path}"
