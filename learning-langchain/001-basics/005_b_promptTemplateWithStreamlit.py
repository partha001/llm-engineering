import os
from langchain_openai import ChatOpenAI
import streamlit as st
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
llm = ChatOpenAI(model="gpt-4o", api_key=OPENAI_API_KEY)


st.title("Cuisine info")
prompt_template = PromptTemplate(
    inpout_variables=["country"], #for now having only one variable . however there can be multiple variables as well
    template="""
    You are an expert in traditional cuisines. Your provide 
    information about a specific dish from a specific country.    
    Answer the question: What is the traditional cuisine of {country}?
    """
)

countryInput = st.text_input("enter the country")

if countryInput:
    response = llm.invoke(prompt_template.format(country=countryInput))
    st.write(response.content)
