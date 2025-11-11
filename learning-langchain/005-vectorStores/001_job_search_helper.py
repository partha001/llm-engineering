'''
this program show how to create a vector store from a file and then query on top of it
'''

import os
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
llm=OpenAIEmbeddings(api_key=OPENAI_API_KEY)

document = TextLoader("job_listings.txt").load() # this is to load the document
text_splitter= RecursiveCharacterTextSplitter(chunk_size=200,
                                              chunk_overlap=10)  #creating the splitter
chunks=text_splitter.split_documents(document) #finally breaking the document into chunks using splitter
db=Chroma.from_documents(chunks,llm) # loading the chunks into database
retriever = db.as_retriever()

text = input("Enter the query\n") # taking the search input from the user
embedding_vector = llm.embed_query(text) # getting the embeddings for the input

docs = db.similarity_search_by_vector(embedding_vector)
print(docs)

# ################# program output:
# Enter the query
# software
# [Document(id='e8365e96-a002-4727-a3d0-734473041373', metadata={'source': 'job_listings.txt'}, page_content='of project management software.'), Document(id='8193eb88-9c3d-4e99-a576-e96968ec484b', metadata={'source': 'job_listings.txt'}, page_content='in network security and experience with security tools.'), Document(id='95900272-ca40-4f0c-a671-dce3e6a8b90d', metadata={'source': 'job_listings.txt'}, page_content='in Java, Python, and SQL.'), Document(id='89e2e54d-faf1-4238-b2c3-2fc0b35ac091', metadata={'source': 'job_listings.txt'}, page_content='1. Software Engineer at TechCorp - Responsibilities include developing and maintaining software applications, collaborating with cross-functional teams, and ensuring code quality. Requires proficiency')]
