from typing import TypedDict
from langgraph.graph import END, START, StateGraph


#defining the structure of the input state (customer support request)
class SupportRequest(TypedDict):
    message: str
    priority: int # 1=high 2=medium 3=low


# function to categorize the support request
def categorize_request(request: SupportRequest):
    print(f"received request: {request}")
    # TODO: Implement the conditional routing logic
    if "urgent" in request["message"].lower() or request['priority']==1:
        return "urgent"
    return "standard"


# finction to process standard requests
def handle_standard(request: SupportRequest):
    print(f"routing to standard support team: {request}")
    return request


def handle_urgent(request: SupportRequest):
    print(f"routing to urgent support team: {request}")
    return request


# creating the state graph
graph = StateGraph(SupportRequest)
graph.add_node("urgent", handle_urgent)
graph.add_node("standard", handle_standard)

graph.add_conditional_edges(START, categorize_request)
graph.add_edge("urgent", END)
graph.add_edge("standard", END)

runnable = graph.compile()

#simulating a customer support request
print(runnable.invoke({"message":"My account was hacked! Urgent help needed.", "priority":1}))
print(runnable.invoke({"message":"I need help with password reset", "priority":3}))
