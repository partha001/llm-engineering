import asyncio
import os
import sys

from langchain_openai import ChatOpenAI
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv

# client = MultiServerMCPClient({
#     "tools":{
#         "url":"http://localhost:8000/mcp",
#         "transport":"streamable_http"
#     }
# })

### stdio related change
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

task = input("assign me any task: ")
if task:
    response = asyncio.run(agent.ainvoke({"messages": task}))
    final_output = response["messages"][-1].content
    print(final_output)

