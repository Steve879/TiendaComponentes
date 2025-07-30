from fastapi import APIRouter, Query
from controllers.inventory_controller import (
    create_inventory_item, get_inventory_item,
    update_inventory_item, delete_inventory_item,
    list_inventory_items
)
from models.inventory import Inventory, InventoryCreate, InventoryUpdate

router = APIRouter(prefix="/inventory", tags=["Inventory"])

@router.post("/", response_model=Inventory)
async def create_new_inventory_item(item: InventoryCreate):
    return await create_inventory_item(item)

@router.get("/", response_model=list[Inventory])
async def get_all_inventory_items(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100)
):
    return await list_inventory_items(skip, limit)

@router.get("/{item_id}", response_model=Inventory)
async def get_single_inventory_item(item_id: str):
    return await get_inventory_item(item_id)

@router.put("/{item_id}", response_model=Inventory)
async def update_existing_inventory_item(item_id: str, update: InventoryUpdate):
    return await update_inventory_item(item_id, update)

@router.delete("/{item_id}")
async def remove_inventory_item(item_id: str):
    return await delete_inventory_item(item_id)