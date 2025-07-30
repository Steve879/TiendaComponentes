# mi_api/routes/pipeline_routes.py
from fastapi import APIRouter
from controllers.pipeline_controller import obtener_clientes_con_pedidos

router = APIRouter(tags=["Pipelines"])

@router.get("/clientes-pedidos", 
           summary="Clientes con sus pedidos",
           description="""Pipeline que muestra:
           - Datos básicos del cliente
           - Cantidad total de pedidos
           - Últimos 5 pedidos con detalles""")
async def clientes_con_pedidos():
    return await obtener_clientes_con_pedidos()