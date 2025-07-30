from fastapi import HTTPException
from models.order import Order, OrderCreate, OrderUpdate
from utils.mongo import get_collection
from bson import ObjectId
import logging

logger = logging.getLogger(__name__)

async def create_order(order: OrderCreate) -> Order:
    try:
        coll = get_collection("orders")
        order_data = order.dict()
        result = coll.insert_one(order_data)
        return Order(**{**order_data, "_id": str(result.inserted_id)})
    except Exception as e:
        logger.error(f"Error creating order: {str(e)}")
        raise HTTPException(500, "Database error")

async def get_order(order_id: str) -> Order:
    try:
        coll = get_collection("orders")
        order = coll.find_one({"_id": ObjectId(order_id)})
        if not order:
            raise HTTPException(404, "Order not found")
        return Order(**order)
    except Exception as e:
        logger.error(f"Error getting order: {str(e)}")
        raise HTTPException(500, "Database error")

async def update_order(order_id: str, update: OrderUpdate) -> Order:
    try:
        coll = get_collection("orders")
        update_data = {k: v for k, v in update.dict().items() if v is not None}
        result = coll.update_one(
            {"_id": ObjectId(order_id)},
            {"$set": update_data}
        )
        if result.matched_count == 0:
            raise HTTPException(404, "Order not found")
        return await get_order(order_id)
    except Exception as e:
        logger.error(f"Error updating order: {str(e)}")
        raise HTTPException(500, "Database error")

async def delete_order(order_id: str):
    try:
        coll = get_collection("orders")
        result = coll.delete_one({"_id": ObjectId(order_id)})
        if result.deleted_count == 0:
            raise HTTPException(404, "Order not found")
        return {"message": "Order deleted successfully"}
    except Exception as e:
        logger.error(f"Error deleting order: {str(e)}")
        raise HTTPException(500, "Database error")

async def list_orders(skip: int = 0, limit: int = 10):
    try:
        coll = get_collection("orders")
        orders = list(coll.find().skip(skip).limit(limit))
        return [Order(**order) for order in orders]
    except Exception as e:
        logger.error(f"Error listing orders: {str(e)}")
        raise HTTPException(500, "Database error")