from fastapi import HTTPException
from models.client import Client, ClientCreate, ClientUpdate
from utils.mongo import get_collection
from bson import ObjectId
import logging


logger = logging.getLogger(__name__)

async def create_client(client: ClientCreate) -> Client:
    try:
        coll = get_collection("clients")
        client_data = client.dict()
        result = coll.insert_one(client_data)
        return Client(**{**client_data, "_id": str(result.inserted_id)})
    except Exception as e:
        logger.error(f"Error creating client: {str(e)}")
        raise HTTPException(500, "Database error")

async def get_client(client_id: str) -> Client:
    try:
        coll = get_collection("clients")
        client = coll.find_one({"_id": ObjectId(client_id)})
        if not client:
            raise HTTPException(404, "Client not found")
        return Client(**client)
    except Exception as e:
        logger.error(f"Error getting client: {str(e)}")
        raise HTTPException(500, "Database error")

async def update_client(client_id: str, update: ClientUpdate) -> Client:
    try:
        coll = get_collection("clients")
        update_data = {k: v for k, v in update.dict().items() if v is not None}
        result = coll.update_one(
            {"_id": ObjectId(client_id)},
            {"$set": update_data}
        )
        if result.matched_count == 0:
            raise HTTPException(404, "Client not found")
        return await get_client(client_id)
    except Exception as e:
        logger.error(f"Error updating client: {str(e)}")
        raise HTTPException(500, "Database error")

async def delete_client(client_id: str):
    try:
        coll = get_collection("clients")
        result = coll.delete_one({"_id": ObjectId(client_id)})
        if result.deleted_count == 0:
            raise HTTPException(404, "Client not found")
        return {"message": "Client deleted successfully"}
    except Exception as e:
        logger.error(f"Error deleting client: {str(e)}")
        raise HTTPException(500, "Database error")

async def list_clients(skip: int = 0, limit: int = 10):
    try:
        coll = get_collection("clients")
        clients = list(coll.find().skip(skip).limit(limit))
        return [Client(**client) for client in clients]
    except Exception as e:
        logger.error(f"Error listing clients: {str(e)}")
        raise HTTPException(500, "Database error")