from typing import Annotated, TypedDict
from operator import add
from langgraph.graph import END, START, StateGraph, MessagesState

from langchain_core.messages import AIMessage, HumanMessage




# responses based on intent level
def connect_to_sales(state: MessagesState):
    return {"messages": [AIMessage(content="Great! Let me connect you with our sales team right away",
                                   )]}


def sales_response(state: MessagesState):
    return {"messages": [AIMessage(content="We have the best offer for you",
                                   )]}


# build chatbot conversation flow
graph_builder = StateGraph(MessagesState)

# add nodes
graph_builder.add_node("connect_to_sales", connect_to_sales)
graph_builder.add_node("sales_response", sales_response)

# defining edges/ conversation flow
graph_builder.add_edge(START, "connect_to_sales")
graph_builder.add_edge("connect_to_sales", "sales_response")
graph_builder.add_edge("sales_response", END)

# compiling the chatbot graph
chatbot = graph_builder.compile()

# simulate different conversations
test_inputs = "I want to buy your product."

messages = chatbot.invoke({"messages": [HumanMessage(content=test_inputs)]})

for message in messages["messages"]:
    print(f" **Bot:** {message.content}")

