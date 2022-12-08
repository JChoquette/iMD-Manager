# Generated by Django 2.2.20 on 2021-05-05 17:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("course_flow", "0056_auto_20210427_2228"),
    ]

    operations = [
        migrations.AddField(
            model_name="outcome",
            name="horizontal_outcome_links",
            field=models.ManyToManyField(
                blank=True,
                related_name="reverse_horizontal_outcome_links",
                to="course_flow.Outcome",
            ),
        ),
        migrations.AlterField(
            model_name="node",
            name="linked_workflow",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="linked_nodes",
                to="course_flow.Workflow",
            ),
        ),
    ]
