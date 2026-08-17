from django.urls import path, include
from django.views.generic import TemplateView
from .views import IndexView

app_name = 'core'

urlpatterns = [
    path('', IndexView.as_view(), name='index')

]
