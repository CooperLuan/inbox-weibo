import copy

from instream import env


class BaseModel(object):

    def __init__(self):
        pass


class StatusesModel(BaseModel):

    route = 'crawler.weibo.statuses'

    def get_statuses(self, count=50):
        skip = 0
        while 1:
            c = env.MONGO.webpages.find(
                {'collected.data.route': self.route},
                sort=[('collected.data.body.id', -1)]
            ).skip(skip).limit(count)
            if c.count == 0:
                break
            yield list(c)
            skip += count

    def get_id_period(self):
        result = env.MONGO.webpages.aggregate([
            {'$match': {
                'collected.data.route': self.route,
            }},
            {'$group': {
                '_id': 0,
                'max_id': {'$max': "$collected.data.body.id"},
                'min_id': {'$min': "$collected.data.body.id"}
            }}
        ])['result'][0]
        return result['min_id'], result['max_id']

    def save_statuses(self, template, statuses):
        rows = [copy.deepcopy(template) for i in range(len(statuses))]
        for i in range(len(rows)):
            rows[i]['collected']['data'].update({
                'body': statuses[i],
            })
        return env.MONGO.webpages.insert(rows)
