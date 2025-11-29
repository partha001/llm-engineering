import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
llm = OpenAIEmbeddings( api_key=OPENAI_API_KEY)

response = llm.embed_documents(
    [
        "I love playing video games",
        "I am going to the movie",
        "I love coding",
        "Hello World!"
    ]
)

print(len(response))
print(response[0])
