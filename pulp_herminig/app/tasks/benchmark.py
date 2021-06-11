import logging
import random
import time

logger = logging.getLogger(__name__)

random.seed(0)  # Every time you start Pulp, make the tasking failure pattern randomly deterministic


def test_task(sleep_secs, failure_probability):
    """

    Args:
        sleep_secs: The amount of time in seconds this task should sleep for.
        failure_probability: The probability that the task will fail. This is expected to be in the
            range [0.0, 1.0].

    Returns: None

    """
    time.sleep(sleep_secs)
    if random.random() < failure_probability:
        raise Exception('This task failed')
