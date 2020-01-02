from .models import (
    Course,
    Preparation,
    Activity,
    Assesment,
    Artifact,
    Strategy,
    Node,
    NodeStrategy,
    StrategyActivity,
    ComponentWeek,
    WeekCourse,
    Component,
    Week,
    Program,
    ComponentProgram,
)
from .serializers import (
    ActivitySerializer,
    CourseSerializer,
    StrategySerializer,
    NodeSerializer,
    WeekLevelComponentSerializer,
    ProgramSerializer,
    ProgramLevelComponentSerializer,
)
from django.views.generic.edit import CreateView
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from django.forms import ModelForm
from django.db.models import Q
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
import io
from django.http import JsonResponse
from django.db.models import Count
import uuid
import json
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q

class ProgramUpdateView(UpdateView):
    model = Program
    fields = ["title", "description", "author"]
    template_name = "course_flow_creation_distribution/program_update.html"

    def get_context_data(self, **kwargs):
        context = super(UpdateView, self).get_context_data(**kwargs)
        context["program_json"] = JSONRenderer().render(ProgramSerializer(self.object).data).decode("utf-8")
        context["owned_components"] = Component.objects.filter(Q(content_type=ContentType.objects.get_for_model(Course))|Q(content_type=ContentType.objects.get_for_model(Assesment)))
        context["owned_component_json"] = JSONRenderer().render(ProgramLevelComponentSerializer(context["owned_components"], many=True).data).decode("utf-8")
        return context

    def get_success_url(self):
        return reverse("course-detail", kwargs={"pk": self.object.pk})


class CourseDetailView(DetailView):
    model = Course
    template_name = "course_flow_creation_distribution/course_detail.html"

    def get_context_data(self, **kwargs):
        context = super(DetaileView, self).get_context_data(**kwargs)
        context["week_course_links"] = WeekCourse.objects.filter(
            course=self.get_object()
        )
        context["component_week_links"] = []
        for week in self.get_object().weeks.all():
            context["component_week_links"].append(
                ComponentWeek.objects.filter(week=week)
            )
        return context


class CourseUpdateView(UpdateView):
    model = Course
    fields = ["title", "description", "author"]
    template_name = "course_flow_creation_distribution/course_update.html"

    def get_context_data(self, **kwargs):
        context = super(UpdateView, self).get_context_data(**kwargs)
        context["course_json"] = JSONRenderer().render(CourseSerializer(self.object).data).decode("utf-8")
        context["owned_components"] = Component.objects.exclude(content_type=ContentType.objects.get_for_model(Course))
        context["owned_component_json"] = JSONRenderer().render(WeekLevelComponentSerializer(context["owned_components"], many=True).data).decode("utf-8")
        return context

    def get_success_url(self):
        return reverse("course-detail", kwargs={"pk": self.object.pk})


class NodeForm(ModelForm):
        class Meta:
            model = Node
            fields = ['title', 'description', 'work_classification', 'activity_classification', 'classification']

class StrategyForm(ModelForm):
        class Meta:
            model = Strategy
            fields = ['title', 'description']


class ActivityDetailView(DetailView):
    model = Activity
    template_name = "course_flow_creation_distribution/activity_detail.html"

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        context["activity_json"] = JSONRenderer().render(ActivitySerializer(self.object).data).decode("utf-8")
        return context


class ActivityUpdateView(UpdateView):
    model = Activity
    fields = ["title", "description", "author"]
    template_name = "course_flow_creation_distribution/activity_update.html"

    def get_context_data(self, **kwargs):
        context = super(UpdateView, self).get_context_data(**kwargs)
        context["activity_json"] = JSONRenderer().render(ActivitySerializer(self.object).data).decode("utf-8")
        context["default_strategies"] = Strategy.objects.filter(default=True)
        context["default_strategy_json"] = JSONRenderer().render(StrategySerializer(context["default_strategies"], many=True).data).decode("utf-8")
        context["popular_nodes"] = Node.objects.filter(is_original=True).annotate(num_children=Count('node')).order_by('-num_children')[:3]
        context["popoular_node_json"] = JSONRenderer().render(NodeSerializer(context["popular_nodes"], many=True).data).decode("utf-8")
        context['node_form'] = NodeForm()
        context['strategy_form'] = StrategyForm()
        return context

    def get_success_url(self):
        return reverse("activity-detail", kwargs={"pk": self.object.pk})



