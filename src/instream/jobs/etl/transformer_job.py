from instream.jobs.etl.etl_job import ETLJob


class TransformerJob(ETLJob):
    ns = 'transformed'

    def etl(self, doc):
        self.transform(doc)

    def transform(self, doc):
        raise NotImplementedError
