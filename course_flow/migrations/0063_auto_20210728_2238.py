# Generated by Django 2.2.20 on 2021-07-28 22:38

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("course_flow", "0062_auto_20210721_1733"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="nodelink",
            name="parent_nodelink",
        ),
        migrations.AlterField(
            model_name="column",
            name="created_on",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name="columnworkflow",
            name="added_on",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name="node",
            name="created_on",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name="nodelink",
            name="created_on",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name="nodeweek",
            name="added_on",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name="outcome",
            name="created_on",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name="outcomehorizontallink",
            name="added_on",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name="outcomenode",
            name="added_on",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name="outcomeoutcome",
            name="added_on",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name="outcomeworkflow",
            name="added_on",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name="project",
            name="created_on",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name="week",
            name="created_on",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name="weekworkflow",
            name="added_on",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name="workflow",
            name="created_on",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name="workflowproject",
            name="added_on",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
