from statistics import mean

class Item:
    def __init__(self, *, name, orders, rate = None, **kwargs):
        self.name = name
        self.orders = orders
        self.rate = rate

        prices = sorted([listing['platinum'] for listing in self.online_listings()])
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

    def add_rate(self, rate: float):
        self.rate = rate

    def online_listings(self):
        return [order for order in self.orders if order['user']['status'] != 'offline' and order['order_type'] == 'sell']

    def bid(self) -> int:
        buy_orders = sorted([listing['platinum'] for listing in self.orders if
                         listing['user']['status'] != 'offline' and listing['order_type'] == 'buy'])
        if len(buy_orders) == 0:
            return 0
        return buy_orders[-1]

    def spread_percent(self) -> float:
        return self.spread / self.min * 100