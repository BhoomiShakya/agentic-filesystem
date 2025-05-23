from graph.builder import graph

if __name__ == "__main__":
    input_data = {
        "action": "creat", 
        "path": "test_create.txt",
        "content":"this is my dummy text in test_create"
    }

    result = graph.invoke(input_data)
    print("Result:", result.get("result", "<no result>"))
