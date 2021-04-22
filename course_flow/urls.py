from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.urls import include, path
from rest_framework import routers
from django.views.i18n import JavaScriptCatalog

from . import lti, views

router = routers.SimpleRouter()
router.register(r"workflow/read", views.WorkflowViewSet)


app_name = "course_flow"


def flow_patterns():
    return [
        url(r"^register/$", views.registration_view, name="registration"),
        url(
            r"^login/$",
            auth_views.LoginView.as_view(
                template_name="course_flow/registration/login.html"
            ),
            name="login",
        ),
        url(r"^logout/$", auth_views.LogoutView.as_view(), name="logout"),
        url(r"home/$", views.home_view, name="home"),
        url(r"explore/$", views.ExploreView.as_view(), name="explore"),
        url(r"import/$", views.import_view, name="import"),
        url(
            r"^project/(?P<pk>[0-9]+)/update/$",
            views.ProjectUpdateView.as_view(),
            name="project-update",
        ),
        url(
            r"^outcome/(?P<pk>[0-9]+)/update/$",
            views.OutcomeUpdateView.as_view(),
            name="outcome-update",
        ),
        url(
            r"^workflow/(?P<pk>[0-9]+)/update/$",
            views.WorkflowUpdateView.as_view(),
            name="workflow-update",
        ),
        url(
            r"^workflow/updatevalue/$", views.update_value, name="update-value"
        ),
        url(r"^workflow/delete-self/$", views.delete_self, name="delete-self"),
        url(
            r"^workflow/update-outcomenode-degree/$",
            views.update_outcomenode_degree,
            name="update-outcomenode-degree",
        ),
        url(
            r"^workflow/duplicate-self/$",
            views.duplicate_self,
            name="duplicate-self",
        ),
        url(
            r"^project/duplicate-workflow/$",
            views.duplicate_workflow_ajax,
            name="duplicate-workflow",
        ),
        url(
            r"^project/duplicate-outcome/$",
            views.duplicate_outcome_ajax,
            name="duplicate-outcome",
        ),
        url(
            r"^project/duplicate-project/$",
            views.duplicate_project_ajax,
            name="duplicate-project",
        ),
        url(
            r"^project/duplicate-strategy/$",
            views.duplicate_strategy_ajax,
            name="duplicate-strategy",
        ),
        url(
            r"^workflow/insert-sibling/$",
            views.insert_sibling,
            name="insert-sibling",
        ),
        url(
            r"^workflow/insert-child/$",
            views.insert_child,
            name="insert-child",
        ),
        url(r"^workflow/inserted-at/$", views.inserted_at, name="inserted-at"),
        url(
            r"^node/change-column/$", views.change_column, name="change-column"
        ),
        url(
            r"^node/add-outcome-to-node/$",
            views.add_outcome_to_node,
            name="add-outcome-to-node",
        ),
        url(r"^workflow/column/new", views.new_column, name="new-column"),
        url(r"^workflow/node/new", views.new_node, name="new-node"),
        url(
            r"^workflow/strategy/add", views.add_strategy, name="add-strategy"
        ),
        url(
            r"^workflow/strategy/toggle",
            views.week_toggle_strategy,
            name="toggle-strategy",
        ),
        url(
            r"^project/from-json/",
            views.project_from_json,
            name="project-from-json",
        ),
        url(
            r"^project/get-disciplines/",
            views.DisciplineListView.as_view(),
            name="get-disciplines",
        ),
        url(
            r"^favourites/toggle", views.toggle_favourite, name="toggle-favourite"
        ),
        url(
            r"^permissions/set", views.set_permission, name="set-permission"
        ),
        url(
            r"^workflow/node/set-linked-workflow/$",
            views.set_linked_workflow_ajax,
            name="set-linked-workflow",
        ),
        url(
            r"^workflow/node-link/new",
            views.new_node_link,
            name="new-node-link",
        ),
        url(
            r"^workflow/get-possible-linked-workflows/",
            views.get_possible_linked_workflows,
            name="get-possible-linked-workflows",
        ),
        url(
            r"^workflow/get-workflow-data/",
            views.get_workflow_data,
            name="get-workflow-data",
        ),
        url(
            r"^project/get-project-data/",
            views.get_project_data,
            name="get-project-data",
        ),
        url(
            r"^outcome/get-outcome-data/",
            views.get_outcome_data,
            name="get-outcome-data",
        ),
        url(
            r"^project/get-users-for-object/",
            views.get_users_for_object,
            name="get-users-for-object",
        ),
        url(
            r"^users/get-user-list/",
            views.get_user_list,
            name="get-user-list",
        ),
        url(
            r"^workflow/(?P<pk>[0-9]+)/$",
            views.WorkflowDetailView.as_view(),
            name="workflow-detail-view",
        ),
        url(
            r"^project/create/$",
            views.ProjectCreateView.as_view(),
            name="project-create",
        ),
        url(
            r"^project/(?P<pk>[0-9]+)/$",
            views.ProjectDetailView.as_view(),
            name="project-detail-view",
        ),
        url(
            r"^outcome/(?P<projectPk>[0-9]+)/create/$",
            views.OutcomeCreateView.as_view(),
            name="outcome-create",
        ),
        url(
            r"^outcome/(?P<pk>[0-9]+)/$",
            views.OutcomeDetailView.as_view(),
            name="outcome-detail-view",
        ),
        url(
            r"^program/(?P<projectPk>[0-9]+)/create/$",
            views.ProgramCreateView.as_view(),
            name="program-create",
        ),
        url(
            r"^program/(?P<pk>[0-9]+)/$",
            views.ProgramDetailView.as_view(),
            name="program-detail-view",
        ),
        url(
            r"^course/(?P<projectPk>[0-9]+)/create/$",
            views.CourseCreateView.as_view(),
            name="course-create",
        ),
        url(
            r"^course-strategy/create/$",
            views.CourseStrategyCreateView.as_view(),
            name="course-strategy-create",
        ),
        url(
            r"^course/(?P<pk>[0-9]+)/$",
            views.CourseDetailView.as_view(),
            name="course-detail-view",
        ),
        url(
            r"^activity/(?P<projectPk>[0-9]+)/create/$",
            views.ActivityCreateView.as_view(),
            name="activity-create",
        ),
        url(
            r"^activity-strategy/create/$",
            views.ActivityStrategyCreateView.as_view(),
            name="activity-strategy-create",
        ),
        url(
            r"^activity/(?P<pk>[0-9]+)/$",
            views.ActivityDetailView.as_view(),
            name="activity-detail-view",
        ),
    ] + router.urls


def lti_patterns():
    return [path("course-list/", lti.get_course_list, name="course-list")]


urlpatterns = sum(
    [
        [path("lti/", include("django_lti_tool_provider.urls"))],
        [path("jsi18n/",JavaScriptCatalog.as_view(),name="javascript-catalog")],
        flow_patterns(),
        lti_patterns(),
    ],
    [],
)
