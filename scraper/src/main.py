from scraper import config
import item_listings
from make_requests import save_listings


def main():
    save_listings(item_listings, log_file=config.LOG_FILE)

if __name__ == '__main__':
    main()
