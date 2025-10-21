from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Sum
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.views.generic import (
    DetailView, ListView, TemplateView,
    CreateView, UpdateView, DeleteView
)
from .forms import EmployeeSkillFormSet
from .models import EmployeeProfile
from .forms import EmployeeProfileCreateForm
from .models import Skill
from .forms import SkillForm

class StaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    login_url = "/admin/login/"
    def test_func(self):
        return self.request.user.is_staff

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
        context["recent_employees"] = EmployeeProfile.objects.order_by("-hire_date")[:4]
        context["employee_count"] = EmployeeProfile.objects.count()
        context["title"] = "Главная страница"
        return context

class EmployeeListView(LoginRequiredMixin, ListView):
    model = EmployeeProfile
    template_name = "employees/employee_list.html"
    context_object_name = "employees"
    paginate_by = 10
    login_url = "/admin/login/"

class EmployeeDetailView(LoginRequiredMixin, DetailView):
    model = EmployeeProfile
    template_name = "employees/employee_detail.html"
    context_object_name = "employee"
    login_url = "/admin/login/"

# ▶️ HTML-формы для сотрудника
class EmployeeCreateView(StaffRequiredMixin, CreateView):
    model = EmployeeProfile
    form_class = EmployeeProfileCreateForm
    template_name = "employees/employee_form.html"
    success_url = reverse_lazy("employees:employee_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['skill_formset'] = EmployeeSkillFormSet(self.request.POST)
        else:
            context['skill_formset'] = EmployeeSkillFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        skill_formset = context['skill_formset']
        if form.is_valid() and skill_formset.is_valid():
            self.object = form.save()
            skill_formset.instance = self.object
            skill_formset.save()
            # Получаем "next" из URL, если есть — редиректим туда, иначе на success_url
            next_url = self.request.GET.get('next')
            return redirect(next_url or self.success_url)
        return self.render_to_response(self.get_context_data(form=form))

class EmployeeUpdateView(StaffRequiredMixin, UpdateView):
    model = EmployeeProfile
    fields = "__all__"
    template_name = "employees/employee_form.html"
    success_url = reverse_lazy("employees:employee_list")

class EmployeeDeleteView(StaffRequiredMixin, DeleteView):
    model = EmployeeProfile
    template_name = "employees/employee_confirm_delete.html"
    success_url = reverse_lazy("employees:employee_list")

class SkillCreateView(CreateView):
    model = Skill
    form_class = SkillForm
    template_name = "employees/skill_form.html"
    success_url = "/employees/add/"

    def form_valid(self, form):
        self.object = form.save()
        return super().form_valid(form)

class WatcherOrAdminMixin(UserPassesTestMixin):
    login_url = "/admin/login/"
    def test_func(self):
        user = self.request.user
        return user.is_staff or (hasattr(user, "profile") and user.profile.is_watcher)

class EmployeeMoveWorkplaceView(WatcherOrAdminMixin, UpdateView):
    model = EmployeeProfile
    fields = ['workplace']
    template_name = 'employees/move_workplace_form.html'
    success_url = reverse_lazy('employees:employee_list')  # важно: employees:employee_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f"Перемещение сотрудника: {self.object.full_name}"
        return context