from datetime import date
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

class InventoryBase(BaseModel):
    id_product: str = Field(..., description="ID del producto relacionado")
    name: str = Field(..., min_length=2, description="Nombre del producto")
    stock: int = Field(..., ge=0, description="Cantidad disponible")
    location: str = Field(..., description="Ubicación en almacén")
    entry_date: date = Field(default_factory=date.today, description="Fecha de ingreso")
    exit_date: Optional[date] = Field(None, description="Fecha de salida")
    cost_per_unit: float = Field(..., gt=0, description="Costo por unidad")

    model_config = ConfigDict(
        populate_by_name=True,
        json_encoders={
            date: lambda v: v.isoformat()
        }
    )

    @property
    def total_price(self) -> float:
        """Calcula el valor total del inventario"""
        return self.stock * self.cost_per_unit

class InventoryCreate(InventoryBase):
    pass

class InventoryUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2)
    stock: Optional[int] = Field(None, ge=0)
    location: Optional[str] = None
    exit_date: Optional[date] = None
    cost_per_unit: Optional[float] = Field(None, gt=0)

class Inventory(InventoryBase):
    id: str = Field(..., alias="_id")