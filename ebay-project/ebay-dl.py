import argparse
import requests
from bs4 import BeautifulSoup
import json
import re


# -----------------------------
# Read search term from CLI
# -----------------------------
parser = argparse.ArgumentParser()
parser.add_argument("search_term", help="item to search on ebay")
args = parser.parse_args()

search_term = args.search_term
search_term_url = search_term.replace(" ", "+")


# -----------------------------
# Store results here
# -----------------------------
items = []


# -----------------------------
# Loop through first 10 pages
# -----------------------------
for page in range(1, 11):

    url = f"https://www.ebay.com/sch/i.html?_nkw={search_term_url}&_pgn={page}"

    response = requests.get(url)

    soup = BeautifulSoup(response.text, "html.parser")

    results = soup.find_all("li", class_="s-item")

    for r in results:

        # -----------------------------
        # Name
        # -----------------------------
        name_tag = r.find("div", class_="s-item__title")
        name = name_tag.text if name_tag else None


        # -----------------------------
        # Price (convert to cents)
        # -----------------------------
        price_tag = r.find("span", class_="s-item__price")
        price = None

        if price_tag:
            text = price_tag.text
            match = re.search(r"\$([\d\.]+)", text)

            if match:
                dollars = float(match.group(1))
                price = int(dollars * 100)


        # -----------------------------
        # Item condition
        # -----------------------------
        status_tag = r.find("span", class_="SECONDARY_INFO")
        status = status_tag.text if status_tag else None


        # -----------------------------
        # Shipping cost
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
        # Free returns
        # -----------------------------
        returns_tag = r.find("span", class_="s-item__free-returns")
        free_returns = True if returns_tag else False


        # -----------------------------
        # Items sold
        # -----------------------------
        sold_tag = r.find("span", class_="s-item__hotness")
        items_sold = None

        if sold_tag:
            match = re.search(r"\d+", sold_tag.text)

            if match:
                items_sold = int(match.group())


        # -----------------------------
        # Create dictionary
        # -----------------------------
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
# Save results to JSON
# -----------------------------
filename = search_term.replace(" ", "_") + ".json"

with open(filename, "w") as f:
    json.dump(items, f, indent=4)