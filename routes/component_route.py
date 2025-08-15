from fastapi import APIRouter, Request, HTTPException
from models.component_model import Components
from utils.security import validateuser
from controllers.component_controller import (
    create_component,
    get_component_by_id,
    get_all_components,
    update_component,
    delete_component
)

router = APIRouter(tags=["Components"])


@router.post("/components", response_model=Components)
@validateuser
async def create_component_endpoint(request: Request, component: Components):
    return await create_component(component)


@router.get("/components/{component_id}", response_model=Components)
async def get_component_by_id_endpoint(component_id: str):
    return await get_component_by_id(component_id)


@router.get("/components", response_model=list[Components])
async def list_all_components_endpoint():
    return await get_all_components()


@router.put("/components/{component_id}", response_model=Components)
@validateuser
async def update_component_endpoint(request: Request, component_id: str, updated_data: Components):
    return await update_component(component_id, updated_data)


@router.delete("/components/{component_id}")
@validateuser
async def delete_component_endpoint(request: Request, component_id: str):
    return await delete_component(component_id)
