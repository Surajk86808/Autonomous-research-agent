from app.graph.build_graph import build_graph

def test():
    graph = build_graph()
    result = graph.invoke({"question": "test"})
    print("Result:")
    print(result)

if __name__ == "__main__":
    test()
