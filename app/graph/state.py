from typing import List, TypedDict
from typing_extensions import Annotated
import operator


class AgentState(TypedDict, total=False):
    question: str
    task: str
    tasks: List[str]
    findings: Annotated[List[str], operator.add]
    final_answer: str
