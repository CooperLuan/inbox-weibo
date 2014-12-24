import argparse

import pymongo
import yaml
from celery import Celery

import env


def setup_db(d):
    mongo_url = d['mongo_url']
    db = mongo_url.split('/')[3]
    env.MONGO = pymongo.MongoClient(mongo_url)[db]


def setup_celery(d):
    env.APP_CELERY = Celery('tasks', **d)


def setup(conf_path):
    conf = yaml.load(conf_path)
    setup_db(conf)
    setup_celery(conf['celery'])


def main():
    parser = argparse.ArgumentParser(description="InboxStream")
    parser.add_argument('config', metavar="<yml-file>", type=str,
                        help="Configuration file")

    args = parser.parse_args()

    setup(args.config)


if __name__ == '__main__':
    main()
