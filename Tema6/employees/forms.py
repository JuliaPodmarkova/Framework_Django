from django import forms
from django.contrib.auth.models import User
from .models import EmployeeProfile, EmployeeSkill, Skill

class EmployeeProfileCreateForm(forms.ModelForm):
    username = forms.CharField(label="Логин пользователя")
    email = forms.EmailField(label="Email")
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput)

    class Meta:
        model = EmployeeProfile
        exclude = ['user']

    def save(self, commit=True):
        username = self.cleaned_data['username']
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']
        last_name = self.cleaned_data.get('last_name')
        first_name = self.cleaned_data.get('first_name')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )

        instance = super().save(commit=False)
        instance.user = user
        if commit:
            instance.save()
        return instance

class EmployeeSkillForm(forms.ModelForm):
    class Meta:
        model = EmployeeSkill
        fields = ['skill', 'level']

EmployeeSkillFormSet = forms.inlineformset_factory(
    EmployeeProfile,
    EmployeeSkill,
    form=EmployeeSkillForm,
    extra=5,
    can_delete=True
)

class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ['name']