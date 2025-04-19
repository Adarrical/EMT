from pydantic import BaseModel

class AvgMunicipio(BaseModel):
    provincia: str
    comarca: str
    municipi:str
    nom_variable: str
    valor_medio: float

class AvgComarca(BaseModel):
    provincia: str
    comarca: str
    nom_variable: str
    valor_medio: float

class AvgProvincia(BaseModel):
    provincia: str
    nom_variable: str
    valor_medio: float