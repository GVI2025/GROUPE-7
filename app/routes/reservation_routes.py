from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import date, time
import uuid

from app.lib.db import models
from app.lib.db.dependencies import get_db
from pydantic import BaseModel

router = APIRouter()

# --- Schemas Pydantic ---
class ReservationBase(BaseModel):
    salle_id: str
    date: date
    heure: time
    utilisateur: str

class ReservationCreate(ReservationBase):
    pass

class Reservation(ReservationBase):
    id: str

    class Config:
        orm_mode = True

# --- Endpoints Réservation ---

@router.post("/reservations/", response_model=Reservation, status_code=status.HTTP_201_CREATED)
def create_reservation(reservation: ReservationCreate, db: Session = Depends(get_db)):
    salle = db.query(models.Salle).filter(models.Salle.id == reservation.salle_id).first()
    if not salle:
        raise HTTPException(status_code=404, detail="Salle non trouvée")

    existing = db.query(models.Reservation).filter(
        models.Reservation.salle_id == reservation.salle_id,
        models.Reservation.date == reservation.date,
        models.Reservation.heure == reservation.heure
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Créneau déjà réservé pour cette salle")

    db_reservation = models.Reservation(
        id=str(uuid.uuid4()),
        salle_id=reservation.salle_id,
        date=reservation.date,
        heure=reservation.heure,
        utilisateur=reservation.utilisateur
    )
    db.add(db_reservation)
    db.commit()
    db.refresh(db_reservation)
    return db_reservation

@router.get("/reservations/", response_model=List[Reservation])
def read_reservations(db: Session = Depends(get_db)):
    return db.query(models.Reservation).all()

@router.get("/reservations/{reservation_id}", response_model=Reservation)
def read_reservation(reservation_id: str, db: Session = Depends(get_db)):
    reservation = db.query(models.Reservation).filter(models.Reservation.id == reservation_id).first()
    if not reservation:
        raise HTTPException(status_code=404, detail="Réservation non trouvée")
    return reservation
