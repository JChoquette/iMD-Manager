# Generated by Django 3.2.15 on 2022-11-18 15:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("course_flow", "0095_updatenotification"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="node",
            name="students",
        ),
        migrations.DeleteModel(
            name="NodeCompletionStatus",
        ),
    ]
