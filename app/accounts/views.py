
from .models import SkillsModel, ProfileModel
from django.views.generic.base import TemplateView
from projects.models import Project


class IndexView(TemplateView):
    template_name = 'index/index.html'
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "skills": SkillsModel.objects.filter(is_visible=True).order_by("order", "title"),
            'profile': ProfileModel.objects.first(),
            "projects": (Project.objects.filter(is_published=True)
                         .prefetch_related('tags')
                         .order_by('-created_at'))[:3]

        })
        return context
