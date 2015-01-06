from instream.jobs.etl.loader_job import LoaderJob
__all__ = ['WeiboStatusesLoaderJob']


class WeiboStatusesLoaderJob(LoaderJob):
    next_job = 'nlp.weibo.statuses'
    required_keys = []

    def load(self, doc):
        transformed = doc['transformed']['data']
        self.data = transformed
        transformed_user = transformed.pop('user')
        transformed['user'] = {
            'source': 'weibo',
            'id': transformed_user['id'],
            'name': transformed_user['name'],
        }
        _id = self.upsert_stream(['source', 'id'], transformed)
        self.upsert_profile(['source', 'id'], transformed_user)
        self.next_job_id = _id
