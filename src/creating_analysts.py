from src.utils.nodes import create_analyst, human_feedback
from src.utils.edges import should_continue
from langgraph.graph import START, END, StateGraph
from src.utils.states import GenerateAnalystState
from dotenv import load_dotenv

load_dotenv()

# create graph 
# state - GenerateAnalystState 
# nodes
# edges
builder = StateGraph(GenerateAnalystState)

builder.add_node("create_analysts", create_analyst)
builder.add_node("human_feedback", human_feedback)

builder.add_edge(START, "create_analysts")
builder.add_edge("create_analysts", "human_feedback")
builder.add_conditional_edges("human_feedback", should_continue) 

graph = builder.compile()

