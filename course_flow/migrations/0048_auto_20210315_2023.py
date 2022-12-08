# Generated by Django 2.2.16 on 2021-03-15 20:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("course_flow", "0047_auto_20210315_1952"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="project",
            name="discipline",
        ),
        migrations.AddField(
            model_name="project",
            name="disciplines",
            field=models.ManyToManyField(
                blank=True, to="course_flow.Discipline"
            ),
        ),
    ]
