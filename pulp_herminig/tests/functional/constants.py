"""Constants for Pulp Herminig plugin tests."""
from urllib.parse import urljoin

from pulp_smash.constants import PULP_FIXTURES_BASE_URL
from pulp_smash.pulp3.constants import (
    BASE_DISTRIBUTION_PATH,
    BASE_PUBLICATION_PATH,
    BASE_REMOTE_PATH,
    BASE_REPO_PATH,
    BASE_CONTENT_PATH,
)

# FIXME: list any download policies supported by your plugin type here.
# If your plugin supports all download policies, you can import this
# from pulp_smash.pulp3.constants instead.
# DOWNLOAD_POLICIES = ["immediate", "streamed", "on_demand"]
DOWNLOAD_POLICIES = ["immediate"]

# FIXME: replace 'unit' with your own content type names, and duplicate as necessary for each type
HERMINIG_CONTENT_NAME = "herminig.unit"

# FIXME: replace 'unit' with your own content type names, and duplicate as necessary for each type
HERMINIG_CONTENT_PATH = urljoin(BASE_CONTENT_PATH, "herminig/units/")

HERMINIG_REMOTE_PATH = urljoin(BASE_REMOTE_PATH, "herminig/herminig/")

HERMINIG_REPO_PATH = urljoin(BASE_REPO_PATH, "herminig/herminig/")

HERMINIG_PUBLICATION_PATH = urljoin(BASE_PUBLICATION_PATH, "herminig/herminig/")

HERMINIG_DISTRIBUTION_PATH = urljoin(BASE_DISTRIBUTION_PATH, "herminig/herminig/")

# FIXME: replace this with your own fixture repository URL and metadata
HERMINIG_FIXTURE_URL = urljoin(PULP_FIXTURES_BASE_URL, "herminig/")
"""The URL to a herminig repository."""

# FIXME: replace this with the actual number of content units in your test fixture
HERMINIG_FIXTURE_COUNT = 3
"""The number of content units available at :data:`HERMINIG_FIXTURE_URL`."""

HERMINIG_FIXTURE_SUMMARY = {HERMINIG_CONTENT_NAME: HERMINIG_FIXTURE_COUNT}
"""The desired content summary after syncing :data:`HERMINIG_FIXTURE_URL`."""

# FIXME: replace this with the location of one specific content unit of your choosing
HERMINIG_URL = urljoin(HERMINIG_FIXTURE_URL, "")
"""The URL to an herminig file at :data:`HERMINIG_FIXTURE_URL`."""

# FIXME: replace this with your own fixture repository URL and metadata
HERMINIG_INVALID_FIXTURE_URL = urljoin(PULP_FIXTURES_BASE_URL, "herminig-invalid/")
"""The URL to an invalid herminig repository."""

# FIXME: replace this with your own fixture repository URL and metadata
HERMINIG_LARGE_FIXTURE_URL = urljoin(PULP_FIXTURES_BASE_URL, "herminig_large/")
"""The URL to a herminig repository containing a large number of content units."""

# FIXME: replace this with the actual number of content units in your test fixture
HERMINIG_LARGE_FIXTURE_COUNT = 25
"""The number of content units available at :data:`HERMINIG_LARGE_FIXTURE_URL`."""