def update_activity_json(request):
    data = json.loads(request.POST.get("json"))
    serializer = ActivitySerializer(Activity.objects.get(id=data['id']), data=data)
    serializer.is_valid()
    serializer.save()
    return JsonResponse({"action": "updated"})

def update_course_json(request):
    data = json.loads(request.POST.get("json"))
    serializer = CourseSerializer(Course.objects.get(id=data['id']), data=data)
    serializer.is_valid()
    serializer.save()
    return JsonResponse({"action": "updated"})

def update_program_json(request):
    data = json.loads(request.POST.get("json"))
    serializer = ProgramSerializer(Program.objects.get(id=data['id']), data=data)
    serializer.is_valid()
    serializer.save()
    return JsonResponse({"action": "updated"})

def duplicate_node(node):
    new_node = Node.objects.create(title=node.title,
        description=node.description,
        is_original=False,
        parent_node=node,
        work_classification=node.work_classification,
        activity_classification=node.activity_classification,
        classification=node.classification
    )
    return new_node

def add_node(request):
    node = Node.objects.get(pk=request.POST.get("nodePk"))
    strategy = Strategy.objects.get(pk=request.POST.get("strategyPk"))

    NodeStrategy.objects.create(
        strategy=strategy,
        node=duplicate_node(node),
        rank=strategy.nodestrategy_set.order_by("-rank").first().rank + 1
    )

    activity = Activity.objects.get(pk=request.POST.get("activityPk"))

    return JsonResponse(JSONRenderer().render(ActivitySerializer(activity).data).decode("utf-8"), safe=False)

def duplicate_strategy(strategy):
    new_strategy = Strategy.objects.create(title=strategy.title, description=strategy.description, is_original=False, parent_strategy=strategy)
    for node in strategy.nodes.all():
        NodeStrategy.objects.create(
            strategy=new_strategy,
            node=duplicate_node(node),
            rank=NodeStrategy.objects.get(node=node, strategy=strategy).rank,
        )
    return new_strategy

def add_strategy(request):
    strategy = Strategy.objects.get(pk=request.POST.get("strategyPk"))
    activity = Activity.objects.get(pk=request.POST.get("activityPk"))

    StrategyActivity.objects.create(
        activity=activity,
        strategy=duplicate_strategy(strategy),
        rank=(activity.strategyactivity_set.order_by("-rank").first().rank if activity.strategyactivity_set else -1) + 1
    )

    activity = Activity.objects.get(pk=request.POST.get("activityPk"))

    return JsonResponse(JSONRenderer().render(ActivitySerializer(activity).data).decode("utf-8"), safe=False)

def duplicate_component_course_level(component):
    if type(component.content_object) == Activity:
        new_component = Component.objects.create(content_object=Activity.objects.create(title=component.content_object.title, description=component.content_object.description, is_original=False, parent_activity=component.content_object))
        for strategy in component.content_object.strategies.all():
            StrategyActivity.objects.create(
                activity=new_component.content_object,
                strategy=duplicate_strategy(strategy),
                rank=StrategyActivity.objects.get(strategy=strategy, activity=component.content_object).rank,
            )
    elif type(component.content_object) == Preparation:
        new_component = Component.objects.create(content_object=Preparation.objects.create(title=component.content_object.title, description=component.content_object.description, is_original=False, parent_preparation=component.content_object))
    elif type(component.content_object) == Assesment:
        new_component = Component.objects.create(content_object=Assesment.objects.create(title=component.content_object.title, description=component.content_object.description, is_original=False, parent_assesment=component.content_object))
    else:
        new_component = Component.objects.create(content_object=Artifact.objects.create(title=component.content_object.title, description=component.content_object.description, is_original=False, parent_artifact=component.content_object))
    return new_component

