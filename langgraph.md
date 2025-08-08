
- [Python packages](#python-packages)
  - [Typing package](#typing-package)
    - [TypeDict](#typedict)
    - [Annoted](#annoted)
- [LLM Tools](#llm-tools)
  - [Basic LLM Tools](#basic-llm-tools)
    - [Defining your own tool function](#defining-your-own-tool-function)
    - [Proprties of the tool](#proprties-of-the-tool)
  - [Tavily search](#tavily-search)
  - [Code Execution](#code-execution)
- [Common Langgraph \& Langchain](#common-langgraph--langchain)
  - [llm response in Langgraph, Langchain](#llm-response-in-langgraph-langchain)
    - [response with no tool calls](#response-with-no-tool-calls)
      - [input](#input)
      - [output](#output)
    - [response with tool calls](#response-with-tool-calls)
      - [input](#input-1)
      - [output](#output-1)
  - [Invoking the LLM](#invoking-the-llm)
    - [Invoking just the LLM](#invoking-just-the-llm)
    - [Structured output](#structured-output)
    - [Creating a chain before invoking](#creating-a-chain-before-invoking)
- [Langchain](#langchain)
  - [Agents in langchain](#agents-in-langchain)
  - [Document class](#document-class)
  - [Retirever tool in langchain](#retirever-tool-in-langchain)
- [Langgraph](#langgraph)
  - [MessageGraph](#messagegraph)
    - [Accessing properties of these message classes](#accessing-properties-of-these-message-classes)
    - [AIMessages details](#aimessages-details)
      - [tool\_calls attribute](#tool_calls-attribute)
    - [BaseMessage details](#basemessage-details)
    - [HumanMessage details](#humanmessage-details)
    - [ToolMessage details](#toolmessage-details)
  - [StateGraph](#stategraph)
    - [streammode](#streammode)
    - [graph end](#graph-end)
    - [updating graph state](#updating-graph-state)
  - [Subgraphs](#subgraphs)
    - [Option 1: Shared Schema](#option-1-shared-schema)
    - [Option 2: Different Schema](#option-2-different-schema)
  - [Streaming the app](#streaming-the-app)
  - [Seeing the graph](#seeing-the-graph)
  - [CheckPointers in Langgraph](#checkpointers-in-langgraph)
    - [In Memory checkpointer](#in-memory-checkpointer)
      - [How it works](#how-it-works)
    - [DB checkpointer (SqlLite3)](#db-checkpointer-sqllite3)
      - [How it works](#how-it-works-1)
  - [Interrupt class](#interrupt-class)
    - [Operations with Interrupt](#operations-with-interrupt)
    - [Interrupt while compiling](#interrupt-while-compiling)
  - [Command class in langgraph](#command-class-in-langgraph)
  - [Langgraph functions](#langgraph-functions)
    - [add\_messages](#add_messages)
    - [dumps](#dumps)
    - [ToolNode](#toolnode)

# Python packages
## Typing package
- Used in Langgraph extensively
`from typing import TypedDict, List, Annotated`

### TypeDict
- Allows creation of class which is a custom dict
- Usually used to represent the state of the Langgraph
- Example 
```python
from typing import TypedDict, List
class SimpleState(TypedDict):
    count: int
    sum: int
    history: List[int]
```

### Annoted 
- Allows lambda like function inside a TypeDict class
- Example
```python
class SimpleState(TypedDict):
    count: int
    sum: Annotated[int, operator.add]
    history: Annotated[List[int], operator.add]

# Without Annotate
def increment(state: SimpleState) -> SimplState
    new_count = state["count"]+1
    return {
        "count": new_count,
        "sum": state["sum"]+new_count
        "history":  state["history"] + [new_count]
    }

# With Annotate
def increment(state: SimpleState) -> SimpleState: 
    new_count = state["count"] + 1
    return {
        "count": new_count, 
        "sum": new_count, 
        "history": [new_count]
 }
```
- Annotate will perform the simple operation as defined by operator

# LLM Tools
## Basic LLM Tools
- use the bind_tools functions to give tools to the different llms
```python
from langchain_openai import ChatOpenAI
search_tool = TavilySearchResults(max_results=2)
tools = [search_tool]
llm = ChatOpenAI(model="gpt-4o-mini")
llm_with_tools = llm.bind_tools(tools=tools)
```
- bind_tools is native function supported by most llms like ChatOpenAI, ChatGroq
 
### Defining your own tool function
- The `@tool` decorator can convert a function into a tool
- Langgraph also has built in tools like Tavilty
```python
# own tool
@tool
def get_system_time(format: str = "%Y-%m-%d %H:%M:%S"):
    """ Returns the current date and time in the specified format """

    current_time = datetime.datetime.now()
    formatted_time = current_time.strftime(format)
    return formatted_time

#  Built in tool
search_tool = TavilySearchResults(max_results=2)
```

### Proprties of the tool
- The following properties of the tool can be extracted
  - Name
  - Description
  - Args
```python
print(get_system_time.name)
print(get_system_time.description)
print(get_system_time.args)
print(search_tool.name)
print(search_tool.description)
print(search_tool.args)
```
- You will see the following output
```
get_system_time
Returns the current date and time in the specified format
{'format': {'default': '%Y-%m-%d %H:%M:%S', 'title': 'Format', 'type': 'string'}}

tavily_search_results_json
A search engine optimized for comprehensive, accurate, and trusted results. Useful for when you need to answer questions about current events. Input should be a search query.
{'query': {'description': 'search query to look up', 'title': 'Query', 'type': 'string'}}
```

## Tavily search 
- Returns a list of dicts where list is the number of search results requested in Tavily setup. Each dict has the following keys
  - title: a title for the search result
  - url: the url returned for the search 
  - content: the data from the url
  - score: A score of some kind

## Code Execution
- Uses the `PythonREPLTool()` tool
```python
from langchain_experimental.tools import PythonREPLTool
python_repl_tool.invoke("x = 5; print(x)")
```

# Common Langgraph & Langchain
## llm response in Langgraph, Langchain
### response with no tool calls
- content has the answer from the message

#### input
```python
response = llm.invoke("Hi my name is rohan")
json_response = dumps(response)
print(json_response)
```
#### output
```json
{
        "content": "Hi Rohan! How can I assist you today?",
        "additional_kwargs": {
            "refusal": null
        },
        "response_metadata": {
            "token_usage": {
                "completion_tokens": 11,
                "prompt_tokens": 13,
                "total_tokens": 24,
                "completion_tokens_details": {
                    "accepted_prediction_tokens": 0,
                    "audio_tokens": 0,
                    "reasoning_tokens": 0,
                    "rejected_prediction_tokens": 0
                },
                "prompt_tokens_details": {
                    "audio_tokens": 0,
                    "cached_tokens": 0
                }
            },
            "model_name": "gpt-4o-mini-2024-07-18",
            "system_fingerprint": null,
            "id": "chatcmpl-BsRTLyXWqhEh1tferXl0Yw7z3kooz",
            "service_tier": "default",
            "finish_reason": "stop",
            "logprobs": null
        },
        "type": "ai",
        "id": "run--6473cefd-ff1f-4629-9c2e-12763b0430ce-0",
        "usage_metadata": {
            "input_tokens": 13,
            "output_tokens": 11,
            "total_tokens": 24,
            "input_token_details": {
                "audio": 0,
                "cache_read": 0
            },
            "output_token_details": {
                "audio": 0,
                "reasoning": 0
            }
        },
        "tool_calls": [],
        "invalid_tool_calls": []
    }

```

### response with tool calls
- content is empty
- tool_calls list has info about what tools to call

#### input
```python
response = llm_with_tools.invoke("What is the weather in Boston")
json_response = dumps(response)
print(json_response)
```
#### output
```json
{
        "content": "",
        "additional_kwargs": {
            "tool_calls": [
                {
                    "id": "call_kPvlkv9TMY2xfrHTJnZpBM7r",
                    "function": {
                        "arguments": "{\"query\":\"Boston weather\"}",
                        "name": "tavily_search_results_json"
                    },
                    "type": "function"
                }
            ],
            "refusal": null
        },
        "response_metadata": {
            "token_usage": {
                "completion_tokens": 19,
                "prompt_tokens": 85,
                "total_tokens": 104,
                "completion_tokens_details": {
                    "accepted_prediction_tokens": 0,
                    "audio_tokens": 0,
                    "reasoning_tokens": 0,
                    "rejected_prediction_tokens": 0
                },
                "prompt_tokens_details": {
                    "audio_tokens": 0,
                    "cached_tokens": 0
                }
            },
            "model_name": "gpt-4o-mini-2024-07-18",
            "system_fingerprint": null,
            "id": "chatcmpl-BsRh1SiaE1lc8fpc7LtSiV1DCvzaz",
            "service_tier": "default",
            "finish_reason": "tool_calls",
            "logprobs": null
        },
        "type": "ai",
        "id": "run--6ef562a8-1360-4af9-a6f3-7a49284f5512-0",
        "tool_calls": [
            {
                "name": "tavily_search_results_json",
                "args": {
                    "query": "Boston weather"
                },
                "id": "call_kPvlkv9TMY2xfrHTJnZpBM7r",
                "type": "tool_call"
            }
        ],
        "usage_metadata": {
            "input_tokens": 85,
            "output_tokens": 19,
            "total_tokens": 104,
            "input_token_details": {
                "audio": 0,
                "cache_read": 0
            },
            "output_token_details": {
                "audio": 0,
                "reasoning": 0
            }
        },
        "invalid_tool_calls": []
    }

```

## Invoking the LLM
- The LLM for a graph or chain can be invoked in multiple ways

### Invoking just the LLM
- Create the LLM, add tool to the LLM, add structure output to the LLM and invoke it
```python
llm = ChatGroq(model="llama-3.1-8b-instant")
llm.invoke(state["messages"])
# with tools 
search_tool = TavilySearchResults(max_results=2)
tools = [search_tool]
llm_with_tools = llm.bind_tools(tools=tools)
llm_with_tools.invoke(state["messages"])
# with structured output
class GradeQuestion(BaseModel):
    score: str = Field(
        description="Question is about the specified topics? If yes -> 'Yes' if not -> 'No'"
    )
structured_llm = llm.with_structured_output(GradeQuestion)
structured_llm.invoke(state["messages"])
```

### Structured output
- Force the LLM to output a fixed response or string or Literals
- Managed using the pydantic class
```python
# forces LLM to ouput next as a Literal and only these 3 values
class Supervisor(BaseModel):
    next: Literal["enhancer", "researcher", "coder"] = Field(
        description="Determines which specialist to activate next in the workflow sequence: "
                    "'enhancer' when user input requires clarification, expansion, or refinement, "
                    "'researcher' when additional facts, context, or data collection is necessary, "
                    "'coder' when implementation, computation, or technical problem-solving is required."
    )
    reason: str = Field(
        description="Detailed justification for the routing decision, explaining the rationale behind selecting the particular specialist and how this advances the task toward completion."
    )

response = llm.with_structured_output(Supervisor).invoke(messages)
goto = response.next
reason = response.reason
```
- LLM response with be a dict with the keys defined in the pydantic model

### Creating a chain before invoking
- Create a chain by adding a prompt to the LLM before invoking
```python
llm = ChatOpenAI(model="gpt-4o")
template = """Answer the question based on the following context and the Chathistory. Especially take the latest question into consideration:
Chathistory: {history}
Context: {context}
Question: {question}
"""
prompt = ChatPromptTemplate.from_template(template)
llm = ChatOpenAI(model="gpt-4o")
rag_chain = prompt | llm
response = rag_chain.invoke(
        {"history": history, "context": documents, "question": rephrased_question}
    )
generation = response.content.strip()
```
- `.strip` removes unnecessary content from the LLM response




# Langchain
## Agents in langchain
- Import pre-built agents using `langchain.agents` 
```python
from langchain.agents import tool, create_react_agent,
```
- In this example we create a react agent which return a runnable
- invoking the runnable outputs Agent state class such as
  - AgentAction
  - AgentFinish
  - None
- Input to the runnable is the State dict which is used to craete the StateGraph
```python
def reason_node(state: AgentState):
    agent_outcome = react_agent_runnable.invoke(state)
    return {"agent_outcome": agent_outcome}
```

## Document class
- Class for storing a piece of text and associated metadata
```python
docs = [
    Document(
        page_content="Peak Performance Gym was founded in 2015 by former Olympic athlete Marcus Chen. With over 15 years of experience in professional athletics, Marcus established the gym to provide personalized fitness solutions for people of all levels. The gym spans 10,000 square feet and features state-of-the-art equipment.",
        metadata={"source": "about.txt"}
    ),
    Document(
        page_content="Peak Performance Gym is open Monday through Friday from 5:00 AM to 11:00 PM. On weekends, our hours are 7:00 AM to 9:00 PM. We remain closed on major national holidays. Members with Premium access can enter using their key cards 24/7, including holidays.",
        metadata={"source": "hours.txt"}
    )
]
```
## Retirever tool in langchain
- The class is called `create_retriever_tool`
```python
from langchain.tools.retriever import create_retriever_tool
```
- Parameters
  - retriever (BaseRetriever) – The retriever to use for the retrieval
  - name (str) – The name for the tool. This will be passed to the language model, so should be unique and somewhat descriptive.
  - description (str) – The description for the tool. This will be passed to the language model, so should be descriptive.
  - document_prompt (Optional[BasePromptTemplate]) – The prompt to use for the document. Defaults to None.
  - document_separator (str) – The separator to use between documents. Defaults to “nn”.
  - response_format (Literal['content', 'content_and_artifact']) – The tool response format. If “content” then the output of the tool is interpreted as the contents of a ToolMessage. If “content_and_artifact” then the output is expected to be a two-tuple corresponding to the (content, artifact) of a ToolMessage (artifact being a list of documents in this case). Defaults to “content”.
- Example:
```python
db = Chroma.from_documents(docs, embedding_function)
retriever = db.as_retriever(search_type="mmr", search_kwargs = {"k": 3})
retriever_tool = create_retriever_tool(
    retriever,
    "retriever_tool",
    "Information related to Gym History & Founder, Operating Hours, Membership Plans, Fitness Classes, Personal Trainers, and Facilities & Equipment of Peak Performance Gym",
)
```


# Langgraph
## MessageGraph
- Stores a list of class of messages like AIMessage, HummanMessage, ToolMessage
- The 'state' object being passed as an argument is that list of messages
- Each of these message is a class on one of these types
  - <class 'langchain_core.messages.human.HumanMessage'>
  - <class 'langchain_core.messages.ai.AIMessage'>
  - <class 'langchain_core.messages.tool.ToolMessage'>
  - <class 'langchain_core.messages.base.BaseMessage'>
  
### Accessing properties of these message classes
- The content message is accessed via the 'content' attribute which is of type str
- print(state[0].content)

### AIMessages details
- Response message from the AI
#### tool_calls attribute
- List of dict which is the tool calls sent to LLM

### BaseMessage details
- A placegolder for all types of messages from and back from the AI

### HumanMessage details
- Message supposed to coming from the human input or intervention
- Attribute "content" has the final answer unless overridden by a tool call for formatting. Then answer gors into args of tool_calls

### ToolMessage details
- Message coming from call to different Tools
- Has the following JSON structure
```json
tool_calls=[
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
```

## StateGraph
- There is blueprint of a state provided as input which is passed to all nodes
- Blueprint is TypeDict or Dict
- The blueprint needs to be specified when graph is initialized

```python
graph = StateGraph(SimpleState)
```

- The state variable has to be initialized and passed to it when the graph is invoked
```python
state = {
    "count": 0
}
result = app.invoke(state)
```
### streammode
- Setting stream mode in invoking allows us to see intermediate states
- Code is `result = app.invoke(state, stream_mode="updates")`
- Setting `stream_mode="values"` lets us see the values of the intermediate states

### graph end
- Typically graph is terminated by END
- Another way to terminate on a node is to assign node as the end node
```python
graph.set_finish_point("xxx_node")
```
- `xxx_node` is the name of node

### updating graph state
- Not necessary to update all the variables/keys in a graph.
- Example
```python
# Define parent graph with different schema
class QueryState(TypedDict):
    query: str
    response: str

# Function to invoke subgraph
def search_agent(state: QueryState) -> Dict:
    # Transform from parent schema to subgraph schema
    subgraph_input = {
        "messages": [HumanMessage(content=state["query"])]
    }
    
    # Invoke the subgraph
    subgraph_result = search_app.invoke(subgraph_input)
    
    # Transform response back to parent schema
    assistant_message = subgraph_result["messages"][-1]
    return {"response": assistant_message.content}

# Create parent graph
parent_graph = StateGraph(QueryState)

# Add transformation node that invokes subgraph
parent_graph.add_node("search_agent", search_agent)

# Connect the flow
parent_graph.add_edge(START, "search_agent")
parent_graph.add_edge("search_agent", END)

# Compile parent graph
parent_app = parent_graph.compile()

# Run the parent graph
result = parent_app.invoke({"query": "How is the weather in Chennai?", "response": ""})
print(result)
```
- All variables need to be set at invocation time
- The `query` key is being set at invocation and `reponse` key is empty str
- The `response` key is being set at the LLM call but `query` is not being set 

## Subgraphs
- Graph calling another graph
  - Two ways of linking parent graph aand subgraphh
  
### Option 1: Shared Schema
- Both parent graph and subgraph (child graph) state machines share the same schema/keys
- Add subgraph as anode
```python
class ChildState(TypedDict):
    messages: Annotated[list, add_messages]
subgraph = StateGraph(ChildState)
search_app = subgraph.compile()
# Define parent graph with the same schema
class ParentState(TypedDict):
    messages: Annotated[list, add_messages]

# Create parent graph
parent_graph = StateGraph(ParentState)
# Add the subgraph as a node
parent_graph.add_node("search_agent", search_app)

```
  
### Option 2: Different Schema
- parent graph and subgraph (child graph have different schemas. Need to add a node function that translates back and forth between the two graphs
- Create a function that does the transformation and add the function as a node
  - As compared to the same schema where you can add the subgraph as a node directly
```python
class ChildState(TypedDict):
    messages: Annotated[list, add_messages]
subgraph = StateGraph(ChildState)
search_app = subgraph.compile()
# Define parent graph with different schema
class QueryState(TypedDict):
    query: str
    response: str

# Function to invoke subgraph
def search_agent(state: QueryState) -> Dict:
    # Transform from parent schema to subgraph schema
    subgraph_input = {
        "messages": [HumanMessage(content=state["query"])]
    }
    
    # Invoke the subgraph
    subgraph_result = search_app.invoke(subgraph_input)
    
    # Transform response back to parent schema
    assistant_message = subgraph_result["messages"][-1]
    return {"response": assistant_message.content}

# Create parent graph
parent_graph = StateGraph(QueryState)
```

## Streaming the app
- Instead of `invoke` we use `stream` to see realtime output from each node
```python
events = app.stream({
    "messages": [HumanMessage(content="What is the current weather in Boston?")]
}, config=config, stream_mode="values")

for event in events:
    event["messages"][-1].pretty_print()
```
- Need to print the events as they occur

## Seeing the graph
- Best way to see the graph is with Juypter notebook using 
```python
from IPython.display import Image, display
display(Image(app.get_graph().draw_mermaid_png()))
```

## CheckPointers in Langgraph
- Allow addition of memory to the LLM
- Stores the state so when you invoke the graph from the start it remembers previos conversations
- Can store in memory or in DB

### In Memory checkpointer
- Use `from langgraph.checkpoint.memory import MemorySaver` which is an in memory saver
- The dict is kept in memory, so the dictionary operations run as fast as a regular dictionary.
- Write to disk is delayed until close or sync (similar to gdbm's fast mode).
- Input file format is automatically discovered.
- Output file format is selectable between pickle, json, and csv.
 #### How it works
 - Init in memory saved `memory = MemorySaver()`
 - Provide to app when compiling `app = graph.compile(checkpointer=memory)`
 - Also needs a thread id to keep tabs of different chats defined via a config dict
```python
# create thread id
config = {"configurable": {
    "thread_id": 1
}}
result = app.invoke({
            "messages": [HumanMessage(content=user_input)]              # now we retain memory
        }, config=config)
```

### DB checkpointer (SqlLite3)
- Use `from langgraph.checkpoint.sqlite import SqliteSaver` which is an in Sql Lite memory saver creating a DB on disk
- Also needs `import sqlite3` from Python
- The dict is kept in hard drive, 
 #### How it works
 - Create a thread to SqlLite `sqlite_conn = sqlite3.connect("checkpoint.sqlite", check_same_thread=False)`
   - The `check_same_thread=False` allows different thread IDs to R?W into sqllite DB
 - Init in memory saved `memory = SqliteSaver(sqlite_conn)`
 - Provide to app when compiling `app = graph.compile(checkpointer=memory)`
 - Also needs a thread id to keep tabs of different chats defined via a config file
```python
# create thread id
config = {"configurable": {
    "thread_id": 1
}}
result = app.invoke({
            "messages": [HumanMessage(content=user_input)]              # now we retain memory
        }, config=config)
```

## Interrupt class
- Interrupt the graph to take human feedback
- Exits the graph and graph needs to be restarted from the `START`
- Needs memory checkpointer to save the graph state on interrupt because we exit the graph
- Code is `human_response = interrupt("Do you want to go to C or D? Type C/D")`
- Behave similar to `input()`
- When we call interupt it exits the graph altogther and graph needs to be resumed using the invoke function and the keyword `resume`
- Code is `app.invoke(Command(resume="C"), config=config, stream_mode="updates")`
- `resume=xxx` is the response to the `interrupt` or answer to `input` 
- To see the next state of where graph stopped when can call the `get_state` function with the config which has the thread_id 
```python
print(app.get_state(config).next)
```
- Can only use `app.invoke` for `interrupt` and not `app.stream` to resume the graph

### Operations with Interrupt
1. Resume: Pause, take input and resume without changing state
2. Update and Resume: Update state and continue execution
3. Rewind/Time-Travel: Go back to a previous checkpoint
4. Branch: Create a new branch from current execution state to explore alternative paths
5. Abort: Cancel current execution completely

### Interrupt while compiling
- One can interrupt while compiling the graph so code automatically interrupts before a node
- Needs checkpointer to remember state as before
- Code is `app = graph.compile(checkpointer=memory, interrupt_before=["tools"])`
- Like ` interrupt_before` we also have ` interrupt_after`

## Command class in langgraph
- Built in class from langgraph
- Works as a return from a function
- Has a `'goto` and `update` section for updating the state and deciding which state to go to next
```python
def node_b(state: State): 
    print("Node B")
    return Command(
        goto="node_c", 
        update={
            "text": state["text"] + "b"
        }
    )
```
- With this you now don't need to provide `add_edge` command as `goto` provides the next node and creates the edge 


## Langgraph functions
### add_messages
- allows merging of lists, used for merging message memory with message respone from llm
```python
class BasicChatState(TypedDict):
    messages: Annotated[list, add_messages]
```

### dumps
- converts message list into json
- json.dumps() cannot serialize langchain list of dicts
```python
response = llm.invoke("Hi my name is rohan")
json_response = dumps(response)
print(json_response)
```

### ToolNode
- creates a function of Tools instead of using `def()` 
```python
search_tool = TavilySearchResults(max_results=2)
tools = [search_tool]
tool_node = ToolNode(tools=tools)
graph.add_node("tool_node", tool_node)
```
- the ToolNode looks for the `messages` key in the AI message that is sent to it
- To use a different key need to change the call to `tool_node = ToolNode(tools=tools, messages_key="somethingElse")`
