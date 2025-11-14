import os
from dotenv import load_dotenv
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableMap, RunnableLambda

# === Load model and embeddings ===
llm = ChatOllama(model="llama3.2:latest")
embeddings = OllamaEmbeddings(model="llama3.2:latest")

# === Load and split document ===
document = TextLoader("product-data.txt").load()
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
chunks = text_splitter.split_documents(document)

# === Create vector store and retriever ===
vector_store = Chroma.from_documents(chunks, embeddings)
retriever = vector_store.as_retriever()

# === Define prompt ===
prompt_template = ChatPromptTemplate.from_messages([
    ("system", """You are an assistant for answering questions.
                  Use the provided context to respond. If the answer isn't clear, acknowledge that you don't know.
                  Limit your response to three concise sentences.
                  {context}"""),
    ("human", "{input}")
])

# === Define chain1: prompt + LLM ===
qa_chain = prompt_template | llm

# === Define chain2: retrieval + context formatting + qa_chain ===
rag_chain = (
        RunnableMap({"context": retriever, "input": RunnablePassthrough()})
        | qa_chain
)

# === Interactive chat ===
print("Chat with Document (using local LLaMA 3.2)")
question = input("Enter your question: ")
if question:
    response = rag_chain.invoke(question)
    print("\nAnswer:\n", response.content)