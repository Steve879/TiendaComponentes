from utils.mongodb import get_collection
from bson.objectid import ObjectId


def get_components_with_inventory():
    coll = get_collection("components")
    pipeline = [
        {
            "$lookup": {
                "from": "inventory",
                "localField": "_id",
                "foreignField": "component_id",
                "as": "inventory_data"
            }
        }
    ]
    return list(coll.aggregate(pipeline))


def get_inventory_count_by_component():
    coll = get_collection("inventory")
    pipeline = [
        {
            "$group": {
                "_id": "$component_id",
                "total_quantity": {"$sum": "$quantity"},
                "average_cost": {"$avg": "$unit_cost"}
            }
        }
    ]
    return list(coll.aggregate(pipeline))


def get_components_out_of_stock():
    coll = get_collection("components")
    pipeline = [
        {
            "$lookup": {
                "from": "inventory",
                "localField": "_id",
                "foreignField": "component_id",
                "as": "inventory_data"
            }
        },
        {
            "$match": {
                "$or": [
                    {"inventory_data": {"$size": 0}},
                    {"inventory_data.quantity": {"$lte": 0}}
                ]
            }
        }
    ]
    return list(coll.aggregate(pipeline))
