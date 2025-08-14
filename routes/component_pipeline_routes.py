from fastapi import APIRouter
from controllers import component_pipeline_controller as pipeline_ctrl

router = APIRouter(prefix="/components/pipeline", tags=["Component Pipelines"])


@router.get("/with-inventory")
async def components_with_inventory():
    return await pipeline_ctrl.fetch_components_with_inventory()


@router.get("/inventory-stats")
async def inventory_stats():
    return await pipeline_ctrl.fetch_inventory_stats()


@router.get("/out-of-stock")
async def components_out_of_stock():
    return await pipeline_ctrl.fetch_out_of_stock_components()
