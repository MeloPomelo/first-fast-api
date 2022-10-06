from datetime import date

from pydantic import BaseModel


class FuelBase(BaseModel):
    title: str
    price: float


class FuelCreate(FuelBase):
    pass


class Fuel(FuelBase):
    id: int
    oil_price_id: int
    date: date

    class Config:
        orm_mode = True


class OilBase(BaseModel):
    title: str
    price: float
    date: date


class OilCreate(OilBase):
    pass


class OilUpdate(BaseModel):
    title: str
    price: float


class Oil(OilBase):
    id: int
    fuels_prices: list[Fuel] = []

    class Config:
        orm_mode = True
