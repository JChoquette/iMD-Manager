# Generated by Django 2.2.25 on 2022-05-20 18:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("course_flow", "0083_auto_20220322_2153"),
    ]

    operations = [
        migrations.AddField(
            model_name="week",
            name="is_dropped",
            field=models.BooleanField(default=True),
        ),
    ]
