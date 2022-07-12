from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime

app = FastAPI()


class FuelPrice(BaseModel):
    title = str
    price = float
    datetime = datetime


class OilPrice(BaseModel):
    title = str
    price = float
    datetime = datetime


FUEL_DB = [
    FuelPrice(title='test1', price='1000', datetime=datetime.now()),
    FuelPrice(title='test2', price='2000', datetime=datetime.now()),
    FuelPrice(title='test3', price='3000', datetime=datetime.now()),
    FuelPrice(title='test4', price='4000', datetime=datetime.now()),
    FuelPrice(title='test5', price='5000', datetime=datetime.now()),
]

OIL_DB = [
    OilPrice(title='test1', price='1000', datetime=datetime.now()),
    OilPrice(title='test2', price='2000', datetime=datetime.now()),
    OilPrice(title='test3', price='3000', datetime=datetime.now()),
    OilPrice(title='test4', price='4000', datetime=datetime.now()),
    OilPrice(title='test5', price='5000', datetime=datetime.now()),
]


@app.get("/fuel")
def read_products():
    return FUEL_DB


@app.get("/fuel/{item_id}")
def read_product(item_id: int):
    return FUEL_DB[item_id]


@app.post("/fuel/create")
def create_product(item: FuelPrice):
    FUEL_DB.append(item)
    return {'status': 'ok'}


@app.put("/fuel/{item_id}")
def update_product(item_id: int, item: FuelPrice):
    FUEL_DB[item_id] = item
    return {'status': 'ok'}


@app.delete("/fuel/{item_id}")
def update_product(item_id: int):
    FUEL_DB.remove(item_id)
    return {'status': 'ok'}



