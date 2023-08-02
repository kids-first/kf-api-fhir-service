import time

import requests

from src.config import (
    BASE_URL,
)


def elapsed_time_hms(start_time):
    """
    Get time elapsed since start_time in hh:mm:ss str format
    """
    elapsed = time.time() - start_time
    return time.strftime('%H:%M:%S', time.gmtime(elapsed))


