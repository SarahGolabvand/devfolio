from django.urls import path
from .views import project_view, project_detail_view

app_name = 'projects'

urlpatterns = [
    path('', view=project_view, name='projects_list'), # اسم رو برای شفافیت تغییر دادم
    path('<slug:slug>/', view=project_detail_view, name='project_detail'), # اصلاح نام و اضافه کردن /
]
