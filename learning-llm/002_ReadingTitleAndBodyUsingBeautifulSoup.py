'''
reading the title and body of website using beautifulSoup
'''
import requests
from bs4 import BeautifulSoup


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

website = Website("https://www.screener.in/")
print(website.title)
print(website.text)