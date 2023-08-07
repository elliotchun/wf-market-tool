from time import sleep
import urllib.parse
import urllib.request
import urllib.response
import json
from pathlib import Path
from statistics import mean
from item import Item

SAVED_ITEMS_PATH = Path('./saved-items/')
URL = 'https://api.warframe.market/v1/'
SEARCH = 'S'
CALCULATE = 'C'
REFRESH = 'R'
GET = 'E'
DELETE = 'D'
HELP = 'H'
QUIT = 'Q'

YES = 'Y'
NO = 'N'


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
    print('Warframe.Market Grofit Analyzer')
    mode = input().upper()
    last_item = None
    while mode != QUIT:
        if mode == HELP:
            help_menu()
        elif mode == SEARCH:
            last_item = search_price()
            print_listing_info(last_item)
        elif mode == CALCULATE:
            last_item = calculate_rate(last_item)
            save_item(last_item)
            print_rate_info(last_item)
        elif mode == REFRESH:
            recalculate_items()

        if mode != QUIT:
            mode = input().upper()

def save_item(item: Item):
    """Saves item locally"""
    path_to_item = path_to_saved_item(item.name)
    with open(path_to_item, 'w') as file:
        json.dump(item.__dict__, file)

def load_item(item: str):
    path_to_item = path_to_saved_item(item)
    with open(path_to_item, 'r') as file:
        data = json.loads(file)
    return Item(*data)

def path_to_saved_item(item_name: str):
    return SAVED_ITEMS_PATH.joinpath(f'{item_name}.json')

def help_menu():
    print('Usage:')
    print(f'[{SEARCH}]: Search listings of an item')
    print(f'[{CALCULATE}]: Calculator for farming platinum')
    print(f'[{REFRESH}]: Recalculate platinum values of locally saved items')
    print(f'[{HELP}]: Help menu')
    print(f'[{QUIT}]: Quit')

def search_price() -> Item:
    """Search for item listings on Warframe.Market"""
    item_name = input('Query platinum prices for an item: ')
    item_name = _input_sanitize(item_name)
    return market_retrieve(item_name)


def market_retrieve(item_name: str):
    orders = get_listings(item_name)
    (p_min, p_max, p_median, p_mean) = _get_price_info(orders)
    return _save_price_info(item_name, orders, p_min, p_max, p_median, p_mean)

def print_listing_info(item: Item):
    print(f'=== {len(item.orders)} listing{"s" if len(item.orders) != 1 else ""} for {item.formatted_name()} ===')
    print(f'Min: {item.min}\t(Max: {item.max})\nMedian: {item.median}\t(Mean: {item.mean})')

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

def _calculate_plat_rate(item):
    chance = float(input('Chance to obtain item in a run: '))
    time = float(input('Run time for item in minutes: '))
    exp_time = time / chance
    item.add_rate(exp_time * 60)
    return item

def recalculate_items():
    for file in SAVED_ITEMS_PATH.iterdir():
        sleep(1)
        item_name = file.stem
        market_retrieve(item_name)


def get_listings(item_name: str):
    """Gets all the listings for given item"""
    item_name = _input_sanitize(item_name)
    listings_url = URL + f'items/{item_name}/orders'
    with urllib.request.urlopen(listings_url) as res:
        orders = json.loads(res.read())['payload']
        return orders

def _get_price_info(orders: dict):
    """Gets the plat price information from a list of sell orders."""
    prices = sorted([listing['platinum'] for listing in orders['orders']])
    p_min = prices[0]
    p_max = prices[-1]
    p_median = prices[int(len(prices) / 2)]
    p_mean = mean(prices)
    return p_min, p_max, p_median, p_mean

def _save_price_info(name, orders, i_min, i_max, i_median, i_mean):
    """Constructs a new Item and saves it to the database"""
    item = Item(name, orders, i_min, i_max, i_median, i_mean)
    save_item(item)
    return item

def _input_sanitize(q_item: str):
    """Sanitizes input of an item name for use with API"""
    return '_'.join(q_item.split()).lower()

if __name__ == '__main__':
    main()