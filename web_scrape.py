import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://www.datart.cz/gamepady-pro-playstation-4.html"

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

        name_raw = product.select_one("h3.item-title a").get_text(strip=True)
        name = name_raw if name_raw else "Unknown"

        rating_raw = product.select_one("span.bold")
        rating = rating_raw.text if rating_raw else "0"

        review_count_raw = product.select_one("span.text-underline").get_text(strip=True)
        review_count = review_count_raw if review_count_raw else "0"

        products.append({
            "Name": name,
            "Rating": rating,
            "Review Count": review_count
            })
        

    df = pd.DataFrame(products)

    df["Rating"] = df["Rating"].fillna("0")

    return df

response = fetch_web_data(url)

soup = parse_html(response)

df = convert_to_df(soup)

print(df)


df.to_csv("products.csv", index=False)
