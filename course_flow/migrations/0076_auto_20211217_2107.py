# Generated by Django 2.2.20 on 2021-12-17 21:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("course_flow", "0075_auto_20211217_2053"),
    ]

    operations = [
        migrations.AlterField(
            model_name="comment",
            name="text",
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name="node",
            name="description",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="outcome",
            name="description",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="outcome",
            name="title",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="project",
            name="description",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="week",
            name="description",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="workflow",
            name="description",
            field=models.TextField(blank=True, null=True),
        ),
    ]
