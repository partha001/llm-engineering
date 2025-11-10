import os
# from langchain_openai import ChatOpenAI
# from dotenv import load_dotenv
from langchain_ollama import ChatOllama

#load_dotenv()
#OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
#llm = ChatOpenAI(model = "gpt-4o", api_key=OPENAI_API_KEY)

llm = ChatOllama(model="gemma:2b")

question = input("Enter the question \n")
response = llm.invoke(question)
print(response.content)




