from fastapi import APIRouter, HTTPException, Request, status, Depends
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List
from app.lib.db.dependencies import get_db
from app.routes.salle import services
from app.routes.salle.schemas import SalleCreate, SalleUpdate, SalleOut
import traceback

router = APIRouter(prefix="/salle", tags=["salle"])

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_salle(salle: SalleCreate, db: Session = Depends(get_db)):
    new_salle = services.create_salle(db, salle)
    return {"data": SalleOut.from_orm(new_salle)}


@router.get("/{salle_id}")
def get_salle(salle_id: str, db: Session = Depends(get_db)):
    salle = services.get_salle_by_id(db, salle_id)
    return {"data": SalleOut.from_orm(salle)}


@router.get("/")
def get_all_salles(disponible: bool = None, db: Session = Depends(get_db)):
    salle = services.get_all_salles(db, disponible)
    return {"data": [SalleOut.from_orm(s) for s in salle]}


@router.put("/{salle_id}")
def update_salle(salle_id: str, salle_update: SalleUpdate, db: Session = Depends(get_db)):
    salle = services.update_salle(db, salle_id, salle_update)
    return {"data": SalleOut.from_orm(salle)}


@router.delete("/{salle_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_salle(salle_id: str, db: Session = Depends(get_db)):
    success = services.delete_salle(db, salle_id)
    return