import json
from typing import List, Dict, Any
from langchain_core.messages import AIMessage, BaseMessage, ToolMessage, HumanMessage
from langchain_community.tools import TavilySearchResults


# Create the Tavily search tool
tavily_tool = TavilySearchResults(max_results=2)

# Function to execute search queries from AnswerQuestion tool calls
def execute_tools(state: List[BaseMessage]) -> List[BaseMessage]:
    # state is a list of class of messages 
    print("starting execute Tools")     
    for mssg in state:
        print(type(mssg))

    last_ai_message: AIMessage = state[-1]

    print(f"num tool calls={len(last_ai_message.tool_calls)}")
    for tool_call in last_ai_message.tool_calls:
        print((tool_call['name']))
        print(tool_call.keys())
    
    # Extract tool calls from the AI message
    if not hasattr(last_ai_message, "tool_calls") or not last_ai_message.tool_calls:
        return []
    
    '''
    the tools for LLM are ReviseAnswer or AnswerQuestion which has this structure
                args": {
                    'answer': '', 
                    'search_queries': [
                            'AI tools for small business', 
                            'AI in small business marketing', 
                            'AI automation for small business'
                    ], 
                    'reflection': {
                        'missing': '', 
                        'superfluous': ''
                    }

    '''

    # Process the AnswerQuestion or ReviseAnswer tool calls to extract search queries
    tool_messages = []
    
    for tool_call in last_ai_message.tool_calls:
        if tool_call["name"] in ["AnswerQuestion", "ReviseAnswer"]:
            call_id = tool_call["id"]
            search_queries = tool_call["args"].get("search_queries", [])               
            
            # Execute each search query using the tavily tool
            query_results = {}
            for query in search_queries:
                result = tavily_tool.invoke(query)
                print(f"Tavily result type={type(result)}")
                print(f"Query={query}")
                query_results[query] = result
            
            # Create a tool message with the results
            tool_messages.append(
                ToolMessage(
                    content=json.dumps(query_results),
                    tool_call_id=call_id
                )
            )
    
    print(f"len tool message={len(tool_messages)}")
    print(f"Tool Message Type={type(tool_messages[0])}")
    print("exiting execute Tools")
    return tool_messages

# # Example usage
# test_state = [
#     HumanMessage(
#         content="Write about how small business can leverage AI to grow"
#     ),
#     AIMessage(
#         content="", 
#         tool_calls=[
#             {
#                 "name": "AnswerQuestion",
#                 "args": {
#                     'answer': '', 
#                     'search_queries': [
#                             'AI tools for small business', 
#                             'AI in small business marketing', 
#                             'AI automation for small business'
#                     ], 
#                     'reflection': {
#                         'missing': '', 
#                         'superfluous': ''
#                     }
#                 },
#                 "id": "call_KpYHichFFEmLitHFvFhKy1Ra",
#             }
#         ],
#     )
# ]

# Execute the tools
# results = execute_tools(test_state)

# print("Raw results:", results)
# if results:
#     parsed_content = json.loads(results[0].content)
#     print("Parsed content:", parsed_content)