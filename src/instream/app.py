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


def start_crawler():
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


def start_etl():
    _ids = env.MONGO.webpages.distinct('_id')
    route = 'etl.extractors.weibo.statuses'
    for _id in _ids:
        Route().run(route, _id, 'webpages')


def main():
    # start_crawler()
    start_etl()


if __name__ == '__main__':
    main()
