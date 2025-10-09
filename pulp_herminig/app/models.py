from collections import namedtuple
from logging import getLogger

logger = getLogger(__name__)


TaskingTestResult = namedtuple("TaskingBenchmarkResult", ["count", "task_group"])


TaskingBenchmarkResult = namedtuple(
    "TaskingBenchmarkResult", ["count", "resources_n", "resources_k", "dispatch_time", "prior_tasks", "task_group"]
)
