from typing import Optional
from pydantic import BaseModel
import datetime


class ReservationCreate(BaseModel):
    salle_id: str
    date: datetime.date
    heure: datetime.time
    utilisateur: str
    commentaire: Optional[str] = None


class ReservationUpdate(BaseModel):
    salle_id: Optional[str] = None
    date: Optional[datetime.date] = None
    heure: Optional[datetime.time] = None
    utilisateur: Optional[str] = None
    commentaire: Optional[str] = None


class ReservationOut(BaseModel):
    id: str
    salle_id: str
    date: datetime.date
    heure: datetime.time
    utilisateur: str
    commentaire: Optional[str] = None

    class Config:
        from_attributes = True
