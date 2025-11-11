import os
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
import numpy as np

## this program is to find similarity between embeddings

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
llm = OpenAIEmbeddings( api_key=OPENAI_API_KEY)
text1 = input("enter text1\n")
text2 = input("enter text2\n")
response1 = llm.embed_query(text1)
response2 = llm.embed_query(text2)

# the numpy dot methods takes vector embeddings and then find similarity between them using its own algorithm
# the score is between 0 and 1. where 0 mean no similarity and 1 mean exactly similar
similarity_score = np.dot(response1, response2)
print(f"similarity score: {similarity_score}")

#to get the similarity as percentage
print(f"similarity percentage %: {similarity_score*100}")


### program output:
# enter text1
# cat
# enter text2
# dog
# similarity score: 0.8629575884598418
# similarity percentage %: 86.29575884598418


# enter text1
# cat
# enter text2
# kitten
# similarity score: 0.8604079665584408
# similarity percentage %: 86.04079665584408

