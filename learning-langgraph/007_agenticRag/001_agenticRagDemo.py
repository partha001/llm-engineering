import os
from dotenv import load_dotenv
from typing import List, TypedDict
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from langchain_openai import OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langgraph.graph import StateGraph , START, END

from langchain_chroma import Chroma

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

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
    embedding=OpenAIEmbeddings(),
)
retriever = vectorstore.as_retriever()

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
model = ChatOpenAI()
current_affairs_chain = (
        prompt | model | StrOutputParser()
)


class CurrentAffairsGraphState(TypedDict):
    question: str
    retrieved_news: List[str]
    generation: str


# TODO: Use the retriever and retrieve the matching news
def retrieve_current_affairs(state):
    print("---RETRIEVE CURRENT AFFAIRS---")
    question = state["question"]
    retrieved_news = retriever.invoke(question)
    return {"question": question,"retrieved_news": retrieved_news}


# TODO: Summarize the news
# News Summary Generation Node
def generate_current_affairs_summary(state):
    print("---GENERATE CURRENT AFFAIRS SUMMARY---")
    question = state["question"]
    retrieved_news = retriever.invoke(question)
    generation = current_affairs_chain.invoke({"question": question,"context": retrieved_news})
    return {"question": question, "retrieved_news": retrieved_news,"generation": generation}


# Current Affairs News Workflow Definition
def create_current_affairs_workflow():
    workflow = StateGraph(CurrentAffairsGraphState)
    workflow.add_node("retrieve_current_affairs", retrieve_current_affairs)
    workflow.add_node("generate_current_affairs_summary", generate_current_affairs_summary)
    workflow.add_edge(START, "retrieve_current_affairs")
    workflow.add_edge("retrieve_current_affairs", "generate_current_affairs_summary")
    workflow.add_edge("generate_current_affairs_summary", END)
    return workflow.compile()


# Execute the Current Affairs News Workflow
current_affairs_graph = create_current_affairs_workflow()

#inputs = {"question": "What are the top global headlines today?"}
inputs = {"question": "What are the top sports headlines today?"}
response = current_affairs_graph.invoke(inputs)

print("\n--- CURRENT AFFAIRS SUMMARY ---")
# TODO: Print Response
print(response["generation"])


# ##sample program output:
# USER_AGENT environment variable not set, consider setting it to identify your requests.
# ---RETRIEVE CURRENT AFFAIRS---
# ---GENERATE CURRENT AFFAIRS SUMMARY---
#
# --- CURRENT AFFAIRS SUMMARY ---
# The top global headlines today include India air travel chaos easing but IndiGo crisis still leaving hundreds stranded, insomnia and anxiety affecting Venezuelans amid US military buildup, deadly flooding across Asia due to rogue storms and climate chaos, Pakistan and Afghanistan trading fire along the border with no casualties reported, Trump displaying contempt for Europe in a new national security plan, Congo fighting flaring up despite peace deal ceremony, as reported by The New York Times, Al Jazeera, and CNN.
#
# Process finished with exit code 0


