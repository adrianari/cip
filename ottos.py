import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time



class Product():
    def __init__(self, name, size_ml, price):
        self.name = name
        self.size = size_ml
        self.price = price
        #self.konprice = konprice #konkurrenzprice


url = "https://www.ottos.ch/de/parfum/damenparfum.html"

articles = []
time.sleep(1)
r = requests.get(url)
soup = BeautifulSoup(r.text, "html.parser")

#Seiten
pages = []
for filtering in soup.find_all("a", class_="page"):
    seiten = filtering.get("href")
    if seiten in pages:
        continue
    else:
        pages.append(seiten)
print(pages)

#Parfums
for element in soup.find_all("div", attrs={"class":"product-item-info per-product category-products-grid"}):
    description = element.select_one("h2").text
    name = description[:-5]
    print(name)
    size_ml = description[-6:-2]
    if size_ml[0] == " ":
        size_ml = description[-5:-2]
    print(size_ml)
    for thing in element.find_all("span"):
        daten = thing.get("data-price-amount")
        if daten != None:
            price = daten
        else:
            continue
        print(price)

    # for ding in element.select("div", class_ = ("price-box price-final_price fl-product-price")):
    #     print(ding)
