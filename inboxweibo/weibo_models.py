import env


class BaseModel(object):

    def __init__(self):
        pass


class StatusesModel(BaseModel):

    def get_statuses(self, count=50):
        skip = 0
        while 1:
            c = env.MONGO.statuses.find(
                sort=[('id', -1)]
            ).skip(skip).limit(count)
            if c.count == 0:
                break
            yield c
            skip += count

    def get_id_period(self):
        result = env.MONGO.statuses.aggregate({
            '$group': {
                '_id': 0,
                'max_id': {'$max': "$id"},
                'min_id': {'$min': "$id"}
            },
        })['result'][0]
        return result['min_id'], result['max_id']

    def save_statuses(self, statuses):
        env.MONGO.statuses.insert(statuses)
