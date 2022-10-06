from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date
from sqlalchemy.orm import relationship

from app.models.database import Base


class FuelPrice(Base):
    __tablename__ = "fuel_prices"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    price = Column(Float)
    date = Column(Date)
    oil_price_id = Column(Integer, ForeignKey("oil_prices.id"))

    oil_price = relationship("OilPrice", backref="fuel_prices")

    def __repr__(self):
        return f"{self.title} | {self.price} | {self.date}"
