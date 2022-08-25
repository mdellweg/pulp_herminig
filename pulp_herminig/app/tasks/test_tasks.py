import logging
import time

import backoff

logger = logging.getLogger(__name__)


def sleep_task(sleep_secs):
    """
    Sleep for a specified amount of time.

    Args:
        sleep_secs: The amount of time in seconds this task should sleep for.

    Returns: None

    """
    time.sleep(sleep_secs)


def backoff_sleep_task(sleep_secs):
    """
    Sleep while trying to fend off exceptions.

    Args:
        sleep_secs: The amount of time in seconds this task should sleep for.

    Returns: None

    """
    backoff.on_exception(backoff.expo, ValueError, max_tries=2)(time.sleep)(sleep_secs)
