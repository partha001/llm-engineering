'''
note that if we call the invoke() without passing any parameter we get the below error:

program output:
    Traceback (most recent call last):
      File "C:\ParthaFiles\git\llm-engineering\learning-langgraph\001_workflowBasic\004_1_stateValidation.py", line 34, in <module>
        output = runnable.invoke()
                 ^^^^^^^^^^^^^^^^^
    TypeError: Pregel.invoke() missing 1 required positional argument: 'input'
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
#graph.add_edge(START, "node1")
graph.add_edge("node1", "node2")
graph.add_edge("node2", END)

graph.set_entry_point("node1")

runnable = graph.compile()
display(runnable)
#output = runnable.invoke({"message":"partha"})
output = runnable.invoke()
print(output)

