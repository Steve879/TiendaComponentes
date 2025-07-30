from fastapi import HTTPException
from models.category import Category, CategoryCreate, CategoryUpdate
from utils.mongo import get_collection
from bson import ObjectId
import logging

logger = logging.getLogger(__name__)

async def create_category(category: CategoryCreate) -> Category:
    try:
        coll = get_collection("categories")
        category_data = category.dict()
        result = coll.insert_one(category_data)
        return Category(**{**category_data, "_id": str(result.inserted_id)})
    except Exception as e:
        logger.error(f"Error creating category: {str(e)}")
        raise HTTPException(500, "Database error")

async def get_category(category_id: str) -> Category:
    try:
        coll = get_collection("categories")
        category = coll.find_one({"_id": ObjectId(category_id)})
        if not category:
            raise HTTPException(404, "Category not found")
        return Category(**category)
    except Exception as e:
        logger.error(f"Error getting category: {str(e)}")
        raise HTTPException(500, "Database error")

async def update_category(category_id: str, update: CategoryUpdate) -> Category:
    try:
        coll = get_collection("categories")
        update_data = {k: v for k, v in update.dict().items() if v is not None}
        result = coll.update_one(
            {"_id": ObjectId(category_id)},
            {"$set": update_data}
        )
        if result.matched_count == 0:
            raise HTTPException(404, "Category not found")
        return await get_category(category_id)
    except Exception as e:
        logger.error(f"Error updating category: {str(e)}")
        raise HTTPException(500, "Database error")

async def delete_category(category_id: str):
    try:
        coll = get_collection("categories")
        result = coll.delete_one({"_id": ObjectId(category_id)})
        if result.deleted_count == 0:
            raise HTTPException(404, "Category not found")
        return {"message": "Category deleted successfully"}
    except Exception as e:
        logger.error(f"Error deleting category: {str(e)}")
        raise HTTPException(500, "Database error")

async def list_categories(skip: int = 0, limit: int = 10):
    try:
        coll = get_collection("categories")
        categories = list(coll.find().skip(skip).limit(limit))
        return [Category(**category) for category in categories]
    except Exception as e:
        logger.error(f"Error listing categories: {str(e)}")
        raise HTTPException(500, "Database error")