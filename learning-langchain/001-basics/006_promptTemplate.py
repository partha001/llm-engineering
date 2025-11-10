import os
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
llm = ChatOpenAI(model = "gpt-4o", api_key=OPENAI_API_KEY)

prompt_template = PromptTemplate(
    inpout_variables=["country"], #for now having only one variable . however there can be multiple variables as well
    template="""
    You are an expert in traditional cuisines. Your provide 
    information about a specific dish from a specific country.    
    Answer the question: What is the traditional cuisine of {country}?
    """
)
countryInput = input("Enter any country name: \n")



# response = llm.invoke(question)
response = llm.invoke(prompt_template.format(country= countryInput))
print(response.content)
