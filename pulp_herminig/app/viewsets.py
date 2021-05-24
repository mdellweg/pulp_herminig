import time
from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from rest_framework.views import APIView

from pulpcore.plugin.serializers import AsyncOperationResponseSerializer
from pulpcore.plugin.viewsets import OperationPostponedResponse
from pulpcore.plugin.tasking import dispatch

from . import models, serializers, tasks


class TaskingBenchmarkView(APIView):
    @extend_schema(
        request=serializers.TaskingBenchmarkSerializer,
        description="Trigger an asynchronous task to benchmark the task queueing.",
        responses={
            200: serializers.TaskingBenchmarkResultSerializer,
            202: AsyncOperationResponseSerializer,
        },
    )
    def post(self, request):
        serializer = serializers.TaskingBenchmarkSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        background = serializer.validated_data["background"]
        count = serializer.validated_data["count"]
        if background:
            task = dispatch(tasks.benchmark_tasking, ["benchmark_tasking"], kwargs={"count": count})
            return OperationPostponedResponse(task, request)
        else:
            before = time.perf_counter_ns()
            for i in range(count):
                dispatch(tasks.noop, [])
            after = time.perf_counter_ns()

            benchmark_result = models.TaskingBenchmarkResult(count, after - before)
            response_serializer = serializers.TaskingBenchmarkResultSerializer(benchmark_result)
            return Response(data=response_serializer.data, status=200)
