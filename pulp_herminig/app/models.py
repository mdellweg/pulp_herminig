from collections import namedtuple
from logging import getLogger


logger = getLogger(__name__)


TaskingBenchmarkResult = namedtuple("TaskingBenchmarkResult", ["count", "dispatch_time"])
