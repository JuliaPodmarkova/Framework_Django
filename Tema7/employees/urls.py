from django.urls import path
from .views import (
    EmployeeListView, EmployeeCreateView, EmployeeDetailView, EmployeeUpdateView,
    EmployeeDeleteView, SkillCreateView, EmployeeMoveWorkplaceView
)

app_name = 'employees'

urlpatterns = [
    path('', EmployeeListView.as_view(), name='employee_list'),
    path('add/', EmployeeCreateView.as_view(), name='employee_add'),
    path('<int:pk>/', EmployeeDetailView.as_view(), name='employee_detail'),
    path('<int:pk>/update/', EmployeeUpdateView.as_view(), name='employee_update'),
    path('<int:pk>/delete/', EmployeeDeleteView.as_view(), name='employee_delete'),
    path('skills/add/', SkillCreateView.as_view(), name='skill_create'),
    path('<int:pk>/move_workplace/', EmployeeMoveWorkplaceView.as_view(), name='employee_move_workplace'),  # >>> ЭТО МОЖНО ДОБАВИТЬ СЮДА
]