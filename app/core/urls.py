from django.urls import path
from .views import IndexView
from django.conf import settings
from django.conf.urls.static import static


app_name = 'core'

urlpatterns = [
    path('', IndexView.as_view(), name='index')

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
