import os

from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver


class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Название навыка")

    class Meta:
        verbose_name = "Навык"
        verbose_name_plural = "Навыки"
        ordering = ["name"]

    def __str__(self):
        return self.name


class EmployeeProfile(models.Model):

    class Gender(models.TextChoices):
        MALE = "M", "Мужской"
        FEMALE = "F", "Женский"
        OTHER = "O", "Другой"

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, verbose_name="Пользователь"
    )

    middle_name = models.CharField(max_length=100, blank=True, verbose_name="Отчество")
    gender = models.CharField(max_length=1, choices=Gender.choices, verbose_name="Пол")
    description = RichTextField(blank=True, null=True, verbose_name="Описание")

    skills = models.ManyToManyField(
        Skill, through="EmployeeSkill", related_name="employees", verbose_name="Навыки"
    )

    class Meta:
        verbose_name = "Профиль сотрудника"
        verbose_name_plural = "Профили сотрудников"

    def __str__(self):
        # Будет красиво отображать Имя + Фамилию в админке
        return f"{self.user.first_name} {self.user.last_name}"


class EmployeeSkill(models.Model):
    employee = models.ForeignKey(
        EmployeeProfile, on_delete=models.CASCADE, verbose_name="Сотрудник"
    )
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, verbose_name="Навык")
    level = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name="Уровень освоения (1-10)",
    )

    class Meta:
        verbose_name = "Навык сотрудника"
        verbose_name_plural = "Навыки сотрудников"
        unique_together = ("employee", "skill")

    def __str__(self):
        return f"{self.employee} - {self.skill} (Уровень: {self.level})"


class EmployeeImage(models.Model):
    """Модель для хранения изображений сотрудника."""

    employee = models.ForeignKey(
        EmployeeProfile,
        on_delete=models.CASCADE,
        related_name="images",
        verbose_name="Сотрудник",
    )
    image = models.ImageField(upload_to="employee_gallery/", verbose_name="Изображение")
    order_number = models.PositiveSmallIntegerField(
        default=0, verbose_name="Порядковый номер"
    )

    class Meta:
        verbose_name = "Изображение сотрудника"
        verbose_name_plural = "Галерея сотрудника"
        ordering = ["order_number"]  # Сортировка по умолчанию

    def __str__(self):
        return f"Изображение для {self.employee} (№{self.order_number})"


@receiver(pre_delete, sender=EmployeeImage)
def delete_employee_image_file(sender, instance, **kwargs):
    """Удаляет файл изображения с диска при удалении объекта из БД."""
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)
