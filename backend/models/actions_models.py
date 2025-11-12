from enum import Enum
from pydantic import BaseModel

class action(BaseModel):
    """
    example of datas
    {"name": "Station de compost",
 "type": "compost",
 "quartier": "Cenon",
 }
    """
    user: str
    name: str
    type : str
    quartier: str


class action_impoved(BaseModel):
    """
    example of datas
    {"name": "Station de compost",
 "type": "compost",

 "lat": 44.865,
 "lon": -0.556,
 "impact_co2_kg": 50}
    """
    user: str
    name: str
    lat: float
    lon: float
    quartier: str
    impact_co2_kg: float
