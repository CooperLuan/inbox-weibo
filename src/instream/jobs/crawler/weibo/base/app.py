"""
#author:    @Cooper
#weibo:     http://weibo.com/gsavl
#date:      2014.6.2

save weibo data to MongoDB
oauth url:
https://api.weibo.com/oauth2/authorize?client_id=3349407943&response_type=code&redirect_uri=http://weibo.cooper.me/oauth
"""
import logging
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
import requests

from instream import env
from instream.jobs.crawler.weibo.base.api import WeiboAPI
from instream.jobs.crawler.weibo.base.models import StatusesModel


def oauth():
    host = 'https://api.weibo.com/oauth2/access_token'
    data = {
        'code': 'afe8006ecf84af98f22dceb58eb78f67',
        'client_id': '3349407943',
        'client_secret': 'd52c9f244993ad6b4c551a170f04bc85',
        'grant_type': 'authorization_code',
        'redirect_uri': 'http://weibo.cooper.me/oauth',
    }
    resp = requests.post(host, data=data)
    return resp.json()


class StatusesRobot(object):

    def __init__(self, access_token):
        self.access_token = access_token
        self.since_id = self.get_since_id() or 0
        self.max_id = 0
        self.model_statuses = StatusesModel()
        self.api = WeiboAPI(access_token=self.access_token)

    def get_since_id(self):
        since_id = self.model_statuses.get_statuses(count=1)
        return since_id and since_id['id'] or None

    def fetch_new(self):
        count = 100
        page = 1
        trim_user = 0
        while 1:
            log.info('fetch new from %s page %s' % (self.since_id, page))
            resp = self.api.statuses_friends_timeline(
                since_id=self.since_id, max_id=self.max_id,
                count=count, page=page,
                trim_user=trim_user)
            page += 1
            if resp['statuses']:
                yield resp['statuses']
            else:
                break

    def failover(self):
        env.MONGO.statuses.remove({
            'id': {'$gt': self.since_id}
        })

    def run(self):
        try:
            for resp in self.fetch_new() or []:
                self.model_statuses.save_statuses(resp)
        except Exception as e:
            log.error(e)
            log.warning('roll back')
            self.failover()
            log.warning('please run again')
