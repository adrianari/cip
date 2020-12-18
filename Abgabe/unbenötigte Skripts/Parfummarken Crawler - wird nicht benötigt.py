import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
import csv

zucrawlen = "https://www.parfumo.net/Brands"
time.sleep(1)
r = requests.get(zucrawlen)
lasoupe = BeautifulSoup(r.text, "html.parser")
bad_chars = ["(", ")", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "\n"]
marken =[]
for element in lasoupe.find_all("div", class_="list-col-3"):
    x = element.text
    for i in bad_chars :
        x = x.replace(i, '')
    marken.append(x)
marke = marken[39:-3] #die ersten 39 und letzten drei werden garantiert nicht gebraucht

print(marke)