from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from company.models import Position, Workplace
from employees.models import EmployeeProfile


class URLAccessTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="secret")
        self.position = Position.objects.create(slug="test-slug", name="Test Position")
        self.workplace = Workplace.objects.create(table_number=55)
        self.profile = EmployeeProfile.objects.create(
            user=self.user,
            position=self.position,
            workplace=self.workplace,
            gender="Male",
        )

    def test_public_url_is_accessible(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)

    def test_private_url_redirects_anonymous(self):
        response = self.client.get(
            reverse("employees:employee_detail", args=[self.profile.pk])
        )
        self.assertEqual(response.status_code, 302)
        self.assertIn("/admin/login", response.url)

    def test_private_url_accessible_for_logged_in_user(self):
        self.client.login(username="testuser", password="secret")
        response = self.client.get(
            reverse("employees:employee_detail", args=[self.profile.pk])
        )
        self.assertEqual(response.status_code, 200)
