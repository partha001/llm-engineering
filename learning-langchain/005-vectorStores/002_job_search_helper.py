'''
this is same as the previous program just that here we have played with document object that has been
retrieved and then printed the nested documents one by one
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
#print(docs, end="\n\n")
#print(docs[0].page_content, end="\n\n")

for doc in docs:
    print(doc.page_content)
