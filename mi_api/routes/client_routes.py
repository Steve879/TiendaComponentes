from fastapi import APIRouter, Query
from controllers.client_controller import (
    create_client, get_client, update_client, 
    delete_client, list_clients
)
from models.client import Client, ClientCreate, ClientUpdate

router = APIRouter(prefix="/clients", tags=["Clients"])

@router.post("/", response_model=Client)
async def create_new_client(client: ClientCreate):
    return await create_client(client)

@router.get("/", response_model=list[Client])
async def get_all_clients(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100)
):
    return await list_clients(skip, limit)

@router.get("/{client_id}", response_model=Client)
async def get_single_client(client_id: str):
    return await get_client(client_id)

@router.put("/{client_id}", response_model=Client)
async def update_existing_client(client_id: str, update: ClientUpdate):
    return await update_client(client_id, update)

@router.delete("/{client_id}")
async def remove_client(client_id: str):
    return await delete_client(client_id)