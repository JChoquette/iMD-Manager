# Generated by Django 2.2.16 on 2020-10-16 00:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("course_flow", "0018_node_has_autolink")]

    operations = [
        migrations.AddField(
            model_name="nodelink",
            name="source_port",
            field=models.PositiveIntegerField(
                choices=[(1, "e"), (2, "s"), (3, "w")], default=2
            ),
        ),
        migrations.AddField(
            model_name="nodelink",
            name="target_port",
            field=models.PositiveIntegerField(
                choices=[(0, "n"), (1, "e"), (3, "w")], default=0
            ),
        ),
    ]
