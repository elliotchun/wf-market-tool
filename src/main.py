import config
from src.make_requests import get_all_item_listings
from src.plots import plot_item_stats


def main():
    # get_all_item_listings(log_file=config.LOG_FILE)
    plot_item_stats('acid_shells')

if __name__ == '__main__':
    main()
