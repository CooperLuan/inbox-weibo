"""
文本分类应该用统计方法来做
暂时先用关键词的方法做
"""
from instream.jobs.ml.ml_job import MLJob

__all__ = ['WeiboStatusesMLJob']


class WeiboStatusesMLJob(MLJob):

    def ml(self, doc):
        self.doc = doc
        self.ml_categories(doc)
        self.ml_tags(doc)

    def ml_categories(self, doc):
        """
        - Shopping
        - Technology
        - History
        - Science
        - English
        - Inspiring
        - Bad
        - Sports
        - Education
        - Relaxing
        """
        _buildin_cats = [
            'Shopping', 'Technology', 'History', 'Science', 'English',
            'Inspiring', 'Bad', 'Sports', 'Education', 'Relaxing']
        self.data['categories'] = list(filter(
            lambda x: getattr(self, 'ml_is_%s' % x.lower())(),
            _buildin_cats))

    def ml_is_shopping(self):
        """
        海淘/直邮
        亚马逊
        """
        keywords = '亚马逊'.split('.')
        if self._is_in_user_name(keywords):
            return True
        keywords = ['海淘', '直邮']
        if self._is_in_text(keywords):
            return True
        return False

    def ml_is_technology(self):
        """
        - program languages
        - Google/索尼/微软/苹果/Apple/facebook/三星
        - sdk/开发
        - HN/Hack
        - iOS/数据/分析
        - Solidot
        """
        program_languages = [
            'c++', 'c#', 'java', 'php', 'python',
            'ruby', 'go', 'lua', 'lisp', 'javascript',
            'angular', 'css', 'html', 'js']
        if self._is_in_text(program_languages):
            return True
        companies = 'Google/索尼/微软/苹果/Apple/facebook/三星'.split('/')
        if self._is_in_text(companies):
            return True
        keywords = 'sdk,开发,HN,Hack,iOS,数据,分析'.split(',')
        if self._is_in_text(keywords):
            return True
        names = 'Solidot'.split(',')
        if self._is_in_user_name(names):
            return True
        return False

    def ml_is_history(self):
        """
        - 国学
        - 忆闻官微
        """
        keywords = '国学,王国维,曾国藩'.split(',')
        if self._is_in_text(keywords):
            return True
        keywords = '忆闻官微'.split(',')
        if self._is_in_user_name(keywords):
            return True
        return False

    def ml_is_science(self):
        """
        - NASA/Space
        - 果壳
        - TED
        """
        keywords = 'NASA/Space/果壳/TED'.split('/')
        return self._is_in_text(keywords) or self._is_in_user_name(keywords)

    def ml_is_english(self):
        """
        - 英语
        """
        keywords = '英语'.split('/')
        return self._is_in_user_name(keywords)

    def ml_is_inspiring(self):
        """
        - 一辈子
        - 赋予
        - 母亲
        - 深爱
        - 跑步
        """
        keywords = '一辈子/赋予/母亲/深爱/跑步'.split('/')
        return self._is_in_text(keywords)

    def ml_is_bad(self):
        """
        - 负面
        - 不尊重
        """
        keywords = '负面/不尊重'.split('/')
        return self._is_in_text(keywords)

    def ml_is_sports(self):
        """
        - 利物浦
        - 足球/篮球
        - NBA
        """
        keywords = '利物浦/足球/篮球/NBA'.split('/')
        return self._is_in_text(keywords)

    def ml_is_education(self):
        """
        - 孩子
        - 教育
        """
        keywords = '孩子/教育'.split('/')
        return self._is_in_text(keywords)

    def ml_is_relaxing(self):
        """
        - 旅行
        - 旅游
        - 青旅
        - 穷游
        """
        keywords = '旅游/旅行/青旅/穷游'.split('/')
        return self._is_in_text(keywords)

    def _is_in_text(self, keywords):
        if any(filter(
                lambda x: x.lower() in self.doc['text'].lower(),
                keywords)):
            return True
        return False

    def _is_in_user_name(self, keywords):
        if any(filter(
                lambda x: x.lower() in self.doc['user']['name'].lower(),
                keywords)):
            return True
        return False

    def ml_tags(self, doc):
        self.data['tags'] = []
