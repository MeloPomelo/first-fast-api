from datetime import datetime

from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session

from app.crud import crud
from app.schemas import schemas
from app.models.database import SessionLocal

router = APIRouter(
    prefix="/oil_prices",
    tags=["oil_prices"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=schemas.Oil)
def create_oil_price(oil_price: schemas.OilCreate, db: Session = Depends(get_db)):
    db_oil_price = crud.get_oil_price_by_date(db, date=oil_price.date)
    if db_oil_price:
        raise HTTPException(status_code=400, detail="The price for this day already exists")
    return crud.create_oil_price(db=db, oil_price=oil_price)


@router.post("/parse_prices/", response_model=schemas.Oil)
def parse_prices(db: Session = Depends(get_db)):
    return crud.parse_oil_price(db)


@router.get("/", response_model=list[schemas.Oil])
def read_oil_prices(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    oil_prices = crud.get_oil_prices(db, skip=skip, limit=limit)
    return oil_prices


@router.get("/{oil_price_id}", response_model=schemas.Oil)
def read_oil_price(oil_price_id: int, db: Session = Depends(get_db)):
    db_oil_price = crud.get_oil_price(db, oil_price_id=oil_price_id)
    if db_oil_price is None:
        raise HTTPException(status_code=404, detail="Oil price not found")
    return db_oil_price


@router.get("/{date}", response_model=schemas.Oil)
def read_prices_by_date(dt: str, db: Session = Depends(get_db)):
    dt = datetime.strptime(dt, "%Y-%m-%d").date()
    print(dt)
    db_oil_price = crud.get_oil_price_by_date(db, date=dt)
    if db_oil_price is None:
        raise HTTPException(status_code=404, detail="Oil price not found")
    return db_oil_price


@router.put("/{oil_price_id}", response_model=schemas.Oil)
def update_oil_price(oil_price_id: int, oil_price: schemas.OilUpdate, db: Session = Depends(get_db)):
    db_oil_price = crud.get_oil_price(db, oil_price_id=oil_price_id)
    if db_oil_price is None:
        raise HTTPException(status_code=404, detail="Oil price not found")
    return crud.update_oil_price(db, oil_price_id, oil_price)


@router.delete("/{oil_price_id}", response_model=dict)
def delete_oil_price(oil_price_id: int, db: Session = Depends(get_db)):
    db_oil_price = crud.get_oil_price(db, oil_price_id=oil_price_id)
    if db_oil_price is None:
        raise HTTPException(status_code=404, detail="Oil price not found")
    crud.delete_oil_price(db, oil_price_id)
    return {
        'oil_price_id': oil_price_id,
        'status': 'delete successfully'
    }