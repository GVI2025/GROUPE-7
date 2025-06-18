from typing import List, Optional
from fastapi import Depends
from app.lib.db.models import Salle
from app.routes.salle.schemas import SalleCreate, SalleUpdate
from sqlalchemy.orm import Session
from fastapi import HTTPException


def get_all_salles(db: Session) -> List[Salle]:
    salles = db.query(Salle).all()
    if not salles:
        raise HTTPException(
            status_code=400,
            detail="No salles found"
        )
    return salles


def get_salle_by_id(db: Session, salle_id: str) -> Salle:
    salle = db.query(Salle).filter(Salle.id == salle_id).first()
    if not salle:
        raise HTTPException(
            status_code=404,
            detail="Salle not found"
        )
    return salle


def create_salle(db: Session, salle: SalleCreate) -> Salle:
    nouvelle_salle = Salle(
        nom=salle.nom,
        capacite=salle.capacite,
        localisation=salle.localisation,
        disponible=salle.disponible if salle.disponible else None
    )
    db.add(nouvelle_salle)
    db.commit()
    db.refresh(nouvelle_salle)
    return nouvelle_salle


def update_salle(db: Session, salle_id, new_salle: SalleUpdate) -> Optional[Salle]:
    salle = get_salle_by_id(db, salle_id)
    if not salle:
        return None
    db.query(Salle).filter(Salle.id == salle_id).update({
        Salle.nom: new_salle.nom if new_salle.nom is not None else salle.nom,
        Salle.capacite: new_salle.capacite if new_salle.capacite is not None else salle.capacite,
        Salle.localisation: new_salle.localisation if new_salle.localisation is not None else salle.localisation,
        Salle.disponible: new_salle.disponible if new_salle.disponible is not None else salle.disponible
    })
    db.commit()
    db.refresh(salle)
    return salle


def delete_salle(db: Session, salle_id: str) -> bool:
    salle = get_salle_by_id(db, salle_id)
    if salle:
        db.delete(salle)
        db.commit()
        return True
    return False