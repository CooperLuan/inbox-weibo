from dateutil.parser import parse as dt_parse

from instream.jobs.etl.transformer_job import TransformerJob
__all__ = ['WeiboStatusesTransformerJob']


class WeiboStatusesTransformerJob(TransformerJob):
    next_job = 'etl.loaders.weibo.statuses'
    required_keys = ['id', 'text', 'created_at', 'user']

    def transform(self, doc):
        extracted = doc['extracted']['data']
        self.data = extracted
        f = lambda x: dt_parse(x).timestamp()
        self.data['created_at'] = f(self.data['created_at'])
        if 'retweeted_status' in self.data:
            self.data['retweeted_status']['created_at'] = f(
                self.data['retweeted_status']['created_at'])
        self.data['source'] = 'weibo'
        self.data['user']['source'] = 'weibo'
