'''
thus an input state always has needs to be passed . it can be an empty dictionary as well.

program output
C:\ParthaFiles\git\llm-engineering\learning-langgraph\.learning-langgraph-condaVenv\python.exe C:\ParthaFiles\git\llm-engineering\learning-langgraph\001_workflowBasic\004_2_stateValidation.py
Traceback (most recent call last):
  File "C:\ParthaFiles\git\llm-engineering\learning-langgraph\001_workflowBasic\004_2_stateValidation.py", line 38, in <module>
    output = runnable.invoke({})
             ^^^^^^^^^^^^^^^^^^^
  File "C:\ParthaFiles\git\llm-engineering\learning-langgraph\.learning-langgraph-condaVenv\Lib\site-packages\langgraph\pregel\main.py", line 3068, in invoke
    for chunk in self.stream(
  File "C:\ParthaFiles\git\llm-engineering\learning-langgraph\.learning-langgraph-condaVenv\Lib\site-packages\langgraph\pregel\main.py", line 2643, in stream
    for _ in runner.tick(
  File "C:\ParthaFiles\git\llm-engineering\learning-langgraph\.learning-langgraph-condaVenv\Lib\site-packages\langgraph\pregel\_runner.py", line 167, in tick
    run_with_retry(
  File "C:\ParthaFiles\git\llm-engineering\learning-langgraph\.learning-langgraph-condaVenv\Lib\site-packages\langgraph\pregel\_retry.py", line 42, in run_with_retry
    return task.proc.invoke(task.input, config)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\ParthaFiles\git\llm-engineering\learning-langgraph\.learning-langgraph-condaVenv\Lib\site-packages\langgraph\_internal\_runnable.py", line 656, in invoke
    input = context.run(step.invoke, input, config, **kwargs)
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\ParthaFiles\git\llm-engineering\learning-langgraph\.learning-langgraph-condaVenv\Lib\site-packages\langgraph\_internal\_runnable.py", line 400, in invoke
    ret = self.func(*args, **kwargs)
          ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\ParthaFiles\git\llm-engineering\learning-langgraph\001_workflowBasic\004_2_stateValidation.py", line 14, in node1Hello
    print(f"Hello Node: {state['message']}")
                         ~~~~~^^^^^^^^^^^
KeyError: 'message'
During task with name 'node1' and id '15e7cb78-94be-6192-75a7-3d615cd620da'


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
#output = runnable.invoke({"message":"partha"})
output = runnable.invoke({})
print(output)

