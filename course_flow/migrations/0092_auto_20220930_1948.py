# Generated by Django 3.2.14 on 2022-09-30 19:48

import uuid

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("course_flow", "0091_auto_20220930_1948"),
    ]

    operations = [
        migrations.AlterField(
            model_name="project",
            name="hash",
            field=models.UUIDField(
                default=uuid.uuid4, editable=False, unique=True
            ),
        ),
    ]
