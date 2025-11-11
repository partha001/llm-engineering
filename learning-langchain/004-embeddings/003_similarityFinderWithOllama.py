#from langchain_openai import OpenAIEmbeddings
import numpy as np
from langchain_ollama import OllamaEmbeddings

## this program shows finding similarity between embeddings using ollama and numpy

llm = OllamaEmbeddings(model="llama3.2")
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
