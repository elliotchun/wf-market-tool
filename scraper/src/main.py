import riven_listings
from saved_listing_manager import save_item
from scraper import config


def main():
    item = riven_listings.get_listings('syam')
    save_item(item, config.SAVED_RIVENS_PATH)

if __name__ == '__main__':
    main()
