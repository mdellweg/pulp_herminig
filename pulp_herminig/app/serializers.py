from rest_framework.serializers import Serializer, IntegerField, BooleanField


class TaskingBenchmarkSerializer(Serializer):
    background = BooleanField(default=False)
    count = IntegerField(default=4)


class TaskingBenchmarkResultSerializer(Serializer):
    count = IntegerField()
    dispatch_time = IntegerField()
