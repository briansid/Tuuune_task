from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session


import crud
import models
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(debug=True)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def get_tax(salary: int, detailed: bool = False, db: Session = Depends(get_db)):
    dealers = crud.get_tax(db, salary, detailed)
    return dealers
