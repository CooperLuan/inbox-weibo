from instream.jobs.job import Job
from instream.jobs.route import Route
from instream import env
import time

__all__ = ['Scheduler']


class Scheduler(Job):
    __collection__ = 'schedules'

    def run(self, **kwargs):
        if not all(
                lambda x: x in kwargs,
                ['title', 'route', 'kwargs']):
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
        self.collection.insert(doc)
        # add task
        Route
