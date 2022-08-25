from gettext import gettext as _
import json
import sys

from django.db import connection
from django.db.migrations.loader import MigrationLoader
from django.db.migrations.writer import MigrationWriter
from django.core.management import BaseCommand, CommandError


class Command(BaseCommand):
    """
    Django management command to adjust migration dependencies on core.
    """

    help = _("Adjust migration dependencies on a core migration.")

    def add_arguments(self, parser):
        parser.add_argument("--dry-run", action="store_true", help=_("Don't change anything."))
        parser.add_argument("app-label", help=_("App label of the migrations to rewire."))
        parser.add_argument("dependency-app-label", help=_("App label of the dependency."))
        parser.add_argument("dependency-migration", help=_("Prefix of the dependency migration."))

    def handle(self, *args, **options):
        dry_run = options.get("dry_run", False)
        app_label = options["app-label"]
        dependency_app_label = options["dependency-app-label"]
        dependency_migration_prefix = options["dependency-migration"]

        loader = MigrationLoader(connection)

        dependency_migration = loader.get_migration_by_prefix(
            dependency_app_label, dependency_migration_prefix
        )
        new_dependency = (dependency_app_label, dependency_migration.name)

        # Calculate list of replaceable dependencies
        node = loader.graph.node_map[new_dependency]
        ancestors = node.parents
        replaceable_dependencies = set()
        while ancestors:
            node = ancestors.pop()
            if node.key[0] == dependency_app_label:
                replaceable_dependencies.add(node.key)
            ancestors.update(node.parents)

        for key, migration in loader.disk_migrations.items():
            changed = False
            if key[0] == app_label:
                for i, dependency in enumerate(migration.dependencies):
                    if dependency in replaceable_dependencies:
                        migration.dependencies[i] = new_dependency
                        changed = True
            if changed:
                print(_("Changing migration {}").format(key))
                if not dry_run:
                    writer = MigrationWriter(migration)
                    with open(writer.path, "w") as output_file:
                        output_file.write(writer.as_string())
