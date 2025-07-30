from fastapi import APIRouter, Query
from controllers.component_controller import (
    create_component, get_component,
    update_component, delete_component,
    list_components
)
from models.component import Component, ComponentCreate, ComponentUpdate

router = APIRouter(prefix="/components", tags=["Components"])

@router.post("/", response_model=Component)
async def create_new_component(component: ComponentCreate):
    return await create_component(component)

@router.get("/", response_model=list[Component])
async def get_all_components(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100)
):
    return await list_components(skip, limit)

@router.get("/{component_id}", response_model=Component)
async def get_single_component(component_id: str):
    return await get_component(component_id)

@router.put("/{component_id}", response_model=Component)
async def update_existing_component(component_id: str, update: ComponentUpdate):
    return await update_component(component_id, update)

@router.delete("/{component_id}")
async def remove_component(component_id: str):
    return await delete_component(component_id)