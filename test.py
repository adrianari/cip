import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
import csv

class Product():
    def __init__(self, name, kategorie, size_ml, price):
        self.name = name
        self.kategorie = kategorie
        self.size = size_ml
        self.price = price
        #self.konprice = konprice #konkurrenzprice

class ProductFetcher():

    def fetch(self):
        url = "https://www.ottos.ch/de/parfum/damenparfum.html"

        def namer(bubble):
            name = bubble[:-6]
            return name

        def catsmaker(tester):
            cats = ["Bodylotion", "Bodyspray", "Eau de Cologne", "Eau de Parfum", "Eau de Toilette", "Geschenkset", "Bodymist", "Eau Frâiche", "Eau Fraîche", "Spray", "Körperspray", "EdP"]
            for cat in cats:
                if cat in tester:
                    kategorie = cat
                else:
                    continue
            if kategorie == "EdP":
                kategorie = "Eau de Parfum"
            if kategorie == "Körperspray" and "Spray":
                kategorie = "Bodyspray"
            if kategorie == "Eau Frâiche":
                kategorie = "Eau Fraîche"


            return kategorie

        def sizer(data):
            size_ml = data[-6:-2]
            if size_ml[0] == " ":
                size_ml = data[-5:-2]
            return size_ml

        def beautify(naming):
            cats = ["Bodylotion", "Bodyspray", "Eau de Cologne", "Eau de Parfum", "Eau de Toilette", "Geschenkset", "Bodymist", "Eau Frâiche", "Eau Fraîche", "Spray", "Körperspray", "EdP"]
            for cat in cats:
                if cat in naming:
                    name = naming.replace(cat, "")
            return name

        def crawling(element):
            description = element.select_one("h2").text
            naming = namer(description)
            kategorie = catsmaker(naming)
            name = beautify(naming)
            size_ml = sizer(description)
            for thing in element.find_all("span"):
                daten = thing.get("data-price-amount")
                if daten != None:
                    price = daten
                else:
                    continue

            crawled = Product(name, kategorie, size_ml, price)
            articles.append(crawled)




        articles = []
        time.sleep(1)
        r = requests.get(url)
        soup = BeautifulSoup(r.text, "html.parser")

        for element in soup.find_all("div", attrs={"class":"product-item-info per-product category-products-grid"}):
            crawling(element)

        #Seiten
        pages = []
        for filtering in soup.find_all("a", class_="page"):
            seite = filtering.get("href")
            if seite in pages:
                continue
            else:
                pages.append(seite)

        for thing in pages:
            nextone = urljoin("https://www.ottos.ch/", str(thing))
            link_two = requests.get(nextone)
            suppe = BeautifulSoup(link_two.text, "html.parser")

            for element in suppe.find_all("div", attrs={"class":"product-item-info per-product category-products-grid"}):
                crawling(element)

                for filtering in suppe.find_all("a", class_="page"):
                    seite = filtering.get("href")
                    if seite in pages:
                        continue
                    else:
                        pages.append(seite)


        print(pages)
        return articles




fetcher = ProductFetcher()
#articles = fetcher.fetch()

with open('testertest.csv', 'w', newline='', encoding="utf-8") as csvfile:
    blogwriter = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    for article in fetcher.fetch():
        blogwriter.writerow( [article.name, article.kategorie, article.size, article.price] )



    # for ding in element.select("div", class_ = ("price-box price-final_price fl-product-price")):
    #     print(ding)



