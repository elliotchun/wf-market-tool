from saved_listing_manager import save_item, save_item_list

def save_listings(api_src, save_path, *, list_file_name=None, log_file=None) -> None:
    """Get all item listings currently on WFM"""
    items = api_src.get_items()
    if list_file_name:
        save_item_list(items, save_path, list_file_name)
    log_file.write(f'Got {len(items)} items. Getting listings.\n')
    for item_name in items:
        log_file.write(f'Item name: {item_name}\n')
        item = api_src.get_listings(item_name)
        if not item:
            log_file.write(f'Request not OK for {item_name}. Skipping.\n')
            continue
        log_file.write(f'Got {len(item.orders)} listings. Saving.\n')
        save_item(item, save_path)