from gettext import gettext as _

from pulpcore.plugin.serializers import RelatedField
from rest_framework.serializers import BooleanField, IntegerField, Serializer, ValidationError


class TaskingBenchmarkSerializer(Serializer):
    truncate_tasks = BooleanField(default=False)
    count = IntegerField(default=4)
    resources_N = IntegerField(default=0)
    resources_K = IntegerField(default=0)

    def validate(self, data):
        validated_data = super().validate(data)
        if validated_data["resources_K"] > validated_data["resources_N"]:
            raise ValidationError("'resources_K cannot be greater than 'resources_N'.")
        return validated_data


class TaskingBenchmarkResultSerializer(Serializer):
    count = IntegerField(read_only=True)
    dispatch_time = IntegerField(read_only=True)
    prior_tasks = IntegerField(read_only=True)
    task_group = RelatedField(
        help_text=_("The task group that contains the dispatched tasks."),
        read_only=True,
        view_name="task-groups-detail",
    )
