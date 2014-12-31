from instream.jobs.etl.extractor_job import ExtractorJob
__all__ = ['WeiboStatusesExtractorJob']


class WeiboStatusesExtractorJob(ExtractorJob):
    next_job = 'etl.transformers.weibo.statuses'
    required_keys = ['id', 'text', 'created_at', 'user']

    def extract(self, doc):
        crawled = doc['collected']['data']['body']
        keys = [
            'comments_count', 'idstr', 'text', 'created_at', 'id',
            'in_reply_to_screen_name', 'in_reply_to_user_id',
            'retweeted_status',
            'in_reply_to_status_id', 'mid', 'user']
        user_keys = [
            'city', 'avatar_large', 'id', 'bi_followers_count', 'screen_name',
            'profile_url', 'idstr', 'gender', 'province', 'followers_count',
            'name', 'location']

        apply_filter = lambda data, ks: dict(list(filter(
            lambda x: x[0] in ks,
            data.items())))
        self.data = dict((k, v) for k, v in crawled.items() if k in keys)
        self.data['user'] = apply_filter(self.data['user'], user_keys)
        if 'retweeted_status' in self.data:
            key = 'retweeted_status'
            self.data[key] = apply_filter(
                self.data[key], keys)
            if 'user' in self.data[key]:
                self.data[key]['user'] = apply_filter(
                    self.data[key]['user'], user_keys)
