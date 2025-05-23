import time
import urllib.parse

import requests

from config import REQUEST_HEADERS
from src.item import Item

URL = "https://api.warframe.market/v1/"
RIVEN_WEAPONS_ENDPOINT = "riven/items"
RIVEN_AUCTIONS_ENDPOINT = "auctions/search?"
API_RATE_LIMIT_IN_SECONDS = 1 / 3

last_api_access = time.time()

def get_items() -> list[str]:
    """Get the slug for all weapons that have Riven mods"""
    response = _get_json_or_none_if_not_ok(URL + RIVEN_WEAPONS_ENDPOINT)
    items = response['payload']['items']
    return [item_short['url_name'] for item_short in items]

def get_listings(item_name: str) -> Item:
    """Gets all the Riven auctions for the given weapon"""
    listings_url = URL + RIVEN_AUCTIONS_ENDPOINT + _get_query_string_for_weapon(item_name)
    response = _get_json_or_none_if_not_ok(listings_url)
    all_orders = response['payload']['auctions']
    return Item(name=item_name, orders=all_orders)

def _get_query_string_for_weapon(item_name: str) -> str:
    query_params = {
        'type': 'riven',
        'weapon_url_name': item_name
    }
    return urllib.parse.urlencode(query_params)

def _get_json_or_none_if_not_ok(url: str):
    time_now = time.time()
    seconds_since_last_api_access = time_now - last_api_access
    if seconds_since_last_api_access < API_RATE_LIMIT_IN_SECONDS:
        time.sleep(API_RATE_LIMIT_IN_SECONDS - seconds_since_last_api_access)
    res = requests.get(url, headers=REQUEST_HEADERS)
    if res.status_code != requests.codes.ok:
        return None
    return res.json()