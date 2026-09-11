from django.urls import path
from django.views.generic import TemplateView
from .views import project_view, project_detail_view

app_name = 'projects'

urlpatterns = [
    path('', view=project_view, name='projects'),
    path('<slug:slug>', view=project_detail_view, name='project-detail')

]
