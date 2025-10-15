from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum  # <<< Импортируем Sum
from django.views.generic import DetailView, ListView, TemplateView

from .models import EmployeeProfile


class HomePageView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        top_employees = (
            EmployeeProfile.objects.annotate(
                total_skill_level=Sum("employeeskill__level")
            )
            .filter(total_skill_level__isnull=False)
            .order_by("-total_skill_level")[:5]
        )
        context["top_employees"] = top_employees

        recent_employees = EmployeeProfile.objects.order_by("-hire_date")[:4]
        context["recent_employees"] = recent_employees

        context["employee_count"] = EmployeeProfile.objects.count()
        context["title"] = "Главная страница"

        return context


class EmployeeListView(ListView):
    model = EmployeeProfile
    template_name = "employees/employee_list.html"
    context_object_name = "employees"
    paginate_by = 10


class EmployeeDetailView(LoginRequiredMixin, DetailView):
    model = EmployeeProfile
    template_name = "employees/employee_detail.html"
    context_object_name = "employee"
    login_url = "/admin/login/"
