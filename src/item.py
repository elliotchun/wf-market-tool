from statistics import mean

class Item:
    def __init__(self, *, name, orders, **kwargs):
        self.name = name
        self.orders = orders

        self.prices = sorted([listing['platinum'] for listing in self.sell_orders()])
        if len(self.prices) == 0:
            self.prices = [0]
        self.min = self.prices[0]
        self.max = self.prices[-1]
        self.median = self.prices[int(len(self.prices) / 2)]
        self.mean = mean(self.prices)
        self.bid()
        self.spread = self.min - self.bid()

    def formatted_name(self):
        """Returns the name of the item in Title Case"""
        split_name = self.name.split('_')
        return ' '.join([word[0].upper() + word[1:] for word in split_name])

    def sell_orders(self):
        return [order for order in self.orders if order['type'] == 'sell']

    def buy_orders(self):
        return [order for order in self.orders if order['type'] == 'buy']

    def online_listings(self):
        return [order for order in self.orders if order['user']['status'] != 'offline' and order['type'] == 'sell']

    def bid(self) -> int:
        buy_orders = sorted([listing['platinum'] for listing in self.orders if
                         listing['user']['status'] != 'offline' and listing['type'] == 'buy'])
        if len(buy_orders) == 0:
            return 0
        return buy_orders[-1]

    def spread_percent(self) -> float:
        return self.spread / self.min * 100