import logging
from django.contrib.staticfiles.management.commands import runserver

logger = logging.getLogger(__name__)


def setup_test_data():
    from django.contrib.auth.models import User

    User.objects.create_superuser(
        username="root",
        email="",
        password="pa55w0rt",
        first_name="Max",
        last_name="Mustermann",
    )


class Command(runserver.Command):
    help = "Runs the server with test data"

    def add_arguments(self, parser):
        super().add_arguments(parser)

        # Named (optional) arguments
        parser.add_argument(
            "--skip_app_database_migration",
            action="store_true",
            help="Don't migrate and flush app database on startup",
        )
        parser.add_argument(
            "--skip_event_database_flushing",
            action="store_true",
            help="Don't flush events database on startup",
        )
        
    def run(self, **options):
        from django.core.management import call_command

        if options.get("skip_app_database_migration"):
            logger.info("Skip app database migration")
        else:
            call_command("migrate")
            call_command("flush", interactive=False)

        call_command("migrate", "--database=events_db")
        if options.get("skip_event_database_flushing"):
            logger.info("Skip event database flushing")
        else:

            call_command("flush", "--database=events_db", interactive=False)

        setup_test_data()
        super().run(**options)
