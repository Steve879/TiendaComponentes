from fastapi import APIRouter, Query
from controllers.user_type_controller import (
    create_user_type, get_user_type,
    update_user_type, delete_user_type,
    list_user_types
)
from models.user_type import UserType, UserTypeCreate, UserTypeUpdate

router = APIRouter(prefix="/user-types", tags=["User Types"])

@router.post("/", response_model=UserType)
async def create_new_user_type(user_type: UserTypeCreate):
    return await create_user_type(user_type)

@router.get("/", response_model=list[UserType])
async def get_all_user_types(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100)
):
    return await list_user_types(skip, limit)

@router.get("/{user_type_id}", response_model=UserType)
async def get_single_user_type(user_type_id: str):
    return await get_user_type(user_type_id)

@router.put("/{user_type_id}", response_model=UserType)
async def update_existing_user_type(user_type_id: str, update: UserTypeUpdate):
    return await update_user_type(user_type_id, update)

@router.delete("/{user_type_id}")
async def remove_user_type(user_type_id: str):
    return await delete_user_type(user_type_id)