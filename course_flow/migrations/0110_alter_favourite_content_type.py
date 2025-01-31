# Generated by Django 3.2.15 on 2023-02-19 14:31

import django.db.models.deletion
from django.db import migrations, models


def forwards_func(apps, schema_editor):
    Favourite = apps.get_model("course_flow", "Favourite")
    ContentType = apps.get_model("contenttypes", "ContentType")
    workflow_contenttype = ContentType.objects.get_for_model(
        apps.get_model("course_flow", "Workflow")
    )
    activity_contenttype = ContentType.objects.get_for_model(
        apps.get_model("course_flow", "Activity")
    )
    course_contenttype = ContentType.objects.get_for_model(
        apps.get_model("course_flow", "Course")
    )
    program_contenttype = ContentType.objects.get_for_model(
        apps.get_model("course_flow", "Program")
    )
    db_alias = schema_editor.connection.alias
    Favourite.objects.using(db_alias).filter(
        content_type=activity_contenttype
    ).update(content_type=workflow_contenttype)
    Favourite.objects.using(db_alias).filter(
        content_type=course_contenttype
    ).update(content_type=workflow_contenttype)
    Favourite.objects.using(db_alias).filter(
        content_type=program_contenttype
    ).update(content_type=workflow_contenttype)


def reverse_func(apps, schema_editor):
    Favourite = apps.get_model("course_flow", "Favourite")
    ContentType = apps.get_model("contenttypes", "ContentType")
    Activity = apps.get_model("course_flow", "Activity")
    Course = apps.get_model("course_flow", "Course")
    Program = apps.get_model("course_flow", "Program")
    workflow_contenttype = ContentType.objects.get_for_model(
        apps.get_model("course_flow", "Workflow")
    )
    activity_contenttype = ContentType.objects.get_for_model(Activity)
    course_contenttype = ContentType.objects.get_for_model(Course)
    program_contenttype = ContentType.objects.get_for_model(Program)
    db_alias = schema_editor.connection.alias

    Favourite.objects.using(db_alias).exclude(activity=None).update(
        content_type=activity_contenttype
    )
    Favourite.objects.using(db_alias).exclude(course=None).update(
        content_type=course_contenttype
    )
    Favourite.objects.using(db_alias).exclude(program=None).update(
        content_type=program_contenttype
    )


class Migration(migrations.Migration):

    dependencies = [
        ("contenttypes", "0002_remove_content_type_name"),
        ("course_flow", "0109_objectpermission_last_viewed"),
    ]

    operations = [
        migrations.AlterField(
            model_name="favourite",
            name="content_type",
            field=models.ForeignKey(
                limit_choices_to={
                    "model__in": [
                        "project",
                        "activity",
                        "course",
                        "program",
                        "workflow",
                    ]
                },
                on_delete=django.db.models.deletion.CASCADE,
                to="contenttypes.contenttype",
            ),
        ),
    ]
