import os
from django.core.management import call_command
from django.db import migrations


def populate(apps, schema_editor):
    if os.environ.get("DJANGO_SETTINGS_MODULE") != "config.production":
        return
    from django.contrib.auth import get_user_model
    User = get_user_model()
    User.objects.create_superuser("admin_lab", password=os.environ["PORTFOLIO_ADMIN_PASSWORD"])
    User.objects.create_user("leitor_lab", password=None)
    call_command("loaddata", "portfolio_inicial", database=schema_editor.connection.alias)


class Migration(migrations.Migration):
    dependencies = [
        ("portfolio", "0004_postcover"),
        ("auth", "0012_alter_user_first_name_max_length"),
    ]
    operations = [migrations.RunPython(populate, migrations.RunPython.noop)]
