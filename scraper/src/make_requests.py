from src.item_manager import save_item, save_item_list

def save_listings(api_src, *, log_file=None) -> None:
    """Get all item listings currently on WFM"""
    items = api_src.get_items()
    save_item_list(items)
    log_file.write(f'Got {len(items)} items. Getting listings.\n')
    for item_name in items:
        log_file.write(f'Item name: {item_name}\n')
        item = api_src.get_listings(item_name)
        log_file.write(f'Got {len(item.orders)} listings. Saving.\n')
        save_item(item)