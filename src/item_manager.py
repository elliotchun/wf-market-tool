import json
import pathlib
import time

from config import SAVED_ITEMS_PATH, DATA_DIR
from src.item import Item

ITEM_LIST_NAME = 'items.list'

def save_item(item: Item):
    """Saves item locally"""
    timestamped_filename = item.name + ' - ' + time.strftime('%Y-%m-%d %H:%M', item.timestamp)
    _write_item_file_with_name(item, item.name)
    _write_item_file_with_name(item, timestamped_filename)

def _write_item_file_with_name(item, filename):
    path_to_item = path_to_saved_item(filename)
    with open(path_to_item, 'w') as file:
        json.dump(item.__dict__, file)

def load_item(item_name: str) -> Item:
    path_to_item = path_to_saved_item(item_name)
    with open(path_to_item, 'r') as file:
        data = json.load(file)
    return Item(**data)

def path_to_saved_item(item_name: str):
    return SAVED_ITEMS_PATH.joinpath(f'{item_name}.json')

def get_all_saved_item_paths() -> list[pathlib.Path]:
    return [pathlib.Path(p) for p in SAVED_ITEMS_PATH.iterdir()]

def save_item_list(item_list: list[str]) -> None:
    with open(DATA_DIR / ITEM_LIST_NAME, 'w') as file:
        file.writelines(item_list)

def load_item_list() -> list[str]:
    with open(DATA_DIR / ITEM_LIST_NAME, 'r') as file:
        return [line.rstrip('\n') for line in file]