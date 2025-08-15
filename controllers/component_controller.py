import logging
from fastapi import HTTPException
from bson import ObjectId
from models.component_model import Components
from utils.mongodb import get_collection

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

collection_name = "components"


async def create_component(component: Components) -> Components:
    try:
        coll = get_collection(collection_name)
        component_dict = component.model_dump(exclude={"id"})
        result = coll.insert_one(component_dict)
        component.id = str(result.inserted_id)
        return component
    except Exception as e:
        logger.error(f"Error creating component: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


async def get_component_by_id(component_id: str) -> Components:
    try:
        coll = get_collection(collection_name)
        item = coll.find_one({"_id": ObjectId(component_id)})
        if not item:
            raise HTTPException(status_code=404, detail="Component not found")
        item["id"] = str(item["_id"])
        return Components(**item)
    except Exception as e:
        logger.error(f"Error fetching component: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


async def get_all_components() -> list[Components]:
    try:
        coll = get_collection(collection_name)
        items = []
        for doc in coll.find():
            doc["id"] = str(doc["_id"])
            items.append(Components(**doc))
        return items
    except Exception as e:
        logger.error(f"Error retrieving components list: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


async def update_component(component_id: str, updated_data: Components) -> Components:
    try:
        coll = get_collection(collection_name)
        update_dict = updated_data.model_dump(exclude={"id"})
        result = coll.update_one({"_id": ObjectId(component_id)}, {"$set": update_dict})
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Component not found")
        updated_data.id = component_id
        return updated_data
    except Exception as e:
        logger.error(f"Error updating component: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


async def delete_component(component_id: str) -> dict:
    try:
        coll = get_collection(collection_name)
        result = coll.delete_one({"_id": ObjectId(component_id)})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Component not found")
        return {"message": "Component deleted successfully"}
    except Exception as e:
        logger.error(f"Error deleting component: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
