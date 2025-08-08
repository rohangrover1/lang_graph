from typing import List, Sequence
from dotenv import load_dotenv, find_dotenv
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langgraph.graph import END, MessageGraph
from chains import generation_chain, reflection_chain
import os

REFLECT = "reflect"
GENERATE = "generate"
graph = MessageGraph()

# set the envionment variables
_ = load_dotenv(find_dotenv())
os.environ["LANGSMITH_TRACING"] = "true"
os.environ["LANGSMITH_PROJECT"] = "default"

def generate_node(state):
    print("{} inside generate {}".format("*"*20, "*"*20))
    print(f"STATE-TYPE={type(state)} LEN={len(state)}")
    print("{}\n STATE:{} \n{}".format("^"*20, state, "^"*20))

    response = generation_chain.invoke({
        "messages": state
    })
    print(f"STATE-TYPE={type(state)} LEN={len(state)}")
    print(response.content)
    print("{} exiting generate {}".format("*"*20, "*"*20))
    return response
    


def reflect_node(state):
    print("{} inside reflect {}".format("*"*20, "*"*20))
    print("{}\n STATE:{} \n{}".format("^"*20, state, "^"*20))
    print(f"STATE-TYPE={type(state)} LEN={len(state)}")
    response = reflection_chain.invoke({
        "messages": state
    })
    print(f"STATE-TYPE={type(state)} LEN={len(state)}")
    print(response.content)
    print("{} exiting reflect {}".format("*"*20, "*"*20))
    return [HumanMessage(content=response.content)]
    #return [AIMessage(content=response.content)]


graph.add_node(GENERATE, generate_node)
graph.add_node(REFLECT, reflect_node)
graph.set_entry_point(GENERATE)

def should_continue(state):
    if (len(state) > 2):
        return END 
    return REFLECT

graph.add_conditional_edges(GENERATE, should_continue)
graph.add_edge(REFLECT, GENERATE)
app = graph.compile()

print(app.get_graph().draw_mermaid())
app.get_graph().print_ascii()
response = app.invoke(HumanMessage(content="AI Agents taking over content creation"))
#print(response)

# print the response in readble format
print("{} FINAL RESPONSE {}".format("+"*20, "+"*20))
n = 0
for mssg in response:
    print("{} MSSG COUNT={} {}".format("*"*20, n, "*"*20))
    print(type(mssg))
    print(mssg.content)
    n+=1

