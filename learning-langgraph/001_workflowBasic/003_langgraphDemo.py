'''
this program shows how to visualize the langgraph . for this we have defined our own util calls langgraph_util
and have then used the same here.

note: that ones the graph is compiled we get a runnable . then this runnable can be used to generate the visualization
of the graph
'''

from typing import TypedDict
from langgraph.graph import END, START, StateGraph
from util.langgraph_util import  display

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
graph.add_edge("node1", "node2")
graph.add_edge("node2", END)

graph.set_entry_point("node1")

runnable = graph.compile()
display(runnable)
output = runnable.invoke({"message":"partha"})
print(output)

