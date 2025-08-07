import logging
from fastapi import HTTPException
from bson import ObjectId

from models.inventory_model import Inventory
from utils.mongodb import get_collection

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

collection_name = "inventory"


async def create_inventory(inventory: Inventory) -> Inventory:
    try:
        coll = get_collection(collection_name)
        inventory_dict = inventory.model_dump(exclude={"id"})
        result = coll.insert_one(inventory_dict)
        inventory.id = str(result.inserted_id)
        return inventory
    except Exception as e:
        logger.error(f"Error creating inventory item: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


async def get_inventory_by_id(inventory_id: str) -> Inventory:
    try:
        coll = get_collection(collection_name)
        item = coll.find_one({"_id": ObjectId(inventory_id)})
        if not item:
            raise HTTPException(status_code=404, detail="Inventory item not found")
        item["id"] = str(item["_id"])
        return Inventory(**item)
    except Exception as e:
        logger.error(f"Error fetching inventory item: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


async def get_all_inventory() -> list[Inventory]:
    try:
        coll = get_collection(collection_name)
        items = []
        for doc in coll.find():
            doc["id"] = str(doc["_id"])
            items.append(Inventory(**doc))
        return items
    except Exception as e:
        logger.error(f"Error retrieving inventory list: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


async def update_inventory(inventory_id: str, updated_data: Inventory) -> Inventory:
    try:
        coll = get_collection(collection_name)
        update_dict = updated_data.model_dump(exclude={"id"})
        result = coll.update_one({"_id": ObjectId(inventory_id)}, {"$set": update_dict})
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Inventory item not found")
        updated_data.id = inventory_id
        return updated_data
    except Exception as e:
        logger.error(f"Error updating inventory item: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


async def delete_inventory(inventory_id: str) -> dict:
    try:
        coll = get_collection(collection_name)
        result = coll.delete_one({"_id": ObjectId(inventory_id)})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Inventory item not found")
        return {"message": "Inventory item deleted successfully"}
    except Exception as e:
        logger.error(f"Error deleting inventory item: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")