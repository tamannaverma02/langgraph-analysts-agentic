from dotenv import load_dotenv
from src.utils.states import GenerateAnalystState
from src.utils.models import llm
from src.utils.objects import Analyst, Perspectives
from src.utils.prompts import analyst_instructions
from langchain.messages import SystemMessage, HumanMessage
from langgraph.types import interrupt

load_dotenv()

#nodes 
def create_analyst(state: GenerateAnalystState): 
    """Create analysts"""

    topic = state["topic"]
    max_analyst = state["max_analysts"]
    human_analyst_feedback = state.get("human_analyst_feedback") or ""


    #structured output 
    structured_llm = llm.with_structured_output(Perspectives, method="function_calling")

    system_message = analyst_instructions.format(
        topic=topic,
        max_analyst=max_analyst,
        human_analyst_feedback=human_analyst_feedback
    )

    #generate analyst
    analyst = structured_llm.invoke([SystemMessage(content=system_message)]+[HumanMessage(content="Please generate the set of analyst")])

    return {"analysts": analyst.analysts}

def human_feedback(state: GenerateAnalystState):
    "This is where human give feedback on the generated analysts"
    ""
    feedback = interrupt({
        "question": "Are these analysis okay for you?",
        "analysts": [
            analyst.model_dump() if hasattr(analyst, "model_dump") else analyst for analyst in state.get("analysts", [])
        ],
        "instructions": "Please provide your feedback on the generated analysts. You can suggest improvements, point out any issues, or confirm if they meet your expectations. Or return empty/perfect/okay/none if you are satisfied with the generated analysts."
        
    })
    if feedback is None:
        return {"human_analyst_feedback": None}

    if isinstance(feedback, str):
        feedback = feedback.strip()
        if feedback == "":
            return {"human_analyst_feedback": None}

        if feedback.lower() in ["empty", "perfect", "okay", "none"]:
            return {"human_analyst_feedback": None}
        
        return {"human_analyst_feedback": feedback}
    return {"human_analyst_feedback": None}

