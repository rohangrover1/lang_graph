from typing import TypedDict, Annotated
from langgraph.graph import add_messages, StateGraph, END
#from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, HumanMessage
from dotenv import load_dotenv, find_dotenv
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.load import dumps
import os

_ = load_dotenv(find_dotenv())
os.environ["LANGSMITH_TRACING"] = "true"
os.environ["LANGSMITH_PROJECT"] = "default"
llm = ChatOpenAI(model="gpt-4o-mini")
# llm = ChatGroq(model="llama-3.1-8b-instant")

memory = MemorySaver()                  # in memory saver 

class BasicChatState(TypedDict):
    messages: Annotated[list, add_messages]

def chatbot(state: BasicChatState):
    return {
        "messages": [llm.invoke(state["messages"])]
    }

graph = StateGraph(BasicChatState)

graph.add_node("chatbot", chatbot)
graph.set_entry_point("chatbot")
graph.add_edge("chatbot", END)
app = graph.compile(checkpointer=memory)

# create thread id
config = {"configurable": {
    "thread_id": 1
}}

while True: 
    user_input = input("User: ")
    if(user_input in ["exit", "end"]):
        break
    else: 
        result = app.invoke({
            "messages": [HumanMessage(content=user_input)]              # now we retain memory
        }, config=config)

        print(dumps(app.get_state(config=config)))
        print("AI: " + result["messages"][-1].content)
        

#print(dumps(app.get_state(config=config)))