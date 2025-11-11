import os
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_message_histories.in_memory import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

# this program shows how to remember the chatHistory while having a conversation
# since by default every call to the llm is stateless

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
llm = ChatOpenAI(model="gpt-4o", api_key=OPENAI_API_KEY)

prompt_template = ChatPromptTemplate.from_messages([
    ("system", "You are a Agile coach. Answer any question related to the agile process"),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}")
])


chain = prompt_template | llm

history_for_chain = ChatMessageHistory()

chain_with_history = RunnableWithMessageHistory(
    chain,
    lambda session_id: history_for_chain,
    input_messages_key= "input",
    history_messages_key="chat_history"
)


while True:
    question = input("enter the question related to agile:\n")
    if question:
        response = (chain_with_history
                    .invoke({"input":question},
                            {"configurable": {
                                "session_id":"abc123"
                            }}))
        print(response.content)


# after running the program first ask::  Hi i am partha. what is scrum?
# after the program answers this and asks for more question. ask:: what is my name
# its successfully able to tell my name which mean that its able to remember history
