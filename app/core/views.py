
from .models import SkillsModel, ProfileModel
from django.views.generic.base import TemplateView


class IndexView(TemplateView):
    template_name = 'index/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "skills": SkillsModel.objects.filter(is_visible=True).order_by("order", "title"),
            'profile': ProfileModel.objects.first(),
            # "projects": ProjectModel.objects.filter(is_visible=True).order_by("order")[:6],
        })
        return context
