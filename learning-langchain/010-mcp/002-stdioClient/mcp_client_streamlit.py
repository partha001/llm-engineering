import asyncio
import os

import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv
import sys

client = MultiServerMCPClient({
    "tools":{
        #"command":"python",
        "command": sys.executable,
        "args":["mcp_server.py"],
        "transport":"stdio"
    }
})

tools = asyncio.run(client.get_tools())

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
llm = ChatOpenAI(model = "gpt-4o", api_key=OPENAI_API_KEY)

#agent =  create_react_agent(llm, tools)
agent = create_react_agent(model=llm, tools=tools)

st.title("AI agent (MCP version)")
#task = input("assign me any task: ")
task = st.text_input("assign me a task")

if task:
    response = asyncio.run(agent.ainvoke({"messages": task}))
    ### additionally we want know the inner working of the agent then uncomment the below line
    ### this will give a lot of metadata which will tell us what were the tools that were used by the mcp and what individual response it received
    ### this metadata will give a clear picture of how the agent is thinking
    # st.write(response)
    final_output = response["messages"][-1].content
    #print(final_output)
    st.write(final_output)

