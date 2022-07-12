from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class FuelPrice(Base):
    __tablename__ = "price"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    price = Column(Float)
    datetime = Column(DateTime)

    def __repr__(self):
        return f"{self.title} | {self.price} | {self.datetime}"


class OilPrice(Base):
    __tablename__ = "oil"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    price = Column(Float)
    datetime = Column(DateTime)

    def __repr__(self):
        return f"{self.title} | {self.price} | {self.datetime}"


engine = create_engine("sqlite:///database.sqlite")
Base.metadata.create_all(engine)
session = Session(bind=engine)


def add_fuel_price(prices):
    for fuel in prices:
        title = fuel
        price = prices[fuel]

        session.add(
                FuelPrice(
                    title=title,
                    price=price,
                    datetime=datetime.now(),
                )
            )
        session.commit()


def add_oil_price(title, price):
    session.add(
            OilPrice(
                title=title,
                price=price,
                datetime=datetime.now(),
            )
        )
    session.commit()


def get_fuel_prices():
    print('-----FROM DB-----')
    items = session.query(FuelPrice).all()
    for item in items:
        print(item)


def get_oil_prices():
    print('-----FROM DB-----')
    items = session.query(OilPrice).all()
    for item in items:
        print(item)



