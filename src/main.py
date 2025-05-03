import config
from src.make_requests import get_all_item_listings


def main():
    get_all_item_listings(log_file=config.LOG_FILE)

if __name__ == '__main__':
    main()
