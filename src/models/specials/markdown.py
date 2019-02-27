class Markdown:
    def __init__(self, percentage):
        self.percentage = percentage

    def to_dict(self):
        d = dict()
        d['type'] = 'markdown'
        d['percentage'] = self.percentage
        return d
