from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

import base64
import os
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

def encode_image(image_file):
    return base64.b64encode(image_file.read()).decode()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
llm = ChatOpenAI(model="gpt-4o", api_key=OPENAI_API_KEY)

# FIXED PROMPT — use {image} as a variable
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant that can analyze image and can answer question based upon image"),
        (
            "human",
            [
                {"type": "text", "text": "{input}"},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": "data:image/jpeg;base64,{image}",
                        "detail": "low",
                    },
                },
            ],
        ),
    ]
)

chain = prompt | llm

uploaded_file = st.file_uploader("Upload your image", type=["jpg", "png"])
question = st.text_input("Enter the question about the image")

if uploaded_file and question:
    # encode the uploaded image
    image_b64 = encode_image(uploaded_file)

    # pass BOTH variables to the chain
    response = chain.invoke({
        "input": question,
        "image": image_b64
    })

    st.write(response.content)
