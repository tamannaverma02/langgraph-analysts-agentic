from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os 

load_dotenv()  

llm = ChatOpenAI(
    model="deepseek-chat",
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url=os.getenv("DEEPSEEK_BASE_URL"),
    temperature=0,
)
