from django.urls import path

from pulp_herminig.app.viewsets import TaskingTestView, TaskingBenchmarkView

urlpatterns = [
    path(r"pulp/api/v3/herminig/tasking_test/", TaskingTestView.as_view()),
    path(r"pulp/api/v3/herminig/tasking_benchmark/", TaskingBenchmarkView.as_view()),
]
