class BuyAgetBforCoff:
    def __init__(self, count, get, off):
        self.count = count
        self.get   = get
        self.off   = off

    def to_dict(self):
        d = dict()
        d['type'] = 'buyAgetBforCoff'
        d['buy']  = self.count
        d['get']  = self.get
        d['off']  = self.off
        return d

