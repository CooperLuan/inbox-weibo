from instream.setup_env import main as setup_env
from instream.jobs.crawler.weibo.statuses_job import WeiboStatusesCrawlerJob


def main():
    setup_env()
    job = WeiboStatusesCrawlerJob()
    job.run()
    # job


if __name__ == '__main__':
    main()
