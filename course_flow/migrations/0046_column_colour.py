# Generated by Django 2.2.16 on 2021-03-01 21:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course_flow', '0045_auto_20210211_2350'),
    ]

    operations = [
        migrations.AddField(
            model_name='column',
            name='colour',
            field=models.PositiveIntegerField(null=True),
        ),
    ]
