import urllib.parse
import urllib.request
import urllib.response
import json
from statistics import mean
from item import Item

URL = 'https://api.warframe.market/v1/'
SEARCH = 'S'
CALCULATE = 'C'
REFRESH = 'R'
EDIT = 'E'
DELETE = 'D'
HELP = 'H'
QUIT = 'X'
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
        if mode == SEARCH:
            last_item = research_price()
            print_listing_info(last_item)
        elif mode == CALCULATE:
            calculate_rate(last_item)
        elif mode == HELP:
            help_menu()

        if mode != QUIT:
            mode = input().upper()


def research_price() -> Item:
    """Search for item listings on Warframe.Market"""
    q_item = input('Query platinum prices for an item: ')
    orders = get_listings(q_item)
    (p_min, p_max, p_median, p_mean) = _get_price_info(orders)
    return _save_price_info(q_item, orders, p_min, p_max, p_median, p_mean)


def print_listing_info(item: Item):
    print(f'=== {len(item.orders)} listing{"s" if len(item.orders) != 1 else ""} for {item.formatted_name()} ===')
    print(f'Min: {item.min}\t(Max: {item.max})\nMedian: {item.median}\t(Mean: {item.mean})')

def calculate_rate(item: Item) -> float:
    """Calculator tool to calculate the rate of farming platinum. Returns plat/hr"""
    use_local_item = False
    if item:
        print(f'Your last searched item is {item.formatted_name()}')
        response = input('Calculate farming rate for this item?\n').upper()
        while True:
            if response == YES:
                chance = float(input('Chance to obtain item in a run: '))
                time = float(input('Run time for item in minutes: '))
                exp_time = time / chance
                return item.min / exp_time * 60
            elif response == NO:
                use_local_item = True
                break
            response = input()
    if not item or use_local_item:
        item = input('Item: ')
        raise NotImplementedError

def help_menu():
    print('Usage:')
    print(f'[{SEARCH}]: Search listings of an item')
    print(f'[{CALCULATE}]: Calculator for farming platinum')
    print(f'[{HELP}]: Help menu')
    print(f'[{QUIT}]: Quit')

def get_listings(item: str):
    """Gets all the listings for given item"""
    item = _input_sanitize(item)
    listings_url = URL + f'items/{item}/orders'
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
    return Item(name, orders, i_min, i_max, i_median, i_mean)

def _input_sanitize(q_item: str):
    """Sanitizes input of an item name for use with API"""
    return '_'.join(q_item.split()).lower()

if __name__ == '__main__':
    main()