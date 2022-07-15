from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime


import crud
import models
import schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/oil_prices/", response_model=schemas.Oil)
def create_oil_price(oil_price: schemas.OilCreate, db: Session = Depends(get_db)):
    db_oil_price = crud.get_oil_price_by_date(db, date=oil_price.date)
    if db_oil_price:
        raise HTTPException(status_code=400, detail="The price for this day already exists")
    return crud.create_oil_price(db=db, oil_price=oil_price)


@app.post("/parse_prices/", response_model=schemas.Oil)
def parse_prices(db: Session = Depends(get_db)):
    return crud.parse_oil_price(db)


@app.get("/oil_prices/", response_model=list[schemas.Oil])
def read_oil_prices(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    oil_prices = crud.get_oil_prices(db, skip=skip, limit=limit)
    return oil_prices


@app.get("/oil_prices/{oil_price_id}", response_model=schemas.Oil)
def read_oil_price(oil_price_id: int, db: Session = Depends(get_db)):
    db_oil_price = crud.get_oil_price(db, oil_price_id=oil_price_id)
    if db_oil_price is None:
        raise HTTPException(status_code=404, detail="Oil price not found")
    return db_oil_price


@app.get("/prices/{date}", response_model=schemas.Oil)
def read_prices_by_date(dt: str, db: Session = Depends(get_db)):
    dt = datetime.strptime(dt, "%Y-%m-%d").date()
    print(dt)
    db_oil_price = crud.get_oil_price_by_date(db, date=dt)
    if db_oil_price is None:
        raise HTTPException(status_code=404, detail="Oil price not found")
    return db_oil_price


@app.put("/oil_prices/{oil_price_id}", response_model=schemas.Oil)
def update_oil_price(oil_price_id: int, oil_price: schemas.OilUpdate, db: Session = Depends(get_db)):
    db_oil_price = crud.get_oil_price(db, oil_price_id=oil_price_id)
    if db_oil_price is None:
        raise HTTPException(status_code=404, detail="Oil price not found")
    return crud.update_oil_price(db, oil_price_id, oil_price)


@app.delete("/oil_prices/{oil_price_id}", response_model=dict)
def delete_oil_price(oil_price_id: int, db: Session = Depends(get_db)):
    db_oil_price = crud.get_oil_price(db, oil_price_id=oil_price_id)
    if db_oil_price is None:
        raise HTTPException(status_code=404, detail="Oil price not found")
    crud.delete_oil_price(db, oil_price_id)
    return {
        'oil_price_id': oil_price_id,
        'status': 'delete successfully'
    }


@app.post("/oil_prices/{oil_price_id}/fuel_price/", response_model=schemas.Fuel)
def create_fuel_price(
    oil_price_id: int, fuel_price: schemas.FuelCreate, db: Session = Depends(get_db)
):
    return crud.create_fuel_price(db=db, fuel_price=fuel_price, oil_price_id=oil_price_id)


@app.get("/fuel_prices/", response_model=list[schemas.Fuel])
def read_fuel_prices(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    fuel_prices = crud.get_fuel_prices(db, skip=skip, limit=limit)
    return fuel_prices


@app.get("/fuel_prices/{fuel_price_id}", response_model=schemas.Fuel)
def read_fuel_price(fuel_price_id: int, db: Session = Depends(get_db)):
    db_fuel_price = crud.get_fuel_price(db, fuel_price_id=fuel_price_id)
    if db_fuel_price is None:
        raise HTTPException(status_code=404, detail="Fuel price not found")
    return db_fuel_price


@app.put("/fuel_prices/{fuel_price_id}", response_model=schemas.Fuel)
def update_fuel_price(fuel_price_id: int, fuel_price: schemas.FuelCreate, db: Session = Depends(get_db)):
    db_fuel_price = crud.get_fuel_price(db, fuel_price_id=fuel_price_id)
    if db_fuel_price is None:
        raise HTTPException(status_code=404, detail="Fuel price not found")
    return crud.update_fuel_price(db, fuel_price_id, fuel_price)


@app.delete("/fuel_prices/{fuel_price_id}", response_model=dict)
def delete_fuel_price(fuel_price_id: int, db: Session = Depends(get_db)):
    db_fuel_price = crud.get_fuel_price(db, fuel_price_id=fuel_price_id)
    if db_fuel_price is None:
        raise HTTPException(status_code=404, detail="Fuel price not found")
    crud.delete_fuel_price(db, fuel_price_id)
    return {
        'fuel_price_id': fuel_price_id,
        'status': 'delete successfully'
    }
