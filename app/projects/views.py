from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Project, Tag
# Create your views here.


def project_view(request):
    projects = (Project.objects.filter(is_published=True)
                .prefetch_related('tags')
                .order_by('-created_at'))

    tags = Tag.objects.all()
    return render(request=request,
                  template_name='projects_list/projects.html',
                  context={'projects': projects, 'tags': tags})


def project_detail_view(request, slug):

    project = get_object_or_404(Project, slug=slug)
    return render(request, template_name='project_detail/project_detail.html', context={'project_obj': project})
