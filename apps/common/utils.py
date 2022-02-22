from datetime import timedelta
from time import monotonic, sleep


class Timer:
    """ Context manager timer """

    def __init__(self):
        self.time_start = None
        self.time_stop = None

    def __enter__(self):
        self.time_start = monotonic()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.time_stop = monotonic()

    @property
    def elapsed(self) -> timedelta:
        return timedelta(seconds=self.time_stop - self.time_start)

    @classmethod
    def sleep(cls, secs):
        return sleep(secs)