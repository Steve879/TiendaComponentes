from fastapi import APIRouter, Query
from controllers.category_controller import (
    create_category, get_category, update_category,
    delete_category, list_categories
)
from models.category import Category, CategoryCreate, CategoryUpdate

router = APIRouter(prefix="/categories", tags=["Categories"])

@router.post("/", response_model=Category)
async def create_new_category(category: CategoryCreate):
    return await create_category(category)

@router.get("/", response_model=list[Category])
async def get_all_categories(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100)
):
    return await list_categories(skip, limit)

@router.get("/{category_id}", response_model=Category)
async def get_single_category(category_id: str):
    return await get_category(category_id)

@router.put("/{category_id}", response_model=Category)
async def update_existing_category(category_id: str, update: CategoryUpdate):
    return await update_category(category_id, update)

@router.delete("/{category_id}")
async def remove_category(category_id: str):
    return await delete_category(category_id)