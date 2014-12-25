from instream.jobs.etl.etl_job import ETLJob


class LoaderJob(ETLJob):
    ns = 'loaded'

    def etl(self, doc):
        self.load(doc)

    def load(self, doc):
        raise NotImplementedError
