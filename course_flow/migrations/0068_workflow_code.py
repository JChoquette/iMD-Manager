# Generated by Django 2.2.20 on 2021-09-07 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("course_flow", "0067_customterm_translation_plural"),
    ]

    operations = [
        migrations.AddField(
            model_name="workflow",
            name="code",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
