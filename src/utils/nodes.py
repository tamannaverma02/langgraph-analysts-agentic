from dotenv import load_dotenv
from src.utils.states import GenerateAnalystState, InterviewState
from src.utils.models import llm
from src.utils.objects import Analyst, Perspectives, SearchQuery
from src.utils.prompts import analyst_instructions, question_instructions, search_instructions, answer_instructions, section_writer_instructions
from langchain.messages import SystemMessage, HumanMessage
from langgraph.types import interrupt
from langchain_tavily import TavilySearch
from langchain_core.messages import get_buffer_string

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

def generate_question(state: InterviewState):
    """node to generate question"""

    #get state analyst 
    analyst = state["analyst"]
    if isinstance(analyst, dict):
        analyst = Analyst.model_validate(analyst)

    messages = state["messages"]

    # generate question 
    system_message = question_instructions.format(
        goals=analyst.persona
    )
    question = llm.invoke([SystemMessage(content=system_message)]+messages)

    return {"messages": [question]}

def search_web(state: InterviewState):
    """Retrieve docs from web"""

    # Search query 
    #force llm to produce structured output
    structured_llm = llm.with_structured_output(SearchQuery, method="function_calling")

    #search instruction system message
    search_instruction_system_messge = SystemMessage(content= search_instructions)

    #instructions and messages till now 
    search_query = structured_llm.invoke([search_instruction_system_messge] + state["messages"])

    # search 
    tavily_search = TavilySearch(max_results=3)
    data = tavily_search.invoke({"query":search_query.search_query})
    search_docs = data.get("results",data)

    #format
    formatted_search_docs = " \n\n---\n\n".join(
        [
            f'<Document href="{doc["url"]}/>\n{doc["content"]}\n</Documnet>'
            for doc in search_docs
        ]
    )

    return {"context": [formatted_search_docs]}

def search_web2(state: InterviewState):
    """Retrieve docs from web 2nd node"""

    # Search query 
    #force llm to produce structured output
    structured_llm = llm.with_structured_output(SearchQuery, method="function_calling")

    #search instruction system message
    search_instruction_system_messge = SystemMessage(content= search_instructions)

    #instructions and messages till now 
    search_query = structured_llm.invoke([search_instruction_system_messge] + state["messages"])

    # search 
    tavily_search = TavilySearch(max_results=3)
    data = tavily_search.invoke({"query":search_query.search_query})
    search_docs = data.get("results",data)

    #format
    formatted_search_docs = " \n\n---\n\n".join(
        [
            f'<Document href="{doc["url"]}/>\n{doc["content"]}\n</Documnet>'
            for doc in search_docs
        ]
    )

    return {"context": [formatted_search_docs]}

def generate_answer(state:InterviewState):
    """Node to answer questions"""

    #get state 
    analyst = state["analyst"]
    messages = state["messages"]
    context = state["context"]

    if isinstance(analyst,dict):
        analyst = Analyst.model_validate(analyst)

    #answer qyestion 
    system_message = answer_instructions.format(
        goals = analyst.persona,
        context = context
    )
    answer = llm.invoke([SystemMessage(content=system_message)] + messages)

    #name the message coimg from expert 
    answer.name  = "expert"

    #append interview to state 
    return {"messages": [answer]}

def save_interview(state:InterviewState):
    """save interview"""

    messages = state["messages"]
    interview = get_buffer_string(messages)


    return {"interview": interview}

def write_section(state:InterviewState):
    """node to answer a question """

    interview = state["interview"]
    context = state["context"]
    analyst = state["analyst"]

    if isinstance(analyst,dict):
        analyst = Analyst.model_validate(analyst)

    system_message = section_writer_instructions.format(
        focus = analyst.description
    )
    section = llm.invoke([SystemMessage(content=system_message)]+
                         [HumanMessage(content= f"Use this source to write your section: {context}")])

    return {"sections": [section.content]}


    