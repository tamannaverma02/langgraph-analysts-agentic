from typing_extensions import TypedDict, NotRequired, List
from typing import Optional
from src.utils.objects import Analyst

class GenerateAnalystState(TypedDict):
    topic: str #research topic
    max_analysts: int # number of analysts
    human_analyst_feedback: NotRequired[Optional[str]] #human feedback on the generated analysts
    analysts: NotRequired[List[Analyst]] #list of all analysts
