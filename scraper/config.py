import os
import sys
from pathlib import Path

# File paths
LOG_FILE = sys.stdout
BASE_DIR = Path(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = BASE_DIR / "data"
SAVED_ITEMS_PATH = DATA_DIR / "saved_items"
# Ensure the saved items directory exists
SAVED_ITEMS_PATH.mkdir(exist_ok=True)

REQUEST_HEADERS = {
    'Platform': 'pc',
    'Crossplay': 'true'
}

# Constants
QUIT = "Q"
HELP = "H"
SEARCH = "S"
CALCULATE = "C"
REFRESH = "R"
RECALL = "L"
DELETE = "D"
ALL = "A"
YES = "Y"
NO = "N"
ARROW_RIGHT = "→"
