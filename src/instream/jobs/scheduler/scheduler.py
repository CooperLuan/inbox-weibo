from instream.jobs.job import Job
from instream.jobs.route import Route
from instream import env
import time

__all__ = ['Scheduler']


class Scheduler(Job):

    """
    create shcedule and first seed
    """
    __collection__ = 'schedules'

    def run(self, **kwargs):
        if not all(map(
                lambda x: x in kwargs,
                ['title', 'route', 'kwargs'])):
            raise Exception('invalid schedule %s' % kwargs)
        doc = {
            "title": kwargs.pop('title'),
            "route": kwargs.pop('route'),
            "created": time.time(),
            "incremental": kwargs.pop('incremental', False),
            "kwargs": kwargs.pop('kwargs'),
        }
        if doc['title'] in self.collection.distinct('title'):
            raise Exception('Existed schedule title %s' % doc['title'])
        _id = self.collection.insert(doc)
        doc_seed = {
            "_scheduleId": _id,
            "_status": None,
            "_seedId": None,
            "_ancestors": [],
            "route": doc['route'],
            "incremental": doc['incremental'],
            "created": time.time(),
            "updated": time.time(),
            "kwargs": doc['kwargs']
        }
        _id = env.MONGO.seeds.insert(doc_seed)
        Route().run(doc['route'], _id, 'seeds')
