from typing import List, TypedDict
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langgraph.graph import StateGraph, START, END

# Current Affairs News Sources
news_urls = [
    "https://www.bbc.com/news",
    "https://www.cnn.com/world",
    "https://www.nytimes.com/section/world",
    "https://www.reuters.com/world/",
    "https://www.aljazeera.com/news/"
]

# Load Current Affairs Documents
docs = [WebBaseLoader(url).load() for url in news_urls]
docs_list = [item for sublist in docs for item in sublist]

# Split the articles for embeddings
text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
    chunk_size=300, chunk_overlap=20
)
doc_splits = text_splitter.split_documents(docs_list)

# Store and Retrieve Current Affairs with ChromaDB
vectorstore = Chroma.from_documents(
    documents=doc_splits,
    collection_name="current-affairs-news",
    embedding=OllamaEmbeddings(model="llama3.2"),
)
retriever = vectorstore.as_retriever()


class RAGGraphState(TypedDict):
    input: str
    data: str


# TODO: Use the retriever and retrieve the matching news
def retrieve_data(state: RAGGraphState):
    print("---Retrieve Data")
    input = state["input"]
    data = retriever.invoke(input)
    return {"data": data}


def create_rag_workflow():
    workflow = StateGraph(RAGGraphState)
    workflow.add_node("retrieve_data", retrieve_data)
    workflow.add_edge(START, "retrieve_data")
    workflow.add_edge("retrieve_data", END)
    return workflow.compile()


rag_workflow = create_rag_workflow()


# Prompt for Current Affairs News Summarization
prompt = ChatPromptTemplate.from_template(
    """
    You are a news analyst summarizing the latest current affairs.
    Use the retrieved articles to provide a concise summary.
    Highlight key global events and developments.

    Question: {question}
    News Articles: {context}
    Summary:
    """
)
model = ChatOllama(model="llama3.2")
current_affairs_chain = (
        prompt | model | StrOutputParser()
)


class CurrentAffairsGraphState(TypedDict):
    question: str
    retrieved_news: List[str]
    generation: str


# TODO: Summarize the news
# News Summary Generation Node
def generate_current_affairs_summary(state):
    print("---GENERATE CURRENT AFFAIRS SUMMARY---")
    question = state["question"]
    # TODO: Invoke the rag workflow
    retrieved_news = rag_workflow.invoke({"input": question})
    generation = current_affairs_chain.invoke({"question": question,"context": retrieved_news["data"]})
    return {"question": question, "retrieved_news": retrieved_news,"generation": generation}


# Current Affairs News Workflow Definition
def create_current_affairs_workflow():
    workflow = StateGraph(CurrentAffairsGraphState)
    workflow.add_node("generate_current_affairs_summary", generate_current_affairs_summary)
    workflow.add_edge(START, "generate_current_affairs_summary")
    workflow.add_edge("generate_current_affairs_summary", END)
    return workflow.compile()


# Execute the Current Affairs News Workflow
current_affairs_graph = create_current_affairs_workflow()

inputs = {"question": "What are the top global headlines today?"}

response = current_affairs_graph.invoke(inputs)

print("\n--- CURRENT AFFAIRS SUMMARY ---")
print(response["generation"])


# ## program output:
# D:\git\llm-engineering\learning-langgraph\.learning-langgraph-condaVenv\python.exe D:\git\llm-engineering\learning-langgraph\010_subgraphs\002_rag_demo.py
# USER_AGENT environment variable not set, consider setting it to identify your requests.
# ---GENERATE CURRENT AFFAIRS SUMMARY---
# ---Retrieve Data
#
# --- CURRENT AFFAIRS SUMMARY ---
# Good evening, and welcome to our news analysis segment. We have a few key global headlines that we'd like to highlight today.
#
# Firstly, the US Navy has seized an Iranian oil tanker accused of smuggling sanctioned oil. Venezuela has responded by accusing the US of "theft" and "piracy", claiming that the US is trying to disrupt their economy.
#
# In another developing story, over 30 people have been killed in a Myanmar military air strike on a hospital in Yangon. The junta has stepped up its bombardments in an attempt to reclaim territory from ethnic armies.
#
# Moving on to Asia, researchers have made a groundbreaking discovery after filming killer whales and dolphins working together in the wild for the first time. The footage, captured near the North-West Pacific coast, is believed to be the first recorded evidence of this joint hunt behavior.
#
# Finally, we have some news from the UK, where the government has announced plans to increase funding for the NHS and other public services as part of its economic recovery plan following the COVID-19 pandemic.
#
# These are just a few of the top global headlines making headlines today. We'll continue to monitor these stories and bring you updates as more information becomes available. Thank you for watching.
#
# Process finished with exit code 0
