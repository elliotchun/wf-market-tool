from statistics import mean
from time import gmtime


class Item:
    def __init__(self, *, name: str, orders, timestamp=gmtime(), **kwargs):
        self.name = name
        self.orders = orders
        self.timestamp = timestamp
        prices = sorted([listing['platinum'] for listing in self.online_sell_orders()])
        if len(prices) == 0:
            prices = [1]
        self.min = prices[0]
        self.max = prices[-1]
        self.median = prices[int(len(prices) / 2)]
        self.mean = mean(prices)
        self.bid()
        self.spread = self.min - self.bid()

    def formatted_name(self):
        """Returns the name of the item in Title Case"""
        split_name = self.name.split('_')
        return ' '.join([word[0].upper() + word[1:] for word in split_name])

    def all_sell_orders(self):
        return [order for order in self.orders if order['type'] == 'sell']

    def all_buy_orders(self):
        return [order for order in self.orders if order['type'] == 'buy']

    def online_sell_orders(self):
        return [order for order in self.orders if order['type'] == 'sell' and order['user']['status'] != 'offline']

    def online_buy_orders(self):
        return [order for order in self.orders if order['type'] == 'buy' and order['user']['status'] != 'offline']

    def bid(self) -> int:
        buy_orders = sorted([listing['platinum'] for listing in self.online_buy_orders()])
        if len(buy_orders) == 0:
            return 0
        return buy_orders[-1]

    def spread_percent(self) -> float:
        return self.spread / self.min * 100