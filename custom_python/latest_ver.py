from bs4 import BeautifulSoup
import requests

r = requests.get("https://www.python.org/downloads/")

soup = BeautifulSoup(r.text, "html.parser")


def get_ver():
    return soup.find("div", class_="download-os-source").find("a")["href"][48:-7]
