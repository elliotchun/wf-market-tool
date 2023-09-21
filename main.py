import urllib.parse
import urllib.request
import urllib.response
from urllib.error import HTTPError
import json
from pathlib import Path
from time import sleep
from item import Item

SAVED_ITEMS_PATH = Path('./saved-items/')
URL = 'https://api.warframe.market/v1/'
SEARCH = 'S'
CALCULATE = 'C'
REFRESH = 'R'
RECALL = 'E'
ALL = 'A'
DELETE = 'D'
HELP = 'H'
QUIT = 'Q'

YES = 'Y'
NO = 'N'
ARROW_RIGHT = '->'


def main():
    print(r"""
                             ,
                             B
                            BMB.
                          3BBBMBX
                       .PMBMBMBMBBD,
                     7MBMBMBMBMBMBMBMs
                  :EBMBMBMBMx iMBMBMBMBO:
                7BMBMBBBMBJ     vBBBBBMBMBs
              xMBMBBBMBH,    .    .UBMBMBMBBF
            .BMBBBMBX:      :Br      .FBMBMBBB:
 LR;,.:rUOBMBMBMBM;       ;MBMBBr       :OBMBMBBBRSr:.,:EU
  MBMBMBBBMBMBMM.      :0BMBBEMBMBD:       WMBBBMBMBMBMBM
  HMBBr    BBMc     .HBMBMBK   FBBBMBZ,     ;BBB    rBBBM
  MBM      UMP    .BMBMBZ:       ,HBMBMB:    LBM      MBM
  BBB   BMBMBr   cBMBW:     0BM     .0BMBF   .BMBMB   BMB:
 WBBx   cBL.iB   BMR     cMBM1MBM3     PMB   M7,;BK   ;BMB
 MBM    BM:  .r  BB    RBMB;   :RMBM    RM  c:   MB    MBM
:BM7    BB     , ,M   MBr         ;BM   Or .     BM:   :MBi
:MB,   7B7        .i  B             B  ::        :BS    BM
 BMG    BK             :                         cM:   2MB
  BMH   .Mi     : :                 E:          :M:   sMB
   ;MRui  ;:.   :Fui:;  :;;7i   .;;;rS:,  rr   ,:  :7EO:
        ::::::,   .UUi:77;::37s7Lv7;  ,;3SD,....:;;,
     BM: ..:i7rJLxS:  .      rs: 7   ..;LxxUWRFU;::7OW
      S2r:::iis0r;J3Or.:rvLi:::rBL.  .:;,  .   :ri:.,
                    .ZL. .:L;,r7;i7r;7:
                            xMc     ,
                           :. 3v
                           :S  ;
                            LB;
                             7
    """)
    print('Warframe.Market Grofit Watchlist Tool')
    mode = input().upper()
    last_item = None
    while mode != QUIT:
        if mode == HELP:
            help_menu()
        elif mode == SEARCH:
            try:
                last_item = search_price()
                print_listing_info(last_item)
            except HTTPError as e:
                print('API Error:', e.status)
        elif mode == CALCULATE:
            last_item = calculate_rate(last_item)
            save_item(last_item)
            print_rate_info(last_item)
        elif mode == REFRESH:
            print('Refreshing...')
            recalculate_items()
            print('All saved listings have been refreshed!')
        elif mode == RECALL:
            recall_saved()
        elif mode == DELETE:
            delete_item()
        elif mode == ALL:
            print_all_items()
        if mode != QUIT:
            mode = input().upper()

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

def help_menu():
    print('Usage:')
    print(f'[{SEARCH}]: Search listings of an item')
    print(f'[{CALCULATE}]: Calculator for farming platinum')
    print(f'[{REFRESH}]: Recalculate platinum values of locally saved items')
    print(f'[{RECALL}]: Recalls the information for a locally saved item')
    print(f'[{DELETE}]: Deletes a locally saved item')
    print(f'[{ALL}]: Prints the bid and ask price of each saved item')
    print(f'[{HELP}]: Help menu')
    print(f'[{QUIT}]: Quit')

def recall_saved():
    """Recalls infromation of a saved item"""
    item_name = input('Retrieve the information for a saved item: ')
    item = load_item(_input_sanitize(item_name))
    print_listing_info(item)

def print_all_items():
    """Prints all saved items"""
    PRINT_WIDTH = 65
    print('_' * PRINT_WIDTH)
    print(f'{"Item Name": ^30}   {"Ask": ^5}   {"Bid": ^5}   {"Spread": ^14}')
    print('=' * PRINT_WIDTH)
    for file in SAVED_ITEMS_PATH.iterdir():
        item = load_item(file.stem)
        spread_info = f'{item.spread} ({item.spread_percent():<0.2f}%)'
        print(f'{item.formatted_name(): ^30}   {item.min: ^5}   {item.bid(): ^5}   {spread_info: ^14}')
    print('_' * PRINT_WIDTH)

def search_price() -> Item:
    """Search for item listings on Warframe.Market"""
    item_name = input('Query platinum prices for an item: ')
    return market_retrieve(_input_sanitize(item_name))


