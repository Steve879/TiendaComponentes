# mi_api/pipelines/cliente_pedidos.py
from typing import List, Dict, Any
from bson import ObjectId

def pipeline_clientes_con_pedidos() -> List[Dict[str, Any]]:
    """
    Pipeline que une clientes con sus pedidos usando $lookup
    
    Returns:
        List[Dict]: Pipeline de agregación completo
    """
    return [
        {
            "$lookup": {
                "from": "pedidos",
                "localField": "_id",
                "foreignField": "id_cliente",
                "as": "pedidos"
            }
        },
        {
            "$project": {
                "_id": 0,
                "id": {"$toString": "$_id"},
                "nombre": 1,
                "apellido": 1,
                "email": 1,
                "total_pedidos": {"$size": "$pedidos"},
                "pedidos_recientes": {
                    "$slice": [
                        {
                            "$map": {
                                "input": "$pedidos",
                                "as": "pedido",
                                "in": {
                                    "id_pedido": {"$toString": "$$pedido._id"},
                                    "fecha": "$$pedido.fecha_pedido",
                                    "estado": "$$pedido.estado",
                                    "total": "$$pedido.total"
                                }
                            }
                        },
                        5  # Mostrar solo los últimos 5 pedidos
                    ]
                }
            }
        },
        {
            "$sort": {"total_pedidos": -1}  # Ordenar por clientes con más pedidos
        }
    ]