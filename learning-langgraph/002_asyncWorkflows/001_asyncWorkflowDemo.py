import asyncio

from langgraph.graph import END, START, StateGraph
from pydantic import BaseModel, Field

# defining the state
class HelloWorldState(BaseModel):
    message:str = Field(min_length=2) #adding pydantic validation


async def node1Hello(state: HelloWorldState):
    print(f"Hello Node: {state.message}")
    # TODO: Simulating some long running task like apiCall, databaseCall, RAGCall, etc
    await asyncio.sleep(1)
    return {"message": "Hello "+state.message}

async def node2Bye(state: HelloWorldState):
    print(f"Bye Node: {state.message}")
    # TODO: Simulating some long running task like apiCall, databaseCall, RAGCall, etc
    await asyncio.sleep(1)
    return {"message": "Bye "+state.message}

#creating the graph
graph = StateGraph(HelloWorldState)

#creating the nodes
graph.add_node("node1", node1Hello)
graph.add_node("node2", node2Bye)

#creating edges
graph.add_edge("node1", "node2")
graph.add_edge("node2", END)

graph.set_entry_point("node1")

runnable = graph.compile()

# this method does the async invocation
async def main():
    output = await runnable.ainvoke({"message":"partha"})
    print(output)


asyncio.run(main())

