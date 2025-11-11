import os
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import streamlit as st
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
llm = ChatOpenAI(model="gpt-4o", api_key=OPENAI_API_KEY)

st.title("Agile coach")
prompt_template = ChatPromptTemplate.from_messages([
    ("system", "You are a Agile coach. Answer any question related to the agile process"),
    ("human", "{input}")
])

first_chain = prompt_template | llm

userInput =  st.text_input("enter your question related to agile-practices in software engineering \n")

if userInput:
    response = first_chain.invoke({"input": userInput})
    st.write(response.content)
