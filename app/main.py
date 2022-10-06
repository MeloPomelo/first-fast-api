from fastapi import FastAPI

from api import oil_prices
from api import fuel_prices
from app.models.database import Base
from app.models.database import engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(oil_prices.router)
app.include_router(fuel_prices.router)


@app.get("/")
async def root():
    return {"message": "Hello there"}
