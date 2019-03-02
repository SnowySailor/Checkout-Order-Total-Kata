class Markdown:
    def __init__(self, percentage, limit):
        self.percentage = percentage
        self.limit = limit

    def to_dict(self):
        d = dict()
        d['type'] = 'markdown'
        d['percentage'] = self.percentage
        if self.limit is not None:
            d['limit'] = self.limit
        return d
