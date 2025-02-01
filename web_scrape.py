import requests
from bs4 import BeautifulSoup
import pandas as pd

def fetch_web_data(url):
    response = requests.get(url)
    response.raise_for_status()
    return response

def parse_html(response):
    soup = BeautifulSoup(response.text, "html.parser")
    return soup


def convert_to_df(soup):
    products =[]
    for product in soup.select("div.product-box-top-side"):
        name = product.select_one("h3.item-title a").get_text(strip=True)
        rating = product.select_one("span.bold").get_text(strip=True)
        review_count = product.select_one("span.text-underline").get_text(strip=True)
        products.append({
            "Name": name,
            "Rating": rating,
            "Review Count": review_count
            })
        


    df = pd.DataFrame(products)

    return df

url = "https://www.datart.cz/iphone.html"

response = fetch_web_data(url)

soup = parse_html(response)

df = convert_to_df(soup)

print(df)


df.to_csv("products.csv", index=False)