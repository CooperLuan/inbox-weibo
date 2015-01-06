import re
from subprocess import Popen, PIPE, STDOUT

import jieba

from instream.jobs.nlp.nlp_job import NLPJob
from instream import env

__all__ = ['WeiboStatusesNLPJob']


class WeiboStatusesNLPJob(NLPJob):
    next_job = 'ml.weibo.statuses'

    def nlp(self, doc):
        text = self._extract_text(doc)
        self.nlp_jieba_cut(text)
        self.nlp_ictclas_cut(text)

    def nlp_jieba_cut(self, text):
        stop_words = '。，？：@—,、！![]【】《》“”.…#~ '
        self.data['jieba_cut'] = list(filter(
            lambda x: x.strip(stop_words),
            jieba.cut_for_search(text)))

    def nlp_ictclas_cut(self, text):
        p = Popen(
            ['cd %s; python2 ictclas_py.py "%s"' % (
                env.CONF['ictclas'], text)],
            stdout=PIPE, stdin=PIPE, stderr=STDOUT, shell=True)
        p_stdout = p.communicate()[0].decode(errors='ignore').splitlines()
        self.data['ictclas_cut'] = [
            line.split('\t')
            for line in p_stdout
            if len(line.split('\t')) == 3]

    def _extract_text(self, doc):
        k = 'retweeted_status'
        if k in doc:
            text = doc['text'] + doc[k]['text']
        else:
            text = doc['text']
        text = re.sub(r'http://\S+', r'', text, re.S)
        text = re.sub(r'#.+?#', r'', text, re.S)
        return text
