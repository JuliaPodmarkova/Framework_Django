from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from employees.views import HomePageView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", HomePageView.as_view(), name="home"),
    path("employees/", include("employees.urls", namespace="employees")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
