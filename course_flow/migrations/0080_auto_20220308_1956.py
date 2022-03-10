# Generated by Django 2.2.25 on 2022-03-08 19:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("course_flow", "0079_auto_20220228_1845"),
    ]

    operations = [
        migrations.AddField(
            model_name="node",
            name="ponderation_individual",
            field=models.PositiveIntegerField(default=0, null=True),
        ),
        migrations.AddField(
            model_name="node",
            name="ponderation_practical",
            field=models.PositiveIntegerField(default=0, null=True),
        ),
        migrations.AddField(
            model_name="node",
            name="ponderation_theory",
            field=models.PositiveIntegerField(default=0, null=True),
        ),
        migrations.AddField(
            model_name="node",
            name="time_general_hours",
            field=models.PositiveIntegerField(default=0, null=True),
        ),
        migrations.AddField(
            model_name="node",
            name="time_specific_hours",
            field=models.PositiveIntegerField(default=0, null=True),
        ),
    ]
