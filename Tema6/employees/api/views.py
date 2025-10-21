from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, permissions
from rest_framework.pagination import PageNumberPagination

from employees.models import EmployeeProfile

from .permissions import IsAdminOrReadOnly, IsWatcherOrAdminToChangeWorkplace
from .serializers import (EmployeeProfileCreateUpdateSerializer,
                          EmployeeProfileSerializer)


# --- ПАГИНАЦИЯ ---
class EmployeePagination(PageNumberPagination):
    page_size = 10


# --- СПИСОК сотрудников с фильтрацией ---
class EmployeeListAPIView(generics.ListAPIView):
    queryset = (
        EmployeeProfile.objects.all()
        .select_related("user", "workplace", "position")
        .prefetch_related("skills")
    )
    serializer_class = EmployeeProfileSerializer
    pagination_class = EmployeePagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = {
        "skills__name": ["exact"],  # фильтрация по навыкам: ?skills__name=Python
        "hire_date": ["gte", "lte"],  # фильтрация по стажу: ?hire_date__lte=2022-01-01
    }
    search_fields = ["user__username", "bio", "position__name"]


# --- ДЕТАЛИ сотрудника ---
class EmployeeDetailAPIView(generics.RetrieveAPIView):
    queryset = EmployeeProfile.objects.all()
    serializer_class = EmployeeProfileSerializer


# --- СОЗДАНИЕ сотрудника ---
class EmployeeCreateAPIView(generics.CreateAPIView):
    queryset = EmployeeProfile.objects.all()
    serializer_class = EmployeeProfileCreateUpdateSerializer
    permission_classes = [permissions.IsAdminUser]


# --- ОБНОВЛЕНИЕ сотрудника ---
class EmployeeUpdateAPIView(generics.UpdateAPIView):
    queryset = EmployeeProfile.objects.all()
    serializer_class = EmployeeProfileCreateUpdateSerializer
    permission_classes = [permissions.IsAdminUser]


# --- УДАЛЕНИЕ сотрудника ---
class EmployeeDeleteAPIView(generics.DestroyAPIView):
    queryset = EmployeeProfile.objects.all()
    permission_classes = [permissions.IsAdminUser]
