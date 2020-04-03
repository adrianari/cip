import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
import csv

class Product():
    def __init__(self, title, brand, kategorie, size_ml, price):
        self.title = title
        self.brand = brand
        self.kategorie = kategorie
        self.size = size_ml
        self.price = price

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


            return kategorie.strip()

        def sizer(data):
            size_ml = data[-6:-2]
            if size_ml[0] == " ":
                size_ml = data[-5:-2]
            return size_ml.strip()

        def beautify(naming):
            cats = ["Bodylotion", "Bodyspray", "Eau de Cologne", "Eau de Parfum", "Eau de Toilette", "Geschenkset", "Bodymist", "Eau Frâiche", "Eau Fraîche", "Spray", "Körperspray", "EdP"]
            for cat in cats:
                if cat in naming:
                    name = naming.replace(cat, "")
            return name

        def brander(name):
            global marken
            marken = ["Abercrombie & Fitch", "Arden", "Beyonce", "Biotherm", "Blue Up", "Britney Spears", "Bruno Banani", "Bulgari", "Burberry", "Cabochard", "Cabotine", "Cacharel", "Calvin Klein", "Carolina Herrera", "Cartier", "Cerruti", "Chloé", "Chopard", "Christina Aguilera", "Clean", "Clinique", "Coach", "Davidoff", "Diesel", "Dior", "DKNY", "Dolce & Gabbana", "Emporio Armani", "Escada", "Estée Lauder", "Gaultier", "Giorgio", "Grês", "Gucci", "Guerlain", "Guess", "Hermès", "Hollister", "Hugo Boss", "Issey Miyake", "James Bond", "Jean Patou", "Jean Paul Gaultier", "Jil Sander", "Jimmy Choo", "J.Lo", "JOOP!", "Juicy Couture", "Karl Lagerfeld", "Katy Perry", "Kenzo", "Lacoste", "Lady Gaga", "Lancôme", "Lanvin", "Laura Biagiotti", "Mexx", "Michael Kors", "Missoni", "Moschino", "Musk", "Naomi Campbell", "Narciso Rodriguez", "Nina Ricci", "Paco Rabanne", "Pepe Jeans London", "Prada", "Rainbow", "Ralph Lauren", "Rihanna", "Roberto Cavalli", "Sisley", "Slava Zaitsev", "s.Oliver", "Thierry Mugler", "Grès", "Tiffany", "Tommy Girl", "Vera Wang", "Versace", "Victoria's Secret", "Yves Saint Laurent", "Zadig & Voltaire", "Revlon", "Gabriella Sabatini", "Gloria Vanderbilt", "S. Oliver", "Gabriela Sabatini"]
            global korrektur
            korrektur = {"Gabriella Sabatini": "Gabriela Sabatini", "Giorgio": "Giorgio Armani", "Arden" : "Elizabeth Arden", "Arden Elizabeth" : "Elizabeth Arden", "Gaultier" : "Jean Paul Gaultier", "S. Oliver" : "s.Oliver"}
            for marke in marken:
                if marke in name:
                    brand = marke
                    if marke in korrektur:
                        brand = korrektur.get(marke)
                else:
                    continue
                return brand.strip()

        def finalizing(name):
            for marke in marken:
                if marke in name:
                    if marke in korrektur:
                        marke = korrektur[marke]
                    title = name.replace(marke, "")
                    if title == "" and " " and "\n":
                        title = marke
                else:
                    continue
                return title.strip()

        def crawling(element):
            description = element.select_one("h2").text
            naming = namer(description)
            kategorie = catsmaker(naming)
            name = beautify(naming)
            brand = brander(name)
            title = finalizing(name)
            size_ml = sizer(description)
            for thing in element.find_all("span"):
                daten = thing.get("data-price-amount")
                if daten != None:
                    price = daten.strip()
                else:
                    continue

            crawled = Product(title, brand, kategorie, size_ml, price)
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

with open('ottos.csv', 'w', newline='', encoding="utf-8") as csvfile:
    blogwriter = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    blogwriter.writerow(["Title", "Brand", "Kategorie", "Size in ml", "Price"])




    for article in fetcher.fetch():
        blogwriter.writerow( [article.title, article.brand, article.kategorie, article.size, article.price] )
