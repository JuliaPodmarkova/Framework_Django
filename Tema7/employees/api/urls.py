from django.urls import path
from .views import (
    EmployeeListAPIView, EmployeeDetailAPIView,
    EmployeeCreateAPIView, EmployeeUpdateAPIView, EmployeeDeleteAPIView
)

urlpatterns = [
    path("employees/", EmployeeListAPIView.as_view(), name="api_employee_list"),
    path("employees/<int:pk>/", EmployeeDetailAPIView.as_view(), name="api_employee_detail"),
    path("employees/", EmployeeCreateAPIView.as_view(), name="api_employee_create"),  # POST на этот же адрес
    path("employees/<int:pk>/", EmployeeUpdateAPIView.as_view(), name="api_employee_update"),
    path("employees/<int:pk>/", EmployeeDeleteAPIView.as_view(), name="api_employee_delete"),
]