"""
usage:

    bin/instream-app crawler
"""
import sys

from instream.setup_env import main as setup_main
setup_main('development.yml')
from instream.jobs.scheduler.scheduler import Scheduler as SchedulerJob
from instream.jobs.route import Route
from instream.cli.rc import get_weibo_token
from instream import env


def cleanup():
    env.MONGO.schedules.remove()
    env.MONGO.seeds.remove()
    env.MONGO.webpages.remove()


def start_scheduler():
    cleanup()
    weibo_token = get_weibo_token()
    kwargs = {
        'title': 'Weibo Statuses Crawler',
        'route': 'crawler.weibo.statuses',
        'kwargs': {
            'access_token': weibo_token['access_token'],
        },
    }
    SchedulerJob().run(**kwargs)


def start_crawler():
    _id = env.MONGO.seeds.distinct('_id')[0]
    Route().run('crawler.weibo.statuses', _id, 'seeds')


def start_etl():
    _ids = env.MONGO.webpages.distinct('_id')
    route = 'etl.extractors.weibo.statuses'
    for _id in _ids:
        Route().run(route, _id, 'webpages')


def start_nlp():
    _ids = env.MONGO.streams.distinct('_id')
    route = 'nlp.weibo.statuses'
    for _id in _ids:
        Route().run(route, _id, 'streams')


def start_ml():
    _ids = env.MONGO.streams.distinct('_id')
    route = 'ml.weibo.statuses'
    for _id in _ids:
        Route().run(route, _id, 'streams')


def main():
    try:
        step = sys.argv[1]
    except IndexError:
        print('please input step : scheduler/crawler/etl/nlp')
    func_name = 'start_%s' % step
    func = globals()[func_name]
    func()


if __name__ == '__main__':
    main()
