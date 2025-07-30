from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

class CategoryBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    description: str = Field(..., min_length=5, max_length=200)
    discount: int = Field(default=0, ge=0, le=100)

    model_config = ConfigDict(
        populate_by_name=True,  # Reemplaza allow_population_by_field_name
        json_encoders={
            # Configuración adicional si es necesaria
        }
    )

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=50)
    description: Optional[str] = Field(None, min_length=5, max_length=200)
    discount: Optional[int] = Field(None, ge=0, le=100)

class Category(CategoryBase):
    id: str = Field(..., alias="_id")
    id_inventory: Optional[str] = None