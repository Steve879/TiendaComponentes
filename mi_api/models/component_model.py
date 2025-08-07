from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId

class Components(BaseModel):
    id: Optional[str] = Field(
        default=None,
        description="ID único de componente"
    )
    id_inventario: Optional[str] = Field(
        default=None,
        description="ID del inventario"
    )
    id_pago: Optional[str] = Field(
        default=None,
        description="ID del pago asociada"
    )
    id_category: Optional[str] = Field(
        default=None,
        description="ID de la categoría del componente"
    )
    name: str = Field(
        description="Nombre del componente",
        examples=["Componente A"]
    )
    description: str = Field(
        description="Descripción del componente"
    )
    entry_date: str = Field(
        description="Fecha de entrada"
    )
    exit_date: Optional[str] = Field(
        default=None,
        description="Fecha de salida"
    )
    cost_per_unit: float = Field(
        description="Costo por unidad del componente"
    )
    discount: int = Field(
        description="Descuento aplicable al componente"
    )
    image: str = Field(
        description="URL de la imagen del componente"
    )
    class Config:
        json_encoders = {
            ObjectId: str
        }