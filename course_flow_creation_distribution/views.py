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
)
from .serializers import (
    ActivitySerializer,
    CourseSerializer,
    StrategySerializer,
    NodeSerializer,
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
    template_name = "course_flow_creation_distribution/course_update.html"
    fields = ["title", "description", "author"]

    def get_context_data(self, **kwargs):
        context = super(UpdateView, self).get_context_data(**kwargs)
        context["week_course_links"] = WeekCourse.objects.filter(
            course=self.get_object()
        ).order_by("-rank")
        context["component_week_links"] = ComponentWeek.objects.filter(
            week__in=self.get_object().weeks.all()
        ).order_by("-rank")
        context["preparations"] = Preparation.objects.all()
        context["activities"] = Activity.objects.all()
        context["assesments"] = Assesment.objects.all()
        context["artifacts"] = Artifact.objects.all()
        return context

    def get_success_url(self):
        return reverse("course-detail", kwargs={"pk": self.object.pk})


class CourseDeleteView(DeleteView):
    model = Course
    template_name = "course_flow_creation_distribution/course_delete.html"

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


class ActivityDeleteView(DeleteView):
    model = Activity
    template_name = "course_flow_creation_distribution/activity_delete.html"

def update_activity_json(request):
    data = json.loads(request.POST.get("json"))
    serializer = ActivitySerializer(Activity.objects.get(id=data['id']), data=data)
    serializer.is_valid()
    serializer.save()
    return JsonResponse({"action": "updated"})

def add_node(request):
    node = Node.objects.get(pk=request.POST.get("nodePk"))
    strategy = Strategy.objects.get(pk=request.POST.get("strategyPk"))
    activity = Activity.objects.get(pk=request.POST.get("activityPk"))

    NodeStrategy.objects.create(
        strategy=strategy,
        node=duplicate_node(node),
        rank=strategy.nodestrategy_set.order_by("-rank").first().rank + 1
    )

    return JsonResponse(JSONRenderer().render(ActivitySerializer(activity).data).decode("utf-8"), safe=False)

def duplicate_node(node):
    new_node = node
    new_node.pk = None
    new_node.hash = uuid.uuid4()
    new_node.is_original = False
    new_node.parent_node = node
    new_node.save()
    return new_node

def duplicate_strategy(strategy):
    new_strategy = Strategy.objects.create(title=strategy.title, description=strategy.description, is_original=False, parent_strategy=strategy)
    for node in strategy.nodes.all():
        NodeStrategy.objects.create(
            strategy=new_strategy,
            node=duplicate_node(node),
            rank=strategy.nodestrategy_set.order_by("-rank").first().rank + 1
        )


def add_strategy(request):
    strategy = Strategy.objects.get(pk=request.POST.get("strategyPk"))
    activity = Activity.objects.get(pk=request.POST.get("activityPk"))

    NodeStrategy.objects.create(
        activity=activity,
        strategy=duplicate_strategy(strategy),
        rank=activity.strategyactivity_set.order_by("-rank").first().rank + 1
    )

    return JsonResponse(JSONRenderer().render(ActivitySerializer(activity).data).decode("utf-8"), safe=False)
