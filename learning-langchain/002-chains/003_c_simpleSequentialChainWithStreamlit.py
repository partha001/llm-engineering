import os
from langchain_openai import ChatOpenAI
import streamlit as st
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
llm = ChatOpenAI(model="gpt-4o", api_key=OPENAI_API_KEY)


st.title("Speech generator")
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
first_chain = prompt_template1 | llm | StrOutputParser() | (lambda title : (st.write(title), title)[1])
second_chain = prompt_template2 | llm
final_chain = first_chain | second_chain

#enter an input like: ai and ethics
topicInput = st.text_input("Enter a topic")

## passinc an input: ai and ethics
if topicInput:
    response = final_chain.invoke({"topic": topicInput})
    st.write(response.content)
