import json
import pathlib
import time

from parse_listings import ListingSnapshot

def save_item(listing: ListingSnapshot, data_dir: pathlib.Path):
    """Saves listing information to disk"""
    timestamped_filename = listing.itemname + ' - ' + time.strftime('%Y-%m-%d %H:%M', listing.timestamp)
    _write_listing(listing, data_dir, listing.itemname)
    _write_listing(listing, data_dir, timestamped_filename)

def _write_listing(item, data_dir, filename):
    path_to_item = path_to_saved_item(data_dir, filename)
    with open(path_to_item, 'w') as file:
        json.dump(item.__dict__, file)

def load_item(data_dir: pathlib.Path, item_name: str) -> ListingSnapshot:
    path_to_item = path_to_saved_item(data_dir, item_name)
    with open(path_to_item, 'r') as file:
        data = json.load(file)
    return ListingSnapshot() # TODO

def path_to_saved_item(data_dir, item_name: str):
    return data_dir.joinpath(f'{item_name}.json')

def get_all_saved_item_paths(saved_items_path) -> list[pathlib.Path]:
    return [pathlib.Path(p) for p in saved_items_path.iterdir()]

def save_item_list(item_list: list[str], data_dir: pathlib.Path, list_file_name: str) -> None:
    with open(data_dir / list_file_name, 'w') as file:
        file.writelines(item_list)

def load_item_list(data_dir, list_file_name) -> list[str]:
    with open(data_dir / list_file_name, 'r') as file:
        return [line.rstrip('\n') for line in file]