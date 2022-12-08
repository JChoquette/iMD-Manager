# Generated by Django 2.2.20 on 2021-08-18 22:56

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("course_flow", "0064_auto_20210810_2256"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="column",
            name="published",
        ),
        migrations.RemoveField(
            model_name="node",
            name="published",
        ),
        migrations.RemoveField(
            model_name="nodelink",
            name="published",
        ),
        migrations.RemoveField(
            model_name="week",
            name="published",
        ),
        migrations.CreateModel(
            name="Comment",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("text", models.CharField(max_length=500)),
                (
                    "created_on",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
                (
                    "user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="column",
            name="comments",
            field=models.ManyToManyField(blank=True, to="course_flow.Comment"),
        ),
        migrations.AddField(
            model_name="node",
            name="comments",
            field=models.ManyToManyField(blank=True, to="course_flow.Comment"),
        ),
        migrations.AddField(
            model_name="outcome",
            name="comments",
            field=models.ManyToManyField(blank=True, to="course_flow.Comment"),
        ),
        migrations.AddField(
            model_name="week",
            name="comments",
            field=models.ManyToManyField(blank=True, to="course_flow.Comment"),
        ),
    ]
