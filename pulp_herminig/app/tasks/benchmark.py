import logging
import time

from pulpcore.plugin.models import Task
from pulpcore.plugin.tasking import dispatch


log = logging.getLogger(__name__)


def noop():
    pass


def sleep(sec):
    time.sleep(sec)


def benchmark_tasking(count=8):
    """
    Dispatch a number of tasks.

    Args:
        count (int): Number of tasks to dispatch
    """
    log.info("Starting tasking system benchmark.")
    prior_tasks = Task.objects.count()
    log.info("Prior existing tasks: {}".format(prior_tasks))
    before = time.perf_counter_ns()
    for i in range(count):
        dispatch(noop, [])
    after = time.perf_counter_ns()
    log.info("Dispatching {} tasks took {} ns.".format(count, after - before))
    log.info("Finished tasking system benchmark.")
