from fastapi import HTTPException
from models.component import Component, ComponentCreate, ComponentUpdate
from utils.mongo import get_collection
from bson import ObjectId
import logging

logger = logging.getLogger(__name__)

async def create_component(component: ComponentCreate) -> Component:
    try:
        coll = get_collection("components")
        component_data = component.dict()
        result = coll.insert_one(component_data)
        return Component(**{**component_data, "_id": str(result.inserted_id)})
    except Exception as e:
        logger.error(f"Error creating component: {str(e)}")
        raise HTTPException(500, "Database error")

async def get_component(component_id: str) -> Component:
    try:
        coll = get_collection("components")
        component = coll.find_one({"_id": ObjectId(component_id)})
        if not component:
            raise HTTPException(404, "Component not found")
        return Component(**component)
    except Exception as e:
        logger.error(f"Error getting component: {str(e)}")
        raise HTTPException(500, "Database error")

async def update_component(component_id: str, update: ComponentUpdate) -> Component:
    try:
        coll = get_collection("components")
        update_data = {k: v for k, v in update.dict().items() if v is not None}
        result = coll.update_one(
            {"_id": ObjectId(component_id)},
            {"$set": update_data}
        )
        if result.matched_count == 0:
            raise HTTPException(404, "Component not found")
        return await get_component(component_id)
    except Exception as e:
        logger.error(f"Error updating component: {str(e)}")
        raise HTTPException(500, "Database error")

async def delete_component(component_id: str):
    try:
        coll = get_collection("components")
        result = coll.delete_one({"_id": ObjectId(component_id)})
        if result.deleted_count == 0:
            raise HTTPException(404, "Component not found")
        return {"message": "Component deleted successfully"}
    except Exception as e:
        logger.error(f"Error deleting component: {str(e)}")
        raise HTTPException(500, "Database error")

async def list_components(skip: int = 0, limit: int = 10):
    try:
        coll = get_collection("components")
        components = list(coll.find().skip(skip).limit(limit))
        return [Component(**component) for component in components]
    except Exception as e:
        logger.error(f"Error listing components: {str(e)}")
        raise HTTPException(500, "Database error")