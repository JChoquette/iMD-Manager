from django.conf.urls import include, url
from rest_framework import routers

from . import views


router = routers.SimpleRouter()
router.register(r'activity/read', views.ActivityViewSet)
router.register(r'course/read', views.CourseViewSet)
router.register(r'program/read', views.ProgramViewSet)

def flow_patterns():
    return [
        url(
            r"^program/create/$",
            views.ProgramCreateView.as_view(),
            name="program-create",
        ),
        url(
            r"^program/(?P<pk>[0-9]+)/$",
            views.ProgramDetailView.as_view(),
            name="program-detail",
        ),
        url(
            r"^program/(?P<pk>[0-9]+)/update/$",
            views.ProgramUpdateView.as_view(),
            name="program-update",
        ),
        url(
            r"^course/(?P<pk>[0-9]+)/$",
            views.CourseDetailView.as_view(),
            name="course-detail",
        ),
        url(
            r"^course/(?P<pk>[0-9]+)/update/$",
            views.CourseUpdateView.as_view(),
            name="course-update",
        ),
        url(
            r"^activity/(?P<pk>[0-9]+)/$",
            views.ActivityDetailView.as_view(),
            name="activity-detail",
        ),
        url(
            r"^activity/(?P<pk>[0-9]+)/update/$",
            views.ActivityUpdateView.as_view(),
            name="activity-update",
        ),
        url(
            r"^activity/update-json",
            views.update_activity_json,
            name="update-activity-json",
        ),
        url(
            r"^course/update-json",
            views.update_course_json,
            name="update-course-json",
        ),
        url(
            r"^program/update-json",
            views.update_program_json,
            name="update-program-json",
        ),
        url(
            r"^activity/add-node",
            views.add_node,
            name="add-node",
        ),
        url(
            r"^activity/add-strategy",
            views.add_strategy,
            name="add-strategy",
        ),
        url(
            r"^course/add-component",
            views.add_component_to_course,
            name="add-component-to-course",
        ),
        url(
            r"^program/add-component",
            views.add_component_to_program,
            name="add-component-to-program",
        ),
        url(
            r"^dialog-form/create",
            views.dialog_form_create,
            name="dialog-form-create",
        ),
        url(
            r"^dialog-form/update",
            views.dialog_form_update,
            name="dialog-form-update",
        ),
        url(
            r"^dialog-form/delete",
            views.dialog_form_delete,
            name="dialog-form-delete",
        ),
    ] + router.urls

urlpatterns = sum([flow_patterns()], [])
