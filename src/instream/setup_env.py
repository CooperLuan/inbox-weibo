import argparse

import pymongo
import yaml
from celery import Celery
from redis import StrictRedis
import jieba

from instream import env


def setup_db(d):
    mongo_url = d['mongo_url']
    db = mongo_url.split('/')[3]
    env.MONGO = pymongo.MongoClient(mongo_url)[db]
    env.REDIS = StrictRedis.from_url(d['redis_url'])

    for collection, fields in d['mongo_indexes'].items():
        for field in fields:
            env.MONGO[collection].ensure_index(field)


def setup_celery(d):
    env.APP_CELERY = Celery('tasks', **d)


def setup_jieba():
    jieba.initialize()


def setup(d):
    setup_db(d)
    setup_celery(d['celery'])
    setup_jieba()


def main(config=None):
    if config is None:
        parser = argparse.ArgumentParser(description="InboxStream")
        parser.add_argument('config', type=str,
                            help="Configuration file")

        args = parser.parse_args()
        config = args.config

    setup(yaml.load(open(config).read()))


if __name__ == '__main__':
    main()
