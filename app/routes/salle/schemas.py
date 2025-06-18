from typing import Optional
from pydantic import BaseModel

class SalleCreate(BaseModel):
    nom: str
    capacite: int
    localisation: str
    disponible: Optional[bool] = True

class SalleUpdate(BaseModel):
    nom: Optional[str] = None
    capacite: Optional[int] = None
    localisation: Optional[str] = None
    disponible: Optional[bool] = None

class SalleOut(BaseModel):
    id: str
    nom: str
    capacite: int
    localisation: Optional[str] = None
    disponible: bool = True

    class Config:
        from_attributes = True