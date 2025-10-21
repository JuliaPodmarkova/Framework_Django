from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)
from employees.views import HomePageView
from django.contrib.auth import views as auth_views


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("employees.api.urls")),
    path('company/', include(('company.urls', 'company'), namespace='company')),
    path('employees/', include(('employees.urls', 'employees'), namespace='employees')),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('login/', auth_views.LoginView.as_view(), name='login'),


    # JWT-токены API
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # Домашняя страница САМОЙ последней строкой, чтобы не ломать остальные url-ы!
    path("", HomePageView.as_view(), name="home"),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)