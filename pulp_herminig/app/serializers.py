from gettext import gettext as _

from pulpcore.plugin.serializers import RelatedField
from rest_framework.serializers import (
    BooleanField,
    FloatField,
    IntegerField,
    Serializer,
    ValidationError
)


class TaskingBenchmarkSerializer(Serializer):
    truncate_tasks = BooleanField(
        default=False,
        help_text = _(
            "If True, this will delete all final tasks from the database before dispatching."
        ),
    )
    count = IntegerField(
        default=4,
        min_value=1,
        help_text = _(
            "The number of tasks to dispatch."
        ),
    )
    resources_N = IntegerField(
        default=0,
        min_value=0,
        help_text=_(
            "The number of unique resources these tasks could require."
        ),
    )
    resources_K = IntegerField(
        default=0,
        min_value=0,
        help_text=_(
            "Randomly select K of the N resources for each task to require."
        ),
    )
    sleep_secs = FloatField(
        default=0.0,
        min_value=0.0,
        help_text=_(
            "The amount of time in seconds each task should sleep for."
        ),
    )
    failure_probability = FloatField(
        default=0.0,
        min_value=0.0,
        max_value=1.0,
        help_text=_(
            "The probability that the task will fail."
        ),
    )

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
