from pipelines.component_pipeline import (
    get_components_with_inventory,
    get_inventory_count_by_component,
    get_components_out_of_stock
)


async def fetch_components_with_inventory():
    return get_components_with_inventory()


async def fetch_inventory_stats():
    return get_inventory_count_by_component()


async def fetch_out_of_stock_components():
    return get_components_out_of_stock()
