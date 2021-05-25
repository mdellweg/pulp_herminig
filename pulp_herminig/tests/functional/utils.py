"""Utilities for tests for the herminig plugin."""
from functools import partial
from unittest import SkipTest

from pulp_smash import config, selectors
from pulp_smash.pulp3.utils import require_pulp_3, require_pulp_plugins
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


skip_if = partial(selectors.skip_if, exc=SkipTest)  # pylint:disable=invalid-name
"""The ``@skip_if`` decorator, customized for unittest.

:func:`pulp_smash.selectors.skip_if` is test runner agnostic. This function is
identical, except that ``exc`` has been set to ``unittest.SkipTest``.
"""
