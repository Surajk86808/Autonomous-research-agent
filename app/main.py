from fastapi import FastAPI
from app.graph.build_graph import build_graph

app = FastAPI()

graph = build_graph()


@app.get("/")
def home():
    return {"status": "Agent Running"}


@app.get("/ask")
def ask_agent(question: str):

    result = graph.invoke({
        "question": question
    })

    return result

