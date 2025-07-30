from datetime import date
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

class ComponentBase(BaseModel):
    id_category: str = Field(..., description="ID de categoría")
    id_inventory: str = Field(..., description="ID de inventario")
    name: str = Field(..., min_length=2, description="Nombre del componente")
    stock: int = Field(..., ge=0, description="Cantidad en stock")
    description: str = Field(..., min_length=5, description="Descripción")
    entry_date: date = Field(default_factory=date.today, description="Fecha de ingreso")
    exit_date: Optional[date] = Field(None, description="Fecha de salida")
    cost_per_unit: float = Field(..., gt=0, description="Costo por unidad")
    discount: int = Field(default=0, ge=0, le=100, description="Descuento (0-100%)")
    image_url: Optional[str] = Field(None, description="URL de imagen")

    model_config = ConfigDict(
        populate_by_name=True,
        json_encoders={
            date: lambda v: v.isoformat()
        }
    )

class ComponentCreate(ComponentBase):
    pass

class ComponentUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2)
    stock: Optional[int] = Field(None, ge=0)
    description: Optional[str] = Field(None, min_length=5)
    exit_date: Optional[date] = None
    cost_per_unit: Optional[float] = Field(None, gt=0)
    discount: Optional[int] = Field(None, ge=0, le=100)
    image_url: Optional[str] = None

class Component(ComponentBase):
    id: str = Field(..., alias="_id")