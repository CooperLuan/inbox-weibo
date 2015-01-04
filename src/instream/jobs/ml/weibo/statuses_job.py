from instream.jobs.ml.ml_job import MLJob

__all__ = ['WeiboStatusesMLJob']


class WeiboStatusesMLJob(MLJob):

    def ml(self, doc):
        self.data['category'] = None
        self.data['tags'] = []
