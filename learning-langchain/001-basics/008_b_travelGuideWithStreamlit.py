import os
from langchain_openai import ChatOpenAI
import streamlit as st
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
llm = ChatOpenAI(model="gpt-4o", api_key=OPENAI_API_KEY)


st.title("Travel guide")
prompt_template = PromptTemplate(
    input_variables=["city", "month", "language","budget"], #registering the multiple input variables here
    template="""
    Welcome to the {city} travel guide!
    If you are visiting in {month}, here's whats you can do :
    1. Must-visit attraction.
    2. Local cuisine you must try.
    3. Userful phases in {language}.
    4. Tips for travelling on a {budget} budget.
    Enjoy your trip!
    """
)
cityInput = st.text_input("Enter any city name:")
monthInput = st.text_input("Enter the month of visit")
languageInput = st.text_input("Enter the language you want the important phrases in")
budgetInput = st.selectbox("Travel Budget",["Low","Medium","High"]) #note how to define a drop-down in streamlit


if cityInput:
    response = llm.invoke(prompt_template.format(city=cityInput,
                                                 month= monthInput,
                                                 language= languageInput,
                                                 budget= budgetInput))
    st.write(response.content)
