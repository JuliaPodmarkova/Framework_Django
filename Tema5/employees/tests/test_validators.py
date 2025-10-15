from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase

from employees.models import EmployeeProfile
from company.models import Position, Workplace

class NeighborValidatorTest(TestCase):
    def setUp(self):
        self.qa_position = Position.objects.create(slug="qa-engineer", name="QA")
        self.dev_position = Position.objects.create(slug="backend-developer", name="Backend")
        self.table1 = Workplace.objects.create(table_number=1)
        self.table2 = Workplace.objects.create(table_number=2)

        self.tester = User.objects.create_user(username="tester")
        self.tester_profile = EmployeeProfile.objects.create(
            user=self.tester, position=self.qa_position,
            workplace=self.table2, gender="Male"
        )

    def test_cannot_place_dev_next_to_tester(self):
        dev = User.objects.create_user(username="dev")
        dev_profile = EmployeeProfile(
            user=dev, position=self.dev_position,
            workplace=self.table1, gender="Male"
        )
        with self.assertRaises(ValidationError):
            dev_profile.clean()