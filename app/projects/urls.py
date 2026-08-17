from django.urls import path
from django.views.generic import TemplateView

app_name = 'projects'

urlpatterns = [
    path('', TemplateView.as_view(template_name='projects_list/projects.html'), name='projects'),
    path('single',TemplateView.as_view(template_name='project_detail/project_detail.html'), name='project-detail')

]
