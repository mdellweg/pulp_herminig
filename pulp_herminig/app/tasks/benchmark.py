import logging
import time

from pulpcore.plugin.models import Task
from pulpcore.plugin.tasking import dispatch

log = logging.getLogger(__name__)


def noop():
    pass


def sleep(sec):
    time.sleep(sec)
