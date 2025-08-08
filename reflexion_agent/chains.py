from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
import datetime
from langchain_openai import ChatOpenAI
from localschema import AnswerQuestion, ReviseAnswer
from langchain_core.output_parsers.openai_tools import PydanticToolsParser, JsonOutputToolsParser
from langchain_core.messages import HumanMessage
from langgraph.graph import END, MessageGraph
from dotenv import load_dotenv, find_dotenv
import os

_ = load_dotenv(find_dotenv())
os.environ["LANGSMITH_TRACING"] = "true"
os.environ["LANGSMITH_PROJECT"] = "default"


pydantic_parser = PydanticToolsParser(tools=[AnswerQuestion])

parser = JsonOutputToolsParser(return_id=True)

# Actor Agent Prompt 
actor_prompt_template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are expert AI researcher.
Current time: {time}

1. {first_instruction}
2. Reflect and critique your answer. Be severe to maximize improvement.
3. After the reflection, **list 1-3 search queries separately** for researching improvements. Do not include them inside the reflection.
""",
        ),
        MessagesPlaceholder(variable_name="messages"),
        ("system", "Answer the user's question above using the required format."),
    ]
).partial(
    time=lambda: datetime.datetime.now().isoformat(),
)

first_responder_prompt_template = actor_prompt_template.partial(
    first_instruction="Provide a detailed ~250 word answer"
)

llm = ChatOpenAI(model="gpt-4o-mini")

first_responder_chain = first_responder_prompt_template | llm.bind_tools(tools=[AnswerQuestion], tool_choice='AnswerQuestion') 
#first_responder_chain = first_responder_prompt_template | llm
# validator = PydanticToolsParser(tools=[AnswerQuestion])

# Revisor section
revise_instructions = """Revise your previous answer using the new information.
    - You should use the previous critique to add important information to your answer.
        - You MUST include numerical citations in your revised answer to ensure it can be verified.
        - Add a "References" section to the bottom of your answer (which does not count towards the word limit). In form of:
            - [1] https://example.com
            - [2] https://example.com
    - You should use the previous critique to remove superfluous information from your answer and make SURE it is not more than 250 words.
"""

revisor_chain = actor_prompt_template.partial(
    first_instruction=revise_instructions
) | llm.bind_tools(tools=[ReviseAnswer], tool_choice="ReviseAnswer")


#playing with the first responder chain
# response = first_responder_chain.invoke({
#     "messages": [HumanMessage("Create a blog post about the plane crash in India that happened in June 2025")]      # this hallucinates
# })
# response = first_responder_chain.invoke({
#     "messages": [HumanMessage("Write a blog post about the most famous Formula 1 driver of all time")]      
# })
# print(response)

# # create the geaph to see the state
# graph = MessageGraph()

# def check_node(state):
#     print("{} inside check {}".format("*"*20, "*"*20))
#     print(f"STATE-TYPE={type(state)} LEN={len(state)}")
#     for item in state:
#         print(type(item))
#     print("{} exiting check {}".format("*"*20, "*"*20))

# def responder_node(state):
#     print("{} inside responder {}".format("*"*20, "*"*20))
#     print(f"STATE-TYPE={type(state)} LEN={len(state)}")
#     print("{}\n STATE:{} \n{}".format("^"*20, state, "^"*20))

#     response = first_responder_chain.invoke({
#         "messages": state
#     })
#     print(f"STATE-TYPE={type(state)} LEN={len(state)}")
#     print("{} exiting responder {}".format("*"*20, "*"*20))
#     return response

# graph.add_node("Responder", responder_node)
# graph.add_node("Check", check_node)
# graph.set_entry_point("Responder")
# graph.add_edge("Responder", "Check")
# graph.add_edge("Check", END)
# app = graph.compile()

# print(app.get_graph().draw_mermaid())
# app.get_graph().print_ascii()
# response = app.invoke(HumanMessage(content="Write a blog post about the most famous Formula 1 driver of all time"))
# #print(response)


