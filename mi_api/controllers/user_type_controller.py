from fastapi import HTTPException
from models.user_type import UserType, UserTypeCreate, UserTypeUpdate
from utils.mongo import get_collection
from bson import ObjectId
import logging

logger = logging.getLogger(__name__)

async def create_user_type(user_type: UserTypeCreate) -> UserType:
    try:
        coll = get_collection("user_types")
        user_type_data = user_type.dict()
        result = coll.insert_one(user_type_data)
        return UserType(**{**user_type_data, "_id": str(result.inserted_id)})
    except Exception as e:
        logger.error(f"Error creating user type: {str(e)}")
        raise HTTPException(500, "Database error")

async def get_user_type(user_type_id: str) -> UserType:
    try:
        coll = get_collection("user_types")
        user_type = coll.find_one({"_id": ObjectId(user_type_id)})
        if not user_type:
            raise HTTPException(404, "User type not found")
        return UserType(**user_type)
    except Exception as e:
        logger.error(f"Error getting user type: {str(e)}")
        raise HTTPException(500, "Database error")

async def update_user_type(user_type_id: str, update: UserTypeUpdate) -> UserType:
    try:
        coll = get_collection("user_types")
        update_data = {k: v for k, v in update.dict().items() if v is not None}
        result = coll.update_one(
            {"_id": ObjectId(user_type_id)},
            {"$set": update_data}
        )
        if result.matched_count == 0:
            raise HTTPException(404, "User type not found")
        return await get_user_type(user_type_id)
    except Exception as e:
        logger.error(f"Error updating user type: {str(e)}")
        raise HTTPException(500, "Database error")

async def delete_user_type(user_type_id: str):
    try:
        coll = get_collection("user_types")
        result = coll.delete_one({"_id": ObjectId(user_type_id)})
        if result.deleted_count == 0:
            raise HTTPException(404, "User type not found")
        return {"message": "User type deleted successfully"}
    except Exception as e:
        logger.error(f"Error deleting user type: {str(e)}")
        raise HTTPException(500, "Database error")

async def list_user_types(skip: int = 0, limit: int = 10):
    try:
        coll = get_collection("user_types")
        user_types = list(coll.find().skip(skip).limit(limit))
        return [UserType(**user_type) for user_type in user_types]
    except Exception as e:
        logger.error(f"Error listing user types: {str(e)}")
        raise HTTPException(500, "Database error")