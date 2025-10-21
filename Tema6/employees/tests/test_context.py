from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from employees.models import EmployeeProfile


class ContextTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="contextuser", password="secret")
        from company.models import Position, Workplace

        position = Position.objects.create(slug="junior", name="Junior")
        workplace = Workplace.objects.create(table_number=101)
        self.profile = EmployeeProfile.objects.create(
            user=self.user, position=position, workplace=workplace, gender="Male"
        )

    def test_home_context_contains_employee_count(self):
        client = Client()
        response = client.get(reverse("home"))
        self.assertIn("employee_count", response.context)
        self.assertEqual(
            response.context["employee_count"], EmployeeProfile.objects.count()
        )
