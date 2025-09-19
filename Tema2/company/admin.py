from django.contrib import admin

from .models import EmployeeProfile, EmployeeSkill, Skill


class EmployeeSkillInline(admin.TabularInline):
    model = EmployeeSkill
    extra = 1


@admin.register(EmployeeProfile)
class EmployeeProfileAdmin(admin.ModelAdmin):
    list_display = ("__str__", "user", "gender", "workplace")
    list_filter = ("gender", "skills")
    search_fields = ("user__username", "user__first_name", "user__last_name")
    inlines = [EmployeeSkillInline]


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


admin.site.register(EmployeeSkill)