def market_retrieve(item_name: str) -> Item:
    """Get item information using the given item name"""
    orders = get_listings(item_name)
    item = _get_item_info(item_name)
    if _item_is_mod(item):
        print(item_name, 'is a mod.')
        rank = _ask_for_rank(item)
        orders = [order for order in orders if order['mod_rank'] == rank]
    item = Item(name=item_name, orders=orders)
    save_item(item)
    return item

def print_listing_info(item: Item):
    print(f'=== {len(item.online_listings())} listing{"s" if len(item.online_listings()) != 1 else ""} for {item.formatted_name()} ===')
    print(f'Min/Ask: {item.min}\t(Max: {item.max})\nMedian: {item.median}\t(Mean: {item.mean})\nBid: {item.bid()}\tSpread: {item.spread} ({item.spread_percent()}%)')

def print_rate_info(item: Item):
    print(f'=== Platinum Rate for {item.formatted_name()} ===')
    print(f'Min: {item.min / item.rate}\nMedian: {item.median / item.rate}\t(Mean: {item.mean / item.rate})')

def calculate_rate(item: Item) -> Item:
    """Calculator tool to calculate the rate of farming platinum. Returns plat/hr"""
    use_local_item = False
    if item:
        print(f'Your last searched item is {item.formatted_name()}')
        response = input('Calculate farming rate for this item?\n').upper()
        while True:
            if response == YES:
                return _calculate_plat_rate(item)
            elif response == NO:
                use_local_item = True
                break
            response = input()
    if not item or use_local_item:
        item_name = input('Get farming rate: ')
        item = load_item(_input_sanitize(item_name))
        return _calculate_plat_rate(item)

def delete_item():
    """Prompts user to delete a locally saved item"""
    item_name = input('Saved item you want to delete: ')
    confirmation = ''
    while confirmation != YES and confirmation != NO:
        confirmation = input(f'Please confirm you want to delete this item: {_input_sanitize(item_name)} (Y/N) ')
        if confirmation == YES:
            path_to_saved_item(_input_sanitize(item_name)).unlink()
            print('Saved listing has been deleted.')
        else:
            print('Deletion canceled. Returning to main menu.')

def _calculate_plat_rate(item: Item) -> Item:
    chance = float(input('Chance to obtain item in a run: '))
    time = float(input('Run time for item in minutes: '))
    exp_time = time / chance
    item.add_rate(exp_time * 60)
    return item

def recalculate_items():
    refreshed_items = list()
    for file in SAVED_ITEMS_PATH.iterdir():
        sleep(1)
        item_name = file.stem
        orig_item = load_item(item_name)
        new_item = market_retrieve(item_name)
        refreshed_items.append((orig_item, new_item))
    PRINT_WIDTH = 95
    print('_' * PRINT_WIDTH)
    print(f'{"Item Name": ^30}{"Ask": ^25}{"Bid": ^25}{"Spread": ^20}')
    print('=' * PRINT_WIDTH)
    for item_pair in refreshed_items:
        min_diff_percent = (item_pair[1].min - item_pair[0].min) / item_pair[0].min
        if item_pair[0].bid() != 0:
            bid_diff_percent = (item_pair[1].bid() - item_pair[0].bid()) / item_pair[0].bid()
        else:
            bid_diff_percent = 0
        min_info = f'{item_pair[0].min: ^5}{ARROW_RIGHT}{item_pair[1].min: ^5}({min_diff_percent:<0.2f}%)'
        bid_info = f'{item_pair[0].bid(): ^5}{ARROW_RIGHT}{item_pair[1].bid(): ^5}({bid_diff_percent:<0.2f}%)'
        old_spread_info, new_spread_info = f'{item_pair[0].spread}', f'{item_pair[1].spread}'
        spread_info = f'{old_spread_info: ^5}{ARROW_RIGHT}{new_spread_info: ^5}'
        print(
            f'{item_pair[0].formatted_name(): ^30}   {min_info}   {bid_info}   {spread_info}')
    print('_' * PRINT_WIDTH)

def get_listings(item_name: str):
    """Gets all the listings for given item"""
    item_name = _input_sanitize(item_name)
    listings_url = URL + f'items/{item_name}/orders'
    with urllib.request.urlopen(listings_url) as res:
        orders = json.loads(res.read())['payload']['orders']
        return orders

def _get_item_info(item_name: str):
    """Looks up an item via Warframe.Market API"""
    item_name = _input_sanitize(item_name)
    item_url = URL + f'items/{item_name}'
    with urllib.request.urlopen(item_url) as res:
        items = json.loads(res.read())['payload']['item']['items_in_set']
    for item in items:
        if item['url_name'] == item_name:
            return item

def _ask_for_rank(item) -> int:
    while True:
        rank_choice = input('Rank zero or max rank? (Y/N; Zero/Max) ')
        if rank_choice == YES:
            return 0
        if rank_choice == NO:
            return _mod_max_rank(item)
        print('Not a valid response. [Y] for zero or [N] for max.')

def _item_is_mod(item) -> bool:
    return 'mod_max_rank' in item

def _mod_max_rank(item) -> int:
    return item['mod_max_rank']

def _input_sanitize(q_item: str) -> str:
    """Sanitizes input of an item name for use with API"""
    return '_'.join(q_item.split()).lower()

if __name__ == '__main__':
    main()