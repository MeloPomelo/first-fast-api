from fastapi import FastAPI

import oil_prices
import fuel_prices
import models
from database import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(oil_prices.router)
app.include_router(fuel_prices.router)


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}
