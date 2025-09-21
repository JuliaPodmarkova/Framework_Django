from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, ListView, TemplateView

from .models import EmployeeProfile


class HomePageView(TemplateView):

    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["employees"] = EmployeeProfile.objects.all()
        return context


class EmployeeListView(ListView):
    model = EmployeeProfile
    template_name = "employees/employee_list.html"
    context_object_name = "employees"


class EmployeeDetailView(LoginRequiredMixin, DetailView):
    model = EmployeeProfile
    template_name = "employees/employee_detail.html"
    context_object_name = "employee"
    login_url = "/admin/login/"
