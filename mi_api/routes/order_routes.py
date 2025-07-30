from fastapi import APIRouter, Query
from controllers.order_controller import (
    create_order, get_order, update_order,
    delete_order, list_orders
)
from models.order import Order, OrderCreate, OrderUpdate

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.post("/", response_model=Order)
async def create_new_order(order: OrderCreate):
    return await create_order(order)

@router.get("/", response_model=list[Order])
async def get_all_orders(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100)
):
    return await list_orders(skip, limit)

@router.get("/{order_id}", response_model=Order)
async def get_single_order(order_id: str):
    return await get_order(order_id)

@router.put("/{order_id}", response_model=Order)
async def update_existing_order(order_id: str, update: OrderUpdate):
    return await update_order(order_id, update)

@router.delete("/{order_id}")
async def remove_order(order_id: str):
    return await delete_order(order_id)