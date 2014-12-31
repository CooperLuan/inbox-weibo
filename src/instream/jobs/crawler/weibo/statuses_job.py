import time
import re
import traceback

from instream import env
from instream.jobs.crawler.weibo.base.api import WeiboAPI
from instream.jobs.crawler.weibo.base.models import StatusesModel
from instream.jobs.crawler.crawler_weibo_job import WeiboCrawlerJob
from instream.jobs.route import Route

__all__ = ['WeiboStatusesCrawlerJob']


class WeiboStatusesCrawlerJob(WeiboCrawlerJob):

    """
    TODO
    将 request 和 storage 分开
    OO化
    """

    def __init__(self):
        WeiboCrawlerJob.__init__(self)

    def _get_since_id(self):
        since_id = self.model_statuses.get_statuses(count=1)
        try:
            return next(since_id)[0]['id']
        except (IndexError, StopIteration):
            pass
        except Exception as e:
            self.log.warning(e)

    def _fetch_new(self, since_id):
        count = 100
        page = 1
        trim_user = 0
        while 1:
            self.log.info('fetch new from %s page %s' % (since_id, page))
            resp = self.api.statuses_friends_timeline(
                since_id=since_id, max_id=self.max_id,
                count=count, page=page,
                trim_user=trim_user)
            page += 1
            if resp['statuses']:
                yield resp['statuses']
            else:
                break

    def _failover(self):
        env.MONGO.weibo_statuses.remove({
            'id': {'$gt': self.since_id}
        })

    def run(self, _id, collection):
        seed = env.MONGO[collection].find_one({'_id': _id})
        kwargs = seed.pop('kwargs', {})

        self.model_statuses = StatusesModel()
        self.access_token = kwargs.pop('access_token')
        self.since_id = self._get_since_id() or 0
        self.max_id = 0
        self.api = WeiboAPI(access_token=self.access_token)

        webpage_template = {
            '_seed': {
                '_scheduleId': seed['_scheduleId'],
                '_seedId': seed['_id'],
            },
            'collected': {
                'time': time.time(),
                'errs': [],
                'data': {
                    'route': seed['route'],
                    'body': None,
                }
            }
        }
        next_route = re.sub(r'crawler\.', r'etl.extractors.', seed['route'])
        self.log.info('start crawl weibo statuses from %s' % self.since_id)
        next_job_ids = []
        try:
            for resp in self._fetch_new(self.since_id) or []:
                _ids = self.model_statuses.save_statuses(
                    webpage_template, resp)
                next_job_ids.extend(_ids)
        except:
            self.log.error(traceback.format_exc())
            self.log.warning('roll back')
            self._failover()
            self.log.warning('please run again')
        for _id in next_job_ids:
            self.gen_next_job(next_route, _id)

    def gen_next_job(self, next_route, _id):
        Route().run(next_route, _id, 'webpages')
