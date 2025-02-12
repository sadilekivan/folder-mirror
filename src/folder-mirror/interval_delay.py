import time
import logging

class IntervalDelay:
    """
        Will sleep for interval duration **since** last time slept.
        If time `elapsed_t` is larger than `interval` skip sleeping.
    """
    def __init__(self, interval: float):
        self.interval = interval
        self.last_slept_t = time.time()

    def sleep(self):
        log = logging.getLogger(__name__)
        elapsed_t = time.time() - self.last_slept_t
        sleep_t = self.interval - elapsed_t
        if sleep_t > 0:
            log.debug(f"{self.interval} second interval delay, sleep for {sleep_t:.2f} seconds")
            time.sleep(sleep_t)
        self.last_slept_t = time.time()