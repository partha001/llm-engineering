import os
from langchain_openai import ChatOpenAI
import streamlit as st
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
llm = ChatOpenAI(model="gpt-4o", api_key=OPENAI_API_KEY)



prompt_template = PromptTemplate(
    input_variables=["company", "position", "strengths","weaknesses"], #registering the multiple input variables here
    template="""
    You are a carrer coach. Provide tailored interview tips for the 
    position of {position} at {company}.
    Highlight your strengths in {strengths} and prepare for questions 
    about your weaknesses such as {weaknesses}.
    """
)
st.title("Interview Tips generator")

company = st.text_input("Company name:")
position  = st.text_input("Position title")
strengths = st.text_area("Your strengths", height = 100)
weaknesses = st.text_area("Your weaknesses", height = 100)


if company and position and strengths and weaknesses:
    response = llm.invoke(prompt_template.format(company= company,
                                                 position= position,
                                                 strengths= strengths,
                                                 weaknesses= weaknesses))
    st.write(response.content)
