from dotenv import load_dotenv
from src.utils.states import GenerateAnalystState
from typing import Literal
from langgraph.graph import END
load_dotenv()

# coditional edges  -> define where to go after feedback 
def should_continue(state: GenerateAnalystState) -> Literal["create_analysts", END]:
    """Return the next node to execute"""

    human_analyst_feedback = state.get("human_analyst_feedback",None)
    if human_analyst_feedback:
        return "create_analysts"

    return END

