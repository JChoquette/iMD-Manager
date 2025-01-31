# Generated by Django 2.2.20 on 2021-07-21 17:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("course_flow", "0061_outcomehorizontallink_degree"),
    ]

    operations = [
        migrations.AlterField(
            model_name="favourite",
            name="content_type",
            field=models.ForeignKey(
                limit_choices_to={
                    "model__in": ["project", "activity", "course", "program"]
                },
                on_delete=django.db.models.deletion.CASCADE,
                to="contenttypes.ContentType",
            ),
        ),
        migrations.AlterField(
            model_name="objectpermission",
            name="content_type",
            field=models.ForeignKey(
                limit_choices_to={
                    "model__in": ["project", "activity", "course", "program"]
                },
                on_delete=django.db.models.deletion.CASCADE,
                to="contenttypes.ContentType",
            ),
        ),
    ]
