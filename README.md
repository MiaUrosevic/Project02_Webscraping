# eBay Search Scraper

## Overview

This project contains a Python script called **ebay-dl.py** that scrapes item listings from eBay search results.

The program accepts a search term from the command line, downloads the first 10 pages of eBay search results, and extracts information about each item. The extracted information is stored in a list of dictionaries and saved to a file.

Each item contains the following fields:

* **name** – the item title
* **price** – item price in cents (stored as an integer)
* **status** – condition of the item (Brand New, Refurbished, Pre-owned, etc.)
* **shipping** – shipping cost in cents (0 if shipping is free)
* **free_returns** – boolean value indicating whether the item has free returns
* **items_sold** – number of units sold

If an item does not contain one of these fields, the value is stored as `None`.

By default, results are saved as **JSON files**. If the optional `--csv` flag is used, the results are saved as **CSV files** instead.

---

## How to Run the Program

Run the script from the command line and provide a search term.

Example commands used to generate the JSON files in this repository:

```
python ebay-dl.py "gaming mouse"
python ebay-dl.py basketball
python ebay-dl.py "wireless keyboard"
```

These commands generate:

```
gaming_mouse.json
basketball.json
wireless_keyboard.json
```

---

## Using the CSV Option (Extra Credit)

The script also supports an optional `--csv` flag. When this flag is included, the output will be saved as a CSV file instead of JSON.

Example:

```
python ebay-dl.py "gaming mouse" --csv
python ebay-dl.py basketball --csv
python ebay-dl.py "wireless keyboard" --csv
```

These commands generate:

```
gaming_mouse.csv
basketball.csv
wireless_keyboard.csv
```

---

## Course Project

This assignment was completed as part of the CSCI040 web scraping project.
[CSCI40 Project 2 Instructions](https://github.com/mikeizbicki/cmc-csci040/tree/2026spring/project_02_webscraping)