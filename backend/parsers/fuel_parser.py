import requests
from re import sub
from decimal import Decimal
from bs4 import BeautifulSoup
from backend.db import add_fuel_price

URL = 'https://fuelprices.ru/uralfo/ekaterinburg'

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.5 Safari/605.1.15',
}


def parse_fuel_prices():
    fuel = {}

    page = requests.get(url=URL, headers=headers)
    soup = BeautifulSoup(page.content, "lxml")

    table = soup.find('table', attrs={'class': 'table table-striped table-bordered'})
    rows = table.find_all("tr")

    for i in range(1, 5):
        data = rows[i].find_all("td")
        title = data[0].get_text()
        price = data[1].get_text().replace(",", ".")
        price_float = float(Decimal(sub(r"[^\d\-.]", "", price)))

        fuel[title] = price_float

    add_fuel_price(fuel)

