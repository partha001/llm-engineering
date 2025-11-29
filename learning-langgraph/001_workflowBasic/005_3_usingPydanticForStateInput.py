# program output:
#     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#     pydantic_core._pydantic_core.ValidationError: 1 validation error for HelloWorldState
#         id
#     Field required [type=missing, input_value={'message': 'partha'}, input_type=dict]
#     For further information visit https://errors.pydantic.dev/2.12/v/missing
#     Before task with name 'node1' and path '('__pregel_pull', 'node1')'



from langgraph.graph import END, START, StateGraph
from pydantic import BaseModel, Field
from typing import Optional

# defining the state
class HelloWorldState(BaseModel):
    message:str = Field(min_length=2) #adding pydantic validation
    # id: int  #this will make the id mandatory. and this is the default behavior.

    ## however to make the id optional we have define it like below :
    #id: Optional[int] = None


def node1Hello(state: HelloWorldState):
    print(f"Hello Node: {state.message}")
    return {"message": "Hello "+state.message}

def node2Bye(state: HelloWorldState):
    print(f"Bye Node: {state.message}")
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
output = runnable.invoke({"message":"partha"})
print(output)

