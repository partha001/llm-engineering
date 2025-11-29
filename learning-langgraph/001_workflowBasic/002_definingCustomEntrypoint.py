from typing import TypedDict
from langgraph.graph import END, START, StateGraph
#from langgraph import display

# defining the state
class HelloWorldState(TypedDict):
    message:str

def node1Hello(state: HelloWorldState):
    print(f"Hello Node: {state['message']}")
    return {"message": "Hello "+state['message']}

def node2Bye(state: HelloWorldState):
    print(f"Bye Node: {state['message']}")
    return {"message": "Bye "+state['message']}

#creating the graph
graph = StateGraph(HelloWorldState)

#creating the nodes
graph.add_node("node1", node1Hello)
graph.add_node("node2", node2Bye)

#creating edges
#graph.add_edge(START, "node1")
graph.add_edge("node1", "node2")
graph.add_edge("node2", END)

#run the program by commenting the below line. it will fail .since in that case though we have defined the graph, its nodes and its edges
# however we have not defined the entrypoint . so it doesnt know where to start the execution from and hence it fails.
# so this is another way of defining entry point. however if we already have an edge as START then i will start executing the
# graph from there . hence this is the alternate way of defining entrypoint
graph.set_entry_point("node1")

runnable = graph.compile()
output = runnable.invoke({"message":"partha"})
print(output)

