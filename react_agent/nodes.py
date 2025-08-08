from reason_agent import react_agent_runnable, tools
from react_state import AgentState
import json

def reason_node(state: AgentState):
    print("REASON NODE:\n\tinput={} \n\tagent_outcome={} \n\tlen-intermediate_steps={}\n".format(
        state["input"], state["agent_outcome"],len(state["intermediate_steps"])))
    agent_outcome = react_agent_runnable.invoke(state)
    return {"agent_outcome": agent_outcome}


def act_node(state: AgentState):
    print("ACT NODE: \n\tinput={} \n\tagent_outcome={} \n\tlen-intermediate_steps={}\n".format(
        state["input"], state["agent_outcome"],len(state["intermediate_steps"])))
    agent_action = state["agent_outcome"]
    
    # Extract tool name and input from AgentAction
    tool_name = agent_action.tool
    tool_input = agent_action.tool_input
    
    # Find the matching tool function
    tool_function = None
    for tool in tools:
        if tool.name == tool_name:
            tool_function = tool
            break
    
    # Execute the tool with the input
    if tool_function:
        if isinstance(tool_input, dict):
            output = tool_function.invoke(**tool_input)
        else:
            output = tool_function.invoke(tool_input)
    else:
        output = f"Tool '{tool_name}' not found"
    
    print("TOOL OUTPUT")
    if isinstance(output, list):
        for mssg in output:
            print(f"\ttool-output={mssg}")
    else:
        print(f"\ttool-output={output}")
    return {"intermediate_steps": [(agent_action, str(output))]}