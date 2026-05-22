from services.collection_service import (
    create_collection,
    delete_collection,
    get_collections_lookup,
    get_my_collection,
    update_collection
)


def get_current_collection(collection_id):
    collections = get_collections_lookup()

    for collection in collections:
        if collection.get("id") == collection_id:
            return collection

    return None


def get_sorted_collections():
    return sorted(get_collections_lookup(), key=lambda collection: collection.get("name", "").lower())
