from typing import Optional
from pydantic import BaseModel
from datetime import date, time


class ReservationCreate(BaseModel):
    salle_id: str
    date: date
    heure: time
    utilisateur: str


class ReservationUpdate(BaseModel):
    salle_id: Optional[str] = None
    date: Optional[date] = None
    heure: Optional[time] = None
    utilisateur: Optional[str] = None


class ReservationOut(BaseModel):
    id: str
    salle_id: str
    date: date
    heure: time
    utilisateur: str

    class Config:
        from_attributes = True
