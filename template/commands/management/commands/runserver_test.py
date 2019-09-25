from django.contrib.staticfiles.management.commands import runserver


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

    def run(self, **options):
        from django.core.management import call_command

        call_command("migrate")
        call_command("migrate", "--database=events_db")
        call_command("flush", interactive=False)
        call_command("flush", "--database=events_db", interactive=False)
        setup_test_data()
        super().run(**options)
