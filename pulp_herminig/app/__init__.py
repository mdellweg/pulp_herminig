from pulpcore.plugin import PulpPluginAppConfig


class PulpHerminigPluginAppConfig(PulpPluginAppConfig):
    """Entry point for the herminig plugin."""

    name = "pulp_herminig.app"
    label = "herminig"
    version = "0.1.0a1.dev"
