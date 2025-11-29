from langchain_ollama import OllamaEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_community.vectorstores import FAISS

# this is same as the previous program however instead of using openai we are using the locally
# running lamma here. thus here the embeddings are being calculated using llama3.2

llm = OllamaEmbeddings(model="llama3.2")

document = TextLoader("job_listings.txt").load()
text_splitter= RecursiveCharacterTextSplitter(chunk_size=200,
                                              chunk_overlap=10)
chunks=text_splitter.split_documents(document)
db=FAISS.from_documents(chunks,llm)  ## everything remains the same till here w.r.t the previous program
retriever = db.as_retriever()  # this is another way of fething data from the database using the  retriever

text = input("Enter the query\n")

docs = retriever.invoke(text)

for doc in docs:
    print(doc.page_content)

# ## program output
# Enter the query
# digital marketting
# SEM, and content creation.
# financial modeling.
# of project management software.
# Creative Suite and a strong portfolio.