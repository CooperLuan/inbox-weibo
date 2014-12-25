import argparse

import pymongo
import yaml
from celery import Celery
from redis import StrictRedis

from instream import env


def setup_db(d):
    mongo_url = d['mongo_url']
    db = mongo_url.split('/')[3]
    env.MONGO = pymongo.MongoClient(mongo_url)[db]
    env.REDIS = StrictRedis.from_url(d['redis_url'])

    for coll_name, fields in {
        'weibo_statuses': ['id', 'mid'],
    }.items():
        for field in fields:
            env.MONGO[coll_name].ensure_index(field)


def setup_celery(d):
    env.APP_CELERY = Celery('tasks', **d)


def setup(d):
    setup_db(d)
    setup_celery(d['celery'])


def main():
    parser = argparse.ArgumentParser(description="InboxStream")
    parser.add_argument('config', type=str,
                        help="Configuration file")

    args = parser.parse_args()

    setup(yaml.load(open(args.config).read()))


if __name__ == '__main__':
    main()
