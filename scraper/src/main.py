import sys

import riven_listings
from scraper import config
from scraper.src.make_requests import save_listings


def main():
    save_listings(riven_listings, config.SAVED_RIVENS_PATH, log_file = sys.stdout)

if __name__ == '__main__':
    main()
