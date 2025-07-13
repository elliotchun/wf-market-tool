import sys

import config
from make_requests import save_listings
import riven_listings

def main():
    save_listings(riven_listings, config.SAVED_RIVENS_PATH, log_file = sys.stdout)

if __name__ == '__main__':
    main()
