from celery.task import Task
from celery.utils.log import get_task_logger


class Job(Task):
    name = 'instream'
    max_retries = 3
    default_retry_delay = 10
    ignore_result = True
    store_errors_even_if_ignored = True

    def __init__(self):
        self.log = get_task_logger(__name__)
        self.log.setLevel(20)

    def run(self):
        raise NotImplementedError
