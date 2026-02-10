import os
import re
import json
from dotenv import load_dotenv
from google import genai

from langgraph.graph import StateGraph, END 
from app.graph.state import AgentState
from app.tools.web_search import search_web

from app.memory.vector_db import store_memory, get_memories
import time
from app.llm.router import router
from langgraph.types import Send




load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# New Gemini client
client = genai.Client(api_key=GEMINI_API_KEY)


class LLM:
    def __init__(self, model: str):
        self.model = model

    def invoke(self, prompt: str):

        for attempt in range(3):
            try:
                response = client.models.generate_content(
                    model=self.model,
                    contents=prompt
                )
                return response.text

            except Exception as e:

                if "429" in str(e):
                    time.sleep(5)
                else:
                    raise e

        raise Exception("LLM failed after retries")


print("PLANNER RUNNING")

def planner_node(state: AgentState):
    question = state.get("question", "").strip()

    prompt = f"""
     You are an expert research planner.

        Your job is to break a complex question into smaller,
        independent research questions.

        RULES:

        - Generate between 3  sub-questions.
        - Each must focus on ONE research angle.
        - Do NOT repeat the original question.
        - Do NOT rephrase it.
        - Make them specific and researchable.
        - Cover different perspectives (technology, jobs, economy, future, risks).

        Return ONLY valid JSON.

        Example format:
        {{ 
        "tasks": [
            "What are the current capabilities of AI in software development?",
            "How is AI impacting the demand for software engineers?",
            "What limitations prevent AI from fully replacing engineers?",
            "How might the role of engineers evolve with AI tools?",
            "What do experts predict about AI and programming jobs?"
        ]
        }}

    Question:
    {question}
    """

    response = router.gemini(prompt)

    match = re.search(r"\{.*\}", response, re.DOTALL)

    if not match:
        tasks = [question]
    else:
        try:
            data = json.loads(match.group())
            tasks = data.get("tasks", [question])
        except:
            tasks = [question]

    #PARALLEL MAGIC HERE
    return {
        "question": question,
        "tasks": tasks
    }


def route_to_research(state: AgentState):
    tasks = state.get("tasks", [])
    return [Send("research", {"task": task}) for task in tasks]


print("RESEARCH RUNNING")
def research_node(state: AgentState):
    print("STATE IN RESEARCH:", state)
    task = state.get("task")
    if not task:
        print("TASK IS EMPTY — STATE BROKEN")

    print("RESEARCH TASK:", task)
    # Try memory first
    past_knowledge = get_memories(task, limit=2)

    if past_knowledge:

        prompt = f"""
        Use past research to answer.

        Question:
        {task}

        Past:
        {past_knowledge}
        """

        result = router.gemini(prompt)

    else:

        web_data = search_web(task)
        web_data = web_data[:4000]

        prompt = f"""
        Answer using this web data.

        Question:
        {task}

        Web Data:
        {web_data}
        """

        result = router.groq(prompt)
        print("RESULT:", result)

        store_memory(result)

    # ALWAYS RETURN LIST
    return {
        "findings": [result]
        }



def synthesizer_node(state: AgentState):
    print("FINAL STATE:", state)
    return {}




def build_graph():

    builder = StateGraph(AgentState)

    builder.add_node("planner", planner_node)
    builder.add_node("research", research_node)
    builder.add_node("synthesizer", synthesizer_node)

    builder.set_entry_point("planner")

    builder.add_conditional_edges("planner", route_to_research, ["research"])

    # research → synthesizer
    builder.add_edge("research", "synthesizer")

    # synthesizer → END
    builder.add_edge("synthesizer", END)

    return builder.compile()


