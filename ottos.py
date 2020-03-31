import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
import csv

class Product():
    def __init__(self, name, size_ml, price):
        self.name = name
        self.size = size_ml
        self.price = price
        #self.konprice = konprice #konkurrenzprice

class ProductFetcher():
    def fetch(self):
        url = "https://www.ottos.ch/de/parfum/damenparfum.html"


        articles = []
        time.sleep(1)
        r = requests.get(url)
        soup = BeautifulSoup(r.text, "html.parser")



        for element in soup.find_all("div", attrs={"class":"product-item-info per-product category-products-grid"}):
            description = element.select_one("h2").text
            name = description[:-6]
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

            crawled = Product(name, size_ml, price)
            articles.append(crawled)

        #Seiten
        pages = []
        for filtering in soup.find_all("a", class_="page"):
            seite = filtering.get("href")
            if seite in pages:
                continue
            else:
                pages.append(seite)
        print(pages)



        for thing in pages:
            nextone = urljoin("https://www.ottos.ch/", str(thing))
            link_two = requests.get(nextone)
            suppe = BeautifulSoup(link_two.text, "html.parser")


            for element in suppe.find_all("div", attrs={"class":"product-item-info per-product category-products-grid"}):
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

                    crawled = Product(name, size_ml, price)
                    articles.append(crawled)




                for filtering in suppe.find_all("a", class_="page"):
                    seite = filtering.get("href")
                    if seite in pages:
                        continue
                    else:
                        pages.append(seite)


        print(pages)
        return articles




fetcher = ProductFetcher()
articles = fetcher.fetch()

with open( 'ottos.csv', 'w', newline='', encoding= "utf-8" ) as csvfile:
    blogwriter = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    for article in fetcher.fetch():
        blogwriter.writerow( [article.name, article.size, article.price] )



    # for ding in element.select("div", class_ = ("price-box price-final_price fl-product-price")):
    #     print(ding)



