import os
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda


# this program shows how to invoke an inline lamda expression on top of the output of a chain
# before passing it to the subsequent chain



load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
llm = ChatOpenAI(model = "gpt-4o", api_key=OPENAI_API_KEY)

prompt_template1 = PromptTemplate(
    input_variables=["topic"], #registering the multiple input variables here
    template="""
    You are an experienced speech writer.
    You need to craft an impactful title for a speech on the following topic: {topic}.
    Answer exactly with one title.
    """
)


prompt_template2 = PromptTemplate(
    input_variable= ["title"],
    template="""
    You need to write a powerful speech of 350 words for the following title:  
    {title}
    """
)


first_chain = prompt_template1 | llm | StrOutputParser() | (lambda titleOp: (print(f"Generated Title:{titleOp} \n")))
second_chain = prompt_template2 | llm
final_chain = first_chain | second_chain

## passing an input: ai and ethics
topicInput = input("Enter the topic: \n")
if topicInput:
    response = final_chain.invoke({"topic": topicInput})
    print(response.content)




