# app/main.py
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.lib.db import models
from app.lib.db.database import engine
from app.lib.db.dependencies import get_db
from app.routes import reservation_routes

models.Base.metadata.create_all(bind=engine)  # ← Crée les tables à partir des modèles

app = FastAPI()
app.include_router(reservation_routes.router)

