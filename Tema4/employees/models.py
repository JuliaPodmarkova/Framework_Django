import os
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.utils import timezone

class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Название навыка")

    class Meta:
        verbose_name = "Навык"
        verbose_name_plural = "Навыки"
        ordering = ["name"]

    def __str__(self):
        return self.name

class EmployeeProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="profile"
    )
    gender = models.CharField(
        max_length=10,
        choices=[("Male", "Мужской"), ("Female", "Женский")],
        verbose_name="Пол",
    )
    bio = models.TextField(verbose_name="Биография", blank=True, null=True)

    workplace = models.OneToOneField(
        'company.Workplace',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="employee",
        verbose_name="Рабочее место",
    )

    position = models.ForeignKey(
        'company.Position',
        on_delete=models.SET_NULL,
        null=True,
        related_name="employees",
        verbose_name="Должность",
    )

    skills = models.ManyToManyField(
        Skill,
        through="EmployeeSkill",
        related_name="employees",
        verbose_name="Навыки",
    )

    hire_date = models.DateField(
        verbose_name="Дата приёма на работу",
        default=timezone.now
    )

    class Meta:
        verbose_name = "Профиль сотрудника"
        verbose_name_plural = "Профили сотрудников"
        ordering = ["-hire_date"]

    def __str__(self):
        position_name = self.position.name if self.position else "Без должности"
        full_name = self.user.get_full_name() or self.user.username
        return f"{full_name} ({position_name})"

    def get_work_experience_days(self):
        if not self.hire_date:
            return 0

        today = timezone.now().date()
        if self.hire_date > today:
            return 0

        delta = today - self.hire_date
        return delta.days
    def get_first_image(self):

        return self.images.order_by('order_number').first()

    def clean(self):
        super().clean()

        if not self.position or not self.workplace or not self.workplace.table_number:
            return

        DEVELOPER_SLUGS = ["backend-developer", "frontend-developer"]
        TESTER_SLUGS = ["qa-engineer", "tester"]  # Добавили "tester"

        is_developer = self.position.slug in DEVELOPER_SLUGS
        is_tester = self.position.slug in TESTER_SLUGS

        if not is_developer and not is_tester:
            return

        current_table_num = self.workplace.table_number
        adjacent_tables = [current_table_num - 1, current_table_num + 1]

        neighbors = EmployeeProfile.objects.filter(
            workplace__table_number__in=adjacent_tables
        ).exclude(pk=self.pk).select_related('position', 'workplace', 'user')

        for neighbor in neighbors:
            if not neighbor.position:
                continue

            neighbor_is_developer = neighbor.position.slug in DEVELOPER_SLUGS
            neighbor_is_tester = neighbor.position.slug in TESTER_SLUGS

            conflict = (is_developer and neighbor_is_tester) or \
                       (is_tester and neighbor_is_developer)

            if conflict:
                raise ValidationError(
                    f"Конфликт! Нельзя сажать разработчика и тестировщика рядом. "
                    f"Сосед {neighbor.user.get_full_name()} за столом №{neighbor.workplace.table_number} "
                    f"имеет несовместимую должность.")

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
        ordering = ["order_number"]

    def __str__(self):
        return f"Изображение для {self.employee} (№{self.order_number})"

@receiver(pre_delete, sender=EmployeeImage)
def delete_employee_image_file(sender, instance, **kwargs):
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)