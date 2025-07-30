from fastapi import HTTPException
from models.inventory import Inventory, InventoryCreate, InventoryUpdate
from utils.mongo import get_collection
from bson import ObjectId
import logging

logger = logging.getLogger(__name__)

async def create_inventory_item(item: InventoryCreate) -> Inventory:
    try:
        coll = get_collection("inventory")
        item_data = item.dict()
        result = coll.insert_one(item_data)
        return Inventory(**{**item_data, "_id": str(result.inserted_id)})
    except Exception as e:
        logger.error(f"Error creating inventory item: {str(e)}")
        raise HTTPException(500, "Database error")

async def get_inventory_item(item_id: str) -> Inventory:
    try:
        coll = get_collection("inventory")
        item = coll.find_one({"_id": ObjectId(item_id)})
        if not item:
            raise HTTPException(404, "Inventory item not found")
        return Inventory(**item)
    except Exception as e:
        logger.error(f"Error getting inventory item: {str(e)}")
        raise HTTPException(500, "Database error")

async def update_inventory_item(item_id: str, update: InventoryUpdate) -> Inventory:
    try:
        coll = get_collection("inventory")
        update_data = {k: v for k, v in update.dict().items() if v is not None}
        result = coll.update_one(
            {"_id": ObjectId(item_id)},
            {"$set": update_data}
        )
        if result.matched_count == 0:
            raise HTTPException(404, "Inventory item not found")
        return await get_inventory_item(item_id)
    except Exception as e:
        logger.error(f"Error updating inventory item: {str(e)}")
        raise HTTPException(500, "Database error")

async def delete_inventory_item(item_id: str):
    try:
        coll = get_collection("inventory")
        result = coll.delete_one({"_id": ObjectId(item_id)})
        if result.deleted_count == 0:
            raise HTTPException(404, "Inventory item not found")
        return {"message": "Inventory item deleted successfully"}
    except Exception as e:
        logger.error(f"Error deleting inventory item: {str(e)}")
        raise HTTPException(500, "Database error")

async def list_inventory_items(skip: int = 0, limit: int = 10):
    try:
        coll = get_collection("inventory")
        items = list(coll.find().skip(skip).limit(limit))
        return [Inventory(**item) for item in items]
    except Exception as e:
        logger.error(f"Error listing inventory items: {str(e)}")
        raise HTTPException(500, "Database error")