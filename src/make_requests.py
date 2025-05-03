from src.api import get_items, get_listings
from src.item_manager import save_item, save_item_list


def get_all_item_listings(*, /, log_file=None) -> None:
    """Get all item listings currently on WFM"""
    items = get_items()
    log_file.write(f'Got {len(items)} items. Getting listings.')
    for item_name in items:
        log_file.write(f'Item name: {item_name}')
        item = get_listings(item_name)
        log_file.write(f'Got {len(item.orders)} listings. Saving.')
        save_item(item)
    save_item_list(items)

# def continue_get_all_item_listings() -> None:
#     """"""
#     items = get_saved_items()
#     for item in items:
#         get_saved_listings(item.name)