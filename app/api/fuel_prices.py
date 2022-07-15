from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session

import crud
import schemas
from database import SessionLocal


router = APIRouter(
    prefix="/fuel_prices",
    tags=["fuel_prices"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/{oil_price_id}", response_model=schemas.Fuel)
def create_fuel_price(
    oil_price_id: int, fuel_price: schemas.FuelCreate, db: Session = Depends(get_db)
):
    return crud.create_fuel_price(db=db, fuel_price=fuel_price, oil_price_id=oil_price_id)


@router.get("/", response_model=list[schemas.Fuel])
def read_fuel_prices(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    fuel_prices = crud.get_fuel_prices(db, skip=skip, limit=limit)
    return fuel_prices


@router.get("/{fuel_price_id}", response_model=schemas.Fuel)
def read_fuel_price(fuel_price_id: int, db: Session = Depends(get_db)):
    db_fuel_price = crud.get_fuel_price(db, fuel_price_id=fuel_price_id)
    if db_fuel_price is None:
        raise HTTPException(status_code=404, detail="Fuel price not found")
    return db_fuel_price


@router.put("/{fuel_price_id}", response_model=schemas.Fuel)
def update_fuel_price(fuel_price_id: int, fuel_price: schemas.FuelCreate, db: Session = Depends(get_db)):
    db_fuel_price = crud.get_fuel_price(db, fuel_price_id=fuel_price_id)
    if db_fuel_price is None:
        raise HTTPException(status_code=404, detail="Fuel price not found")
    return crud.update_fuel_price(db, fuel_price_id, fuel_price)


@router.delete("/{fuel_price_id}", response_model=dict)
def delete_fuel_price(fuel_price_id: int, db: Session = Depends(get_db)):
    db_fuel_price = crud.get_fuel_price(db, fuel_price_id=fuel_price_id)
    if db_fuel_price is None:
        raise HTTPException(status_code=404, detail="Fuel price not found")
    crud.delete_fuel_price(db, fuel_price_id)
    return {
        'fuel_price_id': fuel_price_id,
        'status': 'delete successfully'
    }