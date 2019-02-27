# Buy cheese, get any other item of equal or lesser value for 25% off"
class GetEOLforAoff:
    def __init__(self, off):
        self.off = off

    def to_dict(self):
        d = dict()
        d['type'] = 'getEOLforAoff'
        d['off']  = self.off
        return d