import random
import time

from drf_spectacular.utils import extend_schema
from pulpcore.plugin.constants import TASK_FINAL_STATES
from pulpcore.plugin.models import Task, TaskGroup
from pulpcore.plugin.tasking import dispatch
from rest_framework.response import Response
from rest_framework.views import APIView

from . import models, serializers, tasks


class TaskingBenchmarkView(APIView):
    @extend_schema(
        request=serializers.TaskingBenchmarkSerializer,
        description="Benchmark the task queueing.",
        responses={200: serializers.TaskingBenchmarkResultSerializer},
    )
    def post(self, request):
        serializer = serializers.TaskingBenchmarkSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        truncate_tasks = serializer.validated_data["truncate_tasks"]
        count = serializer.validated_data["count"]
        resources = [f"herminig_{i}" for i in range(serializer.validated_data["resources_N"])]
        resources_K = serializer.validated_data["resources_K"]
        # Define the state of the tasking table before starting
        if truncate_tasks:
            Task.objects.filter(state__in=TASK_FINAL_STATES).delete()
        prior_tasks = Task.objects.count()
        # create a task_group to collect all tasks for this run
        task_group = TaskGroup(description="Tasking system benchmark tasks")
        task_group.save()
        # start the test
        before = time.perf_counter_ns()
        for i in range(count):
            dispatch(tasks.noop, random.choices(resources, k=resources_K), task_group=task_group)
        after = time.perf_counter_ns()
        task_group.finish()
        # --------------
        # Collect and return results

        benchmark_result = models.TaskingBenchmarkResult(
            count, after - before, prior_tasks, task_group
        )
        response_serializer = serializers.TaskingBenchmarkResultSerializer(
            benchmark_result, context={"request": request}
        )
        return Response(data=response_serializer.data, status=200)
