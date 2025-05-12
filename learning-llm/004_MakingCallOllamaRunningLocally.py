'''
prerequisite first download and install ollama.

ones installed we can check by visiting http://localhost:11434/
if installed successfully the link will say - Ollama is running
'''
import ollama
import requests

# Constants
OLLAMA_API = "http://localhost:11434/api/chat"
HEADERS = {"Content-Type":"application/json"}
MODEL = "llama3.2"

messages = [
    {"role":"user","content":"Describe some of the business applications of Generative AI"}
]

payload = {
    "model":MODEL,
    "messages":messages,
    "stream":False
}

response = requests.post(OLLAMA_API, json=payload, headers= HEADERS) # getting the response from local llm using requests object
print(response.json()['message']['content']) #here we are basically printing json.message.content


## another way of getting the response from the local llm using ollama object
response = ollama.chat(model=MODEL, messages=messages)
print(response['message']['content'])
