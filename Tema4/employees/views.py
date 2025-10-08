from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum  # <<< Импортируем Sum
from django.views.generic import DetailView, ListView, TemplateView
from .models import EmployeeProfile


class HomePageView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # --- ЗАПРОС №1: Топ 5 сотрудников по навыкам ---
        # Вычисляем суммарный уровень навыков, сортируем и берем 5 лучших.
        top_employees = (
            EmployeeProfile.objects.annotate(
                total_skill_level=Sum("employeeskill__level")
            )
            .filter(total_skill_level__isnull=False)
            .order_by("-total_skill_level")[:5]  # <<< Берем топ 5
        )
        context["top_employees"] = top_employees

        # --- ЗАПРОС №2: Последние нанятые сотрудники ---
        # Это твой оригинальный запрос, просто сортируем по дате и берем 4 последних.
        recent_employees = EmployeeProfile.objects.order_by("-hire_date")[:4]
        context["recent_employees"] = recent_employees

        # --- Остальные данные для страницы ---
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