# Generated by Django 2.2.16 on 2020-09-16 23:23

from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings



  
def switch_to_workflow(apps, schema_editor):
    OldActivity = apps.get_model('course_flow','OldActivity')
    NewActivity = apps.get_model('course_flow','NewActivity')
    StrategyActivity = apps.get_model('course_flow','StrategyActivity')
    OutcomeActivity = apps.get_model('course_flow','OutcomeActivity')
    ColumnActivity = apps.get_model('course_flow','ColumnActivity')
    StrategyWorkflow = apps.get_model('course_flow','StrategyWorkflow')
    OutcomeWorkflow = apps.get_model('course_flow','OutcomeWorkflow')
    ColumnWorkflow = apps.get_model('course_flow','ColumnWorkflow')
    for act in OldActivity.objects.all():
        newact = NewActivity.objects.create(
            author=act.author,
            title=act.title,
            description = act.description,
            created_on = act.created_on,
            last_modified = act.last_modified,
            static = act.static,
            parent_activity=act.parent_activity,
            is_original=act.is_original,
            
        )
        for strat in act.strategies.all():
            StrategyWorkflow.objects.create(
                strategy=strat,
                workflow = newact,
                rank = StrategyActivity.objects.get(strategy=strat, activity=act).rank
            )
        for strat in act.columns.all():
            ColumnWorkflow.objects.create(
                column=strat,
                workflow = newact,
                rank = ColumnActivity.objects.get(column=strat,activity=act).rank
            )
        for strat in act.outcomes.all():
            OutcomeWorkflow.objects.create(
                outcome=strat,
                workflow = newact,
                rank = OutcomeActivity.objects.get(outcome=strat,activity=act).rank
            )
        act.delete()
    
def switch_to_noworkflow(apps, schema_editor):
    OldActivity = apps.get_model('course_flow','OldActivity')
    NewActivity = apps.get_model('course_flow','NewActivity')
    StrategyActivity = apps.get_model('course_flow','StrategyActivity')
    OutcomeActivity = apps.get_model('course_flow','OutcomeActivity')
    ColumnActivity = apps.get_model('course_flow','ColumnActivity')
    StrategyWorkflow = apps.get_model('course_flow','StrategyWorkflow')
    OutcomeWorkflow = apps.get_model('course_flow','OutcomeWorkflow')
    ColumnWorkflow = apps.get_model('course_flow','ColumnWorkflow')
    
    for act in NewActivity.objects.all():
        newact = OldActivity.objects.create(
            title=act.title,
            description = act.description,
            created_on = act.created_on,
            last_modified = act.last_modified,
            static = act.static,
            parent_activity=act.parent_activity,
            is_original=act.is_original,
            
        )
        for strat in act.strategies.all():
            StrategyActivity.objects.create(
                strategy=strat,
                activity = newact,
                rank = StrategyWorkflow.objects.get(strategy=strat,activity=act).rank
            )
        for strat in act.columns.all():
            ColumnActivity.objects.create(
                column=strat,
                activity = newact,
                rank = ColumnWorkflow.objects.get(column=strat,activity=act).rank
            )
        for strat in act.outcomes.all():
            StrategyActivity.objects.outcomes.create(
                outcome=strat,
                activity = newact,
                rank = OutcomeWorkflow.objects.get(outcome=strat,activity=act).rank
            )
        act.delete()

class Migration(migrations.Migration):

    dependencies = [
        ('course_flow', '0006_auto_20200916_2314'),
    ]

    operations = [
        migrations.AlterField('Workflow','parent_activity',
            models.ForeignKey("Workflow",on_delete=models.SET_NULL,null=True)
        ),
        migrations.RenameModel('Activity','OldActivity'),
        migrations.CreateModel(
            name="NewActivity",
            fields=[
                (
                    'workflow_ptr',
                    models.OneToOneField(
                        auto_created=True, 
                        on_delete=django.db.models.deletion.CASCADE, 
                        parent_link=True, 
                        primary_key=True, 
                        serialize=False, 
                        to='course_flow.Workflow'
                    )
                ),
                (
                    "author",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                    )
                ),
                (
                    "students",
                    models.ManyToManyField(
                        blank=True,
                        related_name="assigned_activities",
                        to=settings.AUTH_USER_MODEL,
                    )
                ),
            ],
            bases=('course_flow.workflow',),
        ),
        migrations.RunPython(switch_to_workflow,switch_to_noworkflow),
        migrations.DeleteModel('OldActivity'),
        migrations.DeleteModel('StrategyActivity'),
        migrations.DeleteModel('OutcomeActivity'),
        migrations.DeleteModel('ColumnActivity'),
        migrations.RenameModel('NewActivity','Activity'),
        
    ]

  