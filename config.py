import os
from pathlib import Path

# File paths
BASE_DIR = Path(os.path.dirname(os.path.abspath(__file__)))
SAVED_ITEMS_PATH = BASE_DIR / "data" / "saved_items"
# Ensure the saved items directory exists
SAVED_ITEMS_PATH.mkdir(exist_ok=True)

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
