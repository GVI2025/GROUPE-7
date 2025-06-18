from uuid import uuid4
from sqlalchemy import Column, String, Float, Date, Enum, Integer, Boolean, ForeignKey, Time

from .database import Base

class Salle(Base):
    __tablename__ = "salles"

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    nom = Column(String, nullable=False)
    capacite = Column(Integer, nullable=False)
    localisation = Column(String, nullable=False)
    disponible = Column(Boolean, default=True, nullable=True)

class Reservation(Base):
    __tablename__ = "reservations"

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    salle_id = Column(String, ForeignKey("salles.id"))
    date = Column(Date, nullable=False)
    heure = Column(Time, nullable=False)
    utilisateur = Column(String, nullable=False)
    commentaire = Column(String, nullable=True)