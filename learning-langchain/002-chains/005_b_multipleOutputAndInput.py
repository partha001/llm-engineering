import os
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda
from langchain_ollama import ChatOllama

# this is just another variation of the previous program . in the previous program we have used the lambda while
# defining the final chain. here however we are doing the same thing but as part of chain1

# same as previous program  the second input ie. emotionInput is not passed to chain1 but passed to chain2
# while composing the dictionary which is the input for chain2

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
llm = ChatOpenAI(model = "gpt-4o", api_key=OPENAI_API_KEY)

gemma = ChatOllama(model="gemma:2b")

prompt_template1 = PromptTemplate(
    input_variables=["topic"], #registering the multiple input variables here
    template="""
    You are an experienced speech writer.
    You need to craft an impactful title for a speech on the following topic: {topic}.
    Answer exactly with one title.
    """
)


prompt_template2 = PromptTemplate(
    input_variable= ["title", "emotion"],
    template="""
    You need to write a powerful {emotion} speech of 350 words for the following title:
 
    {title}
    """
)

first_chain = prompt_template1 | llm | StrOutputParser() | (lambda output:{"title":output, "emotion":emotionInput})
second_chain = prompt_template2 | gemma
final_chain = first_chain | second_chain

## passing an input: ai and ethics
topicInput = input("Enter the topic: \n")
emotionInput = input("Enter the emotion: \n")
if topicInput and emotionInput:
    response = final_chain.invoke({"topic": topicInput})
    print(response.content)




