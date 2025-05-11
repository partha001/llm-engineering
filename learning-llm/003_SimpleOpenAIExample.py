import os
import requests
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from IPython.display import Markdown, display
from openai import OpenAI


load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')

openai = OpenAI()

# this class represents a website that we we will scraped
class Website:
    """
    A utility class to represent a website that we h  n   ave scraped
    """
    url: str
    title: str
    text: str

    def __init__(self,url):
        """
        Create this website tobject from the given url using the BeautifulSoup library
        """
        self.url = url
        response = requests.get(url)
        soup = BeautifulSoup(response.content,'html.parser')
        self.title = soup.title.string if soup.title else "No title found"
        for irrelevant in soup.body(["script","style","img","input"]):
            irrelevant.decompose()
        self.text = soup.body.get_text(separator="\n", strip=True)

# website = Website("https://www.screener.in/")
# print(website.title)
# print(website.text)



system_prompt = "You are an assistant that analyzes the contents of a website \
and provices a short summary, ignoring text that might be navigation related. \
Respond in markdown."


def user_prompt_for(website) :
    user_prompt = f"You are looking at a websie titled {website.title}"
    user_prompt += "the contents of this website is a follows: \
please provid a short summary of this website in markdown. \
If it includes news or announcements, then summarize these too.\n\n"
    user_prompt += website.text
    return user_prompt


# print(user_prompt_for(website))


# # see how this function creates exactly the format above
def messages_for(website):
    return [
        {"role":"system", "content":system_prompt},
        {"role":"user", "content": user_prompt_for(website)}
    ]



def summarize(url):
    website = Website(url)
    response = openai.chat.completions.create(
        model = "gpt-4o-mini",
        messages = messages_for(website)
    )
    return response.choices[0].message.content

summarize("https://www.screener.in/")
