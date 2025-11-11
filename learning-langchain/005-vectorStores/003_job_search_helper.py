'''
this program shows how to query against the vector-store using the retriever object
this makes the process of fethcing data much easier
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

document = TextLoader("job_listings.txt").load()
text_splitter= RecursiveCharacterTextSplitter(chunk_size=200,
                                              chunk_overlap=10)
chunks=text_splitter.split_documents(document)
db=Chroma.from_documents(chunks,llm)  ## everything remains the same till here w.r.t the previous program
retriever = db.as_retriever()  # this is another way of fething data from the database using the  retriever

text = input("Enter the query\n")

docs = retriever.invoke(text)

for doc in docs:
    print(doc.page_content)