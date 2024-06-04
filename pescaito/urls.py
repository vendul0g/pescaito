from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from main import views
from canary import views as canary_views


urlpatterns = [
    path('', views.main_page, name='main_page'),
    path("admin/", admin.site.urls),
    path("images/<str:token>/submit.aspx", canary_views.submit, name="submit"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)