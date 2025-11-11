import os
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
llm = ChatOpenAI(model = "gpt-4o", api_key=OPENAI_API_KEY)

prompt_template = PromptTemplate(
    input_variables=["country", "no_of_paras", "language"], #registering the multiple input variables here
    template="""
    You are an expert in traditional cuisines. Your provide 
    information about a specific dish from a specific country. 
    Avoid giving information about fictional places. If the country in fictional or non-existent answer: I dont know.   
    Answer the question: What is the traditional cuisine of {country}?
    Answer in {no_of_paras} short paras in {language}
    """
)
countryInput = input("Enter any country name: \n")
noOfParasInput = input("Enter number of paragraphs\n")
languageInput = input("Enter the language you want the result in\n")


if countryInput:
    response = llm.invoke(prompt_template.format(country= countryInput, no_of_paras=noOfParasInput, language= languageInput))
    print(response.content)
