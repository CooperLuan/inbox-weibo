from instream.jobs.etl.etl_job import ETLJob


class ExtractorJob(ETLJob):
    ns = 'extracted'

    def etl(self, doc):
        self.extract(doc)

    def extract(self, doc):
        raise NotImplementedError
