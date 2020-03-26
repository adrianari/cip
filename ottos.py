import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time



class Product():
    def __init__(self, description, price):
        self.description = description
        self.price = price


url = "https://www.ottos.ch/de/parfum/damenparfum.html"

articles = []
time.sleep(1)
r = requests.get(url)
soup = BeautifulSoup(r.text, "html.parser")



for item in soup.select("h2", {"class_":("product details")}):
    print(item.text)

for price in soup.select("span", {"class_":"price-wrapper"}):
    x = price.get("data-price-amount")
    if x != None:
        print(x)
