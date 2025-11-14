'''
this program shows how to index documents and then
query ask question to the llm . some of the same question that we can try are given the
rag_questions.txt

and here we are making use of llama running locally as the llm model
'''

from langchain_ollama import OllamaEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate

print("Import successful!")



llamma = ChatOllama(model="llama3.2:latest")
embeddings = OllamaEmbeddings(model="llama3.2:latest")


document = TextLoader("product-data.txt").load()
text_splitter= RecursiveCharacterTextSplitter(chunk_size=1000,
                                              chunk_overlap=200)
chunks=text_splitter.split_documents(document)
vector_store=Chroma.from_documents(chunks, embeddings)  ## everything remains the same till here w.r.t the previous program
retriever = vector_store.as_retriever()  # this is another way of fething data from the database using the  retriever



prompt_template = ChatPromptTemplate.from_messages([
    ("system", """You are an assistant for answering questions. 
                    Use the provided context to respond. If the answer isn't clear, acknowledge that you don't know.
                    Limit you response to three concise sentences.
                    {context}"""),
    ("human", "{input}")
])


def answer_with_retrieval(input_text: str):
    # 1. Retrieve relevant chunks
    docs = retriever.invoke(input_text)

    # 2. Concatenate as context
    context = "\n\n".join(d.page_content for d in docs)

    # 3. Format prompt messages
    messages = prompt_template.format_messages(input=input_text, context=context)

    # 4. Call local LLaMA
    result = llamma.invoke(messages)
    return result.content

# === Interactive chat ===
print("Chat with Document (using local LLaMA 3.2)")
question = input("Your Question: ")
if question:
    answer = answer_with_retrieval(question)
    print("\nAnswer:\n", answer)


