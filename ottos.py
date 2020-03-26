import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time



class Product():
    def __init__(self, name, size, price):
        self.name = name
        self.size = size
        self.price = price
        #self.konprice = konprice #konkurrenzprice


url = "https://www.ottos.ch/de/parfum/damenparfum.html"

articles = []
time.sleep(1)
r = requests.get(url)
soup = BeautifulSoup(r.text, "html.parser")


for element in soup.find_all("div", attrs={"class":"product-item-info per-product category-products-grid"}):
    description = element.select_one("h2").text
    name = description[:-5]
    print(name)
    size = description[-6:]
    if size[0] == " ":
        size = description[-5:]
    print(size)
    for thing in element.find_all("span"):
        daten = thing.get("data-price-amount")
        if daten != None:
            price = daten
        else:
            continue
        print(price)




#    konprice = element.select_one("p", attrs={"class":"competitive-price"}).text

