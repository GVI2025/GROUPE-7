# app/main.py
from fastapi import FastAPI, Request, Depends
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.orm import Session
from app.lib.db import models
from app.lib.db.database import engine
from app.lib.db.dependencies import get_db

# Import routes
from app.routes.salle.controller import router as salle_router


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

# Include routes
app.include_router(salle_router)
