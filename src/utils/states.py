from typing_extensions import TypedDict, NotRequired, List, Annotated
from typing import Optional
from src.utils.objects import Analyst
from langgraph.graph import MessagesState
import operator 

class GenerateAnalystState(TypedDict):
    topic: str #research topic
    max_analysts: int # number of analysts
    human_analyst_feedback: NotRequired[Optional[str]] #human feedback on the generated analysts
    analysts: NotRequired[List[Analyst]] #list of all analysts


class InterviewState(MessagesState):
    max_num_turs: int # maximum number of turns in conversation
    context: Annotated[list, operator.add] # add new interview content without replacing using reducer add -> sourec of doc interviewer will use
    analyst: Analyst # the analyst that is being interviewed
    interview: str  #interview transcription
    sections: list # duplicate in outer stste for Send() api
    
