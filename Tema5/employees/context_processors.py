from django.utils.translation import gettext_lazy as _

from .models import EmployeeProfile


def employee_count(request):
    count = EmployeeProfile.objects.count()
    return {"total_employees": count, "gettext_lazy": _}
