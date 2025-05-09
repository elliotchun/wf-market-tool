import numpy as np
import matplotlib.pyplot as plt

from src.item_manager import load_item

def plot_item_stats(item_name: str):
    item = load_item(item_name)
    orders = np.array([[v for k,v in order.items()] for order in item.all_sell_orders()])
    X = orders[:,2]
    X = np.random.randn(100)
    plt.hist(X)
    plt.show()

plot_item_stats('acid_shells')