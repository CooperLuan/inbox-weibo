import importlib

from .job import Job
from instream import env


class Route(Job):

    def run(self, route, _id, collection):
        """
        @route str : crawler.weibo.statuses
        """
        doc = env.MONGO[collection].find_one({'_id': _id})
        kwargs = doc.pop('kwargs', {})
        module_path = 'instream.jobs.' + route + '_job'
        route_parts = route.split('.')
        module = importlib.import_module(module_path)
        job_class = getattr(module, module.__all__[0])
        job_class().apply_async(kwargs=kwargs, queue=route_parts[0])
