from datetime import date
from pydantic import BaseModel, Field, ConfigDict, EmailStr
from typing import Optional

class ClientBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    lastname: str = Field(..., min_length=2, max_length=50)
    age: int = Field(..., gt=0, lt=120)
    date_birth: date
    cellphone: str = Field(..., pattern=r'^\+?[0-9]{7,15}$')
    id_number: str = Field(..., min_length=5, max_length=20)
    email: EmailStr
    direction: str = Field(..., min_length=5, max_length=100)
    active: bool = Field(default=True)

    # Nueva configuración en Pydantic v2
    model_config = ConfigDict(
        populate_by_name=True,  # Reemplaza allow_population_by_field_name
        json_encoders={
            date: lambda v: v.isoformat()
        }
    )

class ClientCreate(ClientBase):
    pass

class ClientUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=50)
    lastname: Optional[str] = Field(None, min_length=2, max_length=50)
    # ... otros campos opcionales para actualización

class Client(ClientBase):
    id: str = Field(..., alias="_id")