from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv, find_dotenv
from langchain.agents import initialize_agent, tool
from langchain_community.tools import TavilySearchResults
from datetime import datetime

# load the environment variables
_ = load_dotenv(find_dotenv())

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")

# test
# result = llm.invoke("give me a fact about cats")
# print(result.content)

# # hallucinating
# result = llm.invoke("give me a tweet about the weather in Bangalore")
# print(result.content)

search_tool = TavilySearchResults(search_depth="basic")
tools = [search_tool]

# langchain agent with basic search
#agent = initialize_agent(tools=tools, llm=llm, agent="zero-shot-react-description", verbose=True)
#agent.invoke("give me a tweet about the weather in Boston")


# langchain agent with basic search and local time
#agent = initialize_agent(tools=tools, llm=llm, agent="zero-shot-react-description", verbose=True)
#agent.invoke("When was SpaceX's last launch relative to my time")
''' Output:
Thought:The search results indicate that the most recent SpaceX launch mentioned is the Starship Flight 9 launch. 
Multiple articles refer to it happening around May 27-28, 2025. Since I don't have the current date, I can't give an exact time relative to "now."
Final Answer: The most recent SpaceX launch mentioned in the search results is Starship Flight 9, which occurred around 
May 27-28, 2025. I am unable to give you the exact time relative to your current time, as I do not have that information.
'''

@tool
def get_current_system_time(format:str="%Y-%m-%d: %H:%M:%S")->str:
    "Return the current date and time in specified format"
    current_time = datetime.now()
    formatted_time = current_time.strftime(format)
    return formatted_time

tools = [search_tool, get_current_system_time]
agent = initialize_agent(tools=tools, llm=llm, agent="zero-shot-react-description", verbose=True)
agent.invoke("When was SpaceX's last launch relative to my time")
