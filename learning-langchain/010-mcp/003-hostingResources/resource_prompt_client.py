import asyncio
import os

#from langchain_openai import ChatOpenAI
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_ollama import ChatOllama

async def main():

    client = MultiServerMCPClient({
        "demo":{
            "url":"http://localhost:8000/mcp",
            "transport":"streamable_http"
        }
    })


    # 1. get bio from the resource
    blobs = await  client.get_resources(server_name="demo", uris="docs://aboutme")


    bio_text = blobs[0].as_string() if blobs else ""
    print("Bio:", bio_text[:120], "...")

    # 2. build prompt messages using the bio as context
    messages = await  client.get_prompt(server_name="demo",
                                        prompt_name="question",
                                        arguments={
                                            "question": "partha has worked on which technologies",
                                            "context": bio_text
                                        })

    # 3. send to llm
    ##llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)    ##uncomment this to use openai instead of ollama
    llm = ChatOllama(model="llama3.2:latest")
    resp = await llm.ainvoke(messages)
    print("\nLLM Answer:\n", resp.content)


if __name__ == "__main__":
    asyncio.run(main())


