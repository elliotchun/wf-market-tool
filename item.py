class Item:
    def __init__(self, name, orders, min, max, median, mean):
        self.name = name
        self.orders = orders
        self.min = min
        self.max = max
        self.median = median
        self.mean = mean
        self.rate = None

    def formatted_name(self):
        split_name = self.name.split('_')
        return ' '.join([word[0].upper() + word[1:] for word in split_name])

    def add_rate(self, rate: int):
        self.rate = rate