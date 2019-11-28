# Generated by Django 2.2.7 on 2019-11-28 22:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('course_flow_creation_distribution', '0018_auto_20191125_2149'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='is_original',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='course',
            name='parent_course',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='course_flow_creation_distribution.Course'),
        ),
    ]
