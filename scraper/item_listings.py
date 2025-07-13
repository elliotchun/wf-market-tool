import time

import requests

import config
from parse_listings import ListingSnapshot

URL = "https://api.warframe.market/v2/"
ALL_ITEMS_PATH_ENDPOINT = "items"
SINGLE_ITEM_ENDPOINT = "orders/item/"
API_RATE_LIMIT_IN_SECONDS = 1 / 3

last_api_access = time.time()

def get_items() -> list[str]:
    response = _get_json_or_none_if_not_ok(URL + ALL_ITEMS_PATH_ENDPOINT)
    items = response['data']
    return [item_short['slug'] for item_short in items]

def get_listings(item_name: str) -> ListingSnapshot:
    """Gets all the listings for given item"""
    listings_url = URL + SINGLE_ITEM_ENDPOINT + item_name
    response = _get_json_or_none_if_not_ok(listings_url)
    all_orders = response['data']
    return ListingSnapshot(name=item_name, orders=all_orders)

def _get_json_or_none_if_not_ok(url: str):
    global last_api_access
    time_now = time.time()
    seconds_since_last_api_access = time_now - last_api_access
    if seconds_since_last_api_access < API_RATE_LIMIT_IN_SECONDS:
        time.sleep(API_RATE_LIMIT_IN_SECONDS - seconds_since_last_api_access)
    res = requests.get(url, headers= config.REQUEST_HEADERS)
    last_api_access = time.time()
    if res.status_code != requests.codes.ok:
        return None
    return res.json()