from instream.testing import BaseTestCase
from instream.jobs.crawler.weibo.base.models import StatusesModel


class StatusesModelTestCase(BaseTestCase):
    def test_get_id_period(self):
        model = StatusesModel()
        result = model.get_id_period()
        self.assertEqual(result, ())
