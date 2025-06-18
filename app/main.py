# app/main.py
from fastapi import FastAPI, Request, Depends
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.lib.db import models
from app.lib.db.database import engine
from app.lib.db.dependencies import get_db

# Import routes
from app.routes.salle.controller import router as salle_router

from app.routes.reservation.controller import router as reservation_router

models.Base.metadata.create_all(bind=engine)  # ← Crée les tables à partir des modèles

app = FastAPI()

# Middleware to handle Body Requests Exceptions
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "error": {
                "message": "Les données envoyées ne sont pas valides",
                "details": exc.errors(),
            }
        },
    )

# Middleware to handle general exceptions
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": {"message": exc.detail}},
    )

# Include routes
app.include_router(salle_router)
app.include_router(reservation_router)

