import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
import csv


class Product():
    def __init__(self, title, brand_line, price, base_price): #, image):
        self.title = title
        self.brand_line = brand_line
        self.price = price
        self.base_price = base_price
        #self.image = image

class ProductFetcher():
    def fetch(self):
        homepages = []
        url = "https://www.douglas.ch/de/c/parfum/damenduefte/damenparfum/010106?page=1"
        articles = []

        while url not in homepages:
            homepages.append(url)
            time.sleep(1)
            r = requests.get(url)
            doc = BeautifulSoup(r.text, "html.parser")

            for product in doc.select(".product-tile"):
                title = product.select_one(".product-tile__top-brand").text
                brand_line = product.select_one(".product-tile__brand-line").text
                #category = product.select_one(".product-tile__category").text
                price = product.select_one(".product-price__no-discount")
                if price:
                    price = price.text
                else:
                    continue
                base_price = product.select_one(".product-price__base-price").text
                #image = product.select_one("img").attrs["src"]


                crawled = Product(title, brand_line, price, base_price) #, image)
                articles.append(crawled)

            for x in doc.find_all("a", class_="link link--text pagination__arrow active"):
                if urljoin(url,x.get("href")) not in homepages:
                    url = urljoin(url,x.get("href"))
                    break
                else:
                    pass


            print(homepages)
        return articles





#for article in articles:
#    print(article.title)
fetcher = ProductFetcher()
articles = fetcher.fetch()

with open( 'douglas.ch.csv', 'w', newline='', encoding= "utf-8" ) as csvfile:
    blogwriter = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    for article in fetcher.fetch():
        blogwriter.writerow( [article.title, article.brand_line, article.price, article.base_price] )
