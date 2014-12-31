from instream.jobs.crawler.crawler_job import CrawlerJob


class WeiboCrawlerJob(CrawlerJob):

    def run(self, **kwargs):
        self.access_token = kwargs.pop('access_token')
