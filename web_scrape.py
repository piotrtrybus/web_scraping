import requests
from bs4 import BeautifulSoup
import pandas as pd

#Fetch from URL
url = "http://books.toscrape.com/"
response = requests.get(url)
response.raise_for_status()

#HTML Parse
soup = BeautifulSoup(response.text, "html.parser")

products = []
for book in soup.select(".product_pod"):
    title = book.h3.a["title"]
    price = book.select_one(".price_color").text
    availability = book.select_one(".availability").text
    link = book.h3.a["href"]

    products.append({
        "Title": title,
        "Price": price,
        "Availability": availability,
        "Link": link
    })


df = pd.DataFrame(products)

df.to_csv("books.csv", index=False)