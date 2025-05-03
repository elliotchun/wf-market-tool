import json

from config import SAVED_ITEMS_PATH, YES, NO
from src.item import Item

ITEM_LIST_NAME = 'items.list'

def save_item(item: Item):
    """Saves item locally"""
    path_to_item = path_to_saved_item(item.name)
    with open(path_to_item, 'w') as file:
        json.dump(item.__dict__, file)

def load_item(item_name: str) -> Item:
    path_to_item = path_to_saved_item(item_name)
    with open(path_to_item, 'r') as file:
        data = json.load(file)
    return Item(**data)

def path_to_saved_item(item_name: str):
    return SAVED_ITEMS_PATH.joinpath(f'{item_name}.json')

def get_all_saved_items():
    return SAVED_ITEMS_PATH.iterdir()

def save_item_list(item_list: list[str]) -> None:
    with open(SAVED_ITEMS_PATH / ITEM_LIST_NAME, 'w') as file:
        file.writelines(item_list)

def load_item_list() -> list[str]:
    with open(SAVED_ITEMS_PATH / ITEM_LIST_NAME, 'r') as file:
        return [line.rstrip('\n') for line in file]
