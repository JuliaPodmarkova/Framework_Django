# company/admin.py
from django.contrib import admin
from .models import Position, Workplace

@admin.register(Workplace)
class WorkplaceAdmin(admin.ModelAdmin):

    list_display = ("table_number", "get_employee_name", "additional_info")
    search_fields = ("table_number",)
    list_select_related = ('employee__user',)
    @admin.display(description="Сотрудник", ordering='employee__user__last_name')
    def get_employee_name(self, obj):
        if obj.employee:
            return obj.employee.user.get_full_name() or obj.employee.user.username
        return "Свободен"

@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}
