from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId

class Inventory(BaseModel):
    id: Optional[str] = Field(
        default=None,
        description="ID único del inventario"
    )
   
    name: str = Field(
        description="Nombre del artículo en el inventario",
        examples=["Componente A"]
    )
    description: str = Field(
        description="Descripción del artículo",
        examples=["Descripción del componente A"]
    )
    stock: int = Field(
        description="Cantidad disponible en el inventario"
    )
    location: str = Field(
        description="Ubicación del artículo en el inventario",
        examples=["Almacén 1"]
    )
    entry_date: str = Field(
        description="Fecha de entrada en el inventario"
    )
    exit_date: Optional[str] = Field(
        default=None,
        description="Fecha de salida del inventario"
    )
    cost_per_unit: float = Field(
        description="Costo unitario del artículo"
    )
    total_price: float = Field(
        description="Precio total (costo unitario * stock)"
    )
    image: str = Field(
        description="URL de la imagen del artículo"
    )
    class Config:
        json_encoders = {
            ObjectId: str
        }