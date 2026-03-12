import argparse
import requests
from bs4 import BeautifulSoup
import json
import csv
import re

# -----------------------------
# command line arguments
# -----------------------------
parser = argparse.ArgumentParser()
parser.add_argument("search_term")
parser.add_argument("--csv", action="store_true")

args = parser.parse_args()

search_term = args.search_term
search_url_term = search_term.replace(" ", "+")

items = []

# headers help avoid being blocked by ebay
headers = {
    "User-Agent": "Mozilla/5.0"
}

# -----------------------------
# loop through 10 pages
# -----------------------------
for page in range(1, 11):

    url = f"https://www.ebay.com/sch/i.html?_nkw={search_url_term}&_pgn={page}"

    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.text, "html.parser")

    results = soup.find_all("li", class_="s-item")

    for r in results:

        # -----------------------------
        # name
        # -----------------------------
        name_tag = r.find("span", class_="s-item__title")
        name = name_tag.text if name_tag else None

        # skip "shop on ebay" placeholder
        if name == "Shop on eBay":
            continue

        # -----------------------------
        # price
        # -----------------------------
        price_tag = r.find("span", class_="s-item__price")
        price = None

        if price_tag:
            match = re.search(r"\$([\d\.]+)", price_tag.text)
            if match:
                price = int(float(match.group(1)) * 100)

        # -----------------------------
        # condition
        # -----------------------------
        status_tag = r.find("span", class_="SECONDARY_INFO")
        status = status_tag.text if status_tag else None

        # -----------------------------
        # shipping
        # -----------------------------
        shipping_tag = r.find("span", class_="s-item__shipping")
        shipping = None

        if shipping_tag:
            text = shipping_tag.text.lower()

            if "free" in text:
                shipping = 0
            else:
                match = re.search(r"\$([\d\.]+)", text)
                if match:
                    shipping = int(float(match.group(1)) * 100)

        # -----------------------------
        # free returns
        # -----------------------------
        returns_tag = r.find("span", class_="s-item__free-returns")
        free_returns = True if returns_tag else False

        # -----------------------------
        # items sold
        # -----------------------------
        sold_tag = r.find("span", class_="s-item__hotness")
        items_sold = None

        if sold_tag:
            match = re.search(r"\d+", sold_tag.text)
            if match:
                items_sold = int(match.group())

        item = {
            "name": name,
            "price": price,
            "status": status,
            "shipping": shipping,
            "free_returns": free_returns,
            "items_sold": items_sold
        }

        items.append(item)

# -----------------------------
# save output
# -----------------------------
filename = search_term.replace(" ", "_")

if args.csv:

    with open(filename + ".csv", "w", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "name",
                "price",
                "status",
                "shipping",
                "free_returns",
                "items_sold"
            ]
        )
        writer.writeheader()
        writer.writerows(items)

else:

    with open(filename + ".json", "w") as f:
        json.dump(items, f, indent=4)