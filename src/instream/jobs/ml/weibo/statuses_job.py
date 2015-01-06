from instream.jobs.ml.ml_job import MLJob

__all__ = ['WeiboStatusesMLJob']


class WeiboStatusesMLJob(MLJob):

    def ml(self, doc):
        self.ml_categories(doc)
        self.ml_tags(doc)

    def ml_categories(self, doc):
        self.data['categories'] = []

    def ml_tags(self, doc):
        self.data['tags'] = []
