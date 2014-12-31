import importlib

from .job import Job
from instream import env


class Route(Job):

    def run(self, route, _id, collection):
        """
        @route str : crawler.weibo.statuses
        """
        # doc = env.MONGO[collection].find_one({'_id': _id})
        # kwargs = doc.pop('kwargs', {})
        module_path = 'instream.jobs.' + route + '_job'
        module = importlib.import_module(module_path)
        job_class = getattr(module, module.__all__[0])
        # route_parts = route.split('.')
        # job_class().apply_async((_id, collection), queue=route_parts[0])
        job_class().run(_id, collection)
