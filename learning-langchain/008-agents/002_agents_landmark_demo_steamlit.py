import os


import streamlit as st
from dotenv import load_dotenv
#from langchain_classic import AgentExecutor
from langchain_classic.agents import AgentExecutor
from langchain_classic import hub
#from langchain_community.agent_toolkits import create_react_agent
from langchain_classic.agents import create_react_agent
from langchain_community.agent_toolkits.load_tools import load_tools
from langchain_openai import ChatOpenAI

#tools
# Tools
from langchain_community.tools.wikipedia.tool import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_community.tools.ddg_search.tool import DuckDuckGoSearchRun
from langchain_core.prompts import ChatPromptTemplate
import base64

def encode_image(image_file):
    return base64.b64encode(image_file.read()).decode()



load_dotenv()
open_ai_key = os.getenv("OPENAI_API_KEY")
llm = ChatOpenAI(model = 'gpt-4o', api_key = open_ai_key)

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant that can identify a landmark"),
        (
            "human",
            [
                {"type": "text", "text": "return the landmark name"},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": "data:image/jpeg;base64,{image1}",
                        "detail": "low",
                    },
                }
            ],
        ),
    ]
)

chain = prompt | llm

st.title("landmark helper")
uploaded_file = st.file_uploader("Upload your image", type=["jpg", "png"])
question = st.text_input("enter a question about the landmark")

task = None
if question:
    # encode the uploaded image
    image = encode_image(uploaded_file)

    # pass BOTH variables to the chain
    response = chain.invoke({
        "input": question,
        "image1": image})
    task = question + response.content



prompt = hub.pull("hwchase17/react")
#tools = load_tools(["wikipedia","ddg-search"])
# FIXED: Manual tool creation (works on LC 1.0.7)
tools = [
    WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper()),
    DuckDuckGoSearchRun(),
]
agent = create_react_agent(llm, tools, prompt)

agent_executor = AgentExecutor(agent = agent, tools =tools, verbose=True)


if task:
    #response = agent_executor.invoke({"input": task})
    response = agent_executor.invoke({"input": task+ " without explanation"})
    st.write(response['output'])

