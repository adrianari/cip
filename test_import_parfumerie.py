import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
import csv
import re


url = "https://www.impo.ch/de/parfum/damend%C3%BCfte/c/m_0007?page=20"
articles = []
time.sleep(1)
r = requests.get("https://www.impo.ch/de/parfum/damend%C3%BCfte/c/m_0007?page=20")
doc = BeautifulSoup(r.text, "html.parser")


articles = []
for product in doc.select(".list-page__item"):
    title = product.select_one(".product-item__name").text
    title = " ".join(title.split())                                       #Könnten wir auch im Tableau Prep machen
    brand_line = product.select_one(".split__key").text
    brand_line = " ".join(brand_line.split())                             #Könnten wir auch im Tableau Prep machen
    price = product.select_one(".product-item__price__value")
    if price:
        price = price.text
        price = " ".join(price.split())                                   #Könnten wir auch im Tableau Prep machen
    else:
        continue
    size = product.select_one('.split__value').text
    size = " ".join(size.split())                                          #Könnten wir auch im Tableau Prep machen
    category = product.select_one('.product-item__description').text
    category = " ".join(category.split())

    crawled = (title, brand_line, price, size, category)  # , base_price) #, image)
    articles.append(crawled)

for article in articles:
    print(article)



with open( 'import_parfumerie.csv', 'w', newline='', encoding= "utf-8" ) as csvfile:
    blogwriter = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    for article in articles:
        blogwriter.writerow( [article] )


