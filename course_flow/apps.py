from django.apps import AppConfig
from django.core.checks import register

from .checks import check_return_url


class CourseFlowConfig(AppConfig):
    name = "course_flow"
    verbose_name = "Course Flow"

    def ready(self):
        register(check_return_url)
