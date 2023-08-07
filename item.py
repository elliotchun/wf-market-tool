from statistics import mean

class Item:
    def __init__(self, *, name, orders, rate = None, **kwargs):
        self.name = name
        self.orders = orders
        self.rate = rate
        prices = sorted([listing['platinum'] for listing in orders['orders'] if listing['user']['status'] != 'offline' and listing['order_type'] == 'sell'])
        self.min = prices[0]
        self.max = prices[-1]
        self.median = prices[int(len(prices) / 2)]
        self.mean = mean(prices)

    def formatted_name(self):
        split_name = self.name.split('_')
        return ' '.join([word[0].upper() + word[1:] for word in split_name])

    def add_rate(self, rate: float):
        self.rate = rate

    def online_listings(self):
        return [order for order in self.orders['orders'] if order['user']['status'] != 'offline' and order['order_type'] == 'sell']