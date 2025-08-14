from fastapi import APIRouter, HTTPException, Request
from models.inventory_model import Inventory
from utils.security import validateadmin
from controllers.inventory_controller import (
    create_inventory,
    get_inventory_by_id,
    get_all_inventory,
    update_inventory,
    delete_inventory
)

router = APIRouter(tags=["Inventory"])


@router.post("/inventory", response_model=Inventory)
@validateadmin
async def create_inventory_item(request: Request, inventory: Inventory):
    return await create_inventory(inventory)


@router.get("/inventory/{inventory_id}", response_model=Inventory)
async def get_inventory_item(inventory_id: str):
    return await get_inventory_by_id(inventory_id)


@router.get("/inventory", response_model=list[Inventory])
async def list_inventory_items():
    return await get_all_inventory()


@router.put("/inventory/{inventory_id}", response_model=Inventory)
@validateadmin
async def update_inventory_item(request: Request, inventory_id: str, updated_data: Inventory):
    return await update_inventory(inventory_id, updated_data)


@router.delete("/inventory/{inventory_id}")
@validateadmin
async def delete_inventory_item(request: Request, inventory_id: str):
    return await delete_inventory(inventory_id)