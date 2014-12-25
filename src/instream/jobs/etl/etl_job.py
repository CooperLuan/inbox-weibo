from instream.jobs.job import Job
from instream import env


class ETLJob(Job):
    ns = 'etl'

    def __init__(self, collection, _id):
        Job.__init__(self)
        self.collection = env.MONGO[collection]
        self._id = _id
        self.errs = []
        self.data = []

    def etl(self, doc):
        raise NotImplementedError

    def run(self):
        doc = self.collection.find_one({'_id': self._id})
        self.etl(doc)
        self.collection.update({
            '_id': self._id,
        }, {
            '$set': {self.ns: {
                'data': self.data,
                'errs': self.errs,
            }}
        })
