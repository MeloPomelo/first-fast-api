from sqlalchemy.orm import Session
from datetime import date
import requests
from re import sub
from decimal import Decimal
from bs4 import BeautifulSoup


import models
import schemas
from constants import *


def get_oil_price(db: Session, oil_price_id: int):
    return db.query(models.OilPrice).filter(models.OilPrice.id == oil_price_id).first()


def get_oil_price_by_date(db: Session, date: date):
    return db.query(models.OilPrice).filter(models.OilPrice.date == date).first()


def get_oil_prices(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.OilPrice).offset(skip).limit(limit).all()


def create_oil_price(db: Session, oil_price: schemas.OilCreate):
    db_oil_price = models.OilPrice(
        title=oil_price.title,
        price=oil_price.price,
        date=oil_price.date,
    )
    db.add(db_oil_price)
    db.commit()
    db.refresh(db_oil_price)
    return db_oil_price


def parse_oil_price(db: Session):
    page = requests.get(url=OIL_URL, headers=headers)
    soup = BeautifulSoup(page.content, "lxml")

    title = soup.find('h1', attrs={'class': 'text-2xl font-semibold instrument-header_title__GTWDv mobile:mb-2'}).get_text()
    price = soup.find('span', attrs={'class': 'text-2xl'}).get_text().replace(",", ".")
    price_float = float(Decimal(sub(r"[^\d\-.]", "", price)))

    db_oil_price = models.OilPrice(
        title=title,
        price=price_float,
        date=date.today(),
    )
    db.add(db_oil_price)
    db.commit()
    db.refresh(db_oil_price)
    parse_fuel_prices(db, db_oil_price.id)
    return db_oil_price


def update_oil_price(db: Session, oil_price_id: int, oil_price: schemas.OilUpdate):
    new_oil_price = db.query(models.OilPrice).filter(models.OilPrice.id == oil_price_id).first()
    new_oil_price.title = oil_price.title
    new_oil_price.price = oil_price.price
    db.add(new_oil_price)
    db.commit()
    db.refresh(new_oil_price)
    return new_oil_price


def delete_oil_price(db: Session, oil_price_id: int):
    db.query(models.OilPrice).filter(models.OilPrice.id == oil_price_id).delete()
    db.query(models.FuelPrice).filter(models.FuelPrice.oil_price_id == oil_price_id).delete()
    db.commit()
    return


def get_fuel_price(db: Session, fuel_price_id: int):
    return db.query(models.FuelPrice).filter(models.FuelPrice.id == fuel_price_id).first()


def get_fuel_prices(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.FuelPrice).offset(skip).limit(limit).all()


def create_fuel_price(db: Session, fuel_price: schemas.FuelCreate, oil_price_id: int):
    oil_price = db.query(models.OilPrice).filter(models.OilPrice.id == oil_price_id).first()
    db_fuel_price = models.FuelPrice(
        title=fuel_price.title,
        price=fuel_price.price,
        date=oil_price.date,
        oil_price_id=oil_price_id,
    )
    db.add(db_fuel_price)
    db.commit()
    db.refresh(db_fuel_price)
    return db_fuel_price


def parse_fuel_prices(db: Session, oil_price_id: int):
    oil_price = db.query(models.OilPrice).filter(models.OilPrice.id == oil_price_id).first()

    page = requests.get(url=FUEL_URL, headers=headers)
    soup = BeautifulSoup(page.content, "lxml")

    table = soup.find('table', attrs={'class': 'table table-striped table-bordered'})
    rows = table.find_all("tr")

    for i in range(1, 5):
        data = rows[i].find_all("td")
        title = data[0].get_text()
        price = data[1].get_text().replace(",", ".")
        price_float = float(Decimal(sub(r"[^\d\-.]", "", price)))

        db_fuel_price = models.FuelPrice(
            title=title,
            price=price_float,
            date=oil_price.date,
            oil_price_id=oil_price_id,
        )
        db.add(db_fuel_price)
        db.commit()
        db.refresh(db_fuel_price)

    return


def update_fuel_price(db: Session, fuel_price_id: int, fuel_price: schemas.FuelCreate):
    new_fuel_price = db.query(models.FuelPrice).filter(models.FuelPrice.id == fuel_price_id).first()
    new_fuel_price.title = fuel_price.title
    new_fuel_price.price = fuel_price.price
    db.add(new_fuel_price)
    db.commit()
    db.refresh(new_fuel_price)
    return new_fuel_price


def delete_fuel_price(db: Session, fuel_price_id: int):
    db.query(models.FuelPrice).filter(models.FuelPrice.id == fuel_price_id).delete()
    db.commit()
    return



