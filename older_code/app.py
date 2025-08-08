import openai
import re
import httpx
import os
from dotenv import load_dotenv, find_dotenv
from openai import OpenAI

_ = load_dotenv(find_dotenv())
api_key_str = os.environ['OPENAI_API_KEY']
client = OpenAI(api_key=api_key_str)

chat_completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "Hello world"}]
)
print(chat_completion.choices[0].message.content)