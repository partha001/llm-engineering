from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

import base64
import os
from dotenv import load_dotenv

load_dotenv()

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
llm = ChatOpenAI(model="gpt-4o", api_key=OPENAI_API_KEY)
image = encode_image("images/airport_terminal_journey.jpeg")
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant that can describe images."),
        (
            "human",
            [
                {"type": "text", "text": "{input}"},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{image}",
                        "detail": "low",
                    },
                },
            ],
        ),
    ]
)


chain = prompt|llm
response = chain.invoke({"input":"Explain"})
print(response.content)

# program output:
# The image depicts a stylish airport scene, featuring a silhouette of a person standing with a suitcase, gazing out at planes landing and taking off. The spacious terminal has large glass windows, allowing natural light from the setting sun to illuminate the area. This creates a dramatic and warm atmosphere, highlighting the vibrant colors of the sunset sky. Shadowy figures of other travelers add to the bustling yet contemplative airport ambiance.
