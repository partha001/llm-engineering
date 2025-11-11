import os
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser

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
    input_variable= ["title", "emption"],
    template="""
    You need to write a powerful {emotion} speech of 350 words for the following title: {title}
    
    Format the output with 2 keys: 'title','speech' and fill them with the respective values
    """
)

first_chain = prompt_template1 | llm | StrOutputParser() | (lambda output:{"title":output, "emotion":emotionInput})
#thus we are retuning a dictionary here from the lambda with the title and emotion which will be the input to the second_chain
second_chain = prompt_template2 | llm | JsonOutputParser()
final_chain = first_chain | second_chain

## passing an input: ai and ethics
topicInput = input("Enter the topic: \n")
emotionInput = input("Enter the emotion: \n")
if topicInput and emotionInput:
    response = final_chain.invoke({"topic": topicInput})
    #print(response.content)
    print(response, end="\n\n")
    print(response['title'], end="\n\n")




