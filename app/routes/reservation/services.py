from fastapi import HTTPException
from typing import List, Optional
from sqlalchemy.orm import Session
from app.lib.db.models import Reservation
from app.routes.reservation.schemas import ReservationCreate, ReservationUpdate


def get_all_reservations(db: Session) -> List[Reservation]:
    return db.query(Reservation).all()


def get_reservation_by_id(db: Session, reservation_id: str) -> Optional[Reservation]:
    reservation = db.query(Reservation).filter(Reservation.id == reservation_id).first()
    if not reservation:
        raise HTTPException(
            status_code=404, 
            detail="Réservation introuvable"
        )
    return reservation


def create_reservation(db: Session, reservation: ReservationCreate) -> Reservation:
    # Vérifie si la salle est disponible pour la date et l'heure spécifiées
    existing_reservation = db.query(Reservation).filter(
        Reservation.salle_id == reservation.salle_id,
        Reservation.date == reservation.date,
        Reservation.heure == reservation.heure
    ).first()
    if existing_reservation:
        raise HTTPException(
            status_code=409,
            detail="La salle est déjà réservée à cette date et heure."
        )
    
    # Crée une nouvelle réservation
    nouvelle_reservation = Reservation(
        salle_id=reservation.salle_id,
        date=reservation.date,
        heure=reservation.heure,
        utilisateur=reservation.utilisateur
    )
    db.add(nouvelle_reservation)
    db.commit()
    db.refresh(nouvelle_reservation)
    return nouvelle_reservation


def update_reservation(db: Session, reservation_id: str, update_data: ReservationUpdate) -> Optional[Reservation]:
    reservation = get_reservation_by_id(db, reservation_id)
    if not reservation:
        return None

    db.query(Reservation).filter(Reservation.id == reservation_id).update({
        Reservation.salle_id: update_data.salle_id if update_data.salle_id is not None else reservation.salle_id,
        Reservation.date: update_data.date if update_data.date is not None else reservation.date,
        Reservation.heure: update_data.heure if update_data.heure is not None else reservation.heure,
        Reservation.utilisateur: update_data.utilisateur if update_data.utilisateur is not None else reservation.utilisateur,
    })

    db.commit()
    db.refresh(reservation)
    return reservation


def delete_reservation(db: Session, reservation_id: str) -> bool:
    reservation = get_reservation_by_id(db, reservation_id)
    if reservation:
        db.delete(reservation)
        db.commit()
        return True
    return False
