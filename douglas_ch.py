import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
import csv


class Product():
    def __init__(self, title, brand_line, price, base_price, discount_price, strikethrough_price): #, image):
        self.title = title
        self.brand_line = brand_line
        self.price = price
        self.base_price = base_price
        self.discount_price = discount_price
        self.strikethrough_price = strikethrough_price
        #self.image = image


class ProductFetcher():
    def fetch(self):
        url = "https://www.douglas.ch/de/c/parfum/damenduefte/damenparfum/010106?page=1"

        articles = []
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
            base_price = product.select_one(".product-price__base-price").text
            discount_price = product.select_one(".product-price__discount")
            if discount_price:
                discount_price = discount_price.text
            strikethrough_price = product.select_one(".product-price__strikethrough")
            if strikethrough_price:
                strikethrough_price = strikethrough_price.text
            #image = product.select_one("img").attrs["src"]


            crawled = Product(title, brand_line, price, base_price, discount_price, strikethrough_price) #, image)
            articles.append(crawled)

        homepages = []
        for x in doc.find_all("a", class_ = "link link--no-decoration pagination-title__option-link active"):
            homepages.append(x.get("href"))

        ################ Seite 2 bis Ende


        for thing in homepages:
            nextone = urljoin("https://www.douglas.ch/", str(thing))
            print(nextone)

            link_two = requests.get(nextone)
            suppe = BeautifulSoup(link_two.text, "html.parser")


            for product in suppe.select(".product-tile"):
                title = product.select_one(".product-tile__top-brand").text
                brand_line = product.select_one(".product-tile__brand-line").text
                #category = product.select_one(".product-tile__category").text
                price = product.select_one(".product-price__no-discount")
                if price:
                    price = price.text
                base_price = product.select_one(".product-price__base-price").text
                discount_price = product.select_one(".product-price__discount")
                if discount_price:
                    discount_price = discount_price.text
                strikethrough_price = product.select_one(".product-price__strikethrough")
                if strikethrough_price:
                    strikethrough_price = strikethrough_price.text
                #image = product.select_one("img").attrs["src"]


                crawled = Product(title, brand_line, price, base_price, discount_price, strikethrough_price) #, image)
                articles.append(crawled)

        return articles


#for article in articles:
#    print(article.title)
fetcher = ProductFetcher()
#articles = fetcher.fetch()

with open( 'douglas.ch.csv', 'w', newline='', encoding= "utf-8" ) as csvfile:
    blogwriter = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    for article in fetcher.fetch():
        blogwriter.writerow( [article.title, article.brand_line, article.price, article.base_price,
                              article.discount_price, article.strikethrough_price] )
