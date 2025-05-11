import os
import requests
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from IPython.display import Markdown, display
from openai import OpenAI


load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')


text = "What is the capital of India?"
openai = OpenAI()
response = openai.chat.completions.create(
    model="gpt-4o",
    messages= [
        {"role":"user", "content": text}
    ]
)
print(response.choices[0])
print(response.choices[0].message.content)