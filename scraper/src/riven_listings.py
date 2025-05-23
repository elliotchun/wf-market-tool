import time
import urllib.parse

import requests

from scraper.config import REQUEST_HEADERS
from scraper.src.parse_listings import ListingSnapshot


URL = "https://api.warframe.market/v1/"
RIVEN_WEAPONS_ENDPOINT = "riven/items"
RIVEN_AUCTIONS_ENDPOINT = "auctions/search?"
API_RATE_LIMIT_IN_SECONDS = 1
RETRIES = 10

last_api_access = time.time()

def get_items() -> list[str]:
    """Get the slug for all weapons that have Riven mods"""
    response = _get_json_or_none_if_not_ok(URL + RIVEN_WEAPONS_ENDPOINT)
    items = response['payload']['items']
    return [item_short['url_name'] for item_short in items]

def get_listings(item_name: str) -> ListingSnapshot | None:
    """Gets all the Riven auctions for the given weapon"""
    listings_url = URL + RIVEN_AUCTIONS_ENDPOINT + _get_query_string_for_weapon(item_name)

    response = _get_json_or_none_if_not_ok(listings_url)
    backoff = 0
    while not response or backoff < RETRIES:
        time.sleep(API_RATE_LIMIT_IN_SECONDS * (backoff + 1))
        response = _get_json_or_none_if_not_ok(listings_url)
    if not response:
        return None
    all_orders = response['payload']['auctions']
    return ListingSnapshot(name=item_name, orders=_convert_orders(all_orders))

def _convert_orders(orders: list[dict]) -> list[dict]:
    def is_direct_sale(order: dict) -> bool:
        return order['is_direct_sell']

    def convert_order(order: dict) -> dict:
        return {
            'type': 'sell',
            'user': {
                'status': order['owner']['status']
            },
            'item': order['item'],
            'platinum': order['buyout_price']
        }

    return [convert_order(order) for order in orders if is_direct_sale(order)]

def _get_query_string_for_weapon(item_name: str) -> str:
    query_params = {
        'type': 'riven',
        'weapon_url_name': item_name
    }
    return urllib.parse.urlencode(query_params)

def _get_json_or_none_if_not_ok(url: str):
    global last_api_access
    time_now = time.time()
    seconds_since_last_api_access = time_now - last_api_access
    if seconds_since_last_api_access < API_RATE_LIMIT_IN_SECONDS:
        time.sleep(API_RATE_LIMIT_IN_SECONDS - seconds_since_last_api_access)
    res = requests.get(url, headers=REQUEST_HEADERS)
    last_api_access = time.time()
    if res.status_code != requests.codes.ok:
        return None
    return res.json()