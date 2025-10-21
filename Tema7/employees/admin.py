from django.contrib import admin

from .models import EmployeeImage, EmployeeProfile, EmployeeSkill, Skill


class EmployeeSkillInline(admin.TabularInline):
    model = EmployeeSkill
    extra = 1


class EmployeeImageInline(admin.TabularInline):
    model = EmployeeImage
    extra = 1
    fields = ("image", "order_number")


@admin.register(EmployeeProfile)
class EmployeeProfileAdmin(admin.ModelAdmin):
    list_display = ("__str__", "user", "gender", "workplace", "is_watcher")
    list_filter = ("gender", "skills", "is_watcher")
    search_fields = ("user__username", "user__first_name", "user__last_name")
    inlines = [EmployeeSkillInline, EmployeeImageInline]


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


admin.site.register(EmployeeSkill)
