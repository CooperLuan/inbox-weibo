from instream.jobs.nlp.nlp_job import NLPJob
import jieba

__all__ = ['WeiboStatusesNLPJob']


class WeiboStatusesNLPJob(NLPJob):

    def nlp(self, doc):
        k = 'retweeted_status'
        if k in doc:
            text = doc['text'] + doc[k]['text']
        else:
            text = doc['text']
        self.data['jieba_cut'] = list(jieba.cut_for_search(text))
