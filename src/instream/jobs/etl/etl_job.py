import time

from instream.jobs.job import Job
from instream import env
from instream.jobs.route import Route


class ETLJob(Job):
    ns = 'etl'
    next_job = None
    required_keys = []

    def __init__(self):
        Job.__init__(self)
        self.errs = []
        self.data = []
        self.ok = False

    def etl(self, doc):
        raise NotImplementedError

    def run(self, _id, collection):
        self.log.info('Job %s _id %s' % (self.__class__.__name__, _id))
        self.collection = env.MONGO[collection]
        doc = self.collection.find_one({'_id': _id})
        self.etl(doc)
        self.ok = self.is_ok()
        self.collection.update({
            '_id': _id,
        }, {
            '$set': {self.ns: {
                'data': self.data,
                'errs': self.errs,
                'time': time.time(),
                'ok': self.ok,
            }}
        })
        if self.ok:
            self.gen_next_job(self.next_job, getattr(self, 'next_job_id', _id))

    def is_ok(self):
        return all(map(lambda x: x in self.data, self.required_keys))

    def gen_next_job(self, route, _id):
        Route().run(self.next_job, _id, 'webpages')
