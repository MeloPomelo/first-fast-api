import requests
from re import sub
from decimal import Decimal
from bs4 import BeautifulSoup
from backend.db import add_oil_price


URL = 'https://ru.investing.com/commodities/brent-oil'

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.5 Safari/605.1.15',
}


def parse_oil_prices():
    page = requests.get(url=URL, headers=headers)
    soup = BeautifulSoup(page.content, "lxml")

    title = soup.find('h1', attrs={'class': 'text-2xl font-semibold instrument-header_title__GTWDv mobile:mb-2'}).get_text()
    price = soup.find('span', attrs={'class': 'text-2xl'}).get_text().replace(",", ".")
    price_float = float(Decimal(sub(r"[^\d\-.]", "", price)))

    add_oil_price(title, price_float)



