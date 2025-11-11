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
    input_variables=["country", "no_of_paras", "language"], #registering the multiple input variables here
    template="""
    You are an expert in traditional cuisines. Your provide 
    information about a specific dish from a specific country.    
    Answer the question: What is the traditional cuisine of {country}?
    Answer in {no_of_paras} short paras in {language}
    """
)
countryInput = st.text_input("Enter any country name:")
noOfParasInput = st.number_input("Enter number of paragraphs", min_value=1, max_value=5)
languageInput = st.text_input("Enter the language you want the result in")


if countryInput:
    response = llm.invoke(prompt_template.format(country=countryInput, no_of_paras= noOfParasInput, language= languageInput))
    st.write(response.content)
