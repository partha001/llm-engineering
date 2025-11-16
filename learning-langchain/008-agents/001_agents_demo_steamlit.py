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

load_dotenv()
open_ai_key = os.getenv("OPENAI_API_KEY")
llm = ChatOpenAI(model = 'gpt-4o', api_key = open_ai_key)

prompt = hub.pull("hwchase17/react")
#tools = load_tools(["wikipedia","ddg-search"])
# FIXED: Manual tool creation (works on LC 1.0.7)
tools = [
    WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper()),
    DuckDuckGoSearchRun(),
]
agent = create_react_agent(llm, tools, prompt)

agent_executor = AgentExecutor(agent = agent, tools =tools, verbose=True)

st.title("AI agent")
task = st.text_input("assign me a task")

if task:
    response = agent_executor.invoke({"input": task})
    st.write(response['output'])

# examplePrompt: who is current prime minister of India

