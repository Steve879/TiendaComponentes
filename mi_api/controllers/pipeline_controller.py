# mi_api/controllers/pipeline_controller.py
from fastapi import HTTPException
from pipelines.cliente_pedidos import pipeline_clientes_con_pedidos
from utils.mongo import get_collection
import logging

logger = logging.getLogger(__name__)

async def obtener_clientes_con_pedidos():
    """
    Ejecuta el pipeline de lookup entre clientes y pedidos
    
    Returns:
        List[Dict]: Resultado del pipeline
    Raises:
        HTTPException: Si hay error en la base de datos
    """
    try:
        coll = get_collection("clientes")
        pipeline = pipeline_clientes_con_pedidos()
        resultados = list(coll.aggregate(pipeline))
        
        if not resultados:
            return {"message": "No se encontraron clientes con pedidos"}
            
        return resultados
        
    except Exception as e:
        logger.error(f"Error en pipeline cliente-pedidos: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Error al obtener clientes con pedidos"
        )