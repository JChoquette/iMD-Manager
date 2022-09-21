# Generated by Django 3.2.14 on 2022-09-21 15:55

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('course_flow', '0087_auto_20220704_1828'),
    ]

    operations = [
        migrations.CreateModel(
            name='LiveProject',
            fields=[
                ('created_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('project', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='course_flow.project')),
                ('default_self_reporting', models.BooleanField(default=True)),
                ('default_assign_to_all', models.BooleanField(default=True)),
                ('default_single_completion', models.BooleanField(default=False)),
            ],
        ),
    ]
