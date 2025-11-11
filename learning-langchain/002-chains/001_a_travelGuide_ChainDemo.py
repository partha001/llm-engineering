import os
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
llm = ChatOpenAI(model = "gpt-4o", api_key=OPENAI_API_KEY)

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

cityInput = input("Enter any city name: \n")
monthInput = input("Enter the month of visit\n")
languageInput = input("Enter the language you want the important phrases in\n")
budgetInput = input("Enter the budget\n")


chain = prompt_template | llm

if cityInput:
    # response = llm.invoke(prompt_template.format(city= cityInput,
    #                                              month=monthInput,
    #                                              language= languageInput,
    #                                              budget= budgetInput))
    response = chain.invoke({"city": cityInput,
                             "month":monthInput,
                             "language": languageInput,
                             "budget": budgetInput})
    print(response.content)
