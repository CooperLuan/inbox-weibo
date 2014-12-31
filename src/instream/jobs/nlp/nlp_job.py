import time

from instream.jobs.job import Job
from instream import env
from instream.jobs.route import Route


class NLPJob(Job):
    ns = 'nlp'

    def __init__(self):
        Job.__init__(self)
        self.data = {}

    def run(self, _id, collection):
        self.log.info('Job %s _id %s' % (self.__class__.__name__, _id))
        self.collection = env.MONGO[collection]
        doc = self.collection.find_one({'_id': _id})
        self.nlp(doc)
        self.collection.update({
            '_id': _id,
        }, {
            '$set': {self.ns: {
                'data': self.data,
                'time': time.time(),
            }}
        })

    def gen_next_job(self, route, _id):
        Route().run(self.next_job, _id, 'webpages')
