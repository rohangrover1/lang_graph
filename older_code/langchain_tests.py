from dotenv import load_dotenv, find_dotenv
from typing import TypedDict, Annotated
from langchain_core.messages import AnyMessage, SystemMessage, HumanMessage, ToolMessage
from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults
import os
import getpass
from langchain_core.prompts import ChatPromptTemplate
import sys

# set the envionment variables
_ = load_dotenv(find_dotenv())
os.environ["LANGSMITH_TRACING"] = "true"
if "LANGCHAIN_API_KEY" not in os.environ:
    os.environ["LANGCHAIN_API_KEY"] = getpass.getpass(
        prompt="Enter your LangSmith API key (optional): "
    )

os.environ["LANGSMITH_PROJECT"] = "default"
# if "LANGSMITH_PROJECT" not in os.environ:
#     os.environ["LANGSMITH_PROJECT"] = getpass.getpass(
#         prompt='Enter your LangSmith Project Name (default = "default"): '
#     )
#     if not os.environ.get("LANGSMITH_PROJECT"):
#         os.environ["LANGSMITH_PROJECT"] = "default"

if "OPENAI_API_KEY" not in os.environ:
    os.environ["OPENAI_API_KEY"] = getpass.getpass(
        prompt="Enter your OpenAI API key (required if using OpenAI): "
    )


def calling_models():
    try:
        # # invoking models
        model = ChatOpenAI(model="gpt-4o-mini", temperature=0.2, timeout=10)
        # messages = [
        #     SystemMessage("Translate the following from English into Italian"),
        #     HumanMessage("hi!"),
        # ]
        # result = model.invoke(messages)
        # print(result)
        # print(type(result))
        
        # other message formats
        '''
        model.invoke("Hello")
        model.invoke([{"role": "system", "content": "Translate the following from English into Hindi"}, {"role": "user", "content": "Hello"}])
        model.invoke([HumanMessage("Hello")])
        '''
        #print(model.invoke([{"role": "system", "content": "Translate the following from English into Hindi"}, {"role": "user", "content": "Hello"}]))

        # streaming mode. Prints output token as a stream 
        # print("streaming mode")
        # messages = [
        #     SystemMessage("You are a world class chef"),
        #     HumanMessage("Give me recipe for chicken tikka masala"),
        # ]
        # for token in model.stream(messages):
        #     print(token.content, end="|")

        # prompt templates. Old school not very useful but good to experiment
        system_template = "Translate the following from English into {language}"
        prompt_template = ChatPromptTemplate.from_messages(
            [("system", system_template), ("user", "{text}")]
        )
        prompt = prompt_template.invoke({"language": "Italian", "text": "hi!"})
        print(prompt.to_messages())
        response = model.invoke(prompt)
        print(response.content) 





    except Exception as e:
        print(
               'line:{} type:{}, message:{}'.format(sys.exc_info()[-1].tb_lineno, type(e).__name__, str(e)))



if __name__ == "__main__":

    # tool = TavilySearchResults(max_results=4) #increased number of results
    # print(type(tool))
    # print(tool.name)

    calling_models()


