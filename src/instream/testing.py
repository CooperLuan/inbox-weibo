import unittest
from instream.setup_env import setup
from instream import env


class BaseTestCase(unittest.TestCase):

    settings = {
        'mongo_url': 'mongodb://localhost:27017/instream',
        'redis_url': 'redis://@localhost:6379/9',
        'celery': {
            'BROKER_URL': 'redis://localhost/9',
            'CELERY_RESULT_BACKEND': 'redis://localhost/9',
            'CELERY_TASK_SERIALIZER': 'json',
            'CELERY_RESULT_SERIALIZER': 'json',
            'CELERY_ACCEPT_CONTENT': ['json'],
            'CELERY_TIMEZONE': 'Asia/Shanghai',
            'CELERY_ENABLE_UTC': True,
        },
        'mongo_indexes': {
            'schedules': ['title', 'route'],
            'seeds': ['_scheduleId', 'route'],
            'webpages': ['collected.data.route', 'scheduled._scheduleId', 'collected.time'],
            'streams': ['souce', 'id', 'ml.data.tags', 'ml.data.categories', 'created_at'],
            'profiles': ['id', 'name'],
        }
    }

    def setUp(self):
        setup(self.settings)

    def tearDown(self):
        env.REDIS.flushdb()
