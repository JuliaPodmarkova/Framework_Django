from django.contrib import admin

from .models import Workplace


@admin.register(Workplace)
class WorkplaceAdmin(admin.ModelAdmin):
    list_display = ("desk_number", "employee")
    list_filter = ("employee",)
    search_fields = ("desk_number", "employee__user__first_name")
