"""
Check `Plugin Writer's Guide`_ for more details.

.. _Plugin Writer's Guide:
    http://docs.pulpproject.org/en/3.0/nightly/plugins/plugin-writer/index.html
"""

from django.db import transaction
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from pulpcore.plugin.viewsets import RemoteFilter
from pulpcore.plugin import viewsets as core
from pulpcore.plugin.actions import ModifyRepositoryActionMixin
from pulpcore.plugin.serializers import (
    AsyncOperationResponseSerializer,
    RepositorySyncURLSerializer,
)
from pulpcore.plugin.tasking import dispatch
from pulpcore.plugin.models import ContentArtifact

from . import models, serializers, tasks


class HerminigContentFilter(core.ContentFilter):
    """
    FilterSet for HerminigContent.
    """

    class Meta:
        model = models.HerminigContent
        fields = [
            # ...
        ]


class HerminigContentViewSet(core.ContentViewSet):
    """
    A ViewSet for HerminigContent.

    Define endpoint name which will appear in the API endpoint for this content type.
    For example::
        http://pulp.example.com/pulp/api/v3/content/herminig/units/

    Also specify queryset and serializer for HerminigContent.
    """

    endpoint_name = "herminig"
    queryset = models.HerminigContent.objects.all()
    serializer_class = serializers.HerminigContentSerializer
    filterset_class = HerminigContentFilter

    @transaction.atomic
    def create(self, request):
        """
        Perform bookkeeping when saving Content.

        "Artifacts" need to be popped off and saved indpendently, as they are not actually part
        of the Content model.
        """
        raise NotImplementedError("FIXME")
        # This requires some choice. Depending on the properties of your content type - whether it
        # can have zero, one, or many artifacts associated with it, and whether any properties of
        # the artifact bleed into the content type (such as the digest), you may want to make
        # those changes here.

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # A single artifact per content, serializer subclasses SingleArtifactContentSerializer
        # ======================================
        # _artifact = serializer.validated_data.pop("_artifact")
        # # you can save model fields directly, e.g. .save(digest=_artifact.sha256)
        # content = serializer.save()
        #
        # if content.pk:
        #     ContentArtifact.objects.create(
        #         artifact=artifact,
        #         content=content,
        #         relative_path= ??
        #     )
        # =======================================

        # Many artifacts per content, serializer subclasses MultipleArtifactContentSerializer
        # =======================================
        # _artifacts = serializer.validated_data.pop("_artifacts")
        # content = serializer.save()
        #
        # if content.pk:
        #   # _artifacts is a dictionary of {"relative_path": "artifact"}
        #   for relative_path, artifact in _artifacts.items():
        #       ContentArtifact.objects.create(
        #           artifact=artifact,
        #           content=content,
        #           relative_path=relative_path
        #       )
        # ========================================

        # No artifacts, serializer subclasses NoArtifactContentSerialier
        # ========================================
        # content = serializer.save()
        # ========================================

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class HerminigRemoteFilter(RemoteFilter):
    """
    A FilterSet for HerminigRemote.
    """

    class Meta:
        model = models.HerminigRemote
        fields = [
            # ...
        ]


class HerminigRemoteViewSet(core.RemoteViewSet):
    """
    A ViewSet for HerminigRemote.

    Similar to the HerminigContentViewSet above, define endpoint_name,
    queryset and serializer, at a minimum.
    """

    endpoint_name = "herminig"
    queryset = models.HerminigRemote.objects.all()
    serializer_class = serializers.HerminigRemoteSerializer


class HerminigRepositoryViewSet(core.RepositoryViewSet, ModifyRepositoryActionMixin):
    """
    A ViewSet for HerminigRepository.

    Similar to the HerminigContentViewSet above, define endpoint_name,
    queryset and serializer, at a minimum.
    """

    endpoint_name = "herminig"
    queryset = models.HerminigRepository.objects.all()
    serializer_class = serializers.HerminigRepositorySerializer

    # This decorator is necessary since a sync operation is asyncrounous and returns
    # the id and href of the sync task.
    @extend_schema(
        description="Trigger an asynchronous task to sync content.",
        summary="Sync from remote",
        responses={202: AsyncOperationResponseSerializer},
    )
    @action(detail=True, methods=["post"], serializer_class=RepositorySyncURLSerializer)
    def sync(self, request, pk):
        """
        Dispatches a sync task.
        """
        repository = self.get_object()
        serializer = RepositorySyncURLSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        remote = serializer.validated_data.get("remote")

        result = dispatch(
            tasks.synchronize,
            [repository, remote],
            kwargs={"remote_pk": str(remote.pk), "repository_pk": str(repository.pk)},
        )
        return core.OperationPostponedResponse(result, request)


class HerminigRepositoryVersionViewSet(core.RepositoryVersionViewSet):
    """
    A ViewSet for a HerminigRepositoryVersion represents a single
    Herminig repository version.
    """

    parent_viewset = HerminigRepositoryViewSet


class HerminigPublicationViewSet(core.PublicationViewSet):
    """
    A ViewSet for HerminigPublication.

    Similar to the HerminigContentViewSet above, define endpoint_name,
    queryset and serializer, at a minimum.
    """

    endpoint_name = "herminig"
    queryset = models.HerminigPublication.objects.exclude(complete=False)
    serializer_class = serializers.HerminigPublicationSerializer

    # This decorator is necessary since a publish operation is asyncrounous and returns
    # the id and href of the publish task.
    @extend_schema(
        description="Trigger an asynchronous task to publish content",
        responses={202: AsyncOperationResponseSerializer},
    )
    def create(self, request):
        """
        Publishes a repository.

        Either the ``repository`` or the ``repository_version`` fields can
        be provided but not both at the same time.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        repository_version = serializer.validated_data.get("repository_version")

        result = dispatch(
            tasks.publish,
            [repository_version.repository],
            kwargs={"repository_version_pk": str(repository_version.pk)},
        )
        return core.OperationPostponedResponse(result, request)


class HerminigDistributionViewSet(core.DistributionViewSet):
    """
    A ViewSet for HerminigDistribution.

    Similar to the HerminigContentViewSet above, define endpoint_name,
    queryset and serializer, at a minimum.
    """

    endpoint_name = "herminig"
    queryset = models.HerminigDistribution.objects.all()
    serializer_class = serializers.HerminigDistributionSerializer
