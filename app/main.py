# app/main.py
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.lib.db import models
from app.lib.db.database import engine
from app.lib.db.dependencies import get_db

models.Base.metadata.create_all(bind=engine)  # ← Crée les tables à partir des modèles

app = FastAPI()

@app.get("/")
def root():
    return {"message": "API OK"}

@app.get("/clients/")
def read_clients(db: Session = Depends(get_db)):
    return db.query(models.Client).all()

@app.post("/clients/")
def create_client(nom: str = "John", db: Session = Depends(get_db)):
    db_client = models.Client(nom=nom)
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client
