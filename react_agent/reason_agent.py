from langchain_openai import ChatOpenAI
from langchain.agents import tool, create_react_agent
import datetime
from langchain_community.tools import TavilySearchResults
from langchain import hub
from dotenv import load_dotenv, find_dotenv


_ = load_dotenv(find_dotenv())
llm = ChatOpenAI(model="gpt-4o-mini")

@tool
def get_system_time(format: str = "%Y-%m-%d %H:%M:%S"):
    """ Returns the current date and time in the specified format """

    current_time = datetime.datetime.now()
    formatted_time = current_time.strftime(format)
    return formatted_time

search_tool = TavilySearchResults(search_depth="advanced", max_results=3)
react_prompt = hub.pull("hwchase17/react")
print(react_prompt)
exit(1)
tools = [get_system_time, search_tool]
react_agent_runnable = create_react_agent(tools=tools, llm=llm, prompt=react_prompt)