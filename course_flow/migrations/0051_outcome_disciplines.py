# Generated by Django 2.2.16 on 2021-03-17 23:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("course_flow", "0050_workflow_disciplines"),
    ]

    operations = [
        migrations.AddField(
            model_name="outcome",
            name="disciplines",
            field=models.ManyToManyField(
                blank=True, to="course_flow.Discipline"
            ),
        ),
    ]
