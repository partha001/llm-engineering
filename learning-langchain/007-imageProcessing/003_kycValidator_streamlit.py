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
        ("system", "You are a helpful assistant that can verify identification documents"),
        (
            "human",
            [
                {"type": "text", "text": "verify the identification details"},
                {"type": "text", "text": "Name : {user_name}"},
                {"type": "text", "text": "DOB : {user_dob}"},
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

st.title("KYC verification application")
st.write("upload your identification document")
uploaded_file = st.file_uploader("Upload your document", type=["jpg", "png"])

user_name = st.text_input("enter your name")
user_dob = st.text_input("enter your date of birth")

if user_name and user_dob and uploaded_file is  not None:
    # encode the uploaded image
    image_b64 = encode_image(uploaded_file)

    # pass BOTH variables to the chain
    response = chain.invoke({
        "user_name": user_name,
        "user_dob": user_dob,
        "image": image_b64
    })

    st.write(response.content)
