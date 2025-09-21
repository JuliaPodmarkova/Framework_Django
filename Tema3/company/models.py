from ckeditor.fields import RichTextField
from django.db import models

from employees.models import EmployeeProfile


class Workplace(models.Model):

    desk_number = models.CharField(
        max_length=50, unique=True, verbose_name="Номер стола"
    )
    additional_info = RichTextField(
        blank=True, null=True, verbose_name="Дополнительная информация"
    )

    employee = models.OneToOneField(
        EmployeeProfile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="workplace",
        verbose_name="Сотрудник",
    )

    class Meta:
        verbose_name = "Рабочее место"
        verbose_name_plural = "Рабочие места"
        ordering = ["desk_number"]

    def __str__(self):
        if self.employee:
            return f"Стол №{self.desk_number} ({self.employee})"
        return f"Стол №{self.desk_number} (Свободен)"
