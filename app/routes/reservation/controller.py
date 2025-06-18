from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from typing import List
from app.lib.db.dependencies import get_db
from app.routes.reservation import services
from app.routes.reservation.schemas import ReservationCreate, ReservationUpdate, ReservationOut
import traceback

router = APIRouter(prefix="/reservation", tags=["reservation"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_reservation(reservation: ReservationCreate, db: Session = Depends(get_db)):
    try:
        new_reservation = services.create_reservation(db, reservation)
        return {"data": ReservationOut.from_orm(new_reservation)}
    except Exception as e:
        print("Erreur lors de la création de la réservation :", e)
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/{reservation_id}")
def get_reservation(reservation_id: str, db: Session = Depends(get_db)):
    reservation = services.get_reservation_by_id(db, reservation_id)
    if not reservation:
        raise HTTPException(status_code=404, detail="Réservation introuvable")
    return {"data": ReservationOut.from_orm(reservation)}


@router.get("/")
def get_all_reservations(db: Session = Depends(get_db)):
    reservations = services.get_all_reservations(db)
    return {"data": [ReservationOut.from_orm(r) for r in reservations]}


@router.put("/{reservation_id}")
def update_reservation(reservation_id: str, reservation_update: ReservationUpdate, db: Session = Depends(get_db)):
    reservation = services.update_reservation(db, reservation_id, reservation_update)
    if not reservation:
        raise HTTPException(status_code=404, detail="Réservation introuvable")
    return {"data": ReservationOut.from_orm(reservation)}


@router.delete("/{reservation_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_reservation(reservation_id: str, db: Session = Depends(get_db)):
    success = services.delete_reservation(db, reservation_id)
    if not success:
        raise HTTPException(status_code=404, detail="Réservation introuvable")