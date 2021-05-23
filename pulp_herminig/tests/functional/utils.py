"""Utilities for tests for the herminig plugin."""
from functools import partial
import requests
from unittest import SkipTest
from tempfile import NamedTemporaryFile

from pulp_smash import api, config, selectors
from pulp_smash.pulp3.utils import (
    gen_remote,
    gen_repo,
    get_content,
    require_pulp_3,
    require_pulp_plugins,
    sync,
)

from pulp_herminig.tests.functional.constants import (
    HERMINIG_CONTENT_NAME,
    HERMINIG_CONTENT_PATH,
    HERMINIG_FIXTURE_URL,
    HERMINIG_PUBLICATION_PATH,
    HERMINIG_REMOTE_PATH,
    HERMINIG_REPO_PATH,
    HERMINIG_URL,
)

from pulpcore.client.pulpcore import (
    ApiClient as CoreApiClient,
    ArtifactsApi,
    TasksApi,
)
from pulpcore.client.pulp_herminig import ApiClient as HerminigApiClient


cfg = config.get_config()
configuration = cfg.get_bindings_config()


def set_up_module():
    """Skip tests Pulp 3 isn't under test or if pulp_herminig isn't installed."""
    require_pulp_3(SkipTest)
    require_pulp_plugins({"herminig"}, SkipTest)


def gen_herminig_client():
    """Return an OBJECT for herminig client."""
    return HerminigApiClient(configuration)


def gen_herminig_remote(url=HERMINIG_FIXTURE_URL, **kwargs):
    """Return a semi-random dict for use in creating a herminig Remote.

    :param url: The URL of an external content source.
    """
    # FIXME: Add any fields specific to a herminig remote here
    return gen_remote(url, **kwargs)


def get_herminig_content_paths(repo, version_href=None):
    """Return the relative path of content units present in a herminig repository.

    :param repo: A dict of information about the repository.
    :param version_href: The repository version to read.
    :returns: A dict of lists with the paths of units present in a given repository.
        Paths are given as pairs with the remote and the local version for different content types.
    """
    # FIXME: The "relative_path" is actually a file path and name
    # It's just an example -- this needs to be replaced with an implementation that works
    # for repositories of this content type.
    return {
        HERMINIG_CONTENT_NAME: [
            (content_unit["relative_path"], content_unit["relative_path"])
            for content_unit in get_content(repo, version_href)[HERMINIG_CONTENT_NAME]
        ],
    }


def gen_herminig_content_attrs(artifact):
    """Generate a dict with content unit attributes.

    :param artifact: A dict of info about the artifact.
    :returns: A semi-random dict for use in creating a content unit.
    """
    # FIXME: Add content specific metadata here.
    return {"_artifact": artifact["pulp_href"]}


def populate_pulp(cfg, url=HERMINIG_FIXTURE_URL):
    """Add herminig contents to Pulp.

    :param pulp_smash.config.PulpSmashConfig: Information about a Pulp application.
    :param url: The herminig repository URL. Defaults to
        :data:`pulp_smash.constants.HERMINIG_FIXTURE_URL`
    :returns: A list of dicts, where each dict describes one herminig content in Pulp.
    """
    client = api.Client(cfg, api.json_handler)
    remote = {}
    repo = {}
    try:
        remote.update(client.post(HERMINIG_REMOTE_PATH, gen_herminig_remote(url)))
        repo.update(client.post(HERMINIG_REPO_PATH, gen_repo()))
        sync(cfg, remote, repo)
    finally:
        if remote:
            client.delete(remote["pulp_href"])
        if repo:
            client.delete(repo["pulp_href"])
    return client.get(HERMINIG_CONTENT_PATH)["results"]


def publish(cfg, repo, version_href=None):
    """Publish a repository.
    :param pulp_smash.config.PulpSmashConfig cfg: Information about the Pulp
        host.
    :param repo: A dict of information about the repository.
    :param version_href: A href for the repo version to be published.
    :returns: A publication. A dict of information about the just created
        publication.
    """
    if version_href:
        body = {"repository_version": version_href}
    else:
        body = {"repository": repo["pulp_href"]}

    client = api.Client(cfg, api.json_handler)
    call_report = client.post(HERMINIG_PUBLICATION_PATH, body)
    tasks = tuple(api.poll_spawned_tasks(cfg, call_report))
    return client.get(tasks[-1]["created_resources"][0])


skip_if = partial(selectors.skip_if, exc=SkipTest)  # pylint:disable=invalid-name
"""The ``@skip_if`` decorator, customized for unittest.

:func:`pulp_smash.selectors.skip_if` is test runner agnostic. This function is
identical, except that ``exc`` has been set to ``unittest.SkipTest``.
"""

core_client = CoreApiClient(configuration)
tasks = TasksApi(core_client)


def gen_artifact(url=HERMINIG_URL):
    """Creates an artifact."""
    response = requests.get(url)
    with NamedTemporaryFile() as temp_file:
        temp_file.write(response.content)
        temp_file.flush()
        artifact = ArtifactsApi(core_client).create(file=temp_file.name)
        return artifact.to_dict()
