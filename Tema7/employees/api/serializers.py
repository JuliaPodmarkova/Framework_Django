from django.contrib.auth.models import User
from rest_framework import serializers

from company.models import Position, Workplace
from employees.models import EmployeeProfile, Skill


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ["id", "name"]


class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = ["id", "name", "slug"]


class WorkplaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workplace
        fields = ["id", "table_number"]


class EmployeeProfileSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    position = PositionSerializer()
    workplace = WorkplaceSerializer()
    skills = SkillSerializer(many=True)

    class Meta:
        model = EmployeeProfile
        fields = [
            "id",
            "user",
            "gender",
            "position",
            "workplace",
            "skills",
            "bio",
            "hire_date",
        ]


class EmployeeProfileCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeProfile
        fields = ["user", "gender", "position", "workplace", "bio", "hire_date"]
