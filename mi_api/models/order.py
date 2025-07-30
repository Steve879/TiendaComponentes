from datetime import date
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

class OrderBase(BaseModel):
    id_user: str = Field(..., description="ID del cliente")
    id_order: str = Field(..., description="ID único del pedido")
    recipient_name: str = Field(..., min_length=2, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    order_date: date = Field(default_factory=date.today)
    destination_address: str = Field(..., min_length=5)
    weight: float = Field(..., gt=0, description="Peso en kg")
    cost: float = Field(..., gt=0)

    model_config = ConfigDict(
        populate_by_name=True,
        json_encoders={
            date: lambda v: v.isoformat()
        }
    )

class OrderCreate(OrderBase):
    pass

class OrderUpdate(BaseModel):
    recipient_name: Optional[str] = Field(None, min_length=2, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    destination_address: Optional[str] = Field(None, min_length=5)
    weight: Optional[float] = Field(None, gt=0)
    cost: Optional[float] = Field(None, gt=0)

class Order(OrderBase):
    id: str = Field(..., alias="_id")