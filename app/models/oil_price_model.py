from sqlalchemy import Column, Integer, String, Float, Date
from sqlalchemy.orm import relationship

from app.models.database import Base


class OilPrice(Base):
    __tablename__ = "oil_prices"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    price = Column(Float)
    date = Column(Date)

    fuels_prices = relationship("FuelPrice", backref="_oil_price")

    def __repr__(self):
        return f"{self.title} | {self.price} | {self.date}"