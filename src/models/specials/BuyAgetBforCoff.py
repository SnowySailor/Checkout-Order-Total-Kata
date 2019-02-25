class BuyAgetBforCoff:
    def __init__(self, count, get, off, limit):
        self.count = count
        self.get   = get
        self.off   = off
        self.limit = limit

    def to_dict(self):
        d = dict()
        d['type'] = 'buyAgetBforCoff'
        d['buy']  = self.count
        d['get']  = self.get
        d['off']  = self.off
        if self.limit is not None:
            d['limit'] = self.limit
        return d

