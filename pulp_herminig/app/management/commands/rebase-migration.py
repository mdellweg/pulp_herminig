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
        parser.add_argument("app-label", help=_("App label of the migrations to rebase."))
        parser.add_argument("migration", help=_("Prefix of the migration to rebase."))

    def handle(self, *args, **options):
        dry_run = options.get("dry_run", False)
        app_label = options["app-label"]
        migration_prefix = options["migration"]

        loader = MigrationLoader(connection)

        migration = loader.get_migration_by_prefix(app_label, migration_prefix)
        key = (app_label, migration.name)
        leaf_keys = loader.graph.leaf_nodes()
        try:
            leaf_keys.remove(key)
        except ValueError:
            raise CommandError(_("Can only rebase leaf migrations."))

        try:
            new_dependency = next((leaf_key for leaf_key in leaf_keys if leaf_key[0] == app_label))
        except StopIteration:
            raise CommandError(_("There is no leaf migration to rebase onto."))

        new_number = int(new_dependency[1][:4]) + 1
        migration.name = f"{new_number:04}{migration.name[4:]}"
        changed = False
        for i, dependency in enumerate(migration.dependencies):
            if dependency[0] == app_label:
                migration.dependencies[i] = new_dependency
                changed = True
            if changed:
                print(_("Changing migration {}").format(key))
                if not dry_run:
                    writer = MigrationWriter(migration)
                    with open(writer.path, "w") as output_file:
                        output_file.write(writer.as_string())
