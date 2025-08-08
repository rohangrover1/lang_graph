from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv, find_dotenv
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from pydantic import BaseModel, Field
from typing_extensions import Annotated, TypedDict
from typing import Optional


_ = load_dotenv(find_dotenv())



llm = ChatOpenAI(model="gpt-4o")

# using Pydantic class for structured Outputs
# with_structured_output converts this into a tool to pass to the LLM
# Needed:
# Description which maps to info. about the tool needed by LLM
# parameters: the paramters of the tool. Some can be made optional
class Country(BaseModel):

    """Joke to tell user"""         

    setup: str = Field(description="the setup of the joke")
    punchline: str = Field(description="lThe punchline of the joke")
    rating: int = Field(description="How funny the joke is, from 1 to 10")
 
structured_llm = llm.with_structured_output(Country)
response = structured_llm.invoke("Tell me joke about cats")
print(response)
print(type(response))


# TypedDict
# Use native python dict instead of a class
class Joke(TypedDict):
    """Joke to tell user."""

    setup: Annotated[str, ..., "The setup of the joke"]

    # Alternatively, we could have specified setup as:

    # setup: str                    # no default, no description
    # setup: Annotated[str, ...]    # no default, no description
    # setup: Annotated[str, "foo"]  # default, no description

    punchline: Annotated[str, ..., "The punchline of the joke"]
    rating: Annotated[Optional[int], None, "How funny the joke is, from 1 to 10"]


structured_llm = llm.with_structured_output(Joke)
response = structured_llm.invoke("Tell me a joke about dogs")
print(response)
print(type(response))

# use json schema directly instead of annoted
json_schema = {
    "title": "joke",
    "description": "Joke to tell user.",
    "type": "object",
    "properties": {
        "setup": {
            "type": "string",
            "description": "The setup of the joke",
        },
        "punchline": {
            "type": "string",
            "description": "The punchline to the joke",
        },
        "rating": {
            "type": "integer",
            "description": "How funny the joke is, from 1 to 10",
            "default": None,
        },
    },
    "required": ["setup", "punchline"],
}
structured_llm = llm.with_structured_output(json_schema)
response = structured_llm.invoke("Tell me a joke about monkeys")
print(response)
print(type(response))
