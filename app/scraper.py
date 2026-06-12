import requests
from bs4 import BeautifulSoup
import json
import os
from urllib.parse import urljoin

BASE_URL = "https://books.toscrape.com/"
OUTPUT_FILE = "data/products.json"

def scrape_books():
    products = []
    page_url = BASE_URL + "catalogue/page-1.html"

    while page_url:
        response = requests.get(page_url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        books = soup.select("article.product_pod")

        for book in books:
            title = book.h3.a["title"]
            price = book.select_one(".price_color").text
            availability = book.select_one(".availability").text.strip()
            rating = book.p["class"][1]
            detail_url = urljoin(page_url, book.h3.a["href"])

            detail_res = requests.get(detail_url, timeout=10)
            detail_soup = BeautifulSoup(detail_res.text, "html.parser")

            description_tag = detail_soup.select_one("#product_description")
            description = ""
            if description_tag:
                description = description_tag.find_next("p").text

            category = detail_soup.select("ul.breadcrumb li a")[-1].text

            specs = {}
            for row in detail_soup.select("table.table.table-striped tr"):
                key = row.th.text.strip()
                value = row.td.text.strip()
                specs[key] = value

            image_tag = detail_soup.select_one(".item.active img")
            image_url = urljoin(detail_url, image_tag["src"]) if image_tag else None

            products.append({
                "name": title,
                "description": description,
                "price": price,
                "category": category,
                "rating": rating,
                "availability": availability,
                "specifications": specs,
                "image": image_url,
                "url": detail_url
            })

        next_btn = soup.select_one("li.next a")
        page_url = urljoin(page_url, next_btn["href"]) if next_btn else None

    os.makedirs("data", exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(products, f, indent=2, ensure_ascii=False)

    print(f"Scraped {len(products)} products.")

if __name__ == "__main__":
    scrape_books()