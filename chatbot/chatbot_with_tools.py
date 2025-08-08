from typing import TypedDict, Annotated
from langgraph.graph import add_messages, StateGraph, END
#from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from dotenv import load_dotenv, find_dotenv
from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.prebuilt import ToolNode
import json
from langchain_core.load import dumps
from langchain_core.tools import tool
from langchain import hub
import os
import datetime

_ = load_dotenv(find_dotenv())
os.environ["LANGSMITH_TRACING"] = "true"
os.environ["LANGSMITH_PROJECT"] = "default"

#llm = ChatOpenAI(model="gpt-4o-mini")
# llm = ChatGroq(model="llama-3.1-8b-instant")

# react_prompt = hub.pull("hwchase17/react")
# print(dumps(react_prompt))
# exit(-1)


class BasicChatBot(TypedDict):
    messages: Annotated[list, add_messages]

@tool
def get_system_time(format: str = "%Y-%m-%d %H:%M:%S"):
    """ Returns the current date and time at user location in the specified format """

    current_time = datetime.datetime.now()
    formatted_time = current_time.strftime(format)
    return formatted_time

@tool
def get_location():
    """ Returns the location in string format """
    return "Boston, MA, USA"

search_tool = TavilySearchResults(max_results=2)
tools = [search_tool, get_system_time, get_location]
llm = ChatOpenAI(model="gpt-4o-mini")
llm_with_tools = llm.bind_tools(tools=tools)
tool_names = []
for tool in tools:
    tool_names.append(tool.name)
print(tool_names)

# # invocation check
# response = llm_with_tools.invoke("What is the weather in Boston")
# json_response = dumps(response)
# print(json_response)

def chatbot(state: BasicChatBot):
    return {
        "messages": [llm_with_tools.invoke(state["messages"])], 
    }

def tools_router(state: BasicChatBot):
    last_message = state["messages"][-1]                # should be of object of Class type AImessage
    print(dumps(last_message))
    print(type(last_message))

    if(hasattr(last_message, "tool_calls") and len(last_message.tool_calls) > 0):
        return "tool_node"
    else: 
        return "print_final_answer"

def print_final_answer(state: BasicChatBot):
    last_message = state["messages"][-1]                # should be of object of Class type AImessage
    if(hasattr(last_message, "content") and len(last_message.content) > 0):
        print(f"FINAL RESPONSE: {last_message.content}")    
    else:
        print("couldn't find last message")

tool_node = ToolNode(tools=tools)

graph = StateGraph(BasicChatBot)

graph.add_node("chatbot", chatbot)
graph.add_node("tool_node", tool_node)
graph.add_node("print_final_answer", print_final_answer)
graph.set_entry_point("chatbot")

graph.add_conditional_edges("chatbot", tools_router)
graph.add_edge("tool_node", "chatbot")
graph.add_edge("print_final_answer", END)

app = graph.compile()
print(app.get_graph().print_ascii())

# system_message = f"""
# "Answer the following questions as best you can. 
# You have access to the following tools:\n\n{tool_names}\n\n
# Use the following format:\n\n
# Question: the input question you must answer\n
# Thought: you should always think about what to do\n
# Action: the action to take, should be one of [{tool_names}]\n
# Action Input: the input to the action\nObservation: the result of the action\n... (this Thought/Action/Action Input/Observation can repeat 3 times)\n
# Thought: I now know the final answer\n
# Final Answer: the final answer to the original input question",
# """

system_message = f"""
"You are a friendly chatbot.
Answer the question as best you can. 
You have access to the following tools:\n\n{tool_names}\n\n
"""


while True: 
    user_input = input("User: ")
    if(user_input in ["exit", "end"]):
        break
    else: 
        result = app.invoke({
            "messages": [
                SystemMessage(content=system_message),
                HumanMessage(content=user_input)
                ]
        })

print("FINAL ANSWER")
print(dumps(result))





