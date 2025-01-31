# Generated by Django 2.2.17 on 2021-03-22 04:30

import uuid

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Column",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "title",
                    models.CharField(blank=True, max_length=50, null=True),
                ),
                ("created_on", models.DateTimeField(auto_now_add=True)),
                ("last_modified", models.DateTimeField(auto_now=True)),
                ("published", models.BooleanField(default=False)),
                ("visible", models.BooleanField(default=True)),
                ("colour", models.PositiveIntegerField(null=True)),
                (
                    "column_type",
                    models.PositiveIntegerField(
                        choices=[
                            (0, "Custom Activity Column"),
                            (1, "Out of Class (Instructor)"),
                            (2, "Out of Class (Students)"),
                            (3, "In Class (Instructor)"),
                            (4, "In Class (Students)"),
                            (10, "Custom Course Column"),
                            (11, "Preparation"),
                            (12, "Lesson"),
                            (13, "Artifact"),
                            (14, "Assessment"),
                            (20, "Custom Program Category"),
                        ],
                        default=0,
                    ),
                ),
                ("is_original", models.BooleanField(default=False)),
                (
                    "hash",
                    models.UUIDField(
                        default=uuid.uuid4, editable=False, unique=True
                    ),
                ),
                (
                    "author",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "parent_column",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="course_flow.Column",
                    ),
                ),
            ],
            options={
                "verbose_name": "Column",
                "verbose_name_plural": "Columns",
            },
        ),
        migrations.CreateModel(
            name="ColumnWorkflow",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("added_on", models.DateTimeField(auto_now_add=True)),
                ("rank", models.PositiveIntegerField(default=0)),
                (
                    "column",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="course_flow.Column",
                    ),
                ),
            ],
            options={
                "verbose_name": "Column-Workflow Link",
                "verbose_name_plural": "Column-Workflow Links",
            },
        ),
        migrations.CreateModel(
            name="Discipline",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "title",
                    models.CharField(
                        help_text="Enter the name of a new discipline.",
                        max_length=100,
                        unique=True,
                        verbose_name="Discipline name",
                    ),
                ),
            ],
            options={
                "verbose_name": "discipline",
                "verbose_name_plural": "disciplines",
            },
        ),
        migrations.CreateModel(
            name="Node",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "title",
                    models.CharField(blank=True, max_length=50, null=True),
                ),
                (
                    "description",
                    models.TextField(blank=True, max_length=500, null=True),
                ),
                ("created_on", models.DateTimeField(auto_now_add=True)),
                ("last_modified", models.DateTimeField(auto_now=True)),
                ("published", models.BooleanField(default=False)),
                ("is_original", models.BooleanField(default=True)),
                ("has_autolink", models.BooleanField(default=False)),
                ("is_dropped", models.BooleanField(default=False)),
                (
                    "context_classification",
                    models.PositiveIntegerField(
                        choices=[
                            (0, "None"),
                            (1, "Individual Work"),
                            (2, "Work in Groups"),
                            (3, "Whole Class"),
                            (101, "Formative"),
                            (102, "Summative"),
                            (103, "Comprehensive"),
                        ],
                        default=0,
                    ),
                ),
                (
                    "task_classification",
                    models.PositiveIntegerField(
                        choices=[
                            (0, "None"),
                            (1, "Gather Information"),
                            (2, "Discuss"),
                            (3, "Problem Solve"),
                            (4, "Analyze"),
                            (5, "Assess/Review Peers"),
                            (6, "Debate"),
                            (7, "Game/Roleplay"),
                            (8, "Create/Design"),
                            (9, "Revise/Improve"),
                            (10, "Read"),
                            (11, "Write"),
                            (12, "Present"),
                            (13, "Experiment/Inquiry"),
                            (14, "Quiz/Test"),
                            (15, "Instructor Resource Curation"),
                            (16, "Instructor Orchestration"),
                            (17, "Instructor Evaluation"),
                            (18, "Other"),
                            (101, "Jigsaw"),
                            (102, "Peer Instruction"),
                            (103, "Case Studies"),
                            (104, "Gallery Walk"),
                            (105, "Reflective Writing"),
                            (106, "Two-Stage Exam"),
                            (107, "Toolkit"),
                            (108, "One Minute Paper"),
                            (109, "Distributed Problem Solving"),
                            (110, "Peer Assessment"),
                        ],
                        default=0,
                    ),
                ),
                (
                    "node_type",
                    models.PositiveIntegerField(
                        choices=[
                            (0, "Activity Node"),
                            (1, "Course Node"),
                            (2, "Program Node"),
                        ],
                        default=0,
                    ),
                ),
                (
                    "time_required",
                    models.CharField(blank=True, max_length=30, null=True),
                ),
                (
                    "time_units",
                    models.PositiveIntegerField(
                        choices=[
                            (0, ""),
                            (1, "seconds"),
                            (2, "minutes"),
                            (3, "hours"),
                            (4, "days"),
                            (5, "weeks"),
                            (6, "months"),
                            (7, "yrs"),
                            (8, "credits"),
                        ],
                        default=0,
                    ),
                ),
                ("represents_workflow", models.BooleanField(default=False)),
                (
                    "hash",
                    models.UUIDField(
                        default=uuid.uuid4, editable=False, unique=True
                    ),
                ),
                (
                    "author",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="authored_nodes",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "column",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="course_flow.Column",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="NodeWeek",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("added_on", models.DateTimeField(auto_now_add=True)),
                ("rank", models.PositiveIntegerField(default=0)),
                (
                    "node",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="course_flow.Node",
                    ),
                ),
            ],
            options={
                "verbose_name": "Node-Week Link",
                "verbose_name_plural": "Node-Week Links",
            },
        ),
        migrations.CreateModel(
            name="Outcome",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=500)),
                ("description", models.TextField(max_length=500)),
                ("created_on", models.DateTimeField(auto_now_add=True)),
                ("last_modified", models.DateTimeField(auto_now=True)),
                ("published", models.BooleanField(default=False)),
                ("is_original", models.BooleanField(default=True)),
                ("is_dropped", models.BooleanField(default=True)),
                ("depth", models.PositiveIntegerField(default=0)),
                (
                    "hash",
                    models.UUIDField(
                        default=uuid.uuid4, editable=False, unique=True
                    ),
                ),
                (
                    "author",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Outcome",
                "verbose_name_plural": "Outcomes",
            },
        ),
        migrations.CreateModel(
            name="OutcomeProject",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("added_on", models.DateTimeField(auto_now_add=True)),
                ("rank", models.PositiveIntegerField(default=0)),
                (
                    "outcome",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="course_flow.Outcome",
                    ),
                ),
            ],
            options={
                "verbose_name": "Outcome-Project Link",
                "verbose_name_plural": "Outcome-Project Links",
            },
        ),
        migrations.CreateModel(
            name="Project",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "title",
                    models.CharField(blank=True, max_length=50, null=True),
                ),
                (
                    "description",
                    models.CharField(blank=True, max_length=500, null=True),
                ),
                ("created_on", models.DateTimeField(auto_now_add=True)),
                ("last_modified", models.DateTimeField(auto_now=True)),
                ("published", models.BooleanField(default=False)),
                ("is_original", models.BooleanField(default=False)),
                (
                    "author",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "outcomes",
                    models.ManyToManyField(
                        blank=True,
                        through="course_flow.OutcomeProject",
                        to="course_flow.Outcome",
                    ),
                ),
                (
                    "parent_project",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="course_flow.Project",
                    ),
                ),
            ],
            options={
                "verbose_name": "Project",
                "verbose_name_plural": "Projects",
            },
        ),
        migrations.CreateModel(
            name="Week",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "title",
                    models.CharField(blank=True, max_length=50, null=True),
                ),
                (
                    "description",
                    models.TextField(blank=True, max_length=500, null=True),
                ),
                ("created_on", models.DateTimeField(auto_now_add=True)),
                ("last_modified", models.DateTimeField(auto_now=True)),
                ("default", models.BooleanField(default=False)),
                ("is_original", models.BooleanField(default=True)),
                ("published", models.BooleanField(default=False)),
                ("is_strategy", models.BooleanField(default=False)),
                (
                    "hash",
                    models.UUIDField(
                        default=uuid.uuid4, editable=False, unique=True
                    ),
                ),
                (
                    "strategy_classification",
                    models.PositiveIntegerField(
                        choices=[
                            (0, "None"),
                            (1, "Jigsaw"),
                            (2, "Peer Instruction"),
                            (3, "Case Studies"),
                            (4, "Gallery Walk"),
                            (5, "Reflective Writing"),
                            (6, "Two-Stage Exam"),
                            (7, "Toolkit"),
                            (8, "One Minute Paper"),
                            (9, "Distributed Problem Solving"),
                            (10, "Peer Assessment"),
                            (11, "Other"),
                        ],
                        default=0,
                    ),
                ),
                (
                    "week_type",
                    models.PositiveIntegerField(
                        choices=[(0, "Part"), (1, "Week"), (2, "Term")],
                        default=0,
                    ),
                ),
                (
                    "author",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "nodes",
                    models.ManyToManyField(
                        blank=True,
                        through="course_flow.NodeWeek",
                        to="course_flow.Node",
                    ),
                ),
            ],
            options={
                "verbose_name": "Week",
                "verbose_name_plural": "Weeks",
            },
        ),
        migrations.CreateModel(
            name="WeekWorkflow",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("added_on", models.DateTimeField(auto_now_add=True)),
                ("rank", models.PositiveIntegerField(default=0)),
                (
                    "week",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="course_flow.Week",
                    ),
                ),
            ],
            options={
                "verbose_name": "Week-Workflow Link",
                "verbose_name_plural": "Week-Workflow Links",
            },
        ),
        migrations.CreateModel(
            name="Workflow",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "title",
                    models.CharField(blank=True, max_length=50, null=True),
                ),
                (
                    "description",
                    models.TextField(blank=True, max_length=500, null=True),
                ),
                ("created_on", models.DateTimeField(auto_now_add=True)),
                ("last_modified", models.DateTimeField(auto_now=True)),
                ("static", models.BooleanField(default=False)),
                ("published", models.BooleanField(default=False)),
                ("is_strategy", models.BooleanField(default=False)),
                ("from_saltise", models.BooleanField(default=False)),
                ("is_original", models.BooleanField(default=True)),
                (
                    "hash",
                    models.UUIDField(
                        default=uuid.uuid4, editable=False, unique=True
                    ),
                ),
                (
                    "outcomes_type",
                    models.PositiveIntegerField(
                        choices=[(0, "Normal"), (1, "Advanced")], default=0
                    ),
                ),
                (
                    "outcomes_sort",
                    models.PositiveIntegerField(
                        choices=[
                            (0, "Time"),
                            (1, "Category"),
                            (2, "Task"),
                            (3, "Context"),
                        ],
                        default=0,
                    ),
                ),
                (
                    "columns",
                    models.ManyToManyField(
                        blank=True,
                        through="course_flow.ColumnWorkflow",
                        to="course_flow.Column",
                    ),
                ),
                (
                    "parent_workflow",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="course_flow.Workflow",
                    ),
                ),
                (
                    "weeks",
                    models.ManyToManyField(
                        blank=True,
                        through="course_flow.WeekWorkflow",
                        to="course_flow.Week",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="WorkflowProject",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("added_on", models.DateTimeField(auto_now_add=True)),
                ("rank", models.PositiveIntegerField(default=0)),
                (
                    "project",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="course_flow.Project",
                    ),
                ),
                (
                    "workflow",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="course_flow.Workflow",
                    ),
                ),
            ],
            options={
                "verbose_name": "Workflow-Project Link",
                "verbose_name_plural": "Workflow-Project Links",
            },
        ),
        migrations.AddField(
            model_name="weekworkflow",
            name="workflow",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="course_flow.Workflow",
            ),
        ),
        migrations.AddField(
            model_name="week",
            name="original_strategy",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="course_flow.Workflow",
            ),
        ),
        migrations.AddField(
            model_name="week",
            name="parent_week",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="course_flow.Week",
            ),
        ),
        migrations.AddField(
            model_name="project",
            name="workflows",
            field=models.ManyToManyField(
                blank=True,
                through="course_flow.WorkflowProject",
                to="course_flow.Workflow",
            ),
        ),
        migrations.CreateModel(
            name="OutcomeWorkflow",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("added_on", models.DateTimeField(auto_now_add=True)),
                ("rank", models.PositiveIntegerField(default=0)),
                (
                    "outcome",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="course_flow.Outcome",
                    ),
                ),
                (
                    "workflow",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="course_flow.Workflow",
                    ),
                ),
            ],
            options={
                "verbose_name": "Outcome-Workflow Link",
                "verbose_name_plural": "Outcome-Workflow Links",
            },
        ),
        migrations.AddField(
            model_name="outcomeproject",
            name="project",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="course_flow.Project",
            ),
        ),
        migrations.CreateModel(
            name="OutcomeOutcome",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("added_on", models.DateTimeField(auto_now_add=True)),
                ("rank", models.PositiveIntegerField(default=0)),
                (
                    "child",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="parent_outcome_links",
                        to="course_flow.Outcome",
                    ),
                ),
                (
                    "parent",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="child_outcome_links",
                        to="course_flow.Outcome",
                    ),
                ),
            ],
            options={
                "verbose_name": "Outcome-Outcome Link",
                "verbose_name_plural": "Outcome-Outcome Links",
            },
        ),
        migrations.CreateModel(
            name="OutcomeNode",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("added_on", models.DateTimeField(auto_now_add=True)),
                ("rank", models.PositiveIntegerField(default=0)),
                ("degree", models.PositiveIntegerField(default=1)),
                (
                    "node",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="course_flow.Node",
                    ),
                ),
                (
                    "outcome",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="course_flow.Outcome",
                    ),
                ),
            ],
            options={
                "verbose_name": "Outcome-Node Link",
                "verbose_name_plural": "Outcome-Node Links",
            },
        ),
        migrations.AddField(
            model_name="outcome",
            name="children",
            field=models.ManyToManyField(
                blank=True,
                related_name="parent_outcomes",
                through="course_flow.OutcomeOutcome",
                to="course_flow.Outcome",
            ),
        ),
        migrations.AddField(
            model_name="outcome",
            name="parent_outcome",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="course_flow.Outcome",
            ),
        ),
        migrations.AddField(
            model_name="nodeweek",
            name="week",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="course_flow.Week",
            ),
        ),
        migrations.CreateModel(
            name="NodeLink",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "title",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                ("published", models.BooleanField(default=False)),
                (
                    "source_port",
                    models.PositiveIntegerField(
                        choices=[(1, "e"), (2, "s"), (3, "w")], default=2
                    ),
                ),
                (
                    "target_port",
                    models.PositiveIntegerField(
                        choices=[(0, "n"), (1, "e"), (3, "w")], default=0
                    ),
                ),
                ("dashed", models.BooleanField(default=False)),
                ("created_on", models.DateTimeField(auto_now_add=True)),
                ("last_modified", models.DateTimeField(auto_now=True)),
                ("is_original", models.BooleanField(default=True)),
                (
                    "hash",
                    models.UUIDField(
                        default=uuid.uuid4, editable=False, unique=True
                    ),
                ),
                (
                    "author",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "parent_nodelink",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="course_flow.NodeLink",
                    ),
                ),
                (
                    "source_node",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="outgoing_links",
                        to="course_flow.Node",
                    ),
                ),
                (
                    "target_node",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="incoming_links",
                        to="course_flow.Node",
                    ),
                ),
            ],
            options={
                "verbose_name": "Node Link",
                "verbose_name_plural": "Node Links",
            },
        ),
        migrations.CreateModel(
            name="NodeCompletionStatus",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("is_completed", models.BooleanField(default=False)),
                (
                    "node",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="course_flow.Node",
                    ),
                ),
                (
                    "student",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Node Completion Status",
                "verbose_name_plural": "Node Completion Statuses",
            },
        ),
        migrations.AddField(
            model_name="node",
            name="linked_workflow",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="course_flow.Workflow",
            ),
        ),
        migrations.AddField(
            model_name="node",
            name="outcomes",
            field=models.ManyToManyField(
                blank=True,
                through="course_flow.OutcomeNode",
                to="course_flow.Outcome",
            ),
        ),
        migrations.AddField(
            model_name="node",
            name="parent_node",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="course_flow.Node",
            ),
        ),
        migrations.AddField(
            model_name="node",
            name="students",
            field=models.ManyToManyField(
                blank=True,
                related_name="assigned_nodes",
                through="course_flow.NodeCompletionStatus",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="columnworkflow",
            name="workflow",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="course_flow.Workflow",
            ),
        ),
        migrations.CreateModel(
            name="Program",
            fields=[
                (
                    "workflow_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="course_flow.Workflow",
                    ),
                ),
                (
                    "author",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            bases=("course_flow.workflow",),
        ),
        migrations.CreateModel(
            name="Course",
            fields=[
                (
                    "workflow_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="course_flow.Workflow",
                    ),
                ),
                (
                    "author",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="authored_courses",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "discipline",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="course_flow.Discipline",
                    ),
                ),
                (
                    "students",
                    models.ManyToManyField(
                        blank=True,
                        related_name="assigned_courses",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            bases=("course_flow.workflow",),
        ),
        migrations.CreateModel(
            name="Activity",
            fields=[
                (
                    "workflow_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="course_flow.Workflow",
                    ),
                ),
                (
                    "author",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="authored_activities",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "students",
                    models.ManyToManyField(
                        blank=True,
                        related_name="assigned_activities",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Activity",
                "verbose_name_plural": "Activities",
            },
            bases=("course_flow.workflow",),
        ),
    ]
