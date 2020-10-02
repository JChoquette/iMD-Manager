# Generated by Django 2.2.16 on 2020-10-02 21:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course_flow', '0014_auto_20201001_1817'),
    ]

    operations = [
        migrations.AlterField(
            model_name='column',
            name='title',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='node',
            name='description',
            field=models.TextField(blank=True, max_length=400, null=True),
        ),
        migrations.AlterField(
            model_name='node',
            name='title',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='strategy',
            name='description',
            field=models.TextField(blank=True, max_length=400, null=True),
        ),
        migrations.AlterField(
            model_name='strategy',
            name='title',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='workflow',
            name='description',
            field=models.TextField(blank=True, max_length=400, null=True),
        ),
        migrations.AlterField(
            model_name='workflow',
            name='title',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
