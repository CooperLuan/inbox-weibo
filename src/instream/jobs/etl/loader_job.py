from instream.jobs.etl.etl_job import ETLJob
from instream import env
from instream.jobs.route import Route


class LoaderJob(ETLJob):
    ns = 'loaded'

    def etl(self, doc):
        self.load(doc)

    def load(self, doc):
        raise NotImplementedError

    def upsert_stream(self, keys, doc):
        resp = env.MONGO.streams.find_and_modify(
            dict((k, doc[k]) for k in keys), {
                '$set': doc
            }, upsert=True, full_response=True)
        if resp['value'] is None:
            return resp['lastErrorObject']['upserted']
        else:
            return resp['value']['_id']

    def upsert_profile(self, keys, doc):
        resp = env.MONGO.profiles.find_and_modify(
            dict((k, doc[k]) for k in keys), {
                '$set': doc
            }, upsert=True, full_response=True)
        if resp['value'] is None:
            return resp['lastErrorObject']['upserted']
        else:
            return resp['value']['_id']

    def gen_next_job(self, route, _id):
        Route().run(self.next_job, _id, 'streams')
