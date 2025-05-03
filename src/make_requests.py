from src.api import get_items, get_listings
from src.item_manager import save_item


def get_all_item_listings() -> None:
    """Get all item listings currently on WFM"""
    items = get_items()
    for item_name in items:
        item = get_listings(item_name)
        # save_item(item)

def get_all_item_listings_saved() -> None:
    """Recall item listings saved locally"""
    items = get_saved_items()
    for item in items:
        get_saved_listings(item.name)