from parse_listings import ListingSnapshot
from item_listings import get_listings
from saved_listing_manager import load_item, path_to_saved_item
from scraper.config import *


PRINT_WIDTH = 95
HEADER_REPEAT_THRESH = 10

def main_loop():
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
    while mode != QUIT:
        if mode == HELP:
            help_menu()
        elif mode == SEARCH:
            search_price()
        elif mode == REFRESH:
            refresh_price()
        elif mode == DELETE:
            delete_item()
        elif mode == ALL:
            print_all_items()
        if mode != QUIT:
            mode = input().upper()


def help_menu():
    print('Usage:')
    print(f'[{SEARCH}]: Show summary of listings for an item')
    print(f'[{REFRESH}]: Update listings for an item')
    print(f'[{DELETE}]: Deletes a locally saved item')
    print(f'[{ALL}]: Prints the bid and ask price of each saved item')
    print(f'[{HELP}]: Help menu')
    print(f'[{QUIT}]: Quit')

def search_price():
    """Search for item listings using saved data"""
    item_name = input('Query platinum prices for an item: ')
    sanitized_name = _input_sanitize(item_name)
    try:
        item = load_item(sanitized_name)
        print_listing_info(item)
    except OSError:
        print_db_error(item_name)

def refresh_price():
    item_name = input('Query platinum prices for an item: ')
    sanitized_name = _input_sanitize(item_name)
    original_item = load_item(sanitized_name)
    new_item = get_listings(sanitized_name)

    print('_' * PRINT_WIDTH)
    print(f'{"Item Name": ^30}{"Ask": ^25}{"Bid": ^25}{"Spread": ^20}')
    print('=' * PRINT_WIDTH)
    min_diff_percent = (new_item.min - original_item.min) / original_item.min
    if original_item.bid() != 0:
        bid_diff_percent = (new_item.bid() - original_item.bid()) / original_item.bid()
    else:
        bid_diff_percent = 0
    min_info = f'{original_item.min: ^5}{ARROW_RIGHT}{new_item.min: ^5}({min_diff_percent:<0.2f}%)'
    bid_info = f'{original_item.bid(): ^5}{ARROW_RIGHT}{new_item.bid(): ^5}({bid_diff_percent:<0.2f}%)'
    old_spread_info, new_spread_info = f'{original_item.spread}', f'{new_item.spread}'
    spread_info = f'{old_spread_info: ^5}{ARROW_RIGHT}{new_spread_info: ^5}'
    print(
        f'{original_item.formatted_name(): ^30}   {min_info}   {bid_info}   {spread_info}')
    print('_' * PRINT_WIDTH)

def delete_item():
    """Prompts user to delete a locally saved item"""
    item_name = input('Saved item you want to delete: ')
    confirmation = ''
    while confirmation != YES and confirmation != NO:
        confirmation = input(f'Please confirm you want to delete this item: {item_name} (Y/N) ')
        if confirmation == YES:
            try:
                path_to_saved_item(_input_sanitize(item_name)).unlink()
                print('Saved listing has been deleted.')
            except OSError:
                print_db_error(item_name)
        else:
            print('Deletion canceled. Returning to main menu.')

def print_db_error(item_name):
    print(f'Error. Could not find {item_name} in database.')

def print_all_items():
    """Prints all saved items"""
    for i, file in enumerate(SAVED_ITEMS_PATH.iterdir()):
        if i % HEADER_REPEAT_THRESH == 0:
            print_item_info_header()
        item = load_item(file.stem)
        spread_info = f'{item.spread} ({item.spread_percent():<0.2f}%)'
        print(f'{item.formatted_name(): ^30}   {item.min: ^5}   {item.bid(): ^5}   {spread_info: ^14}')
    print('_' * PRINT_WIDTH)


def print_item_info_header():
    print('_' * PRINT_WIDTH)
    print(f'{"Item Name": ^30}   {"Ask": ^5}   {"Bid": ^5}   {"Spread": ^14}')
    print('=' * PRINT_WIDTH)


def print_listing_info(listing: ListingSnapshot):
    print(f'=== {len(listing.online_buy_orders())} listing{"s" if len(listing.online_buy_orders()) != 1 else ""} for {listing.formatted_name()} ===')
    print(f'Min/Ask: {listing.min}\t(Max: {listing.max})\nMedian: {listing.median}\t(Mean: {listing.mean})\nBid: {listing.bid()}\tSpread: {listing.spread} ({listing.spread_percent()}%)')

def _input_sanitize(q_item: str) -> str:
    """Sanitizes input of an item name for use with API"""
    return '_'.join(q_item.split()).lower()

if __name__ == '__main__':
    main_loop()