def add_component_to_course(request):
    week = Week.objects.get(pk=request.POST.get("weekPk"))
    component = Component.objects.get(pk=request.POST.get("componentPk"))

    ComponentWeek.objects.create(
        week=week,
        component=duplicate_component_course_level(component),
        rank=(week.componentweek_set.order_by("-rank").first().rank if week.componentweek_set else -1) + 1,
    )

    course = Course.objects.get(pk=request.POST.get("coursePk"))

    return JsonResponse(JSONRenderer().render(CourseSerializer(course).data).decode("utf-8"), safe=False)

def duplicate_week(week):
    new_week = Week.objects.create(title=week.title)
    for component in week.compmonents.all():
        ComponentWeek.objects.create(
            week=new_week,
            component=duplicate_component_course_level(component),
            rank=ComponentWeek.objects.get(week=week, component=component).rank,
        )
    return new_strategy

def duplicate_component_program_level(component):
    if type(component.content_object) == Assesment:
        new_component = Component.objects.create(content_object=Assesment.objects.create(title=component.content_object.title, description=component.content_object.description, is_original=False, parent_assesment=component.content_object))
    else:
        new_component = Component.objects.create(content_object=Course.objects.create(title=component.content_object.title, description=component.content_object.description, is_original=False, parent_course=component.content_object))
        for week in component.content_object.weeks.all():
            WeekCourse.objects.create(
                course=new_component.content_object,
                week=duplicate_week(week),
                rank=WeekCourse.objects.get(week=week, course=component.content_object).rank,
            )
    return new_component

def add_component_to_program(request):
    component = Component.objects.get(pk=request.POST.get("componentPk"))
    program = Program.objects.get(pk=request.POST.get("programPk"))

    ComponentProgram.objects.create(
        program=program,
        component=duplicate_component_program_level(component),
        rank=(program.componentprogram_set.order_by("-rank").first().rank if program.componentprogram_set else -1) + 1,
    )

    return JsonResponse(JSONRenderer().render(ProgramSerializer(program).data).decode("utf-8"), safe=False)

def dialog_form_post(request):
    data = json.loads(request.POST.get("json"))
    props = json.loads(request.POST.get("props"))
    print(props)
    if props["isNode"]:
        print("node cond")
        del data["componentType"]
        serializer = NodeSerializer(data=data)
        data["work_classification"] = int(data["work_classification"]) - 1
        data["activity_classification"] = int(data["activity_classification"]) - 1
        data["parent_node"] = None
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({"action": "posted"})
        else:
            print(serializer.errors)
            return JsonResponse({"action": "error"})
    elif props["isCourse"]:
        del data["componentType"], data["work_classification"], data["activity_classification"]
        serializer = CourseSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({"action": "posted"})
        else:
            return JsonResponse({"action": "error"})
    elif props["isWeek"]:
        del data["componentType"], data["work_classification"], data["activity_classification"], data["description"]
        serializer = WeekSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({"action": "posted"})
        else:
            return JsonResponse({"action": "error"})
    elif (data["componentType"]==1):
        del data["componentType"], data["work_classification"], data["activity_classification"]
        serializer = AssesmentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({"action": "posted"})
        else:
            return JsonResponse({"action": "error"})
    elif (data["componentType"]==2):
        del data["componentType"], data["work_classification"], data["activity_classification"]
        serializer = ArtifactSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({"action": "posted"})
        else:
            return JsonResponse({"action": "error"})
    elif (data["componentType"]==3):
        del data["componentType"], data["work_classification"], data["activity_classification"]
        serializer = PreparationSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({"action": "posted"})
        else:
            return JsonResponse({"action": "error"})
    elif props["isProgramLevelComponent"]:
        del data["componentType"], data["work_classification"], data["activity_classification"]
        serializer = CourseSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({"action": "posted"})
        else:
            return JsonResponse({"action": "error"})
    elif props["isCourseLevelComponent"]:
        del data["componentType"], data["work_classification"], data["activity_classification"]
        serializer = ActivitySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({"action": "posted"})
        else:
            return JsonResponse({"action": "error"})
