from langchain_ollama import ChatOllama
from langchain_core.globals import set_debug

set_debug(True)

llm = ChatOllama(model="gemma:2b")

#question = input("ask any question")
question = "what is the capital of india"
response = llm.invoke(question)
print(response.content)