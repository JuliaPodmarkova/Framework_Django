from ckeditor.fields import RichTextField
from django.db import models

class Workplace(models.Model):
    table_number = models.PositiveIntegerField(
        unique=True, verbose_name="Номер стола"
    )
    additional_info = RichTextField(
        blank=True, null=True, verbose_name="Дополнительная информация"
    )

    class Meta:
        verbose_name = "Рабочее место"
        verbose_name_plural = "Рабочие места"
        ordering = ["table_number"]

    def __str__(self):
        return f"Стол №{self.table_number}"

class Position(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Название должности")
    slug = models.SlugField(max_length=100, unique=True, help_text="Например: backend-developer")

    class Meta:
        verbose_name = "Должность"
        verbose_name_plural = "Должности"
        ordering = ["name"]

    def __str__(self):
        return self.name
