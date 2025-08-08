from dotenv import load_dotenv, find_dotenv
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated
import operator
from langchain_core.messages import AnyMessage, SystemMessage, HumanMessage, ToolMessage
from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults

_ = load_dotenv(find_dotenv())

class AgentState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]
    #messages: Annotated[list[str], operator.add]



class Agent:

    def __init__(self, model, tools, system=""):
        self.system = system
        graph = StateGraph(AgentState)
        graph.add_node("llm", self.call_openai)
        graph.add_node("action", self.take_action)
        graph.add_conditional_edges(
            "llm",
            self.exists_action,
            {True: "action", False: END}
        )
        graph.add_edge("action", "llm")
        graph.set_entry_point("llm")
        self.graph = graph.compile()
        self.tools = {t.name: t for t in tools}
        self.model = model.bind_tools(tools)

    def exists_action(self, state: AgentState):
        result = state['messages'][-1]
        return len(result.tool_calls) > 0

    def call_openai(self, state: AgentState):
        messages = state['messages']
        if self.system:
            messages = [SystemMessage(content=self.system)] + messages
        message = self.model.invoke(messages)
        return {'messages': [message]}

    def take_action(self, state: AgentState):
        tool_calls = state['messages'][-1].tool_calls
        results = []
        for t in tool_calls:
            print(f"Calling: {t}")
            if not t['name'] in self.tools:      # check for bad tool name from LLM
                print("\n ....bad tool name....")
                result = "bad tool name, retry"  # instruct LLM to retry if bad
            else:
                result = self.tools[t['name']].invoke(t['args'])
            results.append(ToolMessage(tool_call_id=t['id'], name=t['name'], content=str(result)))
        print("Back to the model!")
        return {'messages': results}

if __name__ == "__main__":
    tool = TavilySearchResults(max_results=4) #increased number of results
    print(type(tool))
    print(tool.name)

    # understanding AgentState
    # Initialize an agent state
    agent1_state = AgentState(messages=["Hello", "How are you?"])
    print(agent1_state["messages"])

    # Another agent state
    agent2_state = AgentState(messages=["I'm an agent", "I can help you"])
    print(agent2_state["messages"])

    # When combining states, the messages lists would be concatenated
    # due to the operator.add annotation
    combined_messages = agent1_state["messages"] + agent2_state["messages"]
    print(type(combined_messages))
    print(combined_messages)



    