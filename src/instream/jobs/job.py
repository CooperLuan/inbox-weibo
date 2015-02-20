import logging
formatter = '%(asctime)-15s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(level=logging.INFO, format=formatter)

from celery.task import Task
from celery.utils.log import get_task_logger

from instream import env


class Job(Task):
    name = 'instream'
    max_retries = 3
    default_retry_delay = 10
    ignore_result = True
    store_errors_even_if_ignored = True
    __collection__ = 'job'

    def __init__(self):
        self.log = get_task_logger(__name__)
        self.log.setLevel(20)
        self.collection = env.MONGO[self.__collection__]

    def run(self):
        raise NotImplementedError
