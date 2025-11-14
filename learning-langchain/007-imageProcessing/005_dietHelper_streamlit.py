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
        ("system", "You are a helpful assistant that can analyze images of nutrition charts and help choose the right diet"),
        (
            "human",
            [
                {"type": "text", "text": "{input}"},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": "data:image/jpeg;base64,{image1}",
                        "detail": "low",
                    },
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": "data:image/jpeg;base64,{image2}",
                        "detail": "low",
                    },
                },
            ],
        ),
    ]
)

chain = prompt | llm

uploaded_file1 = st.file_uploader("Upload first image", type=["jpg", "png"])
uploaded_file2 = st.file_uploader("Upload second image", type=["jpg", "png"])
question = st.text_input("Enter the question about the image")

if uploaded_file1 and question:
    # encode the uploaded image
    image1 = encode_image(uploaded_file1)
    image2 = encode_image(uploaded_file2)

    # pass BOTH variables to the chain
    response = chain.invoke({
        "input": question,
        "image1": image1,
        "image2": image2
    })

    st.write(response.content)
