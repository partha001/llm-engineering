# scrapper.py  . here in this file we have just added one more method on top of scrapper1.py
import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
}

def get_contents(url):
    """
    Return the title and contents of the website for the given URL
    """
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    title = soup.title.string if soup.title else "No title found"
    for irrelevant in soup.body(["script", "style", "img", "input"]):
        irrelevant.decompose()
    text = soup.body.get_text(separator="\n", strip=True)
    return title + "\n\n" + text


def get_website_links(url):
    """
    Return the links on the website at the given url
    I realize this is an ineffecient as we'r parsing the website twice. This is to keep the code simple
    Feel free to use a class and optimize this. 

    The ideal design will be a class with url as constructor argument. so that the website is parsed only ones
    """
    response  = requests.get(url, headers= headers)
    soup = BeautifulSoup(response.content, "html.parser")
    links = [link.get("href") for link in soup.find_all("a")]

    return [link for link in links if link]