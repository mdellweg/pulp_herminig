from django.conf.urls import url

from pulp_herminig.app.viewsets import TaskingBenchmarkView

urlpatterns = [
    url(r"pulp/api/v3/herminig/tasking_benchmark/", TaskingBenchmarkView.as_view()),
]
