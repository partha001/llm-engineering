from typing import TypedDict
from langgraph.graph import END, START, StateGraph
from pydantic import BaseModel, Field

# defining the state
class HelloWorldState(BaseModel):
    message:str = Field(min_length=2, max_length=10) #adding pydantic validation

def node1Hello(state: HelloWorldState):
    # print(f"Hello Node: {state['message']}")
    # return {"message": "Hello "+state['message']}
    print(f"Hello Node: {state.message}")
    return {"message": "Hello "+state.message}

def node2Bye(state: HelloWorldState):
    # print(f"Bye Node: {state['message']}")
    # return {"message": "Bye "+state['message']}
    print(f"Bye Node: {state.message}")
    return {"message": "Bye "+state.message}

#creating the graph
graph = StateGraph(HelloWorldState)

#creating the nodes
graph.add_node("node1", node1Hello)
graph.add_node("node2", node2Bye)

#creating edges
#graph.add_edge(START, "node1")
graph.add_edge("node1", "node2")
graph.add_edge("node2", END)

graph.set_entry_point("node1")

runnable = graph.compile()
output = runnable.invoke({"message":"partha"})
print(output)

