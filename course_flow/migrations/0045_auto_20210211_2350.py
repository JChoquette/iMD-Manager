# Generated by Django 2.2.16 on 2021-02-11 23:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('course_flow', '0044_auto_20210129_1935'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='is_original',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='project',
            name='parent_project',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='course_flow.Project'),
        ),
    ]
