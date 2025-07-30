from pydantic import BaseModel, Field, ConfigDict
from enum import Enum

class UserTypeEnum(str, Enum):
    admin = "admin"
    user = "user"
    manager = "manager"  # Ejemplo de tipo adicional

class UserTypeBase(BaseModel):
    description: UserTypeEnum = Field(..., description="Tipo de usuario")

    model_config = ConfigDict(
        populate_by_name=True,
        use_enum_values=True  # Para serializar correctamente los Enum
    )

class UserTypeCreate(UserTypeBase):
    pass

class UserTypeUpdate(BaseModel):
    description: Optional[UserTypeEnum] = None  # Campo opcional para actualización

class UserType(UserTypeBase):
    id: str = Field(..., alias="_id